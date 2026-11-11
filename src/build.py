#!/usr/bin/env python3
"""Builds the Conveasy static site.
Outputs:
  ../docs/     the website itself (no preview banner). GitHub Pages serves this folder.
  ../preview/  same pages with a preview banner, plus main.html for the claude.ai preview
Run: python3 build.py
"""
import html, json, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import *  # noqa
from overrides import OV as OVX, apply as apply_overrides
import answers
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "legal"))
import legal_nl, legal_fr, legal_en, legal_tr, legal_de
LEGAL_DOCS = {"nl": legal_nl, "fr": legal_fr, "en": legal_en, "tr": legal_tr, "de": legal_de}

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MONTHLY = {"whatsapp": "99", "webshop": "79", "kiosk": "89"}
FONTS = "https://fonts.googleapis.com/css2?family=Figtree:ital,wght@0,400;0,500;0,600;0,700;1,500&family=JetBrains+Mono:wght@500;700&display=swap"
PLACEHOLDERS = {}  # text -> set of pages

def e(s):
    return html.escape(s, quote=True)

def ph(text, lang, page=""):
    """Turn {{PH:...}} into a visible marker; text otherwise escaped."""
    out, pos = [], 0
    for m in re.finditer(r"\{\{PH:(.*?)\}\}", text):
        out.append(e(text[pos:m.start()]))
        out.append(f'<mark class="ph">[{e(UI[lang]["ph"])}: {e(m.group(1))}]</mark>')
        PLACEHOLDERS.setdefault((lang, m.group(1)), set()).add(page)
        pos = m.end()
    out.append(e(text[pos:]))
    return "".join(out)

def rich(text, lang, page=""):
    # allows <em> in headlines we wrote ourselves
    return ph(text, lang, page).replace("&lt;em&gt;", "<em>").replace("&lt;/em&gt;", "</em>")

def plain(text):
    return re.sub(r"<[^>]+>", "", re.sub(r"\{\{PH:.*?\}\}", "", text)).strip()

def path_of(lang, pid):
    return f"{lang}/{SLUGS[pid][lang]}.html"

def canonical(lang, pid):
    s = SLUGS[pid][lang]
    return f"{SITE}/{lang}/" + ("" if s == "index" else s)

def name_of(lang, pid):
    if pid in PRODUCTS: return P[pid][lang]["name"]
    if pid in SECTORS: return S[pid][lang]["nav"]
    return {"home": UI[lang]["home"], "pricing": UI[lang]["pricing"], "about": UI[lang]["about"],
            "contact": UI[lang]["contact"], "legal": UI[lang]["foot_legal"]}[pid]

def meta_of(lang, pid):
    if pid in PRODUCTS: d = P[pid][lang]
    elif pid in SECTORS: d = S[pid][lang]
    else: d = {"home": HOME, "pricing": PRICING, "about": ABOUT, "contact": CONTACT, "legal": LEGAL}[pid][lang]
    return d["title"], d["desc"]

# ---------------- JSON-LD ----------------
ORG = {"@type": "Organization", "@id": SITE + "/#org", "name": "Conveasy", "url": SITE + "/",
       "description": "AI ordering software for restaurants: phone AI and WhatsApp AI for orders and 24/7 table reservations, commission-free webshop with QR ordering, self-order kiosk and Marketing AI with a digital stamp card in Google and Apple Wallet.",
       "areaServed": ["BE", "NL", "LU"],
       "contactPoint": {"@type": "ContactPoint", "telephone": "+32456564747", "contactType": "sales",
                        "availableLanguage": ["nl", "fr", "en", "tr", "de"]}}

def jsonld(lang, pid, faqs, crumbs):
    title, desc = meta_of(lang, pid)
    graph = [ORG,
             {"@type": "WebPage", "@id": canonical(lang, pid) + "#page", "url": canonical(lang, pid),
              "name": title, "description": desc, "inLanguage": HTML_LANG[lang],
              "isPartOf": {"@type": "WebSite", "name": "Conveasy", "url": SITE + "/"}, "publisher": {"@id": SITE + "/#org"}}]
    if crumbs:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]})
    if pid in PRODUCTS:
        d = P[pid][lang]
        prod = {"@type": "Product", "name": "Conveasy " + d["name"], "description": d["desc"],
                "brand": {"@type": "Brand", "name": "Conveasy"}, "url": canonical(lang, pid)}
        offers = []
        if pid == "phone":
            for n, price, mins, _ in PRICING[lang]["tiers"]:
                offers.append({"@type": "Offer", "name": n + " (" + mins + ")", "price": price, "priceCurrency": "EUR",
                               "priceSpecification": {"@type": "UnitPriceSpecification", "price": price, "priceCurrency": "EUR", "billingDuration": "P1M"}})
        elif pid in MONTHLY:
            m = MONTHLY[pid]
            offers = [{"@type": "Offer", "price": m, "priceCurrency": "EUR",
                       "priceSpecification": {"@type": "UnitPriceSpecification", "price": m, "priceCurrency": "EUR", "billingDuration": "P1M"}}]
        if offers: prod["offers"] = offers
        graph.append(prod)
    good = [(q, a) for q, a in faqs if "{{PH:" not in a]
    if good:
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in good]})
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/") + "</script>"

# ---------------- Pieces ----------------
def head(lang, pid, prefix, faqs, crumbs, main):
    title, desc = meta_of(lang, pid)
    alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{canonical(l, pid)}">' for l in LANGS)
    alts += f'<link rel="alternate" hreflang="x-default" href="{canonical("nl", pid)}">'
    parts = [f"<title>{e(title)}</title>"]
    if main:
        parts.append('<meta name="claude:viewport-fit-sides" content="cover">')
    parts += [f'<meta name="description" content="{e(desc)}">',
              f'<link rel="canonical" href="{canonical(lang, pid)}">', alts,
              '<meta property="og:type" content="website">', '<meta property="og:site_name" content="Conveasy">',
              f'<meta property="og:title" content="{e(title)}">', f'<meta property="og:description" content="{e(desc)}">',
              f'<meta property="og:url" content="{canonical(lang, pid)}">', f'<meta property="og:locale" content="{OG_LOCALE[lang]}">',
              '<meta name="twitter:card" content="summary_large_image">',
              '<meta name="theme-color" content="#000000">',
              '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
              f'<link rel="stylesheet" href="{FONTS}">',
              f'<link rel="stylesheet" href="{prefix}assets/site.css">',
              jsonld(lang, pid, faqs, crumbs)]
    return "\n".join(parts)

def header(lang, pid, prefix):
    u = UI[lang]
    h = lambda p: prefix + path_of(lang, p)
    cur = lambda p: ' aria-current="page"' if p == pid else ""
    prod_links = "".join(f'<a href="{h(p)}"{cur(p)}>{e(P[p][lang]["name"])}<small>{e(P[p][lang]["sub"])}</small></a>' for p in PRODUCTS)
    sec_links = "".join(f'<a href="{h(s)}"{cur(s)}>{e(S[s][lang]["name"])}</a>' for s in SECTORS)
    langs = "".join(f'<a href="{prefix + path_of(l, pid)}" hreflang="{l}" lang="{l}" title="{LANG_NAMES[l]}"{" aria-current=\"true\"" if l == lang else ""}>{l}</a>' for l in LANGS)
    mob_prod = "".join(f'<a href="{h(p)}">{e(P[p][lang]["name"])}</a>' for p in PRODUCTS)
    mob_sec = "".join(f'<a href="{h(s)}">{e(S[s][lang]["name"])}</a>' for s in SECTORS)
    return f'''<header class="site-header"><div class="wrap">
<a class="logo" href="{h("home")}" aria-label="Conveasy home"><span class="logo-mark" aria-hidden="true"></span>Conveasy</a>
<nav class="nav" aria-label="Main">
<details class="dd"><summary>{e(u["products"])}</summary><div class="dd-menu">{prod_links}</div></details>
<details class="dd"><summary>{e(u["sectors"])}</summary><div class="dd-menu">{sec_links}</div></details>
<a href="{h("pricing")}"{cur("pricing")}>{e(u["pricing"])}</a>
<a href="{h("about")}"{cur("about")}>{e(u["about"])}</a>
<a href="{h("contact")}"{cur("contact")}>{e(u["contact"])}</a>
<div class="lang" aria-label="Language">{langs}</div>
</nav>
<a class="btn btn-primary btn-head" href="{h("contact")}">{e(u["demo"])}</a>
<details class="mobile-menu"><summary>{e(u["menu"])}</summary><div class="mobile-panel">
<span class="group-label">{e(u["products"])}</span>{mob_prod}
<span class="group-label">{e(u["sectors"])}</span>{mob_sec}
<span class="group-label">Conveasy</span>
<a href="{h("pricing")}">{e(u["pricing"])}</a><a href="{h("about")}">{e(u["about"])}</a><a href="{h("contact")}">{e(u["demo"])}</a>
<div class="lang" style="margin-top:12px">{langs}</div>
</div></details>
</div></header>'''

