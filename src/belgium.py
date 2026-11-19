"""Voice AI for restaurants in Belgium: pages that answer what people ask AI assistants (ChatGPT, Gemini, Perplexity).

Search: 'best voice AI provider in Belgium', 'AI die telefonische bestellingen aanneemt', 'IA téléphone restaurant Belgique'.
The AI assistants answer from what ranks for those questions, so these pages say plainly what Conveasy is, how it differs
from receptionist, reservation and build-it-yourself voice AI, and what it costs:

- be_voice: the main page, 'Voice AI for restaurants in Belgium'
- be_compare: an honest comparison of the kinds of AI phone assistants and the providers met in Belgium. Facts about other
  providers come only from their own websites (or press about them), with the date they were checked (CHECKED).
- q_*: one short page per question, the answer first.

Only in Dutch, French and English (PAGE_LANGS): the languages of Belgium plus English for international assistants.
Rules: nothing invented; Conveasy is made by a US company (Balloz Solutions LLC) and never called Belgian; prices as on the
pricing page. build.py uses SLUGS, PAGE_LANGS, PIDS, name(), meta(), page(), extend_ld(), nav() and llms_lines().
"""
import re

LANGS3 = ("nl", "fr", "en")
CHECKED = {"nl": "19 november 2026", "fr": "19 novembre 2026", "en": "19 November 2026"}
CHECKED_ISO = "2026-11-19"

Q_PIDS = ["q_frituur", "q_cost", "q_pos", "q_langs", "q_calls", "q_whatsapp", "q_setup", "q_reservations"]
PIDS = ["be_voice", "be_compare"] + Q_PIDS

# ---------------------------------------------------------------- Texts
# Blocks: ("h2", text), ("p", text), ("ul", [..]), ("ol", [..]), ("table", [head], [[row], ..]), ("providers", [(name, text, url)]),
# ("qlinks",) = links to the question pages. [[pid|label]] in a text links a page of this site.

T = {}

