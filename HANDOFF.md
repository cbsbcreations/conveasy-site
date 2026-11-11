# Conveasy.be website: handoff

New conveasy.be (replaces the Framer site). Static HTML, 5 languages (nl, fr, en, tr, de).
Last update: 11 Nov 2026 (chat demo and voice demo connected; test address on GitHub Pages).

## Folders
- src/ : source. build.py builds the site from content.py, lang_de.py, lang_tr.py, overrides.py, answers.py, legal/, site.css, site.js.
  Run: `python3 src/build.py` (from this folder) to rebuild docs/ and preview/.
- docs/ : the finished website (index.html, nl/, fr/, en/, tr/, de/, assets/, sitemap.xml, robots.txt, llms.txt).
  GitHub Pages serves this folder from the repo cbsbcreations/conveasy-site (branch main).
  Test address: https://cbsbcreations.github.io/conveasy-site/ . For conveasy.be itself: add a file docs/CNAME with `conveasy.be`
  (let the build write it), set the custom domain under the repo's Settings > Pages, and point the DNS at One.com to GitHub Pages.
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

## Business facts used on the site
- Company: Balloz Solutions LLC, 1209 Mountain Rd Pl NE STE N, NM 87110 (Albuquerque). Email conveasyai@gmail.com.
- Prices/month: WhatsApp AI 99, webshop 79, kiosk 89, Marketing AI 69 (includes Google/Apple Wallet stamp card).
- Setup: voice AI 299, others 199, bundle voice+WhatsApp+webshop+kiosk 399. Kiosk hardware 899 (21.5" table stand).
- 1 week free trial. Over the limit = upgrade to a bigger plan. Live within max 10 days.
- Phone and WhatsApp AI are 24/7, reservations included. Webshop: own domain or we provide one.
- Demo requests go to conveasyai@gmail.com (form opens email app).
- Legal pages copied from the Framer site and translated (not checked by a lawyer).

## Rules
- Call it "Marketing AI". Never mention Eatpoint on the site. No auto ads/ad testing promised. No kassa/POS page.
- Look: black starfield, orange accent, scroll animations, like the old Framer site.