def footer(lang, prefix, page):
    u = UI[lang]
    h = lambda p: prefix + path_of(lang, p)
    prods = "".join(f'<li><a href="{h(p)}">{e(P[p][lang]["name"])}</a></li>' for p in PRODUCTS)
    secs = "".join(f'<li><a href="{h(s)}">{e(S[s][lang]["name"])}</a></li>' for s in SECTORS)
    return f'''<footer class="site-footer"><div class="wrap"><div class="foot-mark" aria-hidden="true">Conveasy</div>
<div class="foot-cols">
<div style="display:grid;gap:12px;align-content:start"><a class="logo" href="{h("home")}"><span class="logo-mark" aria-hidden="true"></span>Conveasy</a><p>{e(u["foot_tag"])}</p><p>WhatsApp: {e(WA_DISPLAY)}</p></div>
<div><h4>{e(u["products"])}</h4><ul>{prods}</ul></div>
<div><h4>{e(u["sectors"])}</h4><ul>{secs}</ul></div>
<div><h4>Conveasy</h4><ul><li><a href="{h("pricing")}">{e(u["pricing"])}</a></li><li><a href="{h("about")}">{e(u["about"])}</a></li><li><a href="{h("contact")}">{e(u["contact"])}</a></li><li><a href="{h("legal")}">{e(u["foot_legal"])}</a></li><li><a href="{APP_URL}" rel="noopener">{e(u["foot_app"])}</a></li></ul></div>
</div>
<div class="foot-bottom"><span>{ph(u["foot_company"], lang, page)}</span><span>{e(u["foot_rights"])}</span></div>
</div></footer>'''

def ticket_i(lang, items, channel, when):
    u = UI[lang]
    lis = "".join(f'<li class="sub">{e(t)}</li>' if not q else f'<li><span>{e(q)}</span>{e(t)}</li>' for q, t in items)
    return f'''<div class="ticket" role="img" aria-label="{e(u["example"])}: kitchen ticket">
<div class="t-head"><span>CONVEASY</span><span>#1042</span></div>
<div class="t-meta"><span>{e(channel)}</span><span>{e(when)}</span></div>
<ul>{lis}</ul>
<div class="t-foot"><span>{e(u["example"])}</span><span>19:32</span></div>
</div>'''

TICKET_META = {"nl": ("Via telefoon AI", "Levering · klaar 19:55"), "fr": ("Via téléphone IA", "Livraison · prête à 19:55"), "en": ("Via phone AI", "Delivery · ready 19:55")}
HOME_TICKET = S["frituur"]

CHAT = {
    "nl": ("Je zaak", "WhatsApp · AI antwoordt", "Hoi! 1 grote friet met andalouse en een bicky burger, levering aub", "Komt in orde. Je bestelling: 1x grote friet (andalouse), 1x bicky burger. Levering naar je adres. Wil je bevestigen?", "Bevestigen", "Aanpassen"),
    "fr": ("Votre établissement", "WhatsApp · l'IA répond", "Bonjour ! 1 grande frite andalouse et un bicky burger, en livraison svp", "C'est noté. Votre commande : 1x grande frite (andalouse), 1x bicky burger. Livraison à votre adresse. Vous confirmez ?", "Confirmer", "Modifier"),
    "en": ("Your restaurant", "WhatsApp · AI replies", "Hi! 1 large fries with andalouse and a bicky burger, delivery please", "Got it. Your order: 1x large fries (andalouse), 1x bicky burger. Delivery to your address. Confirm?", "Confirm", "Change"),
}
def chat_i(lang):
    n, s, cin, ai, b1, b2 = CHAT[lang]
    return f'''<div class="chat" role="img" aria-label="{e(UI[lang]["example"])}: WhatsApp">
<div class="c-top"><i aria-hidden="true"></i><span>{e(n)}<small>{e(s)}</small></span></div>
<div class="bubble in">{e(cin)}</div><div class="bubble ai">{e(ai)}</div>
<div class="chat-btns"><span>{e(b1)}</span><span>{e(b2)}</span></div>
</div>'''

DASH = {
    "nl": ("Live bestellingen", "Open", [("Telefoon", "#1042 · Levering", "19:55"), ("WhatsApp", "#1043 · Afhalen", "20:05"), ("Webshop", "#1044 · Betaald online", "20:10"), ("Kiosk", "#1045 · Ter plaatse", "nu")], "Uitverkocht: Stoofvleessaus"),
    "fr": ("Commandes en direct", "Ouvert", [("Téléphone", "#1042 · Livraison", "19:55"), ("WhatsApp", "#1043 · À emporter", "20:05"), ("En ligne", "#1044 · Payée en ligne", "20:10"), ("Borne", "#1045 · Sur place", "maint.")], "Épuisé : sauce carbonnade"),
    "en": ("Live orders", "Open", [("Phone", "#1042 · Delivery", "19:55"), ("WhatsApp", "#1043 · Pickup", "20:05"), ("Webshop", "#1044 · Paid online", "20:10"), ("Kiosk", "#1045 · Eat in", "now")], "Sold out: stew sauce"),
}
def dash_i(lang):
    t, st, rows, so = DASH[lang]
    r = "".join(f'<div class="row"><span class="chip">{e(c)}</span><b>{e(o)}</b><small>{e(tm)}</small></div>' for c, o, tm in rows)
    return f'''<div class="panel" role="img" aria-label="{e(UI[lang]["example"])}: dashboard"><div class="p-title">{e(t)}<span>{e(st)}</span></div>{r}
<div class="row"><span class="chip y">!</span><b>{e(so)}</b><small></small></div></div>'''

KIOSK = {"nl": ("Kiosk · Kies je taal", ["Friet & snacks", "Burgers", "Dranken"], "Betalen met kaart"),
         "fr": ("Borne · Choisissez votre langue", ["Frites et snacks", "Burgers", "Boissons"], "Payer par carte"),
         "en": ("Kiosk · Choose your language", ["Fries & snacks", "Burgers", "Drinks"], "Pay by card")}
def kiosk_i(lang):
    t, cats, pay = KIOSK[lang]
    r = "".join(f'<div class="row"><span class="chip">{i+1}</span><b>{e(c)}</b><small>›</small></div>' for i, c in enumerate(cats))
    return f'''<div class="panel" role="img" aria-label="{e(UI[lang]["example"])}: kiosk"><div class="p-title">{e(t)}<span>NL · FR · EN · TR · DE</span></div>{r}
<div class="row"><span class="chip y">€</span><b>{e(pay)}</b><small></small></div></div>'''

MKT = {"nl": ("Deze week", [("Instagram", "Reel: friet in 15 seconden"), ("Facebook", "Advertentie A/B-test"), ("Google", "Openingsuren en menu bijgewerkt"), ("AI-zoeken", "Menu leesbaar voor ChatGPT")]),
       "fr": ("Cette semaine", [("Instagram", "Reel : la frite en 15 secondes"), ("Facebook", "Test A/B de publicité"), ("Google", "Horaires et carte à jour"), ("Recherche IA", "Carte lisible par ChatGPT")]),
       "en": ("This week", [("Instagram", "Reel: fries in 15 seconds"), ("Facebook", "Ad A/B test"), ("Google", "Opening hours and menu updated"), ("AI search", "Menu readable by ChatGPT")])}
def mkt_i(lang):
    t, rows = MKT[lang]
    r = "".join(f'<div class="row"><span class="chip">{e(c)}</span><b>{e(x)}</b><small></small></div>' for c, x in rows)
    return f'''<div class="panel" role="img" aria-label="{e(UI[lang]["example"])}: marketing"><div class="p-title">{e(t)}<span>{e(P["marketing"][lang]["name"])}</span></div>{r}</div>'''