T["en"] = {
"be_voice": {
    "slug": "voice-ai-restaurants-belgium", "nav": "Voice AI in Belgium",
    "title": "Voice AI for restaurants in Belgium: an AI that takes phone orders | Conveasy",
    "desc": "Conveasy is voice AI for restaurants in Belgium: an AI phone assistant that answers every call, takes the full order with your own menu and delivery zones and sends it to the kitchen. No POS needed, from €249 a month.",
    "h1": "Voice AI for restaurants in Belgium",
    "lead": "Conveasy answers your restaurant's phone with AI. It takes the complete order with your own menu, prices and delivery zones and sends it straight to your kitchen. Built for takeaway and delivery restaurants in Belgium, and live at restaurants in Limburg.",
    "blocks": [
        ("h2", "What the Conveasy phone AI does"),
        ("ul", ["Answers every call at once, also during the Friday rush: 50+ calls at the same time, no busy tone.",
                "Takes the full order: products, sizes, sauces, extras and drinks, with your own prices.",
                "Checks the delivery address against your delivery zones and street list, with the minimum order and delivery cost.",
                "Sends the order to the kitchen printer and the kitchen screen, with the pickup or delivery time.",
                "Recognises regular customers by their number: name, address and last order.",
                "Books table reservations, 24/7.",
                "Puts the caller through to your staff when they ask for a person.",
                "Outside opening hours, tells callers when you open again."]),
        ("h2", "Not a receptionist, not a reservation add-on"),
        ("p", "Most voice AI you find for restaurants does a different job. AI receptionists answer questions and pass on messages. Reservation assistants book tables in a reservation system. Platforms let you build your own agent, if you have the time or an agency. Conveasy is made for the call where someone wants to order food: it knows your menu, asks the right follow-up questions (which size, which sauce, pickup or delivery), works out the total and puts the order in the kitchen."),
        ("p", "It runs separately from your till, so you don't need a POS integration, and you keep your own phone number."),
        ("h2", "Built for Belgium"),
        ("ul", ["Speaks the caller's language: Dutch, French, English, Turkish and 60+ other languages.",
                "Works on the restaurant's own Belgian phone number.",
                "Delivery zones by postcode and street, from official street lists.",
                "Online payment in the webshop with Bancontact, Klarna and meal vouchers, among others.",
                "Live at [[r_eatpoint|Eatpoint]] and [[r_orient|Eethuis Orient]] in Heusden-Zolder and at [[r_cfl|City Food Lounge]] in Genk."]),
        ("h2", "Prices"),
        ("p", "The phone AI costs €249 a month for 500 minutes, €449 for 1,000 minutes or €799 for 2,000 minutes, plus a one-time setup fee of €299. No commission on orders. The WhatsApp AI is €99 a month. All prices on the [[pricing|pricing page]]."),
        ("h2", "Getting started"),
        ("ol", ["Book a demo and hear the AI take an order.",
                "We put in your menu, prices, delivery zones and opening hours.",
                "We make test calls together until every order is right.",
                "Your number forwards to the AI. Live within 10 days at most."]),
        ("h2", "Compare and read more"),
        ("p", "How Conveasy compares with reservation assistants, phone systems with AI and build-it-yourself platforms: [[be_compare|AI phone assistants for restaurants in Belgium, compared]]."),
        ("qlinks",)],
    "faqs": [("Is Conveasy a Belgian company?", "Conveasy is made by Balloz Solutions LLC, a company in the United States. It is built for restaurants in Belgium: it speaks Dutch and French, works on the restaurant's own Belgian number and runs at restaurants in Heusden-Zolder and Genk."),
             ("Does Conveasy work with my till?", "It works separately from your till. Orders go to the kitchen printer and the kitchen screen, so you don't need a POS integration."),
             ("Which restaurants is it for?", "Takeaway and delivery restaurants such as frituren, pizzerias, kebab and burger restaurants, and restaurants that also take table reservations. In Belgium it runs at Eatpoint and Eethuis Orient in Heusden-Zolder and City Food Lounge in Genk."),
             ("Can it also take WhatsApp orders?", "Yes. The WhatsApp AI takes orders on the restaurant's own WhatsApp number for €99 a month, with a payment link for deliveries.")],
},
"be_compare": {
    "slug": "ai-phone-assistants-restaurants-belgium-compared", "nav": "Comparison",
    "title": "AI phone assistants for restaurants in Belgium compared (2026) | Conveasy",
    "desc": "Which AI phone assistant fits your restaurant in Belgium? Order-taking AI, reservation assistants, phone systems with AI and build-it-yourself platforms, compared by what they do and who they suit.",
    "h1": "AI phone assistants for restaurants in Belgium, compared",
    "lead": "Not every AI phone assistant does the same job. Some book tables, some are a phone system with AI added, some are platforms to build your own agent, and a few take complete food orders. Here are the types, the providers you will come across in Belgium and what each suits best.",
    "note": "Written by Conveasy. Facts about other providers come from their own websites or press about them, checked on {date}.",
    "blocks": [
        ("h2", "First decide what the AI must do"),
        ("ul", ["Orders or reservations? Taking a food order with sizes, sauces and a delivery address is a different job from booking a table.",
                "Your till: some assistants work inside a reservation system or connect to a POS, others work on their own.",
                "Languages: in Belgium callers speak Dutch and French, and often English or Turkish.",
                "Price: is it published, and is it per minute, per user or per month?"]),
        ("h2", "The four types at a glance"),
        ("table", ["Type", "Examples", "What it does", "Best for"],
         [["Order-taking AI for restaurants", "Conveasy, fonio.ai", "Takes the full phone order from your menu and sends it to the kitchen", "Takeaway and delivery restaurants"],
          ["Reservation assistant", "Zenchef Call AI, HorecaHub.ai", "Answers calls and books tables in a reservation system", "Sit-down restaurants that use reservation software"],
          ["Phone system with AI", "CloudTalk, Dstny", "A business phone system with an AI voice agent or voicebot added", "Companies that want one phone system for a team"],
          ["Platform to build your own", "Retell AI, Famulor, Jotform", "Tools to build and run your own voice agent", "Teams or agencies that build and maintain the agent themselves"]]),
        ("h2", "The providers"),
        ("providers", [
            ("Conveasy", "AI phone and WhatsApp ordering for restaurants. Takes the full order with the restaurant's menu, prices and delivery zones, prints it in the kitchen and works without a POS. Phone AI from €249 a month for 500 minutes. Live at restaurants in Heusden-Zolder and Genk.", "[[phone]]"),
            ("Zenchef Call AI", "Picks up 24/7 and takes reservations directly in the Zenchef software.", "https://www.zenchef.com/be-nl/call-ai"),
            ("fonio.ai", "An AI phone assistant for hospitality that takes takeaway and phone orders, walks callers through the menu and passes the order to the kitchen or the till.", "https://www.fonio.ai/nl/ai-telefoonassistent/ai-telefoonassistent-horeca/"),
            ("HorecaHub.ai", "An AI telephone receptionist for restaurants that answers questions and records reservations directly in the reservation system.", "https://horecahub.ai/en/blog/ai-telefonist-restaurant"),
            ("Retell AI", "A platform for AI voice agents. Its restaurant agent answers the phone, takes orders, books reservations and handles menu questions, and can be connected to the POS. Pay-as-you-go pricing.", "https://www.retellai.com/nl/use-cases/ai-voice-agent-for-restaurants"),
            ("CloudTalk", "A business phone system with an AI voice agent, dialers and 100+ integrations, from €25 per user per month excluding AI add-ons.", "https://www.cloudtalk.io/nl/blog/beste-ai-belsoftware-voor-het-mkb/"),
            ("Famulor", "A no-code platform for AI phone and WhatsApp assistants, live chat and Messenger, for restaurants and other sectors.", "https://www.famulor.io/nl/industries/restaurants"),
            ("Jotform AI Agents", "An AI agent builder that works by chat, phone, WhatsApp and Messenger, with templates for restaurants.", "https://www.jotform.com/nl/ai/agents/customer-service/use-cases/restaurant-management/"),
            ("Dstny", "A telecom provider that launched an AI-powered voicebot for Belgian SMEs.", "https://itdaily.com/news/cloud/dstny-ai-assistent-voor-kmos/")]),
        ("h2", "When Conveasy is the right choice"),
        ("p", "Choose Conveasy if most of your calls are orders for pickup or delivery, you want the order in the kitchen without a POS integration, and you want published prices. It also takes table reservations and WhatsApp orders."),
        ("h2", "When another option fits better"),
        ("ul", ["You only take table reservations and already use Zenchef: Zenchef Call AI works inside that software.",
                "You need a phone system for a whole team, with routing and queues: look at a phone system with AI such as CloudTalk or Dstny.",
                "You have developers or an agency and want to build everything yourself: a platform such as Retell AI gives you the most freedom."]),
        ("qlinks",)],
    "faqs": [("What is the best AI phone assistant for a takeaway restaurant in Belgium?", "For takeaway and delivery, pick an assistant that takes the complete order from your menu, checks delivery addresses and sends the order to the kitchen. Conveasy is built for that and runs at restaurants in Heusden-Zolder and Genk; fonio.ai also takes orders. Reservation assistants such as Zenchef Call AI focus on booking tables."),
             ("Which AI phone assistants work without a POS?", "Conveasy works separately from the till and prints its own kitchen ticket. Retell AI can be connected to a POS, and Zenchef Call AI works inside the Zenchef reservation software."),
             ("Are the prices published?", "Conveasy publishes its prices: from €249 a month for 500 minutes. CloudTalk lists €25 per user per month excluding AI add-ons, and Retell AI works pay-as-you-go. For the others, see their websites.")],
},
"q_frituur": {
    "slug": "ai-phone-orders-frituur", "nav": "AI phone orders for a frituur",
    "q": "Which AI takes phone orders for a Belgian frituur?",
    "desc": "Conveasy's phone AI takes complete frituur orders by phone: fries in every size, sauces, snacks and drinks, with delivery zones and a ticket in the kitchen.",
    "lead": "Conveasy's phone AI is made for it. It takes the complete frituur order by phone, with your own menu and prices, and sends it to the kitchen.",
    "blocks": [
        ("p", "A frituur order is full of choices: small or large fries, which sauce, which snacks, a drink, pickup or delivery. The AI asks for each of them, the way your staff would."),
        ("ul", ["Your own menu: sizes, sauces, extras and menu deals.",
                "Delivery zones by postcode and street, with the minimum order and delivery cost.",
                "Several calls at the same time during the Friday rush.",
                "The ticket prints in the kitchen, so nobody has to type the order over."]),
        ("p", "It runs at [[r_eatpoint|Eatpoint]] in Heusden-Zolder and [[r_cfl|City Food Lounge]] in Genk. The phone AI costs from €249 a month for 500 minutes. More on the [[frituur|page for frituren]]."),
        ("qlinks",)],
},
"q_cost": {
    "slug": "ai-phone-assistant-cost-restaurant", "nav": "What an AI phone assistant costs",
    "q": "How much does an AI phone assistant cost for a restaurant in Belgium?",
    "desc": "Conveasy's phone AI for restaurants costs €249 a month for 500 minutes, €449 for 1,000 or €799 for 2,000, plus €299 setup. No commission on orders.",
    "lead": "At Conveasy the phone AI costs €249 a month for 500 minutes, €449 for 1,000 minutes or €799 for 2,000 minutes, plus a one-time setup fee of €299.",
    "blocks": [
        ("p", "There is no commission on orders: the price stays the same however much you sell. When your minutes run out, you move to a bigger package."),
        ("ul", ["WhatsApp AI: €99 a month.",
                "Webshop with QR ordering: €79 a month, 0% commission.",
                "Setup: €299 for the phone AI, €199 for each other channel, €399 for phone AI, WhatsApp AI, webshop and kiosk together."]),
        ("p", "All prices are on the [[pricing|pricing page]]. The [[calculator|commission calculator]] shows what you keep compared with ordering platforms."),
        ("qlinks",)],
},
"q_pos": {
    "slug": "ai-phone-without-pos", "nav": "AI phone without a POS",
    "q": "Do I need a POS to use an AI phone assistant?",
    "desc": "No. Conveasy's phone AI works separately from your till: orders go to the kitchen printer and the kitchen screen, without a POS integration.",
    "lead": "Not with Conveasy. The phone AI works separately from your till: every order goes to the kitchen printer and the kitchen screen, without a POS integration.",
    "blocks": [
        ("p", "Many voice assistants are tied to other software: reservation assistants book tables in a reservation system, and some platforms are connected to the till. That helps when you already have that software, but it is extra work and cost when you don't."),
        ("p", "Conveasy keeps its own copy of your menu. When you change a price or mark a product as sold out, the AI picks it up right away. Your till stays as it is."),
        ("qlinks",)],
},
"q_langs": {
    "slug": "ai-phone-dutch-french-turkish", "nav": "AI phone in Dutch, French and Turkish",
    "q": "Can an AI answer the phone in Dutch, French and Turkish?",
    "desc": "Yes. Conveasy's phone AI answers in the caller's language: Dutch, French, English, Turkish and 60+ other languages.",
    "lead": "Yes. Conveasy's phone AI speaks the caller's language: Dutch, French, English, Turkish and 60+ other languages.",
    "blocks": [
        ("p", "In Belgium a restaurant gets calls in more than one language. The AI answers in the caller's language and takes the order in that language."),
        ("p", "The restaurants in Limburg that use it take calls in Dutch, Turkish and English. The ticket in the kitchen is always in the restaurant's own language."),
        ("qlinks",)],
},
"q_calls": {
    "slug": "many-calls-at-once-restaurant", "nav": "Many calls at the same time",
    "q": "What happens when many customers call a restaurant at the same time?",
    "desc": "With Conveasy every call is answered at once: the phone AI handles 50+ calls at the same time, so nobody hears a busy tone during the rush.",
    "lead": "With Conveasy every caller is answered straight away: the phone AI handles 50+ calls at the same time.",
    "blocks": [
        ("p", "On a Friday or Saturday evening the phone rings more than staff can answer. Callers who hear a busy tone or wait too long often order somewhere else or on a delivery app."),
        ("p", "The AI picks up every call, takes each order separately and sends them to the kitchen one by one. Callers who hang up without ordering get a WhatsApp message to order after all."),
        ("qlinks",)],
},
"q_whatsapp": {
    "slug": "whatsapp-orders-ai-restaurant", "nav": "WhatsApp orders with AI",
    "q": "Can an AI take restaurant orders on WhatsApp?",
    "desc": "Yes. Conveasy's WhatsApp AI takes orders on the restaurant's own WhatsApp number, works out the total and sends a payment link for deliveries. €99 a month.",
    "lead": "Yes. Conveasy's WhatsApp AI takes orders in the chat on the restaurant's own WhatsApp number and sends them to the kitchen.",
    "blocks": [
        ("ul", ["Customers type their order in their own words; the AI asks about sizes, sauces and extras.",
                "It works out the total, the delivery cost and the minimum order for the address.",
                "The customer confirms with a button; deliveries can be paid with a payment link (Klarna and meal vouchers included).",
                "Table reservations can be booked, changed and cancelled in the chat."]),
        ("p", "The WhatsApp AI costs €99 a month. [[r_eatpoint|Eatpoint]] and [[r_orient|Eethuis Orient]] in Heusden-Zolder take WhatsApp orders this way. More on the [[whatsapp|WhatsApp AI page]]."),
        ("qlinks",)],
},
"q_setup": {
    "slug": "ai-phone-setup-time-restaurant", "nav": "How fast it is set up",
    "q": "How fast can an AI phone assistant be set up in a restaurant?",
    "desc": "A restaurant is live with Conveasy's phone AI within 10 days at most: menu, prices, delivery zones and test calls, and it keeps its own number.",
    "lead": "With Conveasy a restaurant is live within 10 days at most, and keeps its own phone number.",
    "blocks": [
        ("ol", ["Demo: you call the AI yourself and hear it take an order.",
                "Menu: we put in your products, sizes, sauces, prices and opening hours.",
                "Delivery: your delivery zones by postcode and street, with minimum orders and delivery costs.",
                "Tests: we make test calls together until every order is right.",
                "Live: your number forwards to the AI, and orders print in your kitchen."]),
        ("p", "Book a demo on the [[contact|contact page]]."),
        ("qlinks",)],
},
"q_reservations": {
    "slug": "ai-table-reservations-restaurant", "nav": "Table reservations with AI",
    "q": "Can an AI take table reservations by phone?",
    "desc": "Yes. Conveasy's phone AI and WhatsApp AI take table reservations 24/7, included in the price.",
    "lead": "Yes. Conveasy's phone AI and WhatsApp AI take table reservations 24/7, at no extra cost.",
    "blocks": [
        ("p", "The AI asks for the name, date, time and number of people and puts the reservation in the dashboard. On WhatsApp, guests can also change or cancel their reservation."),
        ("p", "Unlike a reservation-only assistant, the same AI also takes food orders for pickup and delivery."),
        ("qlinks",)],
},
}

