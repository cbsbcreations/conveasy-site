# Conveasy.be website: handoff

New conveasy.be (replaces the Framer site). Static HTML, 5 languages (nl, fr, en, tr, de).
Live on https://conveasy.be since 12 Nov 2026 (GitHub Pages, HTTPS enforced); the Framer site plan is cancelled.
Earlier, 11 Nov 2026 (Voor wie: sushi and kebab instead of snackbar, a page for all restaurants; the real
logo mark from the Framer site, favicon, WhatsApp profile pictures; earlier: phone AI and WhatsApp animations, the home
page's top row, "En verder" lists, webshop animation, "50+ calls at once", Marketing AI and kiosk animations, payment methods,
photo library, kiosk hardware 1599, voice greeting per page language, both demos connected, test address on GitHub Pages).

## Folders
- src/ : source. build.py builds the site from content.py, lang_de.py, lang_tr.py, overrides.py, answers.py, extras.py, sectors_more.py,
  legal/, site.css, site.js, favicon.svg and apple-touch-icon.png.
- brand/ : the logo mark (SVG), the WhatsApp profile pictures and the moving Gmail picture (GIF, source in brand/animatie/).
  Not part of the website.
  Run: `python3 src/build.py` (from this folder) to rebuild docs/ and preview/.
- docs/ : the finished website (index.html, nl/, fr/, en/, tr/, de/, assets/, sitemap.xml, robots.txt, llms.txt).
  GitHub Pages serves this folder from the repo cbsbcreations/conveasy-site (branch main).
  Live on conveasy.be since 12 Nov 2026: the build writes docs/CNAME (conveasy.be) and GitHub Pages has conveasy.be as custom
  domain (DNS check successful, certificate issued, Enforce HTTPS on), so the old test address forwards to conveasy.be and
  www.conveasy.be forwards to conveasy.be. DNS is at One.com (account of Selim Balci); Sammy changes it himself:
  A conveasy.be -> 185.199.108.153, .109.153, .110.153, .111.153 (GitHub Pages; before: Framer 31.43.160.6, 31.43.161.6);
  CNAME www -> cbsbcreations.github.io (before: sites.framer.app). Keep as they are: A app.conveasy.be -> 35.219.200.107 plus
  TXT app fah-claim and the _acme-challenge CNAME of app (restaurant portal and kitchen screens on Firebase App Hosting), and
  CNAME api.conveasy.be (self-hosted n8n at Elestio). The A record of app was deleted by mistake during the switch on 12 Nov
  and put back the same evening (A, hostname app, 35.219.200.107, TTL 3600); app.conveasy.be loads again over HTTPS.
  Framer: conveasy.be was removed from the Framer project "Xtract Template (copy)" and its Basic site plan (paid yearly) was
  cancelled on 12 Nov 2026; it stays active on its framer.app address until 13 Jun 2027 and does not renew. The other paid
  Framer site in that workspace (Complex Methods, interconnectedrec.be) is not Conveasy and was left alone.
- Kept from the Framer site: Meta's domain verification tag (FB_DOMAIN_VERIFY, on every page), the addresses /privacy, /terms and
  /data-deletion (Meta's WhatsApp app points to them; each is a real page with that English document), /about and /contact (forward
  to the English pages). 404.html is the not-found page (Dutch and English).
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
- Company: Balloz Solutions LLC, 1209 Mountain Road Pl NE STE N, Albuquerque, NM 87110 ("Road" written out, not "Rd").
  EIN 61-2205005. Email conveasyai@gmail.com. Phone for calls: +1 878 880 1550 (PHONE_DISPLAY / PHONE_TEL in content.py), shown in
  the footer, on the contact page ("Liever bellen?"), in the company details on the about and legal pages, on /privacy, /terms and
  /data-deletion, in llms.txt and in the structured data (Organization: legalName, taxID, address, telephone).
  Since 13 Nov 2026 the WhatsApp number +32 456 56 47 47 is no longer printed anywhere; the WhatsApp buttons still open a chat
  with it (WA_LINK).
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

## Phone AI animation
- phone_scene_i() in build.py + ".pscene" in site.css. Shown at the top of the phone AI page and as the first tile of the home page's
  top visual. Three parts in one 17 second loop, no people in it (Sammy, 11 Nov 2026):
  1. the restaurant counter (menu board, lamps, bell, fries, bag): the desk phone rings, the handset clicks up, the view zooms in;
  2. the call: the AI's voice orb, the caller's number and the call time, what the caller says, the AI's answer, "Bestelling bevestigd";
  3. a laptop with the dashboard: a notification "Nieuwe bestelling", the order lands at the top of the list, the printer prints the
     ticket, then "In het dashboard" and "Ticket geprint".
  The pill on top follows the stages: "Inkomende oproep", "AI neemt op", "In de keuken". With reduced motion it rests on part 2.
- Texts per language: PCALL in build.py (the two sentences, the notification, the items, the two checks); the rest comes from CALL,
  DASH, TICKET_META, WSCENE and P. The counter is one SVG on a 400 x 360 grid with the phone at x = 200. The zoom moves the drawing
  inside its part, which clips it, so nothing reaches past the scene (no sideways scrolling on phones).
- It replaced the paper ticket at the top of the phone AI page, and on 11 Nov (evening) an earlier version with stick figures.