def framed(lang, inner):
    return f'<div>{inner}<p class="mock-label">{e(UI[lang]["example"])}</p></div>'
def ticket(lang, *a): return framed(lang, ticket_i(lang, *a))
def chat(lang): return framed(lang, chat_i(lang))
def dash(lang): return framed(lang, dash_i(lang))
def kiosk(lang): return framed(lang, kiosk_i(lang))
def mkt(lang): return framed(lang, mkt_i(lang))

# ---------------- App visuals: sample data, swap by dropping src/shots/<id>.png (or .jpg/.webp) ----------------
SHOT_DIR = os.path.join(HERE, "shots")
def shot_file(sid):
    for ext in ("png", "jpg", "jpeg", "webp"):
        if os.path.isfile(os.path.join(SHOT_DIR, f"{sid}.{ext}")): return f"{sid}.{ext}"
    return None

def kds_i(lang):
    t, cols, orders = OVX[lang]["kds"]
    cards = {0: "", 1: "", 2: ""}
    for c, num, ch, items, tm in orders:
        lis = "".join(f"<li>{e(x)}</li>" for x in items)
        cards[c] += f'<div class="k-card"><div class="k-top"><b>{e(num)}</b><small>{e(tm)}</small></div><span class="k-ch">{e(ch)}</span><ul>{lis}</ul></div>'
    colh = "".join(f'<div class="k-col k-{i}"><div class="k-h">{e(n)}<span>{sum(1 for o in orders if o[0] == i)}</span></div>{cards[i]}</div>' for i, n in enumerate(cols))
    return f'<div class="kds" role="img" aria-label="{e(UI[lang]["example"])}: {e(t)}"><div class="p-title">{e(t)}<span>19:48</span></div><div class="k-cols">{colh}</div></div>'

def resv_i(lang):
    t, day, rows, foot = OVX[lang]["resv_mock"]
    r = "".join(f'<div class="row"><span class="r-time">{e(tm)}</span><b>{e(nm)} <small>· {e(pp)}</small></b><span class="chip">{e(ch)}</span></div>' for tm, pp, nm, ch in rows)
    return f'<div class="panel resv" role="img" aria-label="{e(UI[lang]["example"])}: {e(t)}"><div class="p-title">{e(t)}<span>{e(day)}</span></div>{r}<div class="row new"><span class="chip y">+</span><b>{e(foot)}</b><small></small></div></div>'

def web_i(lang):
    shop, tag, cats, items, btn = OVX[lang]["web"]
    c = "".join(f'<span{" class=on" if i == 0 else ""}>{e(x)}</span>' for i, x in enumerate(cats))
    it = "".join(f'<div class="w-item"><i aria-hidden="true"></i><b>{e(n)}<small>{e(pr)}</small></b><span class="w-add" aria-hidden="true">+</span></div>' for n, pr in items)
    return f'<div class="phone" role="img" aria-label="{e(UI[lang]["example"])}: webshop"><div class="ph-screen"><div class="w-head"><b>{e(shop)}</b><small>{e(tag)}</small></div><div class="w-cats">{c}</div>{it}<div class="w-btn">{e(btn)}</div></div></div>'

SHOT_FN = {"dash": dash_i, "kds": kds_i, "resv": resv_i, "web": web_i, "kiosk": kiosk_i, "chat": chat_i,
           "ticket": lambda l: ticket_i(l, HOME_TICKET[l]["ticket"], *TICKET_META[l])}
def shot(lang, sid, prefix):
    cap = OVX[lang]["cap"][sid]
    f = shot_file(sid)
    if f:
        inner, lab = f'<img src="{prefix}assets/shots/{f}" alt="{e(cap)}" loading="lazy">', ""
    else:
        inner, lab = SHOT_FN[sid](lang), f' <span>{e(UI[lang]["example"])}</span>'
    return f'<figure class="shot" data-shot="{sid}"><div class="shot-frame">{inner}</div><figcaption>{e(cap)}{lab}</figcaption></figure>'

def shots_band(lang, prefix, ids):
    eb, title, text = OVX[lang]["gallery"]
    return f'<section class="band" id="app"><div class="wrap"><div class="section-head"><span class="eyebrow">{e(eb)}</span><h2>{e(title)}</h2><p>{e(text)}</p></div><div class="shots">{"".join(shot(lang, s, prefix) for s in ids)}</div></div></section>'

def resv_band(lang, prefix):
    r = OVX[lang]["resv"]
    pts = "".join(f"<li>{e(x)}</li>" for x in r["points"])
    return f'<section class="band dark" id="reservaties"><div class="wrap split"><div class="section-head" style="margin:0"><span class="eyebrow">{e(r["eyebrow"])}</span><h2>{e(r["title"])}</h2><p>{e(r["text"])}</p><ul class="ticks">{pts}</ul></div>{shot(lang, "resv", prefix)}</div></section>'

PAGE_SHOTS = {"phone": ["kds", "dash"], "whatsapp": ["dash", "kds"], "webshop": ["dash", "kds"], "kiosk": ["kds", "dash"]}

def mock_for(lang, pid):
    meta = TICKET_META[lang]
    if pid == "phone": return ticket(lang, HOME_TICKET[lang]["ticket"], *meta)
    if pid == "whatsapp": return chat(lang)
    if pid == "webshop": return framed(lang, web_i(lang))
    if pid == "kiosk": return kiosk(lang)
    if pid == "marketing": return mkt(lang)
    if pid in SECTORS: return ticket(lang, S[pid][lang]["ticket"], *meta)
    return ""

def crumbs_html(lang, prefix, trail):
    lis = "".join(f'<li><a href="{prefix + path_of(lang, p)}">{e(n)}</a></li>' if p else f'<li aria-current="page">{e(n)}</li>' for n, p in trail)
    return f'<nav aria-label="Breadcrumb"><ol class="crumbs">{lis}</ol></nav>'

def faq_band(lang, faqs, page):
    u = UI[lang]
    items = "".join(f'<details><summary>{e(q)}</summary><p>{ph(a, lang, page)}</p></details>' for q, a in faqs)
    return f'''<section class="band" id="faq"><div class="wrap faq-wrap"><div class="section-head"><span class="eyebrow">{e(u["faq_eyebrow"])}</span><h2>{e(u["faq_title"])}</h2></div><div class="faq">{items}</div></div></section>'''

def cta_band(lang, prefix):
    u = UI[lang]
    return f'''<section class="band dark cta"><div class="wrap"><h2>{e(u["cta_title"])}</h2><p>{e(u["cta_text"])}</p>
<div class="btn-row"><a class="btn btn-primary" href="{prefix + path_of(lang, "contact")}">{e(u["demo"])} <span class="arr" aria-hidden="true">→</span></a><a class="btn btn-ghost" href="{WA_LINK}" rel="noopener">{e(u["wa"])}: {e(WA_DISPLAY)}</a></div></div></section>'''

def how_band(lang):
    u = UI[lang]
    sw = {"nl": "Stap", "fr": "Étape", "en": "Step", "tr": "Adım", "de": "Schritt"}[lang]
    steps = "".join(f'<li><span class="step-n">{sw} {i}</span><h3>{e(t)}</h3><p class="note">{e(d)}</p></li>' for i, (t, d) in enumerate(u["steps"], 1))
    return f'''<section class="band"><div class="wrap"><div class="section-head"><span class="eyebrow">{e(u["how_eyebrow"])}</span><h2>{e(u["how_title"])}</h2></div><ol class="steps">{steps}</ol></div></section>'''

def product_cards(lang, prefix, exclude=None, only=None):
    u = UI[lang]
    ids = only or PRODUCTS
    out = []
    for p in ids:
        if p == exclude: continue
        d = P[p][lang]
        tag = f'<span class="tag">{e(d["badge"])}</span>' if d.get("badge") else ""
        out.append(f'<a class="card" href="{prefix + path_of(lang, p)}">{tag}<h3>{e(d["name"])}</h3><p>{e(d["card"])}</p><span class="more">{e(u["more"])} →</span></a>')
    return "".join(out)