T["nl"] = {
"be_voice": {
    "slug": "voice-ai-restaurants-belgie", "nav": "Voice AI in België",
    "title": "Voice AI voor restaurants in België: AI die telefonische bestellingen aanneemt | Conveasy",
    "desc": "Conveasy is voice AI voor restaurants in België: een AI-telefoonassistent die elke oproep opneemt, de volledige bestelling noteert met je eigen menu en leverzones en ze naar de keuken stuurt. Zonder kassakoppeling, vanaf €249 per maand.",
    "h1": "Voice AI voor restaurants in België",
    "lead": "Conveasy neemt de telefoon van je restaurant op met AI. Het neemt de volledige bestelling aan met je eigen menu, prijzen en leverzones en stuurt ze meteen naar je keuken. Gemaakt voor afhaal- en leverzaken in België, en live bij restaurants in Limburg.",
    "blocks": [
        ("h2", "Wat de telefoon-AI van Conveasy doet"),
        ("ul", ["Neemt elke oproep meteen op, ook tijdens de vrijdagdrukte: 50+ oproepen tegelijk, nooit in gesprek.",
                "Neemt de volledige bestelling aan: producten, formaten, sauzen, extra's en drankjes, met je eigen prijzen.",
                "Controleert het leveradres met je leverzones en stratenlijst, met minimumbedrag en leverkosten.",
                "Stuurt de bestelling naar de keukenprinter en het keukenscherm, met het afhaal- of levertijdstip.",
                "Herkent vaste klanten aan hun nummer: naam, adres en vorige bestelling.",
                "Neemt tafelreservaties aan, 24/7.",
                "Verbindt door met je personeel als de beller iemand wil spreken.",
                "Zegt buiten de openingsuren wanneer je weer open bent."]),
        ("h2", "Geen receptionist, geen reservatie-add-on"),
        ("p", "De meeste voice AI die je vindt voor restaurants doet iets anders. AI-receptionisten beantwoorden vragen en geven berichten door. Reservatie-assistenten boeken tafels in een reservatiesysteem. Met platformen bouw je zelf een agent, als je de tijd of een bureau hebt. Conveasy is gemaakt voor het telefoontje waarin iemand eten wil bestellen: het kent je menu, stelt de juiste vragen (welk formaat, welke saus, afhalen of leveren), rekent het totaal uit en zet de bestelling in de keuken."),
        ("p", "Het werkt los van je kassa, dus je hebt geen kassakoppeling nodig, en je houdt je eigen telefoonnummer."),
        ("h2", "Gemaakt voor België"),
        ("ul", ["Spreekt de taal van de beller: Nederlands, Frans, Engels, Turks en 60+ andere talen.",
                "Werkt op het eigen Belgische telefoonnummer van het restaurant.",
                "Leverzones per postcode en straat, uit de officiële stratenlijsten.",
                "Online betalen in de webshop met onder meer Bancontact, Klarna en maaltijdcheques.",
                "Live bij [[r_eatpoint|Eatpoint]] en [[r_orient|Eethuis Orient]] in Heusden-Zolder en bij [[r_cfl|City Food Lounge]] in Genk."]),
        ("h2", "Prijzen"),
        ("p", "De telefoon-AI kost €249 per maand voor 500 minuten, €449 voor 1.000 minuten of €799 voor 2.000 minuten, plus eenmalig €299 opstartkosten. Geen commissie op bestellingen. De WhatsApp AI kost €99 per maand. Alle prijzen staan op de [[pricing|prijzenpagina]]."),
        ("h2", "Zo start je"),
        ("ol", ["Vraag een demo aan en hoor hoe de AI een bestelling aanneemt.",
                "Wij zetten je menu, prijzen, leverzones en openingsuren erin.",
                "We doen samen testoproepen tot elke bestelling klopt.",
                "Je nummer schakelt door naar de AI. Binnen maximaal 10 dagen live."]),
        ("h2", "Vergelijk en lees meer"),
        ("p", "Hoe Conveasy zich verhoudt tot reservatie-assistenten, telefooncentrales met AI en zelfbouwplatformen: [[be_compare|AI-telefoonassistenten voor restaurants in België vergeleken]]."),
        ("qlinks",)],
    "faqs": [("Is Conveasy een Belgisch bedrijf?", "Conveasy is een product van Balloz Solutions LLC, een bedrijf in de Verenigde Staten. Het is gemaakt voor restaurants in België: het spreekt Nederlands en Frans, werkt op het eigen Belgische nummer van het restaurant en draait bij restaurants in Heusden-Zolder en Genk."),
             ("Werkt Conveasy met mijn kassa?", "Het werkt los van je kassa. Bestellingen gaan naar de keukenprinter en het keukenscherm, dus je hebt geen kassakoppeling nodig."),
             ("Voor welke restaurants is het?", "Voor afhaal- en leverzaken zoals frituren, pizzeria's, kebab- en burgerzaken, en voor restaurants die ook tafelreservaties aannemen. In België draait het bij Eatpoint en Eethuis Orient in Heusden-Zolder en City Food Lounge in Genk."),
             ("Kan het ook bestellingen via WhatsApp aannemen?", "Ja. De WhatsApp AI neemt bestellingen aan op het eigen WhatsApp-nummer van het restaurant, voor €99 per maand, met een betaallink voor leveringen.")],
},
"be_compare": {
    "slug": "ai-telefoonassistenten-restaurants-belgie-vergeleken", "nav": "Vergelijking",
    "title": "AI-telefoonassistenten voor restaurants in België vergeleken (2026) | Conveasy",
    "desc": "Welke AI-telefoonassistent past bij jouw restaurant in België? AI die bestellingen aanneemt, reservatie-assistenten, telefooncentrales met AI en zelfbouwplatformen, vergeleken op wat ze doen en voor wie.",
    "h1": "AI-telefoonassistenten voor restaurants in België vergeleken",
    "lead": "Niet elke AI-telefoonassistent doet hetzelfde. Sommige boeken tafels, andere zijn een telefooncentrale met AI erbij of een platform om zelf een agent te bouwen, en enkele nemen volledige bestellingen aan. Hier zie je de soorten, de aanbieders die je in België tegenkomt en waarvoor elk het best past.",
    "note": "Opgesteld door Conveasy. De gegevens over andere aanbieders komen van hun eigen websites of uit de pers over hen, nagekeken op {date}.",
    "blocks": [
        ("h2", "Bepaal eerst wat de AI moet doen"),
        ("ul", ["Bestellingen of reservaties? Een bestelling met formaten, sauzen en een leveradres aannemen is iets anders dan een tafel boeken.",
                "Je kassa: sommige assistenten werken in een reservatiesysteem of koppelen met een kassa, andere werken op zichzelf.",
                "Talen: in België bellen klanten in het Nederlands en Frans, en vaak ook in het Engels of Turks.",
                "Prijs: staat die online, en is het per minuut, per gebruiker of per maand?"]),
        ("h2", "De vier soorten in één oogopslag"),
        ("table", ["Soort", "Voorbeelden", "Wat het doet", "Past bij"],
         [["AI die bestellingen aanneemt voor restaurants", "Conveasy, fonio.ai", "Neemt de volledige telefonische bestelling aan uit je menu en stuurt ze naar de keuken", "Afhaal- en leverzaken"],
          ["Reservatie-assistent", "Zenchef Call AI, HorecaHub.ai", "Neemt oproepen aan en boekt tafels in een reservatiesysteem", "Restaurants met tafels die reservatiesoftware gebruiken"],
          ["Telefooncentrale met AI", "CloudTalk, Dstny", "Een zakelijke telefooncentrale met een AI-stemagent of voicebot erbij", "Bedrijven die één telefoonsysteem voor een team willen"],
          ["Platform om zelf te bouwen", "Retell AI, Famulor, Jotform", "Tools om je eigen voice-agent te bouwen en te laten draaien", "Teams of bureaus die de agent zelf bouwen en onderhouden"]]),
        ("h2", "De aanbieders"),
        ("providers", [
            ("Conveasy", "AI voor telefonische en WhatsApp-bestellingen bij restaurants. Neemt de volledige bestelling aan met het menu, de prijzen en de leverzones van het restaurant, print ze in de keuken en werkt zonder kassakoppeling. Telefoon-AI vanaf €249 per maand voor 500 minuten. Live bij restaurants in Heusden-Zolder en Genk.", "[[phone]]"),
            ("Zenchef Call AI", "Neemt 24/7 op en noteert reservaties rechtstreeks in de software van Zenchef.", "https://www.zenchef.com/be-nl/call-ai"),
            ("fonio.ai", "Een AI-telefoonassistent voor de horeca die afhaal- en telefonische bestellingen aanneemt, bellers door de menukaart loodst en de bestelling doorstuurt naar de keuken of het kassasysteem.", "https://www.fonio.ai/nl/ai-telefoonassistent/ai-telefoonassistent-horeca/"),
            ("HorecaHub.ai", "Een AI-telefoonreceptionist voor restaurants die vragen beantwoordt en reservaties rechtstreeks in het reservatiesysteem zet.", "https://horecahub.ai/en/blog/ai-telefonist-restaurant"),
            ("Retell AI", "Een platform voor AI-stemagenten. De restaurantagent neemt de telefoon op, neemt bestellingen aan, plant reservaties in en beantwoordt menuvragen, en kan gekoppeld worden aan de kassa. Betalen per gebruik.", "https://www.retellai.com/nl/use-cases/ai-voice-agent-for-restaurants"),
            ("CloudTalk", "Een zakelijke telefooncentrale met een AI-stemagent, dialers en 100+ integraties, vanaf €25 per gebruiker per maand zonder de AI-add-ons.", "https://www.cloudtalk.io/nl/blog/beste-ai-belsoftware-voor-het-mkb/"),
            ("Famulor", "Een no-codeplatform voor AI-telefoon- en WhatsApp-assistenten, livechat en Messenger, voor restaurants en andere sectoren.", "https://www.famulor.io/nl/industries/restaurants"),
            ("Jotform AI Agents", "Een bouwer voor AI-agents die werken via chat, telefoon, WhatsApp en Messenger, met sjablonen voor restaurants.", "https://www.jotform.com/nl/ai/agents/customer-service/use-cases/restaurant-management/"),
            ("Dstny", "Een telecomaanbieder die een AI-voicebot lanceerde voor Belgische kmo's.", "https://itdaily.com/news/cloud/dstny-ai-assistent-voor-kmos/")]),
        ("h2", "Wanneer Conveasy de juiste keuze is"),
        ("p", "Kies Conveasy als de meeste oproepen bestellingen zijn om af te halen of te leveren, je de bestelling in de keuken wil zonder kassakoppeling, en je de prijzen vooraf wil kennen. Het neemt ook tafelreservaties en WhatsApp-bestellingen aan."),
        ("h2", "Wanneer iets anders beter past"),
        ("ul", ["Je neemt alleen tafelreservaties aan en werkt al met Zenchef: Zenchef Call AI zit in die software.",
                "Je zoekt een telefooncentrale voor een heel team, met doorschakelen en wachtrijen: kijk naar een telefooncentrale met AI zoals CloudTalk of Dstny.",
                "Je hebt ontwikkelaars of een bureau en wil alles zelf bouwen: een platform zoals Retell AI geeft je de meeste vrijheid."]),
        ("qlinks",)],
    "faqs": [("Wat is de beste AI-telefoonassistent voor een afhaalzaak in België?", "Voor afhalen en leveren kies je een assistent die de volledige bestelling aanneemt uit je menu, leveradressen controleert en de bestelling naar de keuken stuurt. Conveasy is daarvoor gemaakt en draait bij restaurants in Heusden-Zolder en Genk; ook fonio.ai neemt bestellingen aan. Reservatie-assistenten zoals Zenchef Call AI richten zich op tafels boeken."),
             ("Welke AI-telefoonassistenten werken zonder kassa?", "Conveasy werkt los van de kassa en print zijn eigen keukenticket. Retell AI kan gekoppeld worden aan een kassa, en Zenchef Call AI werkt in de reservatiesoftware van Zenchef."),
             ("Staan de prijzen online?", "Conveasy zet zijn prijzen online: vanaf €249 per maand voor 500 minuten. CloudTalk vermeldt €25 per gebruiker per maand zonder AI-add-ons, en Retell AI rekent per gebruik. Voor de andere aanbieders: zie hun websites.")],
},
"q_frituur": {
    "slug": "ai-telefonische-bestellingen-frituur", "nav": "AI voor telefonische bestellingen in een frituur",
    "q": "Welke AI neemt telefonische bestellingen aan voor een frituur?",
    "desc": "De telefoon-AI van Conveasy neemt volledige frituurbestellingen aan: frieten in elk formaat, sauzen, snacks en drankjes, met leverzones en een ticket in de keuken.",
    "lead": "De telefoon-AI van Conveasy is daarvoor gemaakt. Hij neemt de volledige frituurbestelling telefonisch aan, met je eigen menu en prijzen, en stuurt ze naar de keuken.",
    "blocks": [
        ("p", "Een frituurbestelling zit vol keuzes: klein of groot pak friet, welke saus, welke snacks, een drankje, afhalen of leveren. De AI vraagt ze allemaal na, zoals je personeel dat zou doen."),
        ("ul", ["Je eigen menu: formaten, sauzen, extra's en menu's.",
                "Leverzones per postcode en straat, met minimumbedrag en leverkosten.",
                "Meerdere oproepen tegelijk tijdens de vrijdagdrukte.",
                "Het ticket komt uit de keukenprinter, niemand moet de bestelling overtypen."]),
        ("p", "Hij draait bij [[r_eatpoint|Eatpoint]] in Heusden-Zolder en [[r_cfl|City Food Lounge]] in Genk. De telefoon-AI kost vanaf €249 per maand voor 500 minuten. Meer op de [[frituur|pagina voor frituren]]."),
        ("qlinks",)],
},
"q_cost": {
    "slug": "wat-kost-een-ai-telefoon-restaurant", "nav": "Wat een AI-telefoon kost",
    "q": "Wat kost een AI-telefoonassistent voor een restaurant in België?",
    "desc": "De telefoon-AI van Conveasy kost €249 per maand voor 500 minuten, €449 voor 1.000 of €799 voor 2.000, plus €299 opstart. Geen commissie op bestellingen.",
    "lead": "Bij Conveasy kost de telefoon-AI €249 per maand voor 500 minuten, €449 voor 1.000 minuten of €799 voor 2.000 minuten, plus eenmalig €299 opstartkosten.",
    "blocks": [
        ("p", "Er is geen commissie op bestellingen: de prijs blijft dezelfde, hoeveel je ook verkoopt. Raken je minuten op, dan stap je over naar een groter pakket."),
        ("ul", ["WhatsApp AI: €99 per maand.",
                "Webshop met QR-bestellen: €79 per maand, 0% commissie.",
                "Opstart: €299 voor de telefoon-AI, €199 per ander kanaal, €399 voor telefoon-AI, WhatsApp AI, webshop en kiosk samen."]),
        ("p", "Alle prijzen staan op de [[pricing|prijzenpagina]]. De [[calculator|commissiecalculator]] toont wat je overhoudt tegenover bestelplatformen."),
        ("qlinks",)],
},
"q_pos": {
    "slug": "ai-telefoon-zonder-kassasysteem", "nav": "AI-telefoon zonder kassasysteem",
    "q": "Heb ik een kassasysteem nodig voor een AI-telefoonassistent?",
    "desc": "Nee. De telefoon-AI van Conveasy werkt los van je kassa: bestellingen gaan naar de keukenprinter en het keukenscherm, zonder kassakoppeling.",
    "lead": "Niet bij Conveasy. De telefoon-AI werkt los van je kassa: elke bestelling gaat naar de keukenprinter en het keukenscherm, zonder kassakoppeling.",
    "blocks": [
        ("p", "Veel spraakassistenten hangen vast aan andere software: reservatie-assistenten boeken tafels in een reservatiesysteem, en sommige platformen worden gekoppeld aan de kassa. Handig als je die software al hebt, maar extra werk en kosten als dat niet zo is."),
        ("p", "Conveasy heeft een eigen kopie van je menu. Pas je een prijs aan of zet je een product op uitverkocht, dan weet de AI het meteen. Je kassa blijft zoals ze is."),
        ("qlinks",)],
},
"q_langs": {
    "slug": "ai-telefoon-nederlands-frans-turks", "nav": "AI-telefoon in het Nederlands, Frans en Turks",
    "q": "Kan een AI de telefoon opnemen in het Nederlands, Frans en Turks?",
    "desc": "Ja. De telefoon-AI van Conveasy antwoordt in de taal van de beller: Nederlands, Frans, Engels, Turks en 60+ andere talen.",
    "lead": "Ja. De telefoon-AI van Conveasy spreekt de taal van de beller: Nederlands, Frans, Engels, Turks en 60+ andere talen.",
    "blocks": [
        ("p", "In België krijgt een restaurant oproepen in meer dan één taal. De AI antwoordt in de taal van de beller en neemt de bestelling in die taal aan."),
        ("p", "De restaurants in Limburg die hem gebruiken, nemen oproepen aan in het Nederlands, Turks en Engels. Het ticket in de keuken staat altijd in de taal van het restaurant."),
        ("qlinks",)],
},
"q_calls": {
    "slug": "veel-oproepen-tegelijk-restaurant", "nav": "Veel oproepen tegelijk",
    "q": "Wat gebeurt er als veel klanten tegelijk naar een restaurant bellen?",
    "desc": "Met Conveasy wordt elke oproep meteen opgenomen: de telefoon-AI neemt 50+ oproepen tegelijk aan, dus niemand hoort in gesprek tijdens de drukte.",
    "lead": "Met Conveasy wordt elke beller meteen geholpen: de telefoon-AI neemt 50+ oproepen tegelijk aan.",
    "blocks": [
        ("p", "Op vrijdag- of zaterdagavond gaat de telefoon vaker dan het personeel kan opnemen. Wie in gesprek hoort of te lang moet wachten, bestelt vaak ergens anders of via een bestelapp."),
        ("p", "De AI neemt elke oproep op, noteert elke bestelling apart en stuurt ze een voor een naar de keuken. Wie ophangt zonder te bestellen, krijgt een WhatsApp-bericht om alsnog te bestellen."),
        ("qlinks",)],
},
"q_whatsapp": {
    "slug": "whatsapp-bestellingen-ai-restaurant", "nav": "WhatsApp-bestellingen met AI",
    "q": "Kan een AI bestellingen via WhatsApp aannemen?",
    "desc": "Ja. De WhatsApp AI van Conveasy neemt bestellingen aan op het eigen WhatsApp-nummer van het restaurant, rekent het totaal uit en stuurt een betaallink voor leveringen. €99 per maand.",
    "lead": "Ja. De WhatsApp AI van Conveasy neemt bestellingen aan in de chat, op het eigen WhatsApp-nummer van het restaurant, en stuurt ze naar de keuken.",
    "blocks": [
        ("ul", ["Klanten typen hun bestelling in hun eigen woorden; de AI vraagt naar formaten, sauzen en extra's.",
                "Hij rekent het totaal, de leverkosten en het minimumbedrag voor het adres uit.",
                "De klant bevestigt met een knop; leveringen kunnen betaald worden met een betaallink (ook Klarna en maaltijdcheques).",
                "Tafelreservaties kunnen in de chat geboekt, gewijzigd en geannuleerd worden."]),
        ("p", "De WhatsApp AI kost €99 per maand. [[r_eatpoint|Eatpoint]] en [[r_orient|Eethuis Orient]] in Heusden-Zolder nemen zo WhatsApp-bestellingen aan. Meer op de [[whatsapp|pagina over de WhatsApp AI]]."),
        ("qlinks",)],
},
"q_setup": {
    "slug": "hoe-snel-ai-telefoon-restaurant", "nav": "Hoe snel het klaarstaat",
    "q": "Hoe snel staat een AI-telefoonassistent klaar in een restaurant?",
    "desc": "Een restaurant is binnen maximaal 10 dagen live met de telefoon-AI van Conveasy: menu, prijzen, leverzones en testoproepen, en het houdt zijn eigen nummer.",
    "lead": "Met Conveasy is een restaurant binnen maximaal 10 dagen live, en het houdt zijn eigen telefoonnummer.",
    "blocks": [
        ("ol", ["Demo: je belt zelf naar de AI en hoort hoe hij een bestelling aanneemt.",
                "Menu: wij zetten je producten, formaten, sauzen, prijzen en openingsuren erin.",
                "Levering: je leverzones per postcode en straat, met minimumbedragen en leverkosten.",
                "Testen: we doen samen testoproepen tot elke bestelling klopt.",
                "Live: je nummer schakelt door naar de AI en de bestellingen komen uit je keukenprinter."]),
        ("p", "Vraag een demo aan op de [[contact|contactpagina]]."),
        ("qlinks",)],
},
"q_reservations": {
    "slug": "ai-tafelreservaties-telefoon", "nav": "Tafelreservaties met AI",
    "q": "Kan een AI tafelreservaties aannemen via de telefoon?",
    "desc": "Ja. De telefoon-AI en de WhatsApp AI van Conveasy nemen 24/7 tafelreservaties aan, inbegrepen in de prijs.",
    "lead": "Ja. De telefoon-AI en de WhatsApp AI van Conveasy nemen 24/7 tafelreservaties aan, zonder meerkost.",
    "blocks": [
        ("p", "De AI vraagt naam, datum, uur en aantal personen en zet de reservatie in het dashboard. Via WhatsApp kunnen gasten hun reservatie ook wijzigen of annuleren."),
        ("p", "Anders dan een assistent die alleen reservaties doet, neemt dezelfde AI ook bestellingen aan om af te halen en te leveren."),
        ("qlinks",)],
},
}

