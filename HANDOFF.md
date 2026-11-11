# Conveasy.be website: handoff

New conveasy.be (replaces the Framer site). Static HTML, 5 languages (nl, fr, en, tr, de).
Last update: 11 Nov 2026 (webshop phone animation, "50+ calls at once" on the phone AI page, Marketing AI animation, kiosk animation, payment methods, photo library, kiosk hardware 1599, voice greeting per page language;
earlier that day: chat demo and voice demo connected, test address on GitHub Pages).

## Folders
- src/ : source. build.py builds the site from content.py, lang_de.py, lang_tr.py, overrides.py, answers.py, legal/, site.css, site.js.
  Run: `python3 src/build.py` (from this folder) to rebuild docs/ and preview/.
- docs/ : the finished website (index.html, nl/, fr/, en/, tr/, de/, assets/, sitemap.xml, robots.txt, llms.txt).
  GitHub Pages serves this folder from the repo cbsbcreations/conveasy-site (branch main).
  Test address: https://cbsbcreations.github.io/conveasy-site/ . For conveasy.be itself: add a file docs/CNAME with `conveasy.be`
  (let the build write it), set the custom domain under the repo's Settings > Pages, and point the DNS at One.com to GitHub Pages.
  The pages link the stylesheet and the script with a fingerprint (site.css?v=..., written by the build), so a browser that still
  holds an older copy fetches the new one together with the new page.
- preview/ : same site with an orange "preview" bar, used for the claude.ai preview (main.html is the page that is published there).
  Not in git; the build makes it. Inside that preview the two live demos cannot run (no microphone, no outside connections); they show a note.
- n8n/ : copy of the two Code nodes of the chat demo workflow.
- PLACEHOLDERS.txt : what still has to be filled in (written by the build).

## The two live demos (home page, phone AI page, WhatsApp AI page)
### WhatsApp chat demo: connected
- src/site.js posts {message, history, lang} to `CHAT_DEMO_ENDPOINT` and gets {reply, buttons}, {limit: true} or {error} back.
  The page keeps the conversation and sends it along each time; nothing is stored on a server.
- Endpoint: n8n workflow "Conveasy — Website chat demo (WhatsApp)" (id 9eb0PIubSSJ6ovPe) on balloz.app.n8n.cloud,
  POST /webhook/conveasy-site-wa-demo. When n8n moves to api.conveasy.be, change CHAT_DEMO_ENDPOINT in src/site.js and rebuild.
