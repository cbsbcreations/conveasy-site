#!/usr/bin/env python3
"""Link preview images (og:image, 1200x630) for both Conveasy sites, one per language, into src/og/og-<lang>.jpg.
The build copies them to assets/og/ and every page points to the image of its language.
Run again after changing the home page headline, the facts or the ticket: python3 tools/og_images.py
Needs Playwright for Python and Google Chrome (or Chromium). The fonts are in tools/fonts (Figtree, SIL Open Font License)."""
import asyncio, html, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
os.environ["CONVEASY_TARGET"] = "ai"
sys.path.insert(0, os.path.join(ROOT, "src"))
import importlib.util
spec = importlib.util.spec_from_file_location("site_build", os.path.join(ROOT, "src", "build.py"))
b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
b.load_extra_langs(); b.apply_overrides(vars(b)); b.answers.apply(vars(b)); b.sectors_more.apply(vars(b))
b.lang_es_pt_it.apply(vars(b), (b.extras, b.sectors_more))
b.ai_wording()

FONT_DIR = os.path.join(HERE, "fonts")
def faces():
    out = []
    for w in (500, 700, 800):
        out.append(f"@font-face{{font-family:F;font-weight:{w};src:url('file://{FONT_DIR}/figtree-latin-ext-{w}-normal.woff2') format('woff2');"
                   "unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}")
        out.append(f"@font-face{{font-family:F;font-weight:{w};src:url('file://{FONT_DIR}/figtree-latin-{w}-normal.woff2') format('woff2');"
                   "unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}")
    return "".join(out)

def page(lang):
    e = lambda s: html.escape(s, quote=True)
    h1 = e(b.HOME[lang]["h1"]).replace("&lt;em&gt;", "<em>").replace("&lt;/em&gt;", "</em>")
    facts = [x for x in b.HOME[lang].get("facts", [])][:3]
    chips = "".join(f"<span>{e(x)}</span>" for x in facts)
    chans = " · ".join(e(b.P[p][lang]["name"]) for p in ("phone", "whatsapp", "webshop", "kiosk"))
    items = b.S["frituur"][lang]["ticket"]
    lis = "".join(f'<li class="sub">{e(t)}</li>' if not q else f"<li><b>{e(q)}</b>{e(t)}</li>" for q, t in items)
    via, when = b.TICKET_META[lang]
    return f"""<!doctype html><html lang="{b.HTML_LANG[lang]}"><head><meta charset="utf-8"><style>{faces()}
*{{box-sizing:border-box;margin:0}}
body{{width:1200px;height:630px;background:#000;color:#F5F5F7;font-family:F,system-ui,sans-serif;overflow:hidden;position:relative}}
.glow{{position:absolute;right:-180px;bottom:-260px;width:900px;height:900px;border-radius:50%;background:radial-gradient(closest-side,rgb(255 122 26/.42),rgb(255 122 26/.12) 55%,transparent 75%)}}
.ring{{position:absolute;right:120px;top:40px;width:520px;height:520px;border-radius:50%;border:2px solid rgb(255 180 92/.18)}}
.wrap{{position:absolute;inset:64px 72px;display:grid;grid-template-rows:auto 1fr auto;gap:24px;width:700px}}
.logo{{display:flex;align-items:center;gap:14px;font-weight:700;font-size:40px;letter-spacing:-.03em}}
.logo svg{{width:46px;height:46px;fill:#fff}}
h1{{align-self:center;font-weight:800;font-size:70px;line-height:1.02;letter-spacing:-.035em;text-wrap:balance}}
h1 em{{font-style:normal;color:#FFB45C}}
.chips{{display:flex;flex-wrap:wrap;gap:10px}}
.chips span{{border:1px solid rgb(255 255 255/.18);background:#0B0B0D;border-radius:999px;padding:9px 16px;font-weight:500;font-size:22px}}
.chans{{font-weight:500;font-size:22px;color:#A3A3AD;margin-top:14px}}
.ticket{{position:absolute;right:70px;top:110px;width:330px;background:#FFFDF6;color:#1E1D19;border-radius:6px;padding:22px 24px 18px;transform:rotate(4deg);
  box-shadow:0 30px 80px rgb(0 0 0/.6),0 0 0 1px rgb(0 0 0/.2);font-family:F,monospace}}
.ticket::after{{content:"";position:absolute;left:0;right:0;bottom:-10px;height:12px;background:linear-gradient(-45deg,transparent 6px,#FFFDF6 0) 0 0/12px 12px repeat-x,linear-gradient(45deg,transparent 6px,#FFFDF6 0) 0 0/12px 12px repeat-x}}
.t-head{{display:flex;justify-content:space-between;font-weight:800;font-size:22px;letter-spacing:.06em;border-bottom:2px dashed #D9D3C0;padding-bottom:12px}}
.t-meta{{display:grid;gap:2px;font-size:16px;color:#5b5a52;padding:12px 0;border-bottom:2px dashed #D9D3C0}}
ul{{list-style:none;padding:12px 0 6px;display:grid;gap:8px;font-size:20px;font-weight:700}}
li b{{display:inline-block;min-width:44px;color:#E8620A}}
li.sub{{font-weight:500;font-size:17px;color:#5b5a52;padding-left:44px;margin-top:-4px}}
</style></head><body><div class="glow"></div><div class="ring"></div>
<div class="wrap"><div class="logo">{b.LOGO_MARK}Conveasy</div><h1>{h1}</h1><div><div class="chips">{chips}</div><div class="chans">{chans}</div></div></div>
<div class="ticket"><div class="t-head"><span>CONVEASY</span><span>#1042</span></div><div class="t-meta"><span>{e(via)}</span><span>{e(when)}</span></div><ul>{lis}</ul></div>
</body></html>"""

async def main():
    from playwright.async_api import async_playwright
    out = os.path.join(ROOT, "src", "og")
    os.makedirs(out, exist_ok=True)
    langs = b.SITE_LANGS["ai"]
    async with async_playwright() as p:
        exe = next((x for x in ("/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser") if os.path.exists(x)), None)
        br = await p.chromium.launch(**({"executable_path": exe} if exe else {}), args=["--no-sandbox", "--allow-file-access-from-files"])
        pg = await br.new_page(viewport={"width": 1200, "height": 630})
        for l in langs:
            tmp = os.path.join(out, f".og-{l}.html")
            with open(tmp, "w", encoding="utf-8") as f: f.write(page(l))
            await pg.goto("file://" + tmp)
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(150)
            await pg.screenshot(path=os.path.join(out, f"og-{l}.jpg"), type="jpeg", quality=86)   # small enough for WhatsApp previews
            os.remove(tmp)
            print("og image", l)
        await br.close()

if __name__ == "__main__":
    asyncio.run(main())