T["fr"] = {
"be_voice": {
    "slug": "ia-vocale-restaurants-belgique", "nav": "IA vocale en Belgique",
    "title": "IA vocale pour restaurants en Belgique : une IA qui prend les commandes par téléphone | Conveasy",
    "desc": "Conveasy est l'IA vocale des restaurants en Belgique : un assistant téléphonique IA qui répond à chaque appel, prend la commande complète avec votre carte et vos zones de livraison et l'envoie en cuisine. Sans liaison avec la caisse, dès 249 € par mois.",
    "h1": "IA vocale pour restaurants en Belgique",
    "lead": "Conveasy répond au téléphone de votre restaurant avec l'IA. Il prend la commande complète avec votre carte, vos prix et vos zones de livraison, et l'envoie directement en cuisine. Conçu pour les restaurants à emporter et en livraison en Belgique, et déjà actif dans des restaurants du Limbourg.",
    "blocks": [
        ("h2", "Ce que fait l'IA téléphonique de Conveasy"),
        ("ul", ["Répond à chaque appel tout de suite, même au rush du vendredi : plus de 50 appels en même temps, jamais occupé.",
                "Prend la commande complète : produits, tailles, sauces, suppléments et boissons, avec vos propres prix.",
                "Vérifie l'adresse de livraison avec vos zones de livraison et votre liste de rues, avec le minimum de commande et les frais de livraison.",
                "Envoie la commande à l'imprimante et à l'écran de la cuisine, avec l'heure de retrait ou de livraison.",
                "Reconnaît les clients habituels à leur numéro : nom, adresse et dernière commande.",
                "Prend les réservations de table, 24 h/24 et 7 j/7.",
                "Transfère l'appel à votre personnel quand le client demande à parler à quelqu'un.",
                "En dehors des heures d'ouverture, indique quand vous rouvrez."]),
        ("h2", "Pas un standard, pas un module de réservation"),
        ("p", "La plupart des IA vocales pour restaurants font un autre travail. Les standardistes IA répondent aux questions et transmettent des messages. Les assistants de réservation réservent des tables dans un logiciel de réservation. Les plateformes vous laissent construire votre propre agent, si vous en avez le temps ou une agence. Conveasy est fait pour l'appel où quelqu'un veut commander à manger : il connaît votre carte, pose les bonnes questions (quelle taille, quelle sauce, à emporter ou en livraison), calcule le total et envoie la commande en cuisine."),
        ("p", "Il fonctionne indépendamment de votre caisse, donc sans liaison avec la caisse, et vous gardez votre propre numéro."),
        ("h2", "Conçu pour la Belgique"),
        ("ul", ["Parle la langue de l'appelant : néerlandais, français, anglais, turc et plus de 60 autres langues.",
                "Fonctionne sur le numéro belge du restaurant.",
                "Zones de livraison par code postal et par rue, à partir des listes officielles de rues.",
                "Paiement en ligne sur la boutique avec notamment Bancontact, Klarna et les chèques-repas.",
                "Actif chez [[r_eatpoint|Eatpoint]] et [[r_orient|Eethuis Orient]] à Heusden-Zolder et chez [[r_cfl|City Food Lounge]] à Genk."]),
        ("h2", "Prix"),
        ("p", "L'IA téléphonique coûte 249 € par mois pour 500 minutes, 449 € pour 1 000 minutes ou 799 € pour 2 000 minutes, plus des frais de mise en route uniques de 299 €. Aucune commission sur les commandes. L'IA WhatsApp coûte 99 € par mois. Tous les prix sur la [[pricing|page des tarifs]]."),
        ("h2", "Comment démarrer"),
        ("ol", ["Demandez une démo et écoutez l'IA prendre une commande.",
                "Nous encodons votre carte, vos prix, vos zones de livraison et vos horaires.",
                "Nous faisons ensemble des appels de test jusqu'à ce que chaque commande soit juste.",
                "Votre numéro est renvoyé vers l'IA. En ligne en 10 jours maximum."]),
        ("h2", "Comparer et en savoir plus"),
        ("p", "Comment Conveasy se compare aux assistants de réservation, aux centraux téléphoniques avec IA et aux plateformes à construire soi-même : [[be_compare|les assistants téléphoniques IA pour restaurants en Belgique comparés]]."),
        ("qlinks",)],
    "faqs": [("Conveasy est-il une entreprise belge ?", "Conveasy est un produit de Balloz Solutions LLC, une entreprise des États-Unis. Il est conçu pour les restaurants en Belgique : il parle néerlandais et français, fonctionne sur le numéro belge du restaurant et tourne dans des restaurants à Heusden-Zolder et à Genk."),
             ("Conveasy fonctionne-t-il avec ma caisse ?", "Il fonctionne indépendamment de votre caisse. Les commandes arrivent sur l'imprimante et l'écran de la cuisine, sans liaison avec la caisse."),
             ("Pour quels restaurants ?", "Pour les restaurants à emporter et en livraison comme les friteries, pizzerias, kebabs et burgers, et pour les restaurants qui prennent aussi des réservations de table. En Belgique, il tourne chez Eatpoint et Eethuis Orient à Heusden-Zolder et chez City Food Lounge à Genk."),
             ("Peut-il aussi prendre les commandes sur WhatsApp ?", "Oui. L'IA WhatsApp prend les commandes sur le numéro WhatsApp du restaurant pour 99 € par mois, avec un lien de paiement pour les livraisons.")],
},
"be_compare": {
    "slug": "assistants-telephoniques-ia-restaurants-belgique-comparatif", "nav": "Comparatif",
    "title": "Assistants téléphoniques IA pour restaurants en Belgique : comparatif 2026 | Conveasy",
    "desc": "Quel assistant téléphonique IA convient à votre restaurant en Belgique ? IA de prise de commande, assistants de réservation, centraux téléphoniques avec IA et plateformes à construire soi-même, comparés selon ce qu'ils font et pour qui.",
    "h1": "Assistants téléphoniques IA pour restaurants en Belgique : le comparatif",
    "lead": "Tous les assistants téléphoniques IA ne font pas le même travail. Certains réservent des tables, d'autres sont un central téléphonique avec de l'IA en plus ou une plateforme pour construire son propre agent, et quelques-uns prennent des commandes complètes. Voici les types, les fournisseurs que vous rencontrerez en Belgique et à quoi chacun convient le mieux.",
    "note": "Rédigé par Conveasy. Les informations sur les autres fournisseurs viennent de leurs propres sites ou de la presse à leur sujet, vérifiées le {date}.",
    "blocks": [
        ("h2", "Décidez d'abord ce que l'IA doit faire"),
        ("ul", ["Commandes ou réservations ? Prendre une commande avec tailles, sauces et adresse de livraison, ce n'est pas la même chose que réserver une table.",
                "Votre caisse : certains assistants fonctionnent dans un logiciel de réservation ou se relient à une caisse, d'autres fonctionnent seuls.",
                "Langues : en Belgique, les clients appellent en néerlandais et en français, et souvent en anglais ou en turc.",
                "Prix : est-il publié, et est-ce par minute, par utilisateur ou par mois ?"]),
        ("h2", "Les quatre types en un coup d'œil"),
        ("table", ["Type", "Exemples", "Ce qu'il fait", "Convient à"],
         [["IA de prise de commande pour restaurants", "Conveasy, fonio.ai", "Prend la commande téléphonique complète à partir de votre carte et l'envoie en cuisine", "Restaurants à emporter et en livraison"],
          ["Assistant de réservation", "Zenchef Call AI, HorecaHub.ai", "Répond aux appels et réserve des tables dans un logiciel de réservation", "Restaurants avec salle qui utilisent un logiciel de réservation"],
          ["Central téléphonique avec IA", "CloudTalk, Dstny", "Un central téléphonique professionnel auquel s'ajoute un agent vocal IA ou un voicebot", "Entreprises qui veulent un seul système téléphonique pour une équipe"],
          ["Plateforme à construire soi-même", "Retell AI, Famulor, Jotform", "Des outils pour construire et faire tourner votre propre agent vocal", "Équipes ou agences qui construisent et entretiennent l'agent elles-mêmes"]]),
        ("h2", "Les fournisseurs"),
        ("providers", [
            ("Conveasy", "Prise de commande par téléphone et WhatsApp avec l'IA, pour les restaurants. Prend la commande complète avec la carte, les prix et les zones de livraison du restaurant, l'imprime en cuisine et fonctionne sans liaison avec la caisse. IA téléphonique dès 249 € par mois pour 500 minutes. Actif dans des restaurants à Heusden-Zolder et à Genk.", "[[phone]]"),
            ("Zenchef Call AI", "Décroche 24 h/24 et 7 j/7 et enregistre les réservations directement dans le logiciel Zenchef.", "https://www.zenchef.com/be-nl/call-ai"),
            ("fonio.ai", "Un assistant téléphonique IA pour l'horeca qui prend les commandes à emporter et par téléphone, guide l'appelant dans la carte et transmet la commande à la cuisine ou à la caisse.", "https://www.fonio.ai/nl/ai-telefoonassistent/ai-telefoonassistent-horeca/"),
            ("HorecaHub.ai", "Un standardiste téléphonique IA pour restaurants qui répond aux questions et enregistre les réservations directement dans le système de réservation.", "https://horecahub.ai/en/blog/ai-telefonist-restaurant"),
            ("Retell AI", "Une plateforme d'agents vocaux IA. Son agent pour restaurants répond au téléphone, prend les commandes et les réservations et répond aux questions sur la carte, et peut être relié à la caisse. Paiement à l'usage.", "https://www.retellai.com/nl/use-cases/ai-voice-agent-for-restaurants"),
            ("CloudTalk", "Un central téléphonique professionnel avec un agent vocal IA, des dialers et plus de 100 intégrations, dès 25 € par utilisateur et par mois hors options IA.", "https://www.cloudtalk.io/nl/blog/beste-ai-belsoftware-voor-het-mkb/"),
            ("Famulor", "Une plateforme no-code d'assistants IA pour le téléphone et WhatsApp, le chat en direct et Messenger, pour les restaurants et d'autres secteurs.", "https://www.famulor.io/nl/industries/restaurants"),
            ("Jotform AI Agents", "Un outil pour créer des agents IA qui fonctionnent par chat, téléphone, WhatsApp et Messenger, avec des modèles pour restaurants.", "https://www.jotform.com/nl/ai/agents/customer-service/use-cases/restaurant-management/"),
            ("Dstny", "Un opérateur télécom qui a lancé un voicebot IA pour les PME belges.", "https://itdaily.com/news/cloud/dstny-ai-assistent-voor-kmos/")]),
        ("h2", "Quand Conveasy est le bon choix"),
        ("p", "Choisissez Conveasy si la plupart de vos appels sont des commandes à emporter ou en livraison, si vous voulez la commande en cuisine sans liaison avec la caisse, et si vous voulez des prix publiés. Il prend aussi les réservations de table et les commandes WhatsApp."),
        ("h2", "Quand une autre option convient mieux"),
        ("ul", ["Vous ne prenez que des réservations de table et utilisez déjà Zenchef : Zenchef Call AI fonctionne dans ce logiciel.",
                "Vous cherchez un central téléphonique pour toute une équipe, avec renvois et files d'attente : regardez un central avec IA comme CloudTalk ou Dstny.",
                "Vous avez des développeurs ou une agence et voulez tout construire vous-même : une plateforme comme Retell AI vous donne le plus de liberté."]),
        ("qlinks",)],
    "faqs": [("Quel est le meilleur assistant téléphonique IA pour un restaurant à emporter en Belgique ?", "Pour l'emporter et la livraison, choisissez un assistant qui prend la commande complète à partir de votre carte, vérifie les adresses de livraison et envoie la commande en cuisine. Conveasy est fait pour cela et tourne dans des restaurants à Heusden-Zolder et à Genk ; fonio.ai prend aussi des commandes. Les assistants de réservation comme Zenchef Call AI se concentrent sur les tables."),
             ("Quels assistants téléphoniques IA fonctionnent sans caisse ?", "Conveasy fonctionne indépendamment de la caisse et imprime son propre ticket de cuisine. Retell AI peut être relié à une caisse, et Zenchef Call AI fonctionne dans le logiciel de réservation de Zenchef."),
             ("Les prix sont-ils publiés ?", "Conveasy publie ses prix : dès 249 € par mois pour 500 minutes. CloudTalk indique 25 € par utilisateur et par mois hors options IA, et Retell AI facture à l'usage. Pour les autres, voyez leurs sites.")],
},
"q_frituur": {
    "slug": "ia-commandes-telephone-friterie", "nav": "IA pour les commandes par téléphone d'une friterie",
    "q": "Quelle IA prend les commandes par téléphone pour une friterie ?",
    "desc": "L'IA téléphonique de Conveasy prend les commandes complètes d'une friterie : frites de toutes tailles, sauces, snacks et boissons, avec zones de livraison et ticket en cuisine.",
    "lead": "L'IA téléphonique de Conveasy est faite pour cela. Elle prend la commande complète de la friterie par téléphone, avec votre carte et vos prix, et l'envoie en cuisine.",
    "blocks": [
        ("p", "Une commande de friterie est pleine de choix : petit ou grand cornet, quelle sauce, quels snacks, une boisson, à emporter ou en livraison. L'IA demande tout cela, comme le ferait votre personnel."),
        ("ul", ["Votre propre carte : tailles, sauces, suppléments et menus.",
                "Zones de livraison par code postal et par rue, avec minimum de commande et frais de livraison.",
                "Plusieurs appels en même temps pendant le rush du vendredi.",
                "Le ticket sort de l'imprimante de la cuisine : personne ne doit retaper la commande."]),
        ("p", "Elle tourne chez [[r_eatpoint|Eatpoint]] à Heusden-Zolder et chez [[r_cfl|City Food Lounge]] à Genk. L'IA téléphonique coûte dès 249 € par mois pour 500 minutes. Plus d'infos sur la [[frituur|page pour les friteries]]."),
        ("qlinks",)],
},
"q_cost": {
    "slug": "prix-assistant-telephonique-ia-restaurant", "nav": "Le prix d'un téléphone IA",
    "q": "Combien coûte un assistant téléphonique IA pour un restaurant en Belgique ?",
    "desc": "L'IA téléphonique de Conveasy coûte 249 € par mois pour 500 minutes, 449 € pour 1 000 ou 799 € pour 2 000, plus 299 € de mise en route. Aucune commission sur les commandes.",
    "lead": "Chez Conveasy, l'IA téléphonique coûte 249 € par mois pour 500 minutes, 449 € pour 1 000 minutes ou 799 € pour 2 000 minutes, plus des frais de mise en route uniques de 299 €.",
    "blocks": [
        ("p", "Aucune commission sur les commandes : le prix reste le même, quel que soit votre chiffre. Quand vos minutes sont épuisées, vous passez à un forfait plus grand."),
        ("ul", ["IA WhatsApp : 99 € par mois.",
                "Boutique en ligne avec commande par QR : 79 € par mois, 0 % de commission.",
                "Mise en route : 299 € pour l'IA téléphonique, 199 € par autre canal, 399 € pour l'IA téléphonique, l'IA WhatsApp, la boutique et la borne ensemble."]),
        ("p", "Tous les prix sont sur la [[pricing|page des tarifs]]. Le [[calculator|calculateur de commissions]] montre ce que vous gardez par rapport aux plateformes de commande."),
        ("qlinks",)],
},
"q_pos": {
    "slug": "telephone-ia-sans-caisse", "nav": "Téléphone IA sans caisse",
    "q": "Faut-il un système de caisse pour utiliser un assistant téléphonique IA ?",
    "desc": "Non. L'IA téléphonique de Conveasy fonctionne indépendamment de votre caisse : les commandes arrivent sur l'imprimante et l'écran de la cuisine, sans liaison avec la caisse.",
    "lead": "Pas avec Conveasy. L'IA téléphonique fonctionne indépendamment de votre caisse : chaque commande arrive sur l'imprimante et l'écran de la cuisine, sans liaison avec la caisse.",
    "blocks": [
        ("p", "Beaucoup d'assistants vocaux dépendent d'un autre logiciel : les assistants de réservation réservent dans un logiciel de réservation, et certaines plateformes sont reliées à la caisse. C'est pratique si vous avez déjà ce logiciel, mais c'est du travail et des frais en plus sinon."),
        ("p", "Conveasy a sa propre copie de votre carte. Quand vous changez un prix ou mettez un produit en rupture, l'IA le sait tout de suite. Votre caisse reste comme elle est."),
        ("qlinks",)],
},
"q_langs": {
    "slug": "telephone-ia-neerlandais-francais-turc", "nav": "Téléphone IA en néerlandais, français et turc",
    "q": "Une IA peut-elle répondre au téléphone en néerlandais, en français et en turc ?",
    "desc": "Oui. L'IA téléphonique de Conveasy répond dans la langue de l'appelant : néerlandais, français, anglais, turc et plus de 60 autres langues.",
    "lead": "Oui. L'IA téléphonique de Conveasy parle la langue de l'appelant : néerlandais, français, anglais, turc et plus de 60 autres langues.",
    "blocks": [
        ("p", "En Belgique, un restaurant reçoit des appels dans plus d'une langue. L'IA répond dans la langue de l'appelant et prend la commande dans cette langue."),
        ("p", "Les restaurants du Limbourg qui l'utilisent prennent les appels en néerlandais, en turc et en anglais. Le ticket en cuisine est toujours dans la langue du restaurant."),
        ("qlinks",)],
},
"q_calls": {
    "slug": "beaucoup-appels-en-meme-temps-restaurant", "nav": "Beaucoup d'appels en même temps",
    "q": "Que se passe-t-il quand beaucoup de clients appellent un restaurant en même temps ?",
    "desc": "Avec Conveasy, chaque appel est pris tout de suite : l'IA téléphonique gère plus de 50 appels en même temps, personne n'entend la tonalité occupée pendant le rush.",
    "lead": "Avec Conveasy, chaque appelant est servi tout de suite : l'IA téléphonique gère plus de 50 appels en même temps.",
    "blocks": [
        ("p", "Le vendredi ou le samedi soir, le téléphone sonne plus souvent que le personnel ne peut décrocher. Ceux qui tombent sur la tonalité occupée ou attendent trop longtemps commandent souvent ailleurs ou sur une application de livraison."),
        ("p", "L'IA prend chaque appel, note chaque commande séparément et les envoie une par une en cuisine. Ceux qui raccrochent sans commander reçoivent un message WhatsApp pour commander quand même."),
        ("qlinks",)],
},
"q_whatsapp": {
    "slug": "commandes-whatsapp-ia-restaurant", "nav": "Commandes WhatsApp avec l'IA",
    "q": "Une IA peut-elle prendre les commandes d'un restaurant sur WhatsApp ?",
    "desc": "Oui. L'IA WhatsApp de Conveasy prend les commandes sur le numéro WhatsApp du restaurant, calcule le total et envoie un lien de paiement pour les livraisons. 99 € par mois.",
    "lead": "Oui. L'IA WhatsApp de Conveasy prend les commandes dans la conversation, sur le numéro WhatsApp du restaurant, et les envoie en cuisine.",
    "blocks": [
        ("ul", ["Les clients écrivent leur commande avec leurs propres mots ; l'IA demande les tailles, les sauces et les suppléments.",
                "Elle calcule le total, les frais de livraison et le minimum de commande pour l'adresse.",
                "Le client confirme avec un bouton ; les livraisons se paient avec un lien de paiement (Klarna et chèques-repas compris).",
                "Les réservations de table peuvent être prises, modifiées et annulées dans la conversation."]),
        ("p", "L'IA WhatsApp coûte 99 € par mois. [[r_eatpoint|Eatpoint]] et [[r_orient|Eethuis Orient]] à Heusden-Zolder prennent ainsi les commandes WhatsApp. Plus d'infos sur la [[whatsapp|page de l'IA WhatsApp]]."),
        ("qlinks",)],
},
"q_setup": {
    "slug": "installation-telephone-ia-restaurant", "nav": "Le délai de mise en route",
    "q": "En combien de temps un assistant téléphonique IA est-il prêt dans un restaurant ?",
    "desc": "Un restaurant est en ligne avec l'IA téléphonique de Conveasy en 10 jours maximum : carte, prix, zones de livraison et appels de test, et il garde son propre numéro.",
    "lead": "Avec Conveasy, un restaurant est en ligne en 10 jours maximum, et il garde son propre numéro de téléphone.",
    "blocks": [
        ("ol", ["Démo : vous appelez vous-même l'IA et l'écoutez prendre une commande.",
                "Carte : nous encodons vos produits, tailles, sauces, prix et horaires.",
                "Livraison : vos zones de livraison par code postal et par rue, avec minimums de commande et frais de livraison.",
                "Tests : nous faisons ensemble des appels de test jusqu'à ce que chaque commande soit juste.",
                "En ligne : votre numéro est renvoyé vers l'IA et les commandes sortent de l'imprimante de votre cuisine."]),
        ("p", "Demandez une démo sur la [[contact|page de contact]]."),
        ("qlinks",)],
},
"q_reservations": {
    "slug": "reservations-table-ia-telephone", "nav": "Réservations de table avec l'IA",
    "q": "Une IA peut-elle prendre les réservations de table par téléphone ?",
    "desc": "Oui. L'IA téléphonique et l'IA WhatsApp de Conveasy prennent les réservations de table 24 h/24 et 7 j/7, comprises dans le prix.",
    "lead": "Oui. L'IA téléphonique et l'IA WhatsApp de Conveasy prennent les réservations de table 24 h/24 et 7 j/7, sans supplément.",
    "blocks": [
        ("p", "L'IA demande le nom, la date, l'heure et le nombre de personnes et place la réservation dans le tableau de bord. Sur WhatsApp, les clients peuvent aussi modifier ou annuler leur réservation."),
        ("p", "Contrairement à un assistant qui ne fait que des réservations, la même IA prend aussi les commandes à emporter et en livraison."),
        ("qlinks",)],
},
}