def hero(lang, prefix, h1, lead, mock, page, badge=None, facts=None, extra=""):
    u = UI[lang]
    b = f'<span class="badge"><i aria-hidden="true"></i>{e(badge)}</span>' if badge else ""
    f = ('<ul class="stats">' + "".join(f"<li><b>{e(x)}</b></li>" for x in facts) + "</ul>") if facts else ""
    st = f'<div class="stage">{mock}</div>' if mock else ""
    return f'''<section class="hero"><div class="hero-bg" aria-hidden="true"></div><div class="wrap"><div class="hero-copy">{extra}{b}<h1>{rich(h1, lang, page)}</h1><p class="lead">{ph(lead, lang, page)}</p>
<div class="btn-row"><a class="btn btn-primary" href="{prefix + path_of(lang, "contact")}">{e(u["demo"])} <span class="arr" aria-hidden="true">→</span></a><a class="btn btn-ghost" href="{WA_LINK}" rel="noopener">{e(u["wa"])}</a></div></div>{st}{f}</div></section>'''

def price_card(name, amount, per, sub, feats, lang, page, pop=False, pop_label="", note=""):
    badge = f'<span class="chip">{e(pop_label)}</span>' if pop else ""
    amt = f'€{e(amount)}<small>{e(per)}</small>' if amount and amount[0].isdigit() else ph(amount, lang, page)
    lis = "".join(f"<li>{e(x)}</li>" for x in feats)
    n = f'<p class="note">{ph(note, lang, page)}</p>' if note else ""
    return f'<div class="price{" pop" if pop else ""}"><h3>{e(name)}{badge}</h3><div class="amount">{amt}</div><p class="sub">{e(sub)}</p><ul>{lis}</ul>{n}</div>'

def phone_tiers(lang, page):
    pr = PRICING[lang]
    return "".join(price_card(n, price, UI[lang]["per_month"], mins, pr["tier_feats"], lang, page, pop, pr["popular"], pr["setup"]) for n, price, mins, pop in pr["tiers"])

def product_price_band(lang, pid, prefix, page):
    u, pr = UI[lang], PRICING[lang]
    if pid == "phone":
        body = f'<div class="price-grid">{phone_tiers(lang, page)}</div>'
    elif pid == "whatsapp":
        body = f'<div class="price-grid">{price_card(P["whatsapp"][lang]["name"], "99", u["per_month"], pr["year"], pr["wa_feats"], lang, page, note=pr["setup_other"])}</div>'
    elif pid == "webshop":
        body = f'<div class="price-grid">{price_card(P["webshop"][lang]["name"], "79", u["per_month"], pr["year"], pr["web_feats"], lang, page, note=pr["setup_other"])}</div>'
    elif pid == "kiosk":
        body = f'<div class="price-grid">{price_card(P["kiosk"][lang]["name"], pr["kiosk_price"], u["per_month"], pr["kiosk_sub"], pr["kiosk_feats"], lang, page, note=pr["setup_other"])}</div>'
    else:
        body = f'<div class="price-grid">{price_card(P["marketing"][lang]["name"], pr["mkt_price"], u["per_month"], "", pr["mkt_feats"], lang, page)}</div>'
    return f'''<section class="band"><div class="wrap"><div class="section-head"><span class="eyebrow">{e(u["pricing"])}</span><h2>{e(u["price_title"])}</h2></div>{body}
<p class="note" style="margin-top:16px"><a href="{prefix + path_of(lang, "pricing")}">{e(u["see_prices"])} →</a></p></div></section>'''

# ---------------- Pages ----------------
# ---------------- round 4: home stage, marquee, order flow ----------------
CALL = {"nl": ("Inkomende oproep", "AI neemt op"), "fr": ("Appel entrant", "L'IA répond"), "en": ("Incoming call", "AI answering"),
        "tr": ("Gelen arama", "YZ cevaplıyor"), "de": ("Eingehender Anruf", "KI nimmt an")}
def home_stage(lang):
    k = kds_i(lang).replace('<div class="k-card">', '<div class="k-card k-new">', 1)
    c1, c2 = CALL[lang]
    call = f'<div class="call" role="img" aria-label="{e(UI[lang]["example"])}: {e(c1)}"><span class="call-dot" aria-hidden="true"></span><span><b>{e(c1)}</b><small>{e(c2)} · 00:42</small></span><span class="wave" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span></div>'
    return (f'<div class="stage-home"><div class="layer l-kds">{k}</div>'
            f'<div class="layer l-ticket">{ticket_i(lang, HOME_TICKET[lang]["ticket"], *TICKET_META[lang])}</div>'
            f'<div class="layer l-phone">{web_i(lang)}</div><div class="layer l-call">{call}</div></div>'
            f'<p class="mock-label">{e(UI[lang]["example"])}</p>')

GREET = ["Goeiedag", "Bonjour", "Hello", "Merhaba", "Guten Tag", "Hola", "Ciao", "مرحبا", "Olá", "Dzień dobry", "Salam", "Hallo"]
MQ_LABEL = {"nl": "De AI spreekt 60+ talen", "fr": "L'IA parle plus de 60 langues", "en": "The AI speaks 60+ languages",
            "tr": "YZ 60'tan fazla dil konuşur", "de": "Die KI spricht über 60 Sprachen"}
def marquee(lang):
    hl = HOME[lang]["facts"][1]
    items = []
    for i, g in enumerate(GREET):
        items.append(f'<span lang="{"ar" if g == "مرحبا" else ""}" dir="auto">{e(g)}</span>'.replace(' lang=""', ''))
        if i == 5: items.append(f'<span class="hl">{e(hl)}</span>')
    row = "".join(items)
    return (f'<section class="marquee"><p class="sr-only">{e(MQ_LABEL[lang])}</p>'
            f'<div class="mq-track" aria-hidden="true"><div>{row}</div><div>{row}</div></div></section>')

FLOW = {
 "nl": ("Van bestelling tot keuken", "Zo loopt een bestelling", [
    ("De klant belt of stuurt een bericht", "Aan de telefoon of op WhatsApp, op elk uur en in de taal van de klant."),
    ("De AI neemt de bestelling op", "Hij vraagt wat nodig is, herhaalt de bestelling en laat de klant bevestigen."),
    ("Het ticket staat in de keuken", "De bon komt uit de keukenprinter en verschijnt op het keukenscherm."),
    ("Alles in één dashboard", "Telefoon, WhatsApp, webshop en kiosk samen op één overzicht.")]),
 "fr": ("De la commande à la cuisine", "Le parcours d'une commande", [
    ("Le client appelle ou envoie un message", "Au téléphone ou sur WhatsApp, à toute heure et dans la langue du client."),
    ("L'IA prend la commande", "Elle pose les bonnes questions, répète la commande et la fait confirmer."),
    ("Le ticket arrive en cuisine", "Le bon sort de l'imprimante cuisine et s'affiche sur l'écran cuisine."),
    ("Tout dans un seul tableau de bord", "Téléphone, WhatsApp, boutique en ligne et borne réunis en un seul aperçu.")]),
 "en": ("From order to kitchen", "How an order flows", [
    ("The customer calls or sends a message", "By phone or on WhatsApp, at any hour and in the customer's language."),
    ("The AI takes the order", "It asks what it needs, repeats the order and has the customer confirm."),
    ("The ticket is in the kitchen", "The ticket prints on the kitchen printer and shows on the kitchen screen."),
    ("Everything in one dashboard", "Phone, WhatsApp, webshop and kiosk together in one overview.")]),
 "tr": ("Siparişten mutfağa", "Bir sipariş nasıl ilerler", [
    ("Müşteri arar ya da mesaj gönderir", "Telefonla veya WhatsApp'tan, her saatte ve müşterinin dilinde."),
    ("YZ siparişi alır", "Gerekenleri sorar, siparişi tekrarlar ve müşteriye onaylatır."),
    ("Fiş mutfakta", "Fiş mutfak yazıcısından çıkar ve mutfak ekranında görünür."),
    ("Hepsi tek panelde", "Telefon, WhatsApp, online sipariş ve kiosk tek bir genel bakışta.")]),
 "de": ("Von der Bestellung bis in die Küche", "So läuft eine Bestellung", [
    ("Der Kunde ruft an oder schreibt", "Am Telefon oder auf WhatsApp, zu jeder Uhrzeit und in der Sprache des Kunden."),
    ("Die KI nimmt die Bestellung auf", "Sie fragt nach, was nötig ist, wiederholt die Bestellung und lässt sie bestätigen."),
    ("Der Bon ist in der Küche", "Der Bon kommt aus dem Küchendrucker und erscheint auf dem Küchenbildschirm."),
    ("Alles in einem Dashboard", "Telefon, WhatsApp, Webshop und Kiosk zusammen in einer Übersicht.")]),
}
def flow_band(lang):
    eb, title, steps = FLOW[lang]
    screens = [chat_i(lang), ticket_i(lang, HOME_TICKET[lang]["ticket"], *TICKET_META[lang]), kds_i(lang), dash_i(lang)]
    stage = "".join(f'<div class="fs" data-s="{i}">{sc}</div>' for i, sc in enumerate(screens))
    lis = "".join(f'<li data-s="{i}"{" class=on" if i == 0 else ""}><span class="fs-n">0{i+1} / 04</span><h3>{e(t)}</h3><p>{e(x)}</p><div class="fs-inline" aria-hidden="true">{screens[i]}</div></li>' for i, (t, x) in enumerate(steps))
    return (f'<section class="band dark flow"><div class="wrap"><div class="section-head"><span class="eyebrow">{e(eb)}</span><h2>{e(title)}</h2></div>'
            f'<div class="flow-grid"><ol class="flow-steps">{lis}</ol><div class="flow-stage" data-step="0" aria-hidden="true">{stage}</div></div></div></section>')