## WhatsApp animation
- chat_i() in build.py + ".wchat" in site.css. The customer types and sends the order, the AI types and answers with the order and two
  buttons, the customer taps "Bevestigen", the AI confirms ("Top! Je bestelling staat in de keuken. Levering rond 19:55.").
  Pure CSS, one 15 second loop. With reduced motion every message is shown.
- Shown at the top of the WhatsApp AI page, as the second tile of the home page's top visual and in "Zo loopt een bestelling" (home).
  The chat's text scales with its width, so it also gets taller when wider; in "Zo loopt een bestelling" its width follows the height of
  the sticky stage (.fs > .wchat in site.css).
- The opening texts are in CHAT, the confirmation in CHAT_DONE (build.py).

## Home page, top visual
- home_stage() in build.py + ".stage-home", ".hs-row", ".hs-item" in site.css: three scenes in a row, each with its product name as a link
  under it: phone AI, WhatsApp AI, webshop phone. Under 860px the row becomes a strip to swipe (the next scene peeks in from the right).
- The paper ticket is a small accent behind the right-hand corner (.l-ticket, scaled to 62%), hidden under 1180px.
- The kitchen screen and the "incoming call" pill are no longer in this visual; the kitchen screen is still in "Zo loopt een bestelling" and
  "Zo ziet het eruit".
- The visual moves up a little while scrolling (px-up in site.css). Where the text sits above the visual (phones, and the home page at
  every width) the travel is short (--px-up: -12px), so the visual never rides up against the buttons.

## "En verder" lists (what the systems also do)
- src/extras.py, shown by more_band() in build.py under the feature tiles of the phone AI, WhatsApp AI and webshop pages (".also" in site.css).
- Phone AI: knows regulars, WhatsApp after a call without an order, address check (streets per postcode, zones, minimum), transfer to the
  team, adding to the order in the same call, answering outside opening hours, the safety net (order still reaches the kitchen when the
  customer hangs up early; an AI checks every ticket after the call).
- WhatsApp AI: change or cancel a reservation, delivery cost per address, asks when it does not recognise a product, voordeelkaarten.
  The "Online betalen" tile now also says: Klarna and meal vouchers, the order only goes to the kitchen once paid, an unpaid link expires
  after 20 minutes.
- Webshop: live order tracking, reorder in one tap, promotions, five designs, 14 allergens per product, the drivers' app, numbers and
  Z-reports with export to Excel (all from the README of the repo conveasy-webshop).
- Source: the live n8n phone and WhatsApp flows and the webshop repo, read on 11 Nov 2026. The phone safety-net flows carry the name Eatpoint
  in n8n: check that they also run for Conveasy's client restaurants, since the site now says so.
- llms.txt carries the same points in English.

## Restaurant types ("Voor wie")
- Since 11 Nov 2026: Frituur, Sushi, Pizzeria, Burger, Kebab and Alle restaurants (SECTORS in content.py). The snackbar page is gone
  (Sammy). Old addresses of it (nl/snackbar, fr/snack, en/snack-bar, tr/snack-bar, de/imbiss) no longer exist.
- Texts of sushi, kebab and "alle" in five languages: src/sectors_more.py, which also holds the home section heading ("Voor elk type
  restaurant" with one line under it), the short card text of "alle" and the about page's description. Frituur, pizzeria and burger
  stay in content.py (nl, fr, en), lang_tr.py and lang_de.py.
- The "Alle restaurants" page shows the kinds of restaurants as chips that pop in, with "+ Jouw zaak" last (TYPES in
  sectors_more.py, types_i() in build.py, .types in site.css).

- Other sectors (Sammy, 12 Nov 2026): conveasy.be stays restaurant-only. The contact page has one line for businesses that are not
  restaurants ("Geen restaurant? We bouwen ook AI-telefonie voor andere sectoren.", OTHER in sectors_more.py). Later each other
  sector (garages, realtors) gets its own site, and all the sector sites will link to each other.

## Logo
- The logo mark is the drawing from the Framer site (white squircle with a small square and an arrow): LOGO_MARK in build.py (header
  and footer), src/favicon.svg (browser tab, white on a black rounded square), src/apple-touch-icon.png (phone home screen), and
  brand/conveasy-logo-mark.svg.
- WhatsApp profile pictures, 1080 x 1080, made from the mark: brand/conveasy-whatsapp-profiel-zwart.png (black with an orange glow) and
  brand/conveasy-whatsapp-profiel-oranje.png. WhatsApp crops them to a circle; the mark stays inside it.
- Moving logo for the Gmail / Google account picture (12 Nov 2026): brand/conveasy-gmail-profiel-bewegend.gif (512 x 512, about
  1 MB) and brand/conveasy-gmail-profiel-bewegend-klein.gif (256 x 256, about 0.4 MB). A 3-second loop: an orange light circles the
  logo, the arrow fills orange (an order coming in), the small square lights up, two waves go out, a light sweep crosses the logo.
  The first frame is the complete logo, because some Google views only show the first frame. Source: brand/animatie/anim.html
  (draws each frame on a canvas from a time 0..1); `node brand/animatie/render.js <folder> 75` writes the 75 frames, then ffmpeg
  makes the GIF (palettegen max_colors=128, paletteuse dither=none, diff_mode=rectangle). Upload: Google Account > Personal info >
  Profile picture > Upload from device.

## Rules
- Call it "Marketing AI". Never mention Eatpoint on the site. No auto ads/ad testing promised. No kassa/POS page.
- Look: black starfield, orange accent, scroll animations, like the old Framer site.