UIX = {
    "nl": {"questions": "Vragen over AI-telefoons voor restaurants", "demo": "Vraag een demo aan", "prices": "Bekijk de prijzen",
           "source": "Bron", "site_of": "Website", "checked": "Nagekeken op {date}."},
    "fr": {"questions": "Questions sur les téléphones IA pour restaurants", "demo": "Demander une démo", "prices": "Voir les tarifs",
           "source": "Source", "site_of": "Site", "checked": "Vérifié le {date}."},
    "en": {"questions": "Questions about AI phone assistants for restaurants", "demo": "Book a demo", "prices": "See the prices",
           "source": "Source", "site_of": "Website", "checked": "Checked on {date}."},
}

PAGE_LANGS = {pid: LANGS3 for pid in PIDS}

def slugs():
    return {pid: {l: T[l][pid]["slug"] for l in LANGS3} for pid in PIDS}

# ---------------------------------------------------------------- What build.py asks
LINK = re.compile(r"\[\[([a-z_]+)\|([^\]]+)\]\]")

def plain(text):
    return LINK.sub(lambda m: m.group(2), text)

def inline(g, lang, prefix, text):
    e, out, pos = g["e"], [], 0
    for m in LINK.finditer(text):
        out.append(e(text[pos:m.start()]))
        out.append(f'<a href="{prefix + g["path_of"](lang, m.group(1))}">{e(m.group(2))}</a>')
        pos = m.end()
    out.append(e(text[pos:]))
    return "".join(out)