# Sammy, Nov 11: "Probeer onze AI" voice demo (Vapi). Assistant ID from Sammy; the public key goes in site.js.
VAPI_ASSISTANT_ID = "7ffc6c16-d943-4f97-98e3-a84351ffd954"
DEMO = {
    "nl": ("Live demo", "Probeer onze AI", "Praat zelf met onze telefoon-AI. Doe alsof je naar een demo-snackbar belt en bestel iets: frietjes, een snack, een saus.",
           "Start gesprek", "Gesprek beëindigen", "Verbinden…", "Je bent verbonden. Praat maar.", "Gesprek beëindigd.",
           "De demo kon niet starten. Probeer het later opnieuw.", "De demo is nog niet ingesteld.",
           "De demo duurt maximaal 3 minuten. Je browser vraagt toegang tot je microfoon."),
    "fr": ("Démo en direct", "Essayez notre IA", "Parlez vous-même à notre IA téléphonique. Faites comme si vous appeliez un snack de démonstration et commandez : des frites, un snack, une sauce.",
           "Démarrer l'appel", "Terminer l'appel", "Connexion…", "Vous êtes connecté. Parlez.", "Appel terminé.",
           "La démo n'a pas pu démarrer. Réessayez plus tard.", "La démo n'est pas encore configurée.",
           "La démo dure 3 minutes maximum. Votre navigateur demande l'accès à votre micro."),
    "en": ("Live demo", "Try our AI", "Talk to our phone AI yourself. Pretend you're calling a demo snack bar and order something: fries, a snack, a sauce.",
           "Start call", "End call", "Connecting…", "You're connected. Go ahead and talk.", "Call ended.",
           "The demo couldn't start. Please try again later.", "The demo isn't set up yet.",
           "The demo lasts 3 minutes at most. Your browser will ask for microphone access."),
    "tr": ("Canlı demo", "Yapay zekâmızı dene", "Telefon yapay zekâmızla kendin konuş. Bir demo snack bar'ı arıyormuş gibi yap ve sipariş ver: patates, atıştırmalık, sos.",
           "Görüşmeyi başlat", "Görüşmeyi bitir", "Bağlanıyor…", "Bağlandın. Konuşabilirsin.", "Görüşme bitti.",
           "Demo başlatılamadı. Daha sonra tekrar dene.", "Demo henüz ayarlanmadı.",
           "Demo en fazla 3 dakika sürer. Tarayıcın mikrofon izni ister."),
    "de": ("Live-Demo", "Testen Sie unsere KI", "Sprechen Sie selbst mit unserer Telefon-KI. Tun Sie so, als würden Sie einen Demo-Imbiss anrufen, und bestellen Sie etwas: Pommes, einen Snack, eine Soße.",
           "Gespräch starten", "Gespräch beenden", "Verbinde…", "Sie sind verbunden. Sprechen Sie einfach.", "Gespräch beendet.",
           "Die Demo konnte nicht starten. Bitte versuchen Sie es später erneut.", "Die Demo ist noch nicht eingerichtet.",
           "Die Demo dauert höchstens 3 Minuten. Ihr Browser fragt nach Zugriff auf Ihr Mikrofon."),
}

# Shown instead of the error text on the preview build: inside the Claude preview a page cannot use the microphone or call other servers.
PREVIEW_NOTE = {
    "nl": "In deze preview werkt de live demo niet. Op de echte website werkt hij wel.",
    "fr": "La démo en direct ne fonctionne pas dans cet aperçu. Elle fonctionne sur le vrai site.",
    "en": "The live demo doesn't work inside this preview. It does on the real website.",
    "tr": "Canlı demo bu önizlemede çalışmaz. Gerçek sitede çalışır.",
    "de": "Die Live-Demo funktioniert in dieser Vorschau nicht. Auf der echten Website funktioniert sie.",
}

def demo_band(lang):
    eb, h2, txt, start, stop, wait, live, ended, err, notset, note = DEMO[lang]
    return (f'<section class="band demo-band" id="demo"><div class="wrap"><div class="demo">'
            f'<div class="demo-copy"><span class="eyebrow">{e(eb)}</span><h2>{e(h2)}</h2><p>{e(txt)}</p><p class="demo-note">{e(note)}</p></div>'
            f'<div class="demo-ctl"><div class="demo-orb" aria-hidden="true"><i></i><i></i><i></i></div>'
            f'<button type="button" class="btn btn-primary demo-btn" data-vapi="{VAPI_ASSISTANT_ID}" data-state="idle" '
            f'data-l-start="{e(start)}" data-l-stop="{e(stop)}" data-l-wait="{e(wait)}" data-m-live="{e(live)}" data-m-ended="{e(ended)}" data-m-error="{e(err)}" data-m-notset="{e(notset)}" data-m-preview="{e(PREVIEW_NOTE[lang])}">'
            f'<span class="mic" aria-hidden="true"></span><span class="demo-label">{e(start)}</span></button>'
            f'<p class="demo-state" role="status" aria-live="polite"></p></div></div></div></section>')

WADEMO = {
    "nl": {"eb": "Live demo", "h2": "Bestel via WhatsApp", "txt": "Typ zelf een bestelling, net zoals je klanten op WhatsApp doen. Onze AI antwoordt en neemt je bestelling op.",
           "greet": "Hallo! Welkom bij Mario's Snackbar. Wat mag het zijn vandaag?", "ph": "Typ een bericht", "send": "Versturen", "typing": "Aan het typen…",
           "notset": "Deze chatdemo is nog niet ingesteld.", "err": "Er ging iets mis. Probeer het later opnieuw.", "note": "Demo, er wordt niets echt besteld.",
           "chips": ["Een grote friet met mayo", "Welke burgers hebben jullie?"], "online": "AI-assistent · online", "limit": "Dat was het einde van de demo. Bedankt!"},
    "fr": {"eb": "Démo en direct", "h2": "Commandez par WhatsApp", "txt": "Tapez vous-même une commande, comme vos clients le font sur WhatsApp. Notre IA répond et prend votre commande.",
           "greet": "Bonjour ! Bienvenue chez Mario's Snackbar. Que puis-je vous servir aujourd'hui ?", "ph": "Écrivez un message", "send": "Envoyer", "typing": "En train d'écrire…",
           "notset": "Cette démo de chat n'est pas encore configurée.", "err": "Un problème est survenu. Réessayez plus tard.", "note": "Démo, rien n'est vraiment commandé.",
           "chips": ["Une grande frite mayo", "Quels burgers avez-vous ?"], "online": "Assistant IA · en ligne", "limit": "C'était la fin de la démo. Merci !"},
    "en": {"eb": "Live demo", "h2": "Order on WhatsApp", "txt": "Type an order yourself, just like your customers do on WhatsApp. Our AI replies and takes your order.",
           "greet": "Hi! Welcome to Mario's Snackbar. What can I get you today?", "ph": "Type a message", "send": "Send", "typing": "Typing…",
           "notset": "This chat demo isn't set up yet.", "err": "Something went wrong. Please try again later.", "note": "Demo, nothing is actually ordered.",
           "chips": ["A large fries with mayo", "Which burgers do you have?"], "online": "AI assistant · online", "limit": "That's the end of the demo. Thanks!"},
    "tr": {"eb": "Canlı demo", "h2": "WhatsApp'tan sipariş ver", "txt": "Müşterilerinin WhatsApp'ta yaptığı gibi sen de bir sipariş yaz. Yapay zekâmız cevap verir ve siparişini alır.",
           "greet": "Merhaba! Mario's Snackbar'a hoş geldin. Bugün ne alırsın?", "ph": "Bir mesaj yaz", "send": "Gönder", "typing": "Yazıyor…",
           "notset": "Bu sohbet demosu henüz ayarlanmadı.", "err": "Bir sorun oluştu. Daha sonra tekrar dene.", "note": "Demo, gerçekten hiçbir şey sipariş edilmez.",
           "chips": ["Mayonezli büyük patates", "Hangi burgerleriniz var?"], "online": "Yapay zekâ asistanı · çevrimiçi", "limit": "Demonun sonuna geldik. Teşekkürler!"},
    "de": {"eb": "Live-Demo", "h2": "Per WhatsApp bestellen", "txt": "Tippen Sie selbst eine Bestellung ein, so wie Ihre Kunden auf WhatsApp. Unsere KI antwortet und nimmt Ihre Bestellung auf.",
           "greet": "Hallo! Willkommen bei Mario's Snackbar. Was darf es heute sein?", "ph": "Nachricht schreiben", "send": "Senden", "typing": "Schreibt…",
           "notset": "Diese Chat-Demo ist noch nicht eingerichtet.", "err": "Etwas ist schiefgelaufen. Bitte versuchen Sie es später erneut.", "note": "Demo, es wird nichts wirklich bestellt.",
           "chips": ["Große Pommes mit Mayo", "Welche Burger haben Sie?"], "online": "KI-Assistent · online", "limit": "Das war das Ende der Demo. Danke!"},
}

