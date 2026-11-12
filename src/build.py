#!/usr/bin/env python3
"""Builds the Conveasy static site.
Outputs:
  ../docs/     the website itself (no preview banner). GitHub Pages serves this folder.
  ../preview/  same pages with a preview banner, plus main.html for the claude.ai preview
Run: python3 build.py
"""
import hashlib, html, json, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import *  # noqa
from overrides import OV as OVX, apply as apply_overrides
import answers
import extras
import sectors_more
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
# The Conveasy logo mark, the same drawing as on the Framer site (white; the colour comes from site.css). Also in brand/.
LOGO_MARK = '<svg class="logo-mark" viewBox="0 0 24 24" aria-hidden="true"><path d="M2 18c0-1.886 0-2.828.586-3.414C3.172 14 4.114 14 6 14s2.828 0 3.414.586C10 15.172 10 16.114 10 18s0 2.828-.586 3.414C8.828 22 7.886 22 6 22s-2.828 0-3.414-.586C2 20.828 2 19.886 2 18z"/><path fill-rule="evenodd" d="M3.464 3.464C2 4.93 2 7.286 2 12v1.138c.509-.333 1.069-.48 1.606-.551.645-.087 1.439-.087 2.305-.087h.179c.865 0 1.659 0 2.304.087.711.095 1.463.32 2.08.938.619.618.844 1.37.94 2.08.086.646.086 1.44.086 2.305v.18c0 .865 0 1.659-.087 2.304-.072.537-.218 1.097-.55 1.605L12 22c4.714 0 7.071 0 8.536-1.464C22 19.07 22 16.713 22 12c0-4.714 0-7.071-1.464-8.536C19.07 2 16.713 2 12 2 7.286 2 4.929 2 3.464 3.464zM15.75 12.75a.75.75 0 0 0 0-1.5h-1.94l3.72-3.72a.75.75 0 0 0-1.06-1.06l-3.72 3.72V8.25a.75.75 0 0 0-1.5 0V12c0 .414.336.75.75.75z"/></svg>'
# Fingerprint behind the address of the stylesheet and the script (site.css?v=1a2b3c4d), set per build in build().
# A browser that still holds last week's stylesheet would otherwise show a new page with the old styles until its copy expires.
ASSET_Q = {"css": "", "js": ""}
def asset_fingerprint(name):
    with open(os.path.join(HERE, name), "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:8]

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
              f'<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="{prefix}assets/apple-touch-icon.png">',
              '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
              f'<link rel="stylesheet" href="{FONTS}">',
              f'<link rel="stylesheet" href="{prefix}assets/site.css{ASSET_Q["css"]}">',
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
<a class="logo" href="{h("home")}" aria-label="Conveasy home">{LOGO_MARK}Conveasy</a>
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
<div style="display:grid;gap:12px;align-content:start"><a class="logo" href="{h("home")}">{LOGO_MARK}Conveasy</a><p>{e(u["foot_tag"])}</p><p>WhatsApp: {e(WA_DISPLAY)}</p></div>
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
# The AI's last message in the chat scene, after the customer tapped the confirm button.
CHAT_DONE = {
    "nl": "Top! Je bestelling staat in de keuken. Levering rond 19:55.",
    "fr": "Parfait ! Votre commande est en cuisine. Livraison vers 19:55.",
    "en": "Great! Your order is in the kitchen. Delivery around 19:55.",
    "tr": "Harika! Siparişin mutfakta. Teslimat 19:55 civarında.",
    "de": "Super! Ihre Bestellung ist in der Küche. Lieferung gegen 19:55.",
}
def chat_i(lang):
    """Animated WhatsApp chat: the customer types and sends an order, the AI answers with the order and two buttons,
    the customer taps the confirm button, the AI confirms. Pure CSS (see .wchat in site.css); without motion every message is shown."""
    n, s, cin, ai, b1, b2 = CHAT[lang]
    dots = '<span class="wc-dots" aria-hidden="true"><i></i><i></i><i></i></span>'
    return f'''<div class="chat wchat" role="img" aria-label="{e(UI[lang]["example"])}: WhatsApp"><div class="wc">
<div class="c-top"><i aria-hidden="true"></i><span>{e(n)}<small>{e(s)}</small></span></div>
<div class="wc-row wc-r1">{dots}<div class="bubble in">{e(cin)}</div></div>
<div class="wc-row wc-r2">{dots}<div class="bubble ai">{e(ai)}</div></div>
<div class="chat-btns"><span class="wc-yes">{e(b1)}<u class="wc-tap"></u></span><span>{e(b2)}</span></div>
<div class="wc-row wc-r3"><div class="bubble in">{e(b1)}</div></div>
<div class="wc-row wc-r4">{dots}<div class="bubble ai">{e(CHAT_DONE[lang])}</div></div>
</div></div>'''

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
# Line icons for the food in the kiosk scene and the webshop scene.
FOOD_ICONS = {
    "burger": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 11a8 6 0 0 1 16 0z"/><path d="M3 14.5h18"/><path d="M5 18h14a1.5 1.5 0 0 1 0 3H5a1.5 1.5 0 0 1 0-3z"/></svg>',
    "fries": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 11l1.5 10h7L17 11z"/><path d="M9 11V4M12 11V3M15 11V5"/></svg>',
    "drink": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 8h10l-1.2 13H8.2z"/><path d="M6 8h12M13 8l1.5-5H17"/></svg>',
    "snack": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5.4 18.6a3 3 0 0 1 0-4.2l9-9a3 3 0 0 1 4.2 4.2l-9 9a3 3 0 0 1-4.2 0z"/><path d="M11.5 9.5l1.5 1.5M9 12l1.5 1.5"/></svg>',
}
def kiosk_i(lang):
    """Animated scene: a figure orders at the kiosk. The screen switches language, adds a burger and fries, pays, and a ticket comes out.
    Pure CSS (see .kscene in site.css); the words on the screen are the same on every page because they show all five languages.
    --ks-i is the place of the page language in those lists: without motion the screen rests on the menu in that language."""
    def roll(words): return '<span class="ks-roll"><span>' + "".join(f"<em>{e(w)}</em>" for w in words) + "</span></span>"
    hello = "".join(f"<em>{e(w)}</em>" for w in ["Welkom", "Bienvenue", "Welcome", "Hoş geldin", "Willkommen"])
    chips = "".join(f"<i>{c}</i>" for c in ["NL", "FR", "EN", "TR", "DE"])
    icons = FOOD_ICONS
    rows = [("burger", ["Burger", "Burger", "Burger", "Burger", "Burger"], "9,00"),
            ("fries", ["Friet", "Frites", "Fries", "Patates", "Pommes"], "4,50"),
            ("drink", ["Drankje", "Boisson", "Drink", "İçecek", "Getränk"], "2,50")]
    items = "".join(f'<div class="ks-item ks-{k}">{icons[k]}<span class="ks-n"><b>{roll(w)}</b><small>€{pr}</small></span><u>+</u></div>' for k, w, pr in rows)
    return f'''<div class="kscene" style="--ks-i: {["nl", "fr", "en", "tr", "de"].index(lang)}" role="img" aria-label="{e(UI[lang]["example"])}: kiosk">
<div class="ks-kiosk"><div class="ks-frame"><div class="ks-screen">
<div class="ks-view ks-lang"><span class="ks-hello"><span>{hello}</span></span><div class="ks-chips">{chips}</div></div>
<div class="ks-view ks-menu"><div class="ks-top">{roll(["Menu", "Carte", "Menu", "Menü", "Speisekarte"])}<span class="ks-cart"><span><em>0</em><em>1</em><em>2</em></span></span></div>{items}<div class="ks-go">{roll(["Bestellen", "Commander", "Order", "Sipariş ver", "Bestellen"])}</div></div>
<div class="ks-view ks-pay"><b>€13,50</b><span class="ks-card"></span><span class="ks-ok"></span></div>
</div></div><div class="ks-slot"><span class="ks-ticket">#47</span></div><div class="ks-stand"></div><div class="ks-base"></div></div>
<svg class="ks-man" viewBox="0 0 100 180" aria-hidden="true"><circle cx="52" cy="22" r="13"/><path d="M52 35v68M52 103l-15 73M52 103l15 73M52 52l15 44"/><g class="ks-arm"><path d="M52 52v46"/><circle cx="52" cy="99" r="3.2"/></g></svg>
<div class="ks-floor"></div></div>'''

MKT = {"nl": ("Deze week", [("Instagram", "Reel: friet in 15 seconden"), ("Facebook", "Advertentie A/B-test"), ("Google", "Openingsuren en menu bijgewerkt"), ("AI-zoeken", "Menu leesbaar voor ChatGPT")]),
       "fr": ("Cette semaine", [("Instagram", "Reel : la frite en 15 secondes"), ("Facebook", "Test A/B de publicité"), ("Google", "Horaires et carte à jour"), ("Recherche IA", "Carte lisible par ChatGPT")]),
       "en": ("This week", [("Instagram", "Reel: fries in 15 seconds"), ("Facebook", "Ad A/B test"), ("Google", "Opening hours and menu updated"), ("AI search", "Menu readable by ChatGPT")])}
def mkt_i(lang):
    t, rows = MKT[lang]
    r = "".join(f'<div class="row"><span class="chip">{e(c)}</span><b>{e(x)}</b><small></small></div>' for c, x in rows)
    return f'''<div class="panel" role="img" aria-label="{e(UI[lang]["example"])}: marketing"><div class="p-title">{e(t)}<span>{e(P["marketing"][lang]["name"])}</span></div>{r}</div>'''

# Marketing scene, per language: word for "orders", name of the e-mail channel, and the message each customer gets
# (WhatsApp announcement, e-mail about an unfinished order, Wallet stamp card). Keep each message under about 30 characters.
MSCENE = {
    "nl": ("Bestellingen", "E-mail", ["Nieuw: Double Smash Burger", "Je mandje staat nog klaar", "Stempel 8\u00a0van\u00a010 gespaard"]),
    "fr": ("Commandes", "E-mail", ["Nouveau\u00a0: Double Smash Burger", "Votre panier vous attend", "Tampon 8\u00a0sur\u00a010 ajouté"]),
    "en": ("Orders", "Email", ["New: Double Smash Burger", "Your basket is still waiting", "Stamp 8\u00a0of\u00a010 collected"]),
    "tr": ("Sipariş", "E-posta", ["Yeni: Double Smash Burger", "Sepetin seni bekliyor", "10\u00a0damgadan 8'i tamam"]),
    "de": ("Bestellungen", "E-Mail", ["Neu: Double Smash Burger", "Ihr Warenkorb wartet noch", "Stempel 8\u00a0von\u00a010 gesammelt"]),
}  # \u00a0 is a no-break space: it keeps "8 van 10" (and the French " :") on one line
def mkt_scene_i(lang):
    """Animated scene for Marketing AI: the restaurant sends, lines run to three customer phones, a message arrives on each
    (WhatsApp, e-mail, Wallet) and orders come back. Pure CSS (see .mscene in site.css).
    The channel icons are plain shapes on purpose (speech bubble, envelope, card), not the logos of those services."""
    orders, mail, texts = MSCENE[lang]
    icons = {
        "wa": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5.5h16A1.5 1.5 0 0 1 21.5 7v9a1.5 1.5 0 0 1-1.5 1.5h-8L7.5 21v-3.5H4A1.5 1.5 0 0 1 2.5 16V7A1.5 1.5 0 0 1 4 5.5z"/></svg>',
        "mail": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="M3 7l9 6.5L21 7"/></svg>',
        "wal": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2.5" y="5.5" width="19" height="13" rx="2.5"/><path d="M2.5 10h19M6.5 14.5h3"/></svg>',
    }
    wires = ["M200 86C200 160 68 150 68 226", "M200 86V226", "M200 86C200 160 332 150 332 226"]
    lines = ("".join(f'<path class="ms-wire" d="{d}"/>' for d in wires)
             + "".join(f'<path class="ms-go ms-g{i}" pathLength="100" d="{d}"/>' for i, d in enumerate(wires, 1))
             + "".join(f'<path class="ms-back ms-b{i}" pathLength="100" d="{d}"/>' for i, d in enumerate(wires, 1)))
    phones = "".join(f'<div class="ms-phone ms-p{i}"><div class="ms-scr"><b>19:48</b></div></div>' for i in (1, 2, 3))
    chans = [("wa", "WhatsApp"), ("mail", mail), ("wal", "Wallet")]
    notes = "".join(f'<div class="ms-note ms-n{i}"><span class="ms-ch ms-{k}">{icons[k]}{e(name)}</span><p>{e(txt)}</p></div>'
                    for i, ((k, name), txt) in enumerate(zip(chans, texts), 1))
    return f'''<div class="mscene" role="img" aria-label="{e(UI[lang]["example"])}: marketing">
<svg class="ms-lines" viewBox="0 0 400 360" preserveAspectRatio="none" aria-hidden="true">{lines}</svg>
<div class="ms-name">Mario's Snackbar<small>{e(P["marketing"][lang]["name"])}</small></div>
<div class="ms-shop"><svg viewBox="0 0 48 48" aria-hidden="true"><path class="ms-awn" d="M10 8h28l5 11a4.75 4.75 0 0 1-9.5 0 4.75 4.75 0 0 1-9.5 0 4.75 4.75 0 0 1-9.5 0 4.75 4.75 0 0 1-9.5 0z"/><path d="M9 27v13h30V27M20 40v-8h8v8"/></svg></div>
<div class="ms-pill"><span>{e(orders)} <span class="ms-count"><span><em>+1</em><em>+2</em><em>+3</em></span></span></span></div>
<div class="ms-phones">{phones}</div>
{notes}
</div>'''

def framed(lang, inner):
    return f'<div>{inner}<p class="mock-label">{e(UI[lang]["example"])}</p></div>'
def ticket(lang, *a): return framed(lang, ticket_i(lang, *a))
def chat(lang): return framed(lang, chat_i(lang))
def dash(lang): return framed(lang, dash_i(lang))
def kiosk(lang): return framed(lang, kiosk_i(lang))
def mkt(lang): return framed(lang, mkt_scene_i(lang))  # the hero of the Marketing AI page; mkt_i (the "this week" list) is no longer shown

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

# Webshop scene, per language. The words of the order page (thanks, eta, left, around, steps, driver, enjoy) are the real
# webshop's own texts (src/lib/i18n/dict in the conveasy-webshop repo); German is not in the webshop yet, so that one is ours.
WSCENE = {
    "nl": {"checkout": "Afrekenen", "modes": ("Afhalen", "Levering"), "addr_label": "Bezorgadres", "addr": "Kerkstraat 12, Zolder",
           "fee": "2,4 km · bezorgkost {fee}", "pay_label": "Betalen met", "cash": "Cash", "total": "Totaal", "place": "Bestelling plaatsen",
           "thanks": ("Bedankt!", "Je bestelling is binnen"), "eta": "Verwachte bezorgtijd", "left": ("Nog ± ", " min"), "around": "Verwacht rond 19:57",
           "steps": ["Ontvangen", "In de keuken", "Onderweg", "Bezorgd"], "driver": "Onderweg met Ali", "enjoy": "Smakelijk!",
           "sub": "Subtotaal", "ship": "Bezorgkost", "delivered": "Afgeleverd om 19:55."},
    "fr": {"checkout": "Paiement", "modes": ("À emporter", "Livraison"), "addr_label": "Adresse de livraison", "addr": "Rue de l'Église 12, Namur",
           "fee": "2,4 km · livraison {fee}", "pay_label": "Payer avec", "cash": "Espèces", "total": "Total", "place": "Passer la commande",
           "thanks": ("Merci !", "Votre commande a bien été reçue"), "eta": "Heure de livraison prévue", "left": ("Encore ± ", " min"), "around": "Prévu vers 19:57",
           "steps": ["Reçu", "En cuisine", "En route", "Livrée"], "driver": "En route avec Ali", "enjoy": "Bon appétit !",
           "sub": "Sous-total", "ship": "Frais de livraison", "delivered": "Livré à 19:55."},
    "en": {"checkout": "Checkout", "modes": ("Pickup", "Delivery"), "addr_label": "Delivery address", "addr": "Kerkstraat 12, Zolder",
           "fee": "2.4 km · delivery {fee}", "pay_label": "Pay with", "cash": "Cash", "total": "Total", "place": "Place order",
           "thanks": ("Thank you!", "Your order is in"), "eta": "Expected delivery time", "left": ("About ", " min to go"), "around": "Expected around 19:57",
           "steps": ["Received", "In the kitchen", "On the way", "Delivered"], "driver": "On the way with Ali", "enjoy": "Enjoy your meal!",
           "sub": "Subtotal", "ship": "Delivery cost", "delivered": "Delivered at 19:55."},
    "tr": {"checkout": "Ödeme", "modes": ("Gel al", "Paket servis"), "addr_label": "Teslimat adresi", "addr": "Kerkstraat 12, Zolder",
           "fee": "2,4 km · teslimat {fee}", "pay_label": "Ödeme yöntemi", "cash": "Nakit", "total": "Toplam", "place": "Siparişi ver",
           "thanks": ("Teşekkürler!", "Siparişin alındı"), "eta": "Tahmini teslimat saati", "left": ("Yaklaşık ", " dk kaldı"), "around": "Tahminen 19:57 civarında",
           "steps": ["Alınan", "Mutfakta", "Yolda", "Teslim edildi"], "driver": "Ali ile yolda", "enjoy": "Afiyet olsun!",
           "sub": "Ara toplam", "ship": "Teslimat ücreti", "delivered": "19:55 saatinde teslim edildi."},
    "de": {"checkout": "Kasse", "modes": ("Abholung", "Lieferung"), "addr_label": "Lieferadresse", "addr": "Kerkstraat 12, Zolder",
           "fee": "2,4 km · Lieferung {fee}", "pay_label": "Bezahlen mit", "cash": "Bar", "total": "Gesamt", "place": "Bestellung aufgeben",
           "thanks": ("Danke!", "Ihre Bestellung ist eingegangen"), "eta": "Voraussichtliche Lieferzeit", "left": ("Noch ± ", " Min."), "around": "Voraussichtlich gegen 19:57",
           "steps": ["Eingegangen", "In der Küche", "Unterwegs", "Geliefert"], "driver": "Unterwegs mit Ali", "enjoy": "Guten Appetit!",
           "sub": "Zwischensumme", "ship": "Liefergebühr", "delivered": "Um 19:55 geliefert."},
}
WS_DELIVERY_CENTS = 250          # the delivery cost in the scene
WS_MINUTES = ["25", "17", "10"]  # the countdown: received, in the kitchen, on the way

def _cents(price):
    m = re.search(r"(\d+)[.,](\d\d)", price)
    return int(m.group(1)) * 100 + int(m.group(2))
def _price_like(cents, like):
    """An amount in the style of an existing price text: "€4,20", "4,20 €" or "€4.20"."""
    m = re.match(r"^(\D*)\d+([.,])\d\d(\D*)$", like)
    return f"{m.group(1)}{cents // 100}{m.group(2)}{cents % 100:02d}{m.group(3)}"

def web_i(lang):
    """Animated phone for the webshop: the customer adds three products, fills in the address (the delivery cost appears),
    picks a way to pay and places the order; then the order page: thank you, the minutes counting down, the steps up to delivered.
    Pure CSS (see .wscene in site.css). Menu texts come from OVX[lang]["web"], the rest from WSCENE; totals are worked out here."""
    shop, tag, cats, items, btn = OVX[lang]["web"]
    w = WSCENE[lang]
    money = lambda c: _price_like(c, items[0][1])
    sums = [0]
    for _, pr in items: sums.append(sums[-1] + _cents(pr))
    roll = lambda words, cls: f'<span class="ws-roll {cls}"><span>' + "".join(f"<em>{e(x)}</em>" for x in words) + "</span></span>"
    tap = '<u class="ws-tap"></u>'
    check = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
    bike = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="18.5" cy="17.5" r="3.5"/><circle cx="5.5" cy="17.5" r="3.5"/><circle cx="15" cy="5" r="1"/><path d="M12 17.5V14l-3-3 4-3 2 3h2"/></svg>'
    c = "".join(f'<span{" class=on" if i == 0 else ""}>{e(x)}</span>' for i, x in enumerate(cats))
    it = "".join(f'<div class="ws-item ws-i{i}"><i>{FOOD_ICONS[ic]}</i><b>{e(n)}<small>{e(pr)}</small></b><span class="ws-add"><em>+</em>{check}{tap}</span></div>'
                 for i, ((n, pr), ic) in enumerate(zip(items, ["fries", "burger", "snack"]), 1))
    menu = (f'<div class="ws-view ws-menu"><div class="ws-head"><b>{e(shop)}</b><small>{e(tag)}</small></div><div class="ws-cats">{c}</div>{it}'
            f'<div class="ws-btn ws-order">{e(btn.split(" · ")[0])} · {roll([money(x) for x in sums], "ws-tot")}{tap}</div></div>')
    typed = "".join(f'<i style="--i:{k}">{e(ch)}</i>' for k, ch in enumerate(w["addr"]))
    chips = f'<span class="ws-chip ws-sel">Bancontact{tap}</span><span class="ws-chip">Klarna</span><span class="ws-chip">{e(w["cash"])}</span>'
    checkout = (f'<div class="ws-view ws-check"><b class="ws-title">{e(w["checkout"])}</b>'
                f'<div class="ws-seg"><span>{e(w["modes"][0])}</span><span class="on">{e(w["modes"][1])}</span></div>'
                f'<div class="ws-lab">{e(w["addr_label"])}</div><div class="ws-field"><span class="ws-type">{typed}</span></div>'
                f'<div class="ws-fee">{check}{e(w["fee"].format(fee=money(WS_DELIVERY_CENTS)))}</div>'
                f'<div class="ws-lab">{e(w["pay_label"])}</div><div class="ws-chips">{chips}</div>'
                f'<div class="ws-sums"><div><span>{e(w["sub"])}</span><span>{money(sums[-1])}</span></div>'
                f'<div><span>{e(w["ship"])}</span><span>{roll(["–", money(WS_DELIVERY_CENTS)], "ws-tot2")}</span></div>'
                f'<div class="ws-sum"><span>{e(w["total"])}</span><b>{roll([money(sums[-1]), money(sums[-1] + WS_DELIVERY_CENTS)], "ws-tot2")}</b></div></div>'
                f'<div class="ws-btn ws-place">{e(w["place"])}{tap}</div></div>')
    steps = "".join(f'<li class="ws-s{i}"><i></i>{e(x)}</li>' for i, x in enumerate(w["steps"], 1))
    route = "M12 21C24 21 22 8 36 8S52 20 64 20 76 9 88 8"   # from the restaurant (left) to the customer (right)
    route_map = ('<div class="ws-map"><svg viewBox="0 0 100 28" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
                 '<path class="ws-road" d="M-2 14H102M26-2V30M58-2V30M84-2V30M-2 3H102M-2 25H102"/>'
                 f'<path class="ws-route" d="{route}"/><path class="ws-ride" pathLength="100" d="{route}"/>'
                 '<circle class="ws-from" cx="12" cy="21" r="2.4"/><circle class="ws-to" cx="88" cy="8" r="2.4"/></svg></div>')
    done = (f'<div class="ws-view ws-done"><span class="ws-okc">{check}</span>'
            f'<div class="ws-thx"><b>{e(w["thanks"][0])}</b><small>{e(w["thanks"][1])}</small></div>'
            f'<div class="ws-eta"><small>{e(w["eta"])}</small><div class="ws-big"><b class="ws-count">{e(w["left"][0])}{roll(WS_MINUTES, "ws-min")}{e(w["left"][1])}</b>'
            f'<b class="ws-enjoy">{e(w["enjoy"])}</b></div><div class="ws-subs"><span class="ws-count">{e(w["around"])}</span><span class="ws-enjoy">{e(w["delivered"])}</span></div>'
            f'<span class="ws-drv">{bike}{e(w["driver"])}</span></div>'
            f'<ol class="ws-steps">{steps}</ol>{route_map}</div>')
    return f'<div class="phone wscene" role="img" aria-label="{e(UI[lang]["example"])}: webshop"><div class="ph-screen ws">{menu}{checkout}{done}</div></div>'

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

def types_i(lang):
    """For the "all restaurants" page: the kinds of restaurants Conveasy works for, as chips, with "your restaurant" last.
    The chips pop in one after the other (see .types in site.css)."""
    title, sub, kinds, yours = sectors_more.TYPES[lang]
    chips = "".join(f'<span style="--i:{i}">{e(k)}</span>' for i, k in enumerate(kinds))
    chips += f'<span class="ty-you" style="--i:{len(kinds)}">+ {e(yours)}</span>'
    return (f'<div class="panel types" role="img" aria-label="{e(UI[lang]["example"])}: {e(title)}">'
            f'<div class="p-title">{e(title)}<span>{e(sub)}</span></div><div class="ty-chips">{chips}</div></div>')

def mock_for(lang, pid):
    meta = TICKET_META[lang]
    if pid == "phone": return framed(lang, phone_scene_i(lang))
    if pid == "whatsapp": return chat(lang)
    if pid == "webshop": return framed(lang, web_i(lang))
    if pid == "kiosk": return kiosk(lang)
    if pid == "marketing": return mkt(lang)
    if pid == "alle": return framed(lang, types_i(lang))
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
# Phone AI scene, per language: what the caller says, what the AI answers, and the words of the call, the dashboard and the
# printer. Sammy, 11 Nov 2026 (evening): no stick figures; the counter with the ringing phone, the AI taking the order, then the
# laptop with the notification and the dashboard, and the printer printing the ticket. The rest comes from CALL, DASH,
# TICKET_META, WSCENE and P.
PCALL = {
    "nl": {"said": "Hallo, 2 grote friet en een bicky burger om af te halen.",
           "answer": "Genoteerd: 2 grote friet en 1 bicky burger. Klaar over 15 minuten.",
           "ok": "Bestelling bevestigd", "new": "Nieuwe bestelling",
           "items": ("2x Grote friet", "1x Bicky burger"), "checks": ("In het dashboard", "Ticket geprint")},
    "fr": {"said": "Bonjour, 2 grandes frites et un bicky burger à emporter.",
           "answer": "C'est noté : 2 grandes frites et 1 bicky burger. Ce sera prêt dans 15 minutes.",
           "ok": "Commande confirmée", "new": "Nouvelle commande",
           "items": ("2x Grande frite", "1x Bicky burger"), "checks": ("Dans le tableau de bord", "Ticket imprimé")},
    "en": {"said": "Hi, 2 large fries and a bicky burger for pickup.",
           "answer": "Got it: 2 large fries and 1 bicky burger. Ready in 15 minutes.",
           "ok": "Order confirmed", "new": "New order",
           "items": ("2x Large fries", "1x Bicky burger"), "checks": ("On the dashboard", "Ticket printed")},
    "tr": {"said": "Merhaba, 2 büyük patates ve bir bicky burger, gel al.",
           "answer": "Not aldım: 2 büyük patates ve 1 bicky burger. 15 dakikada hazır.",
           "ok": "Sipariş onaylandı", "new": "Yeni sipariş",
           "items": ("2x Büyük patates", "1x Bicky burger"), "checks": ("Panelde", "Fiş yazdırıldı")},
    "de": {"said": "Hallo, 2 große Pommes und einen Bicky Burger zum Abholen.",
           "answer": "Notiert: 2 große Pommes und 1 Bicky Burger. In 15 Minuten fertig.",
           "ok": "Bestellung bestätigt", "new": "Neue Bestellung",
           "items": ("2x Große Pommes", "1x Bicky Burger"), "checks": ("Im Dashboard", "Bon gedruckt")},
}
PS_TIMER = ["00:02", "00:05", "00:09", "00:14", "00:18"]   # the call's clock while the AI takes the order

def phone_scene_i(lang):
    """Animated scene for the phone AI, in three parts (pure CSS, see .pscene in site.css; one 17 s loop):
    1) the restaurant counter: the desk phone rings, the handset clicks up and the view zooms into the call;
    2) the call: the AI's voice orb, what the caller says, the AI's answer, "order confirmed";
    3) the result: a notification and the new order on the dashboard (a laptop), the ticket comes out of the printer.
    The pill on top names the stage (incoming call, AI answering, in the kitchen). Without motion it rests on part 2.
    The counter is one SVG on a 400 x 360 grid with the phone at x = 200; the other parts are HTML sized in cqi."""
    t = PCALL[lang]
    ring, picked = CALL[lang]
    chans = [r[0] for r in DASH[lang][2]]            # short channel names: phone, WhatsApp, webshop, kiosk
    check = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
    bell = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 16.5V11a6 6 0 0 1 12 0v5.5l1.5 2h-15z"/><path d="M10 21a2 2 0 0 0 4 0"/></svg>'
    hs = ('<rect x="162" y="165" width="76" height="10" rx="5"/>'
          '<rect x="148" y="158" width="26" height="24" rx="8"/><rect x="226" y="158" width="26" height="24" rx="8"/>')
    keys = "".join(f'<circle cx="{x}" cy="{y}" r="2.4"/>' for y in (200, 207.5, 215) for x in (188, 200, 212))
    counter = f'''<svg class="ps-art" viewBox="0 0 400 360" aria-hidden="true">
<path d="M46 80H74L104 222H16zM326 80H354L384 222H296z" fill="#FFB45C" opacity=".07"/>
<path d="M60 0V64M340 0V64" stroke="#2E2E36" stroke-width="2"/>
<path d="M42 78a18 15 0 0 1 36 0zM322 78a18 15 0 0 1 36 0z" fill="#2A2A32" stroke="#45454F" stroke-width="1.5"/>
<circle cx="60" cy="80" r="4" fill="#FFD9A8"/><circle cx="340" cy="80" r="4" fill="#FFD9A8"/>
<rect x="128" y="64" width="144" height="80" rx="7" fill="#121216" stroke="#2C2C35" stroke-width="1.5"/>
<path d="M144 82H190" stroke="#FF7A1A" stroke-width="5" stroke-linecap="round"/>
<path d="M144 100H210M144 114H200M144 128H216" stroke="#4E4E58" stroke-width="3.2" stroke-linecap="round"/>
<path d="M240 100H256M240 114H256M240 128H256" stroke="#85858F" stroke-width="3.2" stroke-linecap="round"/>
<rect x="26" y="232" width="348" height="128" fill="#111115" stroke="#24242C" stroke-width="1.5"/>
<path d="M142 236V360M258 236V360" stroke="#1C1C23" stroke-width="2"/>
<path d="M26 248H374" stroke="#FF7A1A" stroke-width="2.4" opacity=".55"/>
<rect x="16" y="222" width="368" height="11" rx="4" fill="#2A2A33"/>
<rect x="68" y="216" width="46" height="6" rx="2" fill="#2E2E37"/>
<path d="M73 216a18 17 0 0 1 36 0z" fill="#2A2A32" stroke="#4A4A55" stroke-width="1.5"/>
<rect x="88" y="194" width="6" height="5" rx="1.5" fill="#4A4A55"/>
<path d="M80 210a11 10 0 0 1 7-7.5" stroke="#fff" stroke-opacity=".22" stroke-width="2" stroke-linecap="round"/>
<path d="M294 186l-3-16M301 184l-1-18M308 184l1-17M315 186l3-15" stroke="#FFC845" stroke-width="4.5" stroke-linecap="round"/>
<path d="M288 184H322L316 222H294z" fill="#E8620A"/><path d="M291 196H319" stroke="#FFFDF6" stroke-opacity=".55" stroke-width="2"/>
<path d="M346 188v-6a8 8 0 0 1 16 0v6" stroke="#4A4A55" stroke-width="2"/>
<rect x="336" y="188" width="36" height="34" rx="2.5" fill="#1F1F26" stroke="#3A3A44" stroke-width="1.5"/><circle cx="354" cy="205" r="5.5" fill="#FF7A1A"/>
<path d="M154 222L165 186Q167 179 174 179H226Q233 179 235 186L246 222z" fill="#1A1A20" stroke="#3E3E48" stroke-width="2" stroke-linejoin="round"/>
<rect x="184" y="186" width="32" height="7" rx="2" fill="#2A2A33"/><g fill="#3A3A44">{keys}</g>
<g class="ps-hs ps-hs-s" fill="#26262E" stroke="#4A4A55" stroke-width="2">{hs}</g>
<g class="ps-ringing"><rect x="184" y="186" width="32" height="7" rx="2" fill="#FF7A1A"/>
<g class="ps-hs ps-hs-r" fill="#26262E" stroke="#4A4A55" stroke-width="2">{hs}</g>
<g stroke="#FF7A1A" stroke-width="3.5" stroke-linecap="round"><path class="ps-arc" d="M139 156Q131 170 139 184M261 156Q269 170 261 184"/><path class="ps-arc ps-arc2" d="M128 150Q117 170 128 190M272 150Q283 170 272 190"/></g></g>
<circle class="ps-ripple" cx="200" cy="168" r="40" stroke="#FFB45C" stroke-width="2.5"/>
<path class="ps-burst" d="M200 106V92M220.7 111.2L227.2 98.8M179.3 111.2L172.8 98.8M236 124.8L247.5 116.7M164 124.8L152.5 116.7" stroke="#FFB45C" stroke-width="3.5" stroke-linecap="round"/>
</svg>'''
    timer = '<span class="ps-time"><span>' + "".join(f"<em>{x}</em>" for x in PS_TIMER) + "</span></span>"
    call = (f'<div class="ps-act ps-a2"><div class="ps-orb"><span class="ps-wv">{"<i></i>" * 7}</span></div>'
            f'<p class="ps-who">+32 470 •• •• 18 · {timer}</p>'
            f'<p class="ps-say ps-s1">{e(t["said"])}</p><p class="ps-say ps-s2">{e(t["answer"])}</p>'
            f'<p class="ps-ok">{check}{e(t["ok"])}</p></div>')
    rows = [("#1043", chans[0], "19:55", ", ".join(t["items"]), " ps-new"),
            ("#1042", chans[1], "19:48", "1x Pizza margherita, 1x Cola", ""),
            ("#1041", chans[3], "19:44", "2x Cheeseburger, 2x Cola", "")]
    rws = "".join(f'<div class="ps-row{cls}"><div><b>{n}</b><span>{e(ch)}</span><small>{tm}</small></div><p>{e(it)}</p></div>'
                  for n, ch, tm, it, cls in rows)
    tk = "".join(f"<span>{e(x)}</span>" for x in t["items"])
    result = (f'<div class="ps-act ps-a3">'
              f'<div class="ps-scr"><div class="ps-bar"><b>{e(DASH[lang][0])}</b><span>19:41</span></div>'
              f'<div class="ps-list"><div class="ps-rows">{rws}</div></div>'
              f'<div class="ps-toast"><i>{bell}</i><span><b>{e(t["new"])}</b><small>#1043 · {e(P["phone"][lang]["name"])}</small></span></div></div>'
              f'<div class="ps-base"></div><div class="ps-box"><i class="ps-led"></i></div>'
              f'<div class="ps-paper"><div class="ps-tk"><b><span>CONVEASY</span><span>#1043</span></b><small>{e(TICKET_META[lang][0])}</small>{tk}'
              f'<small class="ps-tf">{e(WSCENE[lang]["modes"][0])} · 19:55</small></div></div>'
              f'<div class="ps-checks"><span class="ps-c1">{check}{e(t["checks"][0])}</span><span class="ps-c2">{check}{e(t["checks"][1])}</span></div></div>')
    wave = '<span class="wave"><i></i><i></i><i></i><i></i><i></i></span>'
    pill = (f'<div class="ps-pill"><span class="ps-p ps-p1"><i class="ps-dot"></i>{e(ring)}</span>'
            f'<span class="ps-p ps-p2"><i class="ps-dot ps-ai"></i>{e(picked)}{wave}</span>'
            f'<span class="ps-p ps-p3"><i class="ps-dot ps-go"></i>{e(WSCENE[lang]["steps"][1])}</span></div>')
    return (f'<div class="pscene" role="img" aria-label="{e(UI[lang]["example"])}: {e(P["phone"][lang]["name"])}">'
            f'<div class="ps-act ps-a1">{counter}</div>{call}{result}{pill}</div>')

def home_stage(lang, prefix):
    """Top visual of the home page: the three ways customers order, each as a small animation with a link to its page
    (phone AI, WhatsApp AI, webshop), and the kitchen ticket as a small accent. On phones the three become a row to swipe."""
    def tile(cls, inner, pid):
        return (f'<figure class="hs-item {cls}">{inner}<figcaption><a href="{prefix + path_of(lang, pid)}">{e(P[pid][lang]["name"])}'
                f' <span aria-hidden="true">→</span></a></figcaption></figure>')
    row = tile("hs-phone", phone_scene_i(lang), "phone") + tile("hs-chat", chat_i(lang), "whatsapp") + tile("hs-web", web_i(lang), "webshop")
    return (f'<div class="stage-home"><div class="hs-row">{row}</div>'
            f'<div class="layer l-ticket" aria-hidden="true">{ticket_i(lang, HOME_TICKET[lang]["ticket"], *TICKET_META[lang])}</div></div>'
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

# The voice demo greets in the language of the page: sent to Vapi as the first message when the call starts.
VOICE_FIRST = {
    "nl": "Hallo, met Sara van Mario's Snackbar.",
    "fr": "Bonjour, ici Sara de Mario's Snackbar.",
    "en": "Hello, this is Sara from Mario's Snackbar.",
    "tr": "Merhaba, Mario's Snackbar'dan Sara.",
    "de": "Hallo, hier ist Sara von Mario's Snackbar.",
}

def demo_band(lang):
    eb, h2, txt, start, stop, wait, live, ended, err, notset, note = DEMO[lang]
    return (f'<section class="band demo-band" id="demo"><div class="wrap"><div class="demo">'
            f'<div class="demo-copy"><span class="eyebrow">{e(eb)}</span><h2>{e(h2)}</h2><p>{e(txt)}</p><p class="demo-note">{e(note)}</p></div>'
            f'<div class="demo-ctl"><div class="demo-orb" aria-hidden="true"><i></i><i></i><i></i></div>'
            f'<button type="button" class="btn btn-primary demo-btn" data-vapi="{VAPI_ASSISTANT_ID}" data-first="{e(VOICE_FIRST[lang])}" data-state="idle" '
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
    sec_text = f'<p>{e(d["sectors_text"])}</p>' if d.get("sectors_text") else ""
    sec_cards = "".join(f'<a class="card" href="{prefix + path_of(lang, s)}"><h3>{e(S[s][lang]["name"])}</h3><p>{e(S[s][lang].get("card", S[s][lang]["pains"][0][1]))}</p><span class="more">{e(u["more"])} →</span></a>' for s in SECTORS)
    dash_feats = "".join(f'<div class="feature"><h3>{e(t)}</h3><p>{e(x)}</p></div>' for t, x in d["dash_feats"])
    body = hero(lang, prefix, d["h1"], d["lead"] + " " + d["made_by"], home_stage(lang, prefix), pg, badge=d["badge"], facts=d["facts"])
    body = body.replace('<section class="hero">', '<section class="hero hero-home">', 1)
    body += demo_band(lang) + wa_demo_band(lang) + marquee(lang) + flow_band(lang)
    body += f'''<section class="band" id="producten"><div class="wrap"><div class="section-head"><span class="eyebrow">{e(d["products_eyebrow"])}</span><h2>{e(d["products_title"])}</h2><p>{e(d["products_text"])}</p></div>
<div class="bento">{product_cards(lang, prefix)}<a class="card" href="{prefix + path_of(lang, "marketing")}"><h3>{e(P["webshop"][lang]["extra_title"])}</h3><p>{e(P["webshop"][lang]["extra_text"])}</p><span class="more">{e(u["more"])} →</span></a><a class="card" href="{prefix + path_of(lang, "phone")}#reservaties"><span class="tag">24/7</span><h3>{e(OVX[lang]["resv"]["card"][0])}</h3><p>{e(OVX[lang]["resv"]["card"][1])}</p><span class="more">{e(u["more"])} →</span></a></div></div></section>
<section class="band dark"><div class="wrap" style="display:grid;gap:40px;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));align-items:center">
<div style="display:grid;gap:24px;min-width:0"><div class="section-head" style="margin:0"><span class="eyebrow">{e(d["dash_eyebrow"])}</span><h2>{e(d["dash_title"])}</h2><p>{e(d["dash_text"])}</p></div><div class="grid">{dash_feats}</div></div>{dash(lang)}</div></section>
{shots_band(lang, prefix, ["kds", "resv", "web", "kiosk"])}
<section class="band"><div class="wrap"><div class="section-head"><span class="eyebrow">{e(d["sectors_eyebrow"])}</span><h2>{e(d["sectors_title"])}</h2>{sec_text}</div><div class="grid">{sec_cards}</div></div></section>
{how_band(lang)}
<section class="band"><div class="wrap grid-3" style="align-items:start">
<div class="section-head" style="margin:0;grid-column:span 2;max-width:none"><span class="eyebrow">{e(d["story_eyebrow"])}</span><h2>{e(d["story_title"])}</h2><p class="lead">{e(d["story_text"])}</p><p><a href="{prefix + path_of(lang, "about")}">{e(d["story_link"])} →</a></p></div>
<div class="card"><span class="eyebrow" style="margin:0">{e(d["price_eyebrow"])}</span><h3>{e(d["price_title"])}</h3><p>{e(d["price_text"])}</p><a class="more" href="{prefix + path_of(lang, "pricing")}">{e(u["see_prices"])} →</a></div>
</div></section>'''
    body += faq_band(lang, d["faq"], pg) + cta_band(lang, prefix)
    return body, d["faq"], []

# Online payment methods, shown on the webshop and QR page
PAY = {
    "nl": ("Online betalen", "Alle betaalmethodes op je webshop en bij QR-bestellen", "Je klanten betalen zoals zij dat willen.", "Maaltijdcheques"),
    "fr": ("Paiement en ligne", "Tous les moyens de paiement sur votre boutique et en commande par QR", "Vos clients paient comme ils le souhaitent.", "Titres-repas"),
    "en": ("Online payment", "Every payment method on your webshop and QR ordering", "Your customers pay the way they want.", "Meal vouchers"),
    "tr": ("Online ödeme", "Online siparişte ve QR siparişte tüm ödeme yöntemleri", "Müşterilerin istediği gibi öder.", "Yemek çekleri"),
    "de": ("Online bezahlen", "Alle Zahlungsarten im Webshop und bei der QR-Bestellung", "Ihre Kunden zahlen so, wie sie möchten.", "Essensgutscheine"),
}
def pay_band(lang):
    eb, title, text, vouchers = PAY[lang]
    names = ["Bancontact", "iDEAL", "Klarna", "Riverty", "PayPal", vouchers, "Visa", "Mastercard", "Apple Pay", "Google Pay"]
    lis = "".join(f"<li>{e(n)}</li>" for n in names)
    return f'<section class="band" id="betalen"><div class="wrap"><div class="section-head"><span class="eyebrow">{e(eb)}</span><h2>{e(title)}</h2><p>{e(text)}</p></div><ul class="pay-list">{lis}</ul></div></section>'

def more_band(lang, pid):
    """The list under the feature tiles: more that the real systems do (texts in extras.py)."""
    label, title, rows = extras.MORE[pid][lang]
    lis = "".join(f"<li><b>{e(t)}</b><span>{e(x)}</span></li>" for t, x in rows)
    return f'<section class="band"><div class="wrap"><div class="section-head"><span class="eyebrow">{e(label)}</span><h2>{e(title)}</h2></div><ul class="also">{lis}</ul></div></section>'

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
    if pid in extras.MORE:
        body += more_band(lang, pid)
    if pid == "webshop":
        body += pay_band(lang)
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
    body = f'''<section class="hero"><div class="wrap" style="grid-template-columns:minmax(0,1fr)"><div class="hero-copy">{crumbs_html(lang, prefix, trail)}<h1>{e(d["h1"])}</h1><p class="lead">{e(d["lead"])}</p><p class="other-note">{e(sectors_more.OTHER[lang])}</p></div></div></section>
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
    inner = f'{bar}{header(lang, pid, prefix)}<main>{body}</main>{footer(lang, prefix, f"{lang}/{pid}")}<script src="{prefix}assets/site.js{ASSET_Q["js"]}"></script>'
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
         "- Phone AI: €249/month (500 minutes), €449/month (1,000 minutes), €799/month (2,000 minutes). Handles 50+ calls at the same time.",
         "- Phone AI also: recognises returning callers (name, address, last order), checks the delivery address against the street list and delivery zones, transfers to staff when the caller asks, takes add-ons in the same call, answers outside opening hours to say when the restaurant opens again, and sends callers who hung up without ordering a WhatsApp message to order after all.",
         "- WhatsApp AI: €99/month, on the restaurant's own WhatsApp number. Payment link for deliveries (Klarna and meal vouchers included, an unpaid link expires after 20 minutes); delivery cost, minimum order and free delivery worked out per address; table reservations can be booked, changed and cancelled in the chat; prepaid cards accepted.",
         "- Webshop + QR ordering: €79/month, 0% commission on orders. Live order tracking with a countdown and a map, one-tap reorder, promotions (2-for-1, discount codes, free delivery, menu deals), five designs, the 14 allergens per product, an app for the restaurant's own drivers, analytics and Z-reports.",
         "- Self-order kiosk: €89/month; 21.5-inch table-stand kiosk hardware €1,599 one-time (payable in 3 instalments), other models on request.",
         "- One-time setup fee: €299 for phone AI, €199 for each other channel, €399 for phone AI + WhatsApp AI + webshop + kiosk together.",
         "- Works separately from the restaurant's till (POS); each channel can be bought on its own.",
         "- Works for every kind of restaurant: it uses the restaurant's own menu. Pages for frituren (Belgian fry shops), sushi restaurants, pizzerias, burger restaurants, kebab shops and all other restaurants.",
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
    for icon in ("favicon.svg", "apple-touch-icon.png"):   # the logo mark as browser and home-screen icon
        shutil.copy(os.path.join(HERE, icon), os.path.join(outdir, "assets", icon))
    # Only for the real site: the claude.ai preview serves its files by plain path and always gets them fresh.
    ASSET_Q.update(css="" if preview else "?v=" + asset_fingerprint("site.css"), js="" if preview else "?v=" + asset_fingerprint("site.js"))
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
        for pid, slug in D["SLUGS"].items():
            if pid in SLUGS: SLUGS[pid][l] = slug
        UI[l] = D["UI"]; PRICING[l] = D["PRICING"]; HOME[l] = D["HOME"]; ABOUT[l] = D["ABOUT"]; CONTACT[l] = D["CONTACT"]; LEGAL[l] = D["LEGAL"]
        for pp in PRODUCTS: P[pp][l] = D["P"][pp]
        for ss in SECTORS:
            if ss in S and ss in D["S"]: S[ss][l] = D["S"][ss]   # sushi, kebab and alle come from sectors_more.py
        for name in ("TICKET_META", "CHAT", "DASH", "KIOSK", "MKT"): globals()[name][l] = D[name]

if __name__ == "__main__":
    load_extra_langs()
    apply_overrides(globals())
    answers.apply(globals())
    sectors_more.apply(globals())
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