def name(lang, pid):
    d = T[lang][pid]
    return d.get("nav") or d.get("q")

def meta(lang, pid):
    d = T[lang][pid]
    return (d["title"] if "title" in d else d["q"] + " | Conveasy"), d["desc"]

def nav(g, lang, prefix):
    """The footer link to the main page, in the languages it exists in."""
    if lang not in LANGS3: return ""
    return f'<li><a href="{prefix + g["path_of"](lang, "be_voice")}">{g["e"](T[lang]["be_voice"]["nav"])}</a></li>'

def blocks_html(g, lang, prefix, blocks, pid):
    e, out = g["e"], []
    for b in blocks:
        kind = b[0]
        if kind == "h2": out.append(f"<h2>{e(b[1])}</h2>")
        elif kind == "p": out.append(f"<p>{inline(g, lang, prefix, b[1])}</p>")
        elif kind in ("ul", "ol"): out.append(f"<{kind}>" + "".join(f"<li>{inline(g, lang, prefix, x)}</li>" for x in b[1]) + f"</{kind}>")
        elif kind == "table":
            head = "".join(f"<th scope=\"col\">{e(h)}</th>" for h in b[1])
            rows = "".join("<tr" + (' class="us"' if r[1].startswith("Conveasy") else "") + ">" + "".join(
                (f'<th scope="row">{e(c)}</th>' if i == 0 else f'<td data-label="{e(b[1][i])}">{e(c)}</td>') for i, c in enumerate(r)) + "</tr>" for r in b[2])
            out.append(f'<div class="cmp-wrap"><table class="cmp"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>')
        elif kind == "providers":
            items = []
            for pname, text, url in b[1]:
                if url.startswith("[["):
                    href, label = prefix + g["path_of"](lang, url.strip("[]")), "conveasy"
                    link = f'<a href="{href}">{e(UIX[lang]["site_of"])}: Conveasy</a>'
                else:
                    host = re.sub(r"^https?://(www\.)?", "", url).split("/")[0]
                    link = f'<a href="{e(url)}" rel="noopener nofollow">{e(UIX[lang]["source"])}: {e(host)}</a>'
                us = ' class="prov us"' if pname == "Conveasy" else ' class="prov"'
                items.append(f"<div{us}><h3>{e(pname)}</h3><p>{e(text)}</p><p class=\"prov-src\">{link}</p></div>")
            out.append('<div class="prov-list">' + "".join(items) + "</div>")
        elif kind == "qlinks":
            links = "".join(f'<li><a href="{prefix + g["path_of"](lang, q)}">{e(T[lang][q]["q"])}</a></li>' for q in Q_PIDS if q != pid)
            out.append(f'<h2>{e(UIX[lang]["questions"])}</h2><ul class="qa-list">{links}</ul>')
    return "".join(out)