def wa_demo_band(lang):
    w = WADEMO[lang]
    chips = "".join(f'<button type="button" class="wa-chip">{e(c)}</button>' for c in w["chips"])
    return (f'<section class="band demo-band" id="whatsapp-demo"><div class="wrap"><div class="demo wa-demo">'
            f'<div class="demo-copy"><span class="eyebrow">{e(w["eb"])}</span><h2>{e(w["h2"])}</h2><p>{e(w["txt"])}</p><p class="demo-note">{e(w["note"])}</p></div>'
            f'<div class="wa" data-wa-demo data-lang="{lang}" data-m-notset="{e(w["notset"])}" data-m-error="{e(w["err"])}" data-m-typing="{e(w["typing"])}" data-m-limit="{e(w["limit"])}" data-m-preview="{e(PREVIEW_NOTE[lang])}">'
            f'<div class="wa-head"><span class="wa-av" aria-hidden="true">M</span><div class="wa-who"><b>Mario&#x27;s Snackbar <span class="wa-check" aria-hidden="true"></span></b><small>{e(w["online"])}</small></div></div>'
            f'<div class="wa-log" role="log" aria-live="polite"><div class="wa-msg in"><p>{e(w["greet"])}</p><time></time></div></div>'
            f'<div class="wa-chips">{chips}</div>'
            f'<form class="wa-input" autocomplete="off"><input type="text" name="wa" maxlength="300" placeholder="{e(w["ph"])}" aria-label="{e(w["ph"])}">'
            f'<button type="submit" class="wa-send" aria-label="{e(w["send"])}"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M3.4 20.4 21 12 3.4 3.6 3.4 10l12.6 2-12.6 2z"/></svg></button></form>'
            f'</div></div></div></section>')

def page_home(lang, prefix):
    d, u = HOME[lang], UI[lang]
    pg = f"{lang}/home"
    sec_cards = "".join(f'<a class="card" href="{prefix + path_of(lang, s)}"><h3>{e(S[s][lang]["name"])}</h3><p>{e(S[s][lang]["pains"][0][1])}</p><span class="more">{e(u["more"])} →</span></a>' for s in SECTORS)
    dash_feats = "".join(f'<div class="feature"><h3>{e(t)}</h3><p>{e(x)}</p></div>' for t, x in d["dash_feats"])
    body = hero(lang, prefix, d["h1"], d["lead"] + " " + d["made_by"], home_stage(lang), pg, badge=d["badge"], facts=d["facts"])
    body = body.replace('<section class="hero">', '<section class="hero hero-home">', 1)
    body += demo_band(lang) + wa_demo_band(lang) + marquee(lang) + flow_band(lang)
    body += f'''<section class="band" id="producten"><div class="wrap"><div class="section-head"><span class="eyebrow">{e(d["products_eyebrow"])}</span><h2>{e(d["products_title"])}</h2><p>{e(d["products_text"])}</p></div>
<div class="bento">{product_cards(lang, prefix)}<a class="card" href="{prefix + path_of(lang, "marketing")}"><h3>{e(P["webshop"][lang]["extra_title"])}</h3><p>{e(P["webshop"][lang]["extra_text"])}</p><span class="more">{e(u["more"])} →</span></a><a class="card" href="{prefix + path_of(lang, "phone")}#reservaties"><span class="tag">24/7</span><h3>{e(OVX[lang]["resv"]["card"][0])}</h3><p>{e(OVX[lang]["resv"]["card"][1])}</p><span class="more">{e(u["more"])} →</span></a></div></div></section>
<section class="band dark"><div class="wrap" style="display:grid;gap:40px;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));align-items:center">
<div style="display:grid;gap:24px;min-width:0"><div class="section-head" style="margin:0"><span class="eyebrow">{e(d["dash_eyebrow"])}</span><h2>{e(d["dash_title"])}</h2><p>{e(d["dash_text"])}</p></div><div class="grid">{dash_feats}</div></div>{dash(lang)}</div></section>
{shots_band(lang, prefix, ["kds", "resv", "web", "kiosk"])}
<section class="band"><div class="wrap"><div class="section-head"><span class="eyebrow">{e(d["sectors_eyebrow"])}</span><h2>{e(d["sectors_title"])}</h2></div><div class="grid">{sec_cards}</div></div></section>
{how_band(lang)}
<section class="band"><div class="wrap grid-3" style="align-items:start">
<div class="section-head" style="margin:0;grid-column:span 2;max-width:none"><span class="eyebrow">{e(d["story_eyebrow"])}</span><h2>{e(d["story_title"])}</h2><p class="lead">{e(d["story_text"])}</p><p><a href="{prefix + path_of(lang, "about")}">{e(d["story_link"])} →</a></p></div>
<div class="card"><span class="eyebrow" style="margin:0">{e(d["price_eyebrow"])}</span><h3>{e(d["price_title"])}</h3><p>{e(d["price_text"])}</p><a class="more" href="{prefix + path_of(lang, "pricing")}">{e(u["see_prices"])} →</a></div>
</div></section>'''
    body += faq_band(lang, d["faq"], pg) + cta_band(lang, prefix)
    return body, d["faq"], []

def page_product(lang, pid, prefix):
    d, u = P[pid][lang], UI[lang]
    pg = f"{lang}/{pid}"
    trail = [(u["home"], "home"), (d["name"], None)]
    feats = "".join(f'<div class="feature"><h3>{e(t)}</h3><p>{ph(x, lang, pg)}</p></div>' for t, x in d["features"])
    body = hero(lang, prefix, d["h1"], d["lead"], mock_for(lang, pid), pg, badge=d.get("badge"), extra=crumbs_html(lang, prefix, trail))
    if pid == "phone":
        body += demo_band(lang)
    if pid == "whatsapp":
        body += wa_demo_band(lang)
    body += f'<section class="band"><div class="wrap"><div class="grid">{feats}</div></div></section>'
    if pid in ("phone", "whatsapp"):
        body += resv_band(lang, prefix)
    if pid in PAGE_SHOTS:
        body += shots_band(lang, prefix, PAGE_SHOTS[pid])
    body += product_price_band(lang, pid, prefix, pg)
    if pid != "marketing":
        body += how_band(lang)
    body += f'''<section class="band"><div class="wrap"><div class="section-head"><span class="eyebrow">{e(u["products"])}</span><h2>{e(u["other_products"])}</h2><p>{e(u["all_in_one"])}.</p></div><div class="grid">{product_cards(lang, prefix, exclude=pid)}</div></div></section>'''
    body += faq_band(lang, d["faq"], pg) + cta_band(lang, prefix)
    crumbs = [(u["home"], canonical(lang, "home")), (d["name"], canonical(lang, pid))]
    return body, d["faq"], crumbs