- The workflow calls Claude Haiku 5.5 directly (credential "Anthropic account"); the menu and rules are in its node "Build Request".
  The menu is a copy of the Vapi assistant "TEST Conveasy" (Mario's Snackbar): change it in both places.
- It only answers these origins: https://conveasy.be, https://www.conveasy.be, https://cbsbcreations.github.io.
  A new test address has to be added in the workflow's trigger "Chat In" (Allowed Origins and Only Run If).
- Limits: 300 characters per message, 20 messages per conversation, 1500 messages per day (top of "Build Request").
- Cost: about $0.0003 per message (Claude Haiku 5.5). Vapi's chat costs $0.005 per message plus the model, so about 15x more.

### Voice demo ("Probeer onze AI"): connected
- src/site.js: `VAPI_PUBLIC_KEY` is the Vapi public key "conveasy.be website" (made 11 Nov 2026). In Vapi it is limited to the origins
  https://conveasy.be, https://www.conveasy.be and https://cbsbcreations.github.io, to the assistant "TEST Conveasy"
  (id 7ffc6c16-d943-4f97-98e3-a84351ffd954), and transient assistants are off. A new address has to be added to the key in Vapi > API Keys.
- Never put the account's general public key (works everywhere, with every assistant) or a private key in the site.
- A call is cut off after 3 minutes (MAX_SECONDS in site.js, sent to Vapi as maxDurationSeconds).
- The Vapi SDK is loaded from jsDelivr on the first click (@vapi-ai/web 3.0.1).
- The assistant greets in the language of the page: VOICE_FIRST in build.py, sent to Vapi as firstMessage when the call starts.
- The assistant "TEST Conveasy" runs on GPT-6 Luna since 11 Nov 2026 (was GPT-5.6 Luna).

## Business facts used on the site
- Company: Balloz Solutions LLC, 1209 Mountain Rd Pl NE STE N, NM 87110 (Albuquerque). Email conveasyai@gmail.com.
- Prices/month: WhatsApp AI 99, webshop 79, kiosk 89, Marketing AI 69 (includes Google/Apple Wallet stamp card).
- Setup: voice AI 299, others 199, bundle voice+WhatsApp+webshop+kiosk 399. Kiosk hardware 1599 (21.5" table stand), payable in 3 instalments.
- 1 week free trial. Over the limit = upgrade to a bigger plan. Live within max 10 days.
- Phone and WhatsApp AI are 24/7, reservations included. Webshop: own domain or we provide one.
- Online payment methods on the webshop and QR ordering (webshop page, PAY in build.py): Bancontact, iDEAL, Klarna, Riverty, PayPal,
  meal vouchers, Visa, Mastercard, Apple Pay, Google Pay.
- Restaurants can pick product photos from our library of high-quality dish photos (webshop page and kiosk page).
- Demo requests go to conveasyai@gmail.com (form opens email app).
- Legal pages copied from the Framer site and translated (not checked by a lawyer).

## Kiosk animation
- kiosk_i() in build.py + ".kscene" in site.css: a figure orders at the kiosk (language choice, burger and fries, pay, ticket).
  Pure CSS, one 14 second loop; shown on the kiosk page (top) and on the home page ("In de app"). With reduced motion it stands still.

## Webshop animation (the phone)
- web_i() in build.py + ".wscene" in site.css. Shown on the webshop page (top), in the home page's top visual and in the home page's
  "Zo ziet het eruit". A customer adds three products, fills in the address (the delivery cost appears), picks Bancontact and places
  the order; then the order page: thank you, the minutes counting down (25, 17, 10), the steps Ontvangen > In de keuken > Onderweg >
  Bezorgd, "Onderweg met Ali", a small map with the route, and "Smakelijk!". Pure CSS, one 16 second loop.
- The words of the order page are the real webshop's own (repo conveasy-webshop, src/lib/i18n/dict: shop-status.ts, tracking.ts,
  driver.ts); German is not in the webshop yet, so that translation is ours. Scene texts: WSCENE in build.py; the menu: OVX[lang]["web"].
- With reduced motion it rests on the menu with a filled basket.

## Phone AI: "50+ calls at the same time"
- Feature tile, the three price tiers, a FAQ entry and llms.txt say this since 11 Nov 2026 (Sammy's wording).
- Vapi limits the simultaneous calls per Vapi account (inbound too; 10 lines included on older accounts, more can be bought, see
  docs.vapi.ai/calls/call-concurrency). Check in Vapi > Billing that the account really has 50+ lines; calls above the limit are not answered.

## Marketing AI animation
- mkt_scene_i() in build.py + ".mscene" in site.css: Mario's Snackbar sends, lines run to three customer phones, a message lands on
  each (WhatsApp, e-mail, Wallet), then orders come back ("Bestellingen +3"). Pure CSS, one 12 second loop; shown at the top of the
  Marketing AI page. With reduced motion it stands still with everything shown. The words per language are in MSCENE in build.py.
- It replaced the "Deze week" list at the top of that page (mkt_i in build.py, no longer shown).
- The channel icons are plain shapes (speech bubble, envelope, card), not the logos of WhatsApp or the wallets.

## Rules
- Call it "Marketing AI". Never mention Eatpoint on the site. No auto ads/ad testing promised. No kassa/POS page.
- Look: black starfield, orange accent, scroll animations, like the old Framer site.