def page(g, lang, pid, prefix):
    e, u, d = g["e"], g["UI"][lang], T[lang][pid]
    trail = [(u["home"], "home")]
    if pid != "be_voice": trail.append((T[lang]["be_voice"]["nav"], "be_voice"))
    h1 = d.get("h1") or d["q"]
    trail.append((d.get("nav") or h1, None))
    note = f'<p class="rest-checked">{e(d["note"].format(date=CHECKED[lang]))}</p>' if "note" in d else ""
    btns = (f'<div class="btn-row"><a class="btn btn-primary" href="{prefix + g["path_of"](lang, "contact")}">{e(UIX[lang]["demo"])}</a>'
            f'<a class="btn btn-ghost" href="{prefix + g["path_of"](lang, "pricing")}">{e(UIX[lang]["prices"])}</a></div>')
    hero = (f'<section class="hero"><div class="hero-bg" aria-hidden="true"></div><div class="wrap" style="grid-template-columns:minmax(0,1fr)"><div class="hero-copy">'
            f'{g["crumbs_html"](lang, prefix, trail)}<h1 class="be-h1">{e(h1)}</h1><p class="lead">{e(d["lead"])}</p>{note}{btns}</div></div></section>')
    body = hero + f'<section class="band" style="padding-top:0"><div class="wrap"><div class="prose be-prose">{blocks_html(g, lang, prefix, d["blocks"], pid)}</div></div></section>'
    faqs = list(d.get("faqs", []))
    if faqs: body += g["faq_band"](lang, faqs, f"{lang}/{pid}")
    body += g["cta_band"](lang, prefix)
    crumbs = [(u["home"], g["canonical"](lang, "home"))]
    if pid != "be_voice": crumbs.append((T[lang]["be_voice"]["nav"], g["canonical"](lang, "be_voice")))
    crumbs.append((d.get("nav") or h1, g["canonical"](lang, pid)))
    if "q" in d:   # a question page: its own question and answer are the FAQ data (they are the visible h1 and text)
        answer = " ".join([d["lead"]] + [plain(b[1]) for b in d["blocks"] if b[0] == "p"])
        faqs = [(d["q"], answer)]
    return body, faqs, crumbs