def page_sector(lang, sid, prefix):
    d, u = S[sid][lang], UI[lang]
    pg = f"{lang}/{sid}"
    trail = [(u["home"], "home"), (d["name"], None)]
    pains = "".join(f'<div class="feature"><h3>{e(t)}</h3><p>{e(x)}</p></div>' for t, x in d["pains"])
    only = ["phone", "whatsapp", "webshop", "kiosk"]
    body = hero(lang, prefix, d["h1"], d["lead"], mock_for(lang, sid), pg, extra=crumbs_html(lang, prefix, trail))
    body += f'<section class="band"><div class="wrap"><div class="grid">{pains}</div></div></section>'
    body += shots_band(lang, prefix, ["dash", "kds"])
    body += f'''<section class="band"><div class="wrap"><div class="section-head"><span class="eyebrow">{e(u["products"])}</span><h2>{e(HOME[lang]["products_title"])}</h2><p>{e(HOME[lang]["products_text"])}</p></div><div class="grid">{product_cards(lang, prefix, only=only)}</div></div></section>'''
    body += how_band(lang) + faq_band(lang, d["faq"], pg) + cta_band(lang, prefix)
    crumbs = [(u["home"], canonical(lang, "home")), (d["name"], canonical(lang, sid))]
    return body, d["faq"], crumbs

def page_pricing(lang, prefix):
    d, u = PRICING[lang], UI[lang]
    pg = f"{lang}/pricing"
    trail = [(u["home"], "home"), (u["pricing"], None)]
    body = f'''<section class="hero"><div class="wrap" style="grid-template-columns:minmax(0,1fr)"><div class="hero-copy">{crumbs_html(lang, prefix, trail)}<h1>{e(d["h1"])}</h1><p class="lead">{e(d["lead"])}</p></div></div></section>
<section class="band"><div class="wrap">
<div class="price-group"><h2>{e(d["phone_h"])}</h2><p class="note">{e(d["phone_note"])}</p><div class="price-grid">{phone_tiers(lang, pg)}</div></div>
<div class="price-group"><h2>{e(d["text_h"])}</h2><div class="price-grid">{price_card(P["whatsapp"][lang]["name"], "99", u["per_month"], d["year"], d["wa_feats"], lang, pg, note=d["setup_other"])}{price_card(P["webshop"][lang]["name"], "79", u["per_month"], d["year"], d["web_feats"], lang, pg, note=d["setup_other"])}</div></div>
<div class="price-group"><h2>{e(d["more_h"])}</h2><div class="price-grid">{price_card(P["kiosk"][lang]["name"], d["kiosk_price"], u["per_month"], d["kiosk_sub"], d["kiosk_feats"], lang, pg, note=d["setup_other"])}{price_card(P["marketing"][lang]["name"], d["mkt_price"], u["per_month"], "", d["mkt_feats"], lang, pg)}</div></div>
<div class="card" style="max-width:820px"><p><strong>{e(d["combo"])}</strong></p><p>{ph(d["trial"], lang, pg)}</p><p>{ph(d["hardware"], lang, pg)}</p><p><a class="more" href="{prefix + path_of(lang, "contact")}">{e(u["demo"])} →</a></p></div>
</div></section>'''
    body += faq_band(lang, d["faq"], pg) + cta_band(lang, prefix)
    return body, d["faq"], [(u["home"], canonical(lang, "home")), (u["pricing"], canonical(lang, "pricing"))]

def page_about(lang, prefix):
    d, u = ABOUT[lang], UI[lang]
    pg = f"{lang}/about"
    trail = [(u["home"], "home"), (u["about"], None)]
    blocks = "".join(f'<div class="card"><h3>{e(t)}</h3><p>{ph(x, lang, pg)}</p></div>' for t, x in d["blocks"])
    body = f'''<section class="hero"><div class="wrap" style="grid-template-columns:minmax(0,1fr)"><div class="hero-copy">{crumbs_html(lang, prefix, trail)}<h1>{e(d["h1"])}</h1><p class="lead">{e(d["lead"])}</p></div></div></section>
<section class="band"><div class="wrap"><div class="grid">{blocks}</div></div></section>'''
    body += cta_band(lang, prefix)
    return body, [], [(u["home"], canonical(lang, "home")), (u["about"], canonical(lang, "about"))]

def page_contact(lang, prefix):
    d, u = CONTACT[lang], UI[lang]
    pg = f"{lang}/contact"
    trail = [(u["home"], "home"), (u["contact"], None)]
    checks = "".join(f'<label><input type="checkbox" id="int-{p}" name="interest" value="{p}"> {e(P[p][lang]["name"])}</label>' for p in PRODUCTS)
    body = f'''<section class="hero"><div class="wrap" style="grid-template-columns:minmax(0,1fr)"><div class="hero-copy">{crumbs_html(lang, prefix, trail)}<h1>{e(d["h1"])}</h1><p class="lead">{e(d["lead"])}</p></div></div></section>
<section class="band" style="padding-top:0"><div class="wrap contact-grid">
<div class="wa-box card"><h2 style="font-size:1.4rem">{e(d["wa_h"])}</h2><p>{e(d["wa_text"])}</p><div class="wa-number">{e(WA_DISPLAY)}</div>
<div class="btn-row"><a class="btn btn-primary" href="{WA_LINK}" rel="noopener">{e(d["open_wa"])}</a><button type="button" class="btn btn-ghost" data-copy="{e(WA_DISPLAY)}" data-done="{e(d["copied"])}">{e(d["copy"])}</button></div>
<h3 style="margin-top:12px">{e(d["email_h"])}</h3><p>{ph(d["email"], lang, pg)}</p></div>
<form class="lead-form" novalidate data-to="conveasyai@gmail.com" data-subject="{e(d["f_subject"])}">
<div class="two"><div class="field"><label for="f-name">{e(d["f_name"])}</label><input id="f-name" name="name" autocomplete="name" required></div>
<div class="field"><label for="f-rest">{e(d["f_rest"])}</label><input id="f-rest" name="restaurant" autocomplete="organization" required></div></div>
<div class="two"><div class="field"><label for="f-city">{e(d["f_city"])}</label><input id="f-city" name="city" autocomplete="address-level2"></div>
<div class="field"><label for="f-phone">{e(d["f_phone"])}</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div></div>
<div class="field"><label for="f-email">{e(d["f_email"])}</label><input id="f-email" name="email" type="email" autocomplete="email"></div>
<fieldset><legend>{e(d["f_int"])}</legend><div class="checks">{checks}</div></fieldset>
<div class="field"><label for="f-msg">{e(d["f_msg"])}</label><textarea id="f-msg" name="message" rows="3"></textarea></div>
<button class="btn btn-primary" type="submit">{e(d["f_send"])}</button>
<p class="form-msg" hidden>{ph(d["f_note"], lang, pg)}</p>
</form></div></section>'''
    return body, [], [(u["home"], canonical(lang, "home")), (u["contact"], canonical(lang, "contact"))]

def page_legal(lang, prefix):
    d, u = LEGAL[lang], UI[lang]
    pg = f"{lang}/legal"
    company = "".join(f'<h2 style="font-size:1.3rem">{e(t)}</h2><p>{ph(x, lang, pg)}</p>' for t, x in d["blocks"][:1])
    mod = LEGAL_DOCS[lang]
    toc = "".join(f'<li><a href="#{doc["id"]}">{e(doc["title"])}</a></li>' for doc in mod.DOCS)
    docs = ""
    for doc in mod.DOCS:
        secs = ""
        for head, parts in doc["sections"]:
            inner = "".join(f"<p>{e(x)}</p>" if isinstance(x, str) else "<ul>" + "".join(f"<li>{e(i)}</li>" for i in x) + "</ul>" for x in parts)
            secs += f'<h3 style="font-size:1.05rem;margin-top:1.4em">{e(head)}</h3>{inner}'
        docs += f'<h2 id="{doc["id"]}" style="font-size:1.5rem;margin-top:2em;scroll-margin-top:96px">{e(doc["title"])}</h2><p style="opacity:.7">{e(doc["updated"])}</p><p>{e(doc["intro"])}</p>{secs}'
    body = f"""<section class="hero"><div class="wrap" style="grid-template-columns:minmax(0,1fr)"><div class="hero-copy"><h1>{e(d["h1"])}</h1></div></div></section>
<section class="band" style="padding-top:0"><div class="wrap"><div class="prose">{company}<ul>{toc}</ul>{docs}</div></div></section>"""
    return body, [], []