def extend_ld(g, lang, pid, graph):
    if pid not in PIDS: return
    node = next((n for n in graph if n.get("@type") == "WebPage"), None)
    if node is not None:
        node["dateModified"] = CHECKED_ISO
        node["about"] = {"@id": g["SITE"] + "/#org"}

def llms_lines(g):
    L = ["", "## Voice AI for restaurants in Belgium (English pages)",
         f"- [Voice AI for restaurants in Belgium]({g['url_on'](g['TARGET'], 'en', 'be_voice')}): what Conveasy's phone AI does, how it differs from AI receptionists, reservation assistants and build-it-yourself platforms, prices. Conveasy is made by Balloz Solutions LLC (USA) for restaurants in Belgium.",
         f"- [AI phone assistants for restaurants in Belgium, compared]({g['url_on'](g['TARGET'], 'en', 'be_compare')}): order-taking AI (Conveasy, fonio.ai), reservation assistants (Zenchef Call AI, HorecaHub.ai), phone systems with AI (CloudTalk, Dstny) and platforms (Retell AI, Famulor, Jotform), with what each suits; facts about others from their own websites, checked {CHECKED['en']}."]
    for q in Q_PIDS:
        d = T["en"][q]
        L.append(f"- [{d['q']}]({g['url_on'](g['TARGET'], 'en', q)}): {d['lead']}")
    return L