def render(lang, pid, prefix, preview, main=False):
    if pid == "home": body, faqs, crumbs = page_home(lang, prefix)
    elif pid in PRODUCTS: body, faqs, crumbs = page_product(lang, pid, prefix)
    elif pid in SECTORS: body, faqs, crumbs = page_sector(lang, pid, prefix)
    else: body, faqs, crumbs = {"pricing": page_pricing, "about": page_about, "contact": page_contact, "legal": page_legal}[pid](lang, prefix)
    bar = f'<div class="preview-bar"><div class="wrap">{e(UI[lang]["preview"])}</div></div>' if preview else ""
    inner = f'{bar}{header(lang, pid, prefix)}<main>{body}</main>{footer(lang, prefix, f"{lang}/{pid}")}<script src="{prefix}assets/site.js"></script>'
    hd = head(lang, pid, prefix, faqs, crumbs, main)
    if main:
        return hd + "\n" + inner + "\n"
    return f'<!doctype html>\n<html lang="{HTML_LANG[lang]}">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{hd}\n</head>\n<body>\n{inner}\n</body>\n</html>\n'

# ---------------- SEO files ----------------
def sitemap():
    rows = []
    for pid in SLUGS:
        for l in LANGS:
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{a}" href="{canonical(a, pid)}"/>' for a in LANGS)
            alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{canonical("nl", pid)}"/>'
            rows.append(f"<url><loc>{canonical(l, pid)}</loc>{alts}</url>")
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(rows) + "\n</urlset>\n"

ROBOTS = f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n"

def llms():
    L = ["# Conveasy", "",
         "> Conveasy is AI ordering software for restaurants in Belgium and the Benelux. An AI takes orders and table reservations by phone and on WhatsApp, 24/7 and in 60+ languages. Restaurants also get a commission-free webshop with QR ordering, a self-order kiosk (card and online payments only) and Marketing AI, which includes a digital stamp card in Google Wallet and Apple Wallet. All orders and reservations land in one dashboard, on the kitchen screen and on the kitchen printer.", "",
         "Key facts:",
         "- Phone AI: €249/month (500 minutes), €449/month (1,000 minutes), €799/month (2,000 minutes).",
         "- WhatsApp AI: €99/month, on the restaurant's own WhatsApp number.",
         "- Webshop + QR ordering: €79/month, 0% commission on orders.",
         "- Self-order kiosk: €89/month; 21.5-inch table-stand kiosk hardware €899 one-time, other models on request.",
         "- One-time setup fee: €299 for phone AI, €199 for each other channel, €399 for phone AI + WhatsApp AI + webshop + kiosk together.",
         "- Works separately from the restaurant's till (POS); each channel can be bought on its own.",
         "- Typical customers: frituren (Belgian fry shops), snack bars, pizzerias, burger restaurants.",
         "- Table reservations 24/7 through the phone AI and the WhatsApp AI; each reservation (name, date, time, party size) lands in the dashboard. Included in the phone AI and WhatsApp AI price at no extra cost.",
         "- Marketing AI: €69/month. Announcements to customers on all channels, Google review links, automatic emails for a second order and for unfinished orders, prepaid cards, and a digital stamp card in Google Wallet and Apple Wallet with notifications.",
         f"- Contact: WhatsApp {WA_DISPLAY}, {SITE}/en/contact", "",
         "## Products (English)"]
    for p in PRODUCTS:
        L.append(f"- [{P[p]['en']['name']}]({canonical('en', p)}): {P[p]['en']['card']}")
    L += ["", "## Restaurant types (English)"]
    for s in SECTORS:
        L.append(f"- [{S[s]['en']['name']}]({canonical('en', s)}): {plain(S[s]['en']['lead'])}")
    L += ["", "## Other pages",
          f"- [Pricing]({canonical('en', 'pricing')})", f"- [About]({canonical('en', 'about')})", f"- [Contact]({canonical('en', 'contact')})", "",
          "## Other languages", f"- Nederlands: {canonical('nl', 'home')}", f"- Français: {canonical('fr', 'home')}", f"- Türkçe: {canonical('tr', 'home')}", f"- Deutsch: {canonical('de', 'home')}", ""]
    return "\n".join(L)

# ---------------- Write ----------------
def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def build(outdir, preview):
    if os.path.isdir(outdir): shutil.rmtree(outdir)
    os.makedirs(os.path.join(outdir, "assets"))
    shutil.copy(os.path.join(HERE, "site.css"), os.path.join(outdir, "assets", "site.css"))
    shutil.copy(os.path.join(HERE, "site.js"), os.path.join(outdir, "assets", "site.js"))
    if os.path.isdir(SHOT_DIR) and any(shot_file(x) for x in SHOT_FN):
        shutil.copytree(SHOT_DIR, os.path.join(outdir, "assets", "shots"))
    for l in LANGS:
        for pid in SLUGS:
            write(os.path.join(outdir, path_of(l, pid)), render(l, pid, "../", preview))
    write(os.path.join(outdir, "index.html"), render("nl", "home", "", preview))
    write(os.path.join(outdir, "sitemap.xml"), sitemap())
    write(os.path.join(outdir, "robots.txt"), ROBOTS)
    write(os.path.join(outdir, "llms.txt"), llms())
    if preview:
        write(os.path.join(outdir, "main.html"), render("nl", "home", "", True, main=True))

def load_extra_langs():
    import importlib
    for mod in ("lang_tr", "lang_de"):
        try:
            m = importlib.import_module(mod)
        except ModuleNotFoundError:
            continue
        l, D = m.LANG, m.DATA
        if l not in LANGS: LANGS.append(l)
        LANG_NAMES[l] = D["LANG_NAME"]; HTML_LANG[l] = D["HTML_LANG"]; OG_LOCALE[l] = D["OG_LOCALE"]
        for pid, slug in D["SLUGS"].items(): SLUGS[pid][l] = slug
        UI[l] = D["UI"]; PRICING[l] = D["PRICING"]; HOME[l] = D["HOME"]; ABOUT[l] = D["ABOUT"]; CONTACT[l] = D["CONTACT"]; LEGAL[l] = D["LEGAL"]
        for pp in PRODUCTS: P[pp][l] = D["P"][pp]
        for ss in SECTORS: S[ss][l] = D["S"][ss]
        for name in ("TICKET_META", "CHAT", "DASH", "KIOSK", "MKT"): globals()[name][l] = D[name]

if __name__ == "__main__":
    load_extra_langs()
    apply_overrides(globals())
    answers.apply(globals())
    build(os.path.join(ROOT, "docs"), False)
    write(os.path.join(ROOT, "docs", ".nojekyll"), "")  # GitHub Pages: serve the files as they are
    PLACEHOLDERS.clear()
    build(os.path.join(ROOT, "preview"), True)
    # placeholder list (Dutch wording) for Sammy
    nl = sorted({t for (l, t) in PLACEHOLDERS if l == "nl"})
    # Only what is still open ends up in PLACEHOLDERS.txt: the two demo settings are read from site.js.
    js = open(os.path.join(HERE, "site.js"), encoding="utf-8").read()
    notes = []
    if "var VAPI_PUBLIC_KEY = 'VAPI_PUBLIC_KEY'" in js:
        notes.append("Vapi public key (spraakdemo): plak de PUBLIC key in src/site.js, regel 2, in plaats van VAPI_PUBLIC_KEY "
                     "(na een nieuwe build staat hij ook in assets/site.js). Beperk de key in Vapi tot conveasy.be en tot de demo-assistent.")
    if "var CHAT_DEMO_ENDPOINT = 'CHAT_DEMO_ENDPOINT'" in js:
        notes.append("Chatdemo in WhatsApp-stijl: zet in src/site.js de URL van de n8n-workflow 'Conveasy — Website chat demo (WhatsApp)' "
                     "in plaats van CHAT_DEMO_ENDPOINT. Die krijgt POST {message, history, lang} en antwoordt {reply, buttons}.")
    write(os.path.join(ROOT, "PLACEHOLDERS.txt"), "\n".join(nl + notes) + ("\n" if (nl or notes) else "Niets meer in te vullen.\n"))
    print("pages per lang:", len(SLUGS), "| placeholders (nl):", len(nl))
    for t in nl: print(" -", t)
