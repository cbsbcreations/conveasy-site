"""Restaurants that take orders with Conveasy: a public directory on conveasy.be and conveasy.ai.

One hub page (pid "restaurants") and one page per restaurant (pid "r_<id>"), in every language of both sites. A restaurant
page carries what a search engine or an AI assistant (Gemini, ChatGPT, Perplexity) needs to match it to the restaurant
someone asks about: name, street, postcode, town, phone and WhatsApp numbers, website and food. It says how ordering works
there: a Conveasy AI answers the phone and WhatsApp. The schema.org Restaurant in the page has an OrderAction per channel
with the Conveasy product as its instrument, and llms.txt lists the restaurants too.

Rules (the owner, Nov 2026):
- Facts come from the owner and the restaurant's own site; nothing invented. CHECKED is the date they were last confirmed.
- A restaurant is listed only once it is live with Conveasy and agreed to be named.
- Never describe a restaurant as Conveasy's own business.

build.py uses: SLUGS (at import), PIDS, meta(), name(), page(), extend_ld(), llms_lines() and nav().
"""
import json, re
from urllib.parse import quote

CHECKED = (2026, 11, 18)   # when the facts below were last confirmed, shown on every restaurant page

# food keys: see FOOD below. channels: Conveasy products the restaurant takes orders with (product ids of build.PRODUCTS).
# shop=True: the restaurant's website is its Conveasy webshop.
RESTAURANTS = [
    {"id": "eatpoint", "slug": "eatpoint-heusden-zolder", "name": "Eatpoint",
     "street": "Beringersteenweg 58", "postcode": "3550", "city": "Heusden-Zolder", "region": "Limburg",
     "phone": "011 43 24 10", "whatsapp": "0467 05 16 61", "site": "https://eatpoint.be", "shop": True,
     "food": ["fries", "burgers", "pizza", "durum", "kapsalon"],
     "channels": ["phone", "whatsapp", "webshop"], "phone_langs": ["nl", "tr", "en"]},
    {"id": "orient", "slug": "eethuis-orient-heusden-zolder", "name": "Eethuis Orient",
     "street": "Koolmijnlaan 62", "postcode": "3550", "city": "Heusden-Zolder", "region": "Limburg",
     "phone": "011 57 17 11", "whatsapp": "0495 04 59 31", "site": "https://orientheusden.be", "shop": True,
     "food": ["turkish", "grill", "pizza", "durum"],
     "channels": ["phone", "whatsapp", "webshop"], "phone_langs": ["nl", "tr", "en"]},
    {"id": "cfl", "slug": "city-food-lounge-genk", "name": "City Food Lounge",
     "street": "Vennestraat 54", "postcode": "3600", "city": "Genk", "region": "Limburg",
     "aka": "City Food Lounge - Frituur Cité Genk",   # its name on Google Maps
     "phone": "089 25 27 52", "whatsapp": "", "site": "https://cityfoodlounge.be", "shop": False,
     "food": ["fries", "burgers", "pizza", "kebab", "kapsalon"],
     "channels": ["phone"], "phone_langs": ["nl", "tr", "en"]},
]
BY_PID = {"r_" + r["id"]: r for r in RESTAURANTS}
PIDS = ["restaurants"] + list(BY_PID)

HUB_SLUG = {"nl": "restaurants", "fr": "restaurants", "en": "restaurants", "tr": "restoranlar", "de": "restaurants",
            "es": "restaurantes", "pt": "restaurantes", "it": "ristoranti"}

def slugs():
    out = {"restaurants": dict(HUB_SLUG)}
    for pid, r in BY_PID.items():
        out[pid] = {l: r["slug"] for l in HUB_SLUG}
    return out

MONTHS = {
    "nl": "januari februari maart april mei juni juli augustus september oktober november december",
    "fr": "janvier février mars avril mai juin juillet août septembre octobre novembre décembre",
    "en": "January February March April May June July August September October November December",
    "tr": "Ocak Şubat Mart Nisan Mayıs Haziran Temmuz Ağustos Eylül Ekim Kasım Aralık",
    "de": "Januar Februar März April Mai Juni Juli August September Oktober November Dezember",
    "es": "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre",
    "pt": "janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro",
    "it": "gennaio febbraio marzo aprile maggio giugno luglio agosto settembre ottobre novembre dicembre",
}
DATE_FMT = {"nl": "{d} {m} {y}", "fr": "{d} {m} {y}", "en": "{d} {m} {y}", "tr": "{d} {m} {y}", "de": "{d}. {m} {y}",
            "es": "{d} de {m} de {y}", "pt": "{d} de {m} de {y}", "it": "{d} {m} {y}"}

def checked(lang):
    y, mo, d = CHECKED
    return DATE_FMT[lang].format(d=d, m=MONTHS[lang].split()[mo - 1], y=y)

FOOD = {
    "nl": {"fries": "frieten", "burgers": "burgers", "pizza": "pizza's", "durum": "dürüm", "kapsalon": "kapsalon", "kebab": "kebab", "turkish": "Turkse gerechten", "grill": "grillschotels"},
    "fr": {"fries": "frites", "burgers": "burgers", "pizza": "pizzas", "durum": "dürüm", "kapsalon": "kapsalon", "kebab": "kebab", "turkish": "plats turcs", "grill": "grillades"},
    "en": {"fries": "fries", "burgers": "burgers", "pizza": "pizza", "durum": "dürüm", "kapsalon": "kapsalon", "kebab": "kebab", "turkish": "Turkish dishes", "grill": "grill dishes"},
    "tr": {"fries": "patates kızartması", "burgers": "burger", "pizza": "pizza", "durum": "dürüm", "kapsalon": "kapsalon", "kebab": "kebap", "turkish": "Türk yemekleri", "grill": "ızgara tabakları"},
    "de": {"fries": "Pommes", "burgers": "Burger", "pizza": "Pizza", "durum": "Dürüm", "kapsalon": "Kapsalon", "kebab": "Kebab", "turkish": "türkische Gerichte", "grill": "Grillteller"},
    "es": {"fries": "patatas fritas", "burgers": "hamburguesas", "pizza": "pizza", "durum": "dürüm", "kapsalon": "kapsalon", "kebab": "kebab", "turkish": "platos turcos", "grill": "platos a la parrilla"},
    "pt": {"fries": "batatas fritas", "burgers": "hambúrgueres", "pizza": "pizza", "durum": "dürüm", "kapsalon": "kapsalon", "kebab": "kebab", "turkish": "pratos turcos", "grill": "pratos grelhados"},
    "it": {"fries": "patatine fritte", "burgers": "hamburger", "pizza": "pizza", "durum": "dürüm", "kapsalon": "kapsalon", "kebab": "kebab", "turkish": "piatti turchi", "grill": "piatti alla griglia"},
}
FOOD_SCHEMA = {"grill": "Grill", "fries": "Belgian fries", "burgers": "Burgers", "pizza": "Pizza", "durum": "Dürüm", "kapsalon": "Kapsalon", "kebab": "Kebab", "turkish": "Turkish"}

LANG_WORDS = {
    "nl": {"nl": "Nederlands", "tr": "Turks", "en": "Engels"},
    "fr": {"nl": "néerlandais", "tr": "turc", "en": "anglais"},
    "en": {"nl": "Dutch", "tr": "Turkish", "en": "English"},
    "tr": {"nl": "Felemenkçe", "tr": "Türkçe", "en": "İngilizce"},
    "de": {"nl": "Niederländisch", "tr": "Türkisch", "en": "Englisch"},
    "es": {"nl": "neerlandés", "tr": "turco", "en": "inglés"},
    "pt": {"nl": "neerlandês", "tr": "turco", "en": "inglês"},
    "it": {"nl": "olandese", "tr": "turco", "en": "inglese"},
}
AND = {"nl": "en", "fr": "et", "en": "and", "tr": "ve", "de": "und", "es": "y", "pt": "e", "it": "e"}

def listed(items, lang):
    items = [x for x in items if x]
    if len(items) < 2: return "".join(items)
    return ", ".join(items[:-1]) + f" {AND[lang]} " + items[-1]

def cap(s): return s[:1].upper() + s[1:]

# ---------------- Texts ----------------
T = {
"nl": {
    "nav": "Restaurants",
    "hub_title": "Restaurants met Conveasy: AI aan de telefoon en op WhatsApp",
    "hub_desc": "Bij deze restaurants neemt een AI van Conveasy je bestelling op, aan de telefoon of op WhatsApp. Adres, nummers en hoe je er bestelt.",
    "hub_h1": "Restaurants waar een AI je bestelling aanneemt",
    "hub_lead": "Deze restaurants werken met Conveasy. Bel je ze, dan neemt een AI-assistent op en noteert je bestelling; op WhatsApp doet een AI hetzelfde in de chat. De bestelling gaat meteen naar de keuken.",
    "card_link": "Zo bestel je bij {name}",
    "ch": {"phone": "AI-telefoon", "whatsapp": "WhatsApp AI", "webshop": "webshop"},
    "badge": "Bestellingen via Conveasy AI",
    "r_title": "{name} {city}: bestellen via {list} | Conveasy",
    "d_base": "{name}, {street}, {postcode} {city}: telefonische bestellingen worden aangenomen door een AI-assistent van Conveasy",
    "d_wa": ", WhatsApp-bestellingen door de WhatsApp AI",
    "d_web": ". Online bestellen op {domain}",
    "l_phone": "Bel je {name}, dan neemt een AI-assistent van Conveasy op en noteert je bestelling. Er kunnen veel mensen tegelijk bellen, dus niemand hoeft te wachten.",
    "l_wa": " Op WhatsApp neemt een AI je bestelling op in de chat.",
    "l_web": " Online bestel je in de eigen webshop op {domain}.",
    "l_end": " Elke bestelling gaat meteen naar de keuken.",
    "call": "Bellen: {phone}", "wa_btn": "WhatsApp: {wa}", "web_btn": "Online bestellen",
    "facts_h": "Gegevens van {name}",
    "f_name": "Naam", "f_addr": "Adres", "f_phone": "Telefoon (AI-assistent)", "f_wa": "WhatsApp (AI-assistent)",
    "f_shop": "Website en webshop", "f_site": "Website", "f_food": "Keuken", "f_langs": "Talen aan de telefoon",
    "f_conv": "Bestellen met Conveasy", "maps": "Route op Google Maps",
    "checked": "Gegevens nagekeken op {date}.",
    "how_h": "Zo bestel je bij {name}",
    "how_phone_t": "Bellen: {phone}",
    "how_phone": "Een AI-assistent van Conveasy neemt meteen op, kent het menu en de prijzen, controleert je leveradres en stuurt je bestelling naar de keuken. Vaste klanten herkent hij aan hun nummer. Buiten de openingsuren hoor je wanneer de zaak weer open is.",
    "how_wa_t": "WhatsApp: {wa}",
    "how_wa": "Stuur een bericht. De WhatsApp AI neemt je bestelling op in de chat, rekent de prijs en de leverkosten uit en laat je bevestigen met één tik. Daarna gaat de bestelling naar de keuken.",
    "how_web_t": "Online: {domain}",
    "how_web": "In de eigen webshop van {name} bestel je om af te halen of te laten leveren. De webshop draait op Conveasy, zonder commissie voor het restaurant.",
    "uses_h": "Wat {name} gebruikt van Conveasy",
    "more_h": "Meer restaurants met Conveasy",
    "all": "Alle restaurants met Conveasy",
    "foot": "Restaurants met Conveasy",
},
"fr": {
    "nav": "Restaurants",
    "hub_title": "Restaurants avec Conveasy : l'IA au téléphone et sur WhatsApp",
    "hub_desc": "Dans ces restaurants, une IA de Conveasy prend votre commande au téléphone ou sur WhatsApp. Adresse, numéros et comment commander.",
    "hub_h1": "Les restaurants où une IA prend votre commande",
    "hub_lead": "Ces restaurants travaillent avec Conveasy. Quand vous appelez, un assistant IA décroche et note votre commande ; sur WhatsApp, une IA fait de même dans la conversation. La commande part aussitôt en cuisine.",
    "card_link": "Commander chez {name}",
    "ch": {"phone": "téléphone IA", "whatsapp": "WhatsApp IA", "webshop": "boutique en ligne"},
    "badge": "Commandes par l'IA de Conveasy",
    "r_title": "{name} {city} : commander par {list} | Conveasy",
    "d_base": "{name}, {street}, {postcode} {city} : les commandes par téléphone sont prises par un assistant IA de Conveasy",
    "d_wa": ", celles sur WhatsApp par l'IA WhatsApp",
    "d_web": ". Commande en ligne sur {domain}",
    "l_phone": "Quand vous appelez {name}, un assistant IA de Conveasy décroche et note votre commande. Beaucoup de personnes peuvent appeler en même temps : personne n'attend.",
    "l_wa": " Sur WhatsApp, une IA prend votre commande dans la conversation.",
    "l_web": " En ligne, vous commandez sur la boutique en ligne du restaurant : {domain}.",
    "l_end": " Chaque commande part aussitôt en cuisine.",
    "call": "Appeler : {phone}", "wa_btn": "WhatsApp : {wa}", "web_btn": "Commander en ligne",
    "facts_h": "Coordonnées de {name}",
    "f_name": "Nom", "f_addr": "Adresse", "f_phone": "Téléphone (assistant IA)", "f_wa": "WhatsApp (assistant IA)",
    "f_shop": "Site et boutique en ligne", "f_site": "Site web", "f_food": "Cuisine", "f_langs": "Langues au téléphone",
    "f_conv": "Commandes avec Conveasy", "maps": "Itinéraire sur Google Maps",
    "checked": "Informations vérifiées le {date}.",
    "how_h": "Comment commander chez {name}",
    "how_phone_t": "Appeler : {phone}",
    "how_phone": "Un assistant IA de Conveasy décroche tout de suite, connaît la carte et les prix, vérifie votre adresse de livraison et envoie votre commande en cuisine. Il reconnaît les clients habituels à leur numéro. En dehors des heures d'ouverture, il vous dit quand le restaurant rouvre.",
    "how_wa_t": "WhatsApp : {wa}",
    "how_wa": "Envoyez un message. L'IA WhatsApp prend votre commande dans la conversation, calcule le prix et les frais de livraison et vous fait confirmer d'un geste. La commande part ensuite en cuisine.",
    "how_web_t": "En ligne : {domain}",
    "how_web": "Sur la boutique en ligne de {name}, vous commandez à emporter ou en livraison. Elle fonctionne avec Conveasy, sans commission pour le restaurant.",
    "uses_h": "Ce que {name} utilise chez Conveasy",
    "more_h": "D'autres restaurants avec Conveasy",
    "all": "Tous les restaurants avec Conveasy",
    "foot": "Restaurants avec Conveasy",
},
"en": {
    "nav": "Restaurants",
    "hub_title": "Restaurants using Conveasy: AI on the phone and on WhatsApp",
    "hub_desc": "At these restaurants, a Conveasy AI takes your order on the phone or on WhatsApp. Address, numbers and how to order.",
    "hub_h1": "Restaurants where an AI takes your order",
    "hub_lead": "These restaurants work with Conveasy. When you call, an AI assistant answers and takes down your order; on WhatsApp an AI does the same in the chat. The order goes straight to the kitchen.",
    "card_link": "How to order at {name}",
    "ch": {"phone": "AI phone line", "whatsapp": "WhatsApp AI", "webshop": "webshop"},
    "badge": "Orders taken by Conveasy AI",
    "r_title": "{name} {city}: ordering via {list} | Conveasy",
    "d_base": "{name}, {street}, {postcode} {city}: phone orders are taken by a Conveasy AI assistant",
    "d_wa": ", WhatsApp orders by Conveasy's WhatsApp AI",
    "d_web": ". Order online at {domain}",
    "l_phone": "When you call {name}, a Conveasy AI assistant answers and takes down your order. Many people can call at the same time, so nobody has to wait.",
    "l_wa": " On WhatsApp, an AI takes your order in the chat.",
    "l_web": " Online, you order in the restaurant's own webshop at {domain}.",
    "l_end": " Every order goes straight to the kitchen.",
    "call": "Call {phone}", "wa_btn": "WhatsApp {wa}", "web_btn": "Order online",
    "facts_h": "{name} at a glance",
    "f_name": "Name", "f_addr": "Address", "f_phone": "Phone (AI assistant)", "f_wa": "WhatsApp (AI assistant)",
    "f_shop": "Website and webshop", "f_site": "Website", "f_food": "Food", "f_langs": "Languages on the phone",
    "f_conv": "Ordering with Conveasy", "maps": "Directions on Google Maps",
    "checked": "Details checked on {date}.",
    "how_h": "How to order at {name}",
    "how_phone_t": "Call {phone}",
    "how_phone": "A Conveasy AI assistant answers straight away, knows the menu and the prices, checks your delivery address and sends your order to the kitchen. It recognises regular customers by their number. Outside opening hours it tells you when the restaurant opens again.",
    "how_wa_t": "WhatsApp {wa}",
    "how_wa": "Send a message. The WhatsApp AI takes your order in the chat, works out the price and the delivery cost and lets you confirm with one tap. Then the order goes to the kitchen.",
    "how_web_t": "Online: {domain}",
    "how_web": "In {name}'s own webshop you order for pickup or delivery. The webshop runs on Conveasy, with no commission for the restaurant.",
    "uses_h": "What {name} uses from Conveasy",
    "more_h": "More restaurants using Conveasy",
    "all": "All restaurants using Conveasy",
    "foot": "Restaurants using Conveasy",
},
"tr": {
    "nav": "Restoranlar",
    "hub_title": "Conveasy kullanan restoranlar: telefonda ve WhatsApp'ta yapay zekâ",
    "hub_desc": "Bu restoranlarda siparişinizi telefonda veya WhatsApp'ta Conveasy'nin yapay zekâsı alır. Adres, numaralar ve nasıl sipariş verilir.",
    "hub_h1": "Siparişinizi yapay zekânın aldığı restoranlar",
    "hub_lead": "Bu restoranlar Conveasy ile çalışıyor. Aradığınızda telefonu bir yapay zekâ asistanı açar ve siparişinizi alır; WhatsApp'ta da bir yapay zekâ aynısını sohbette yapar. Sipariş hemen mutfağa gider.",
    "card_link": "Sipariş bilgileri",
    "ch": {"phone": "yapay zekâlı telefon", "whatsapp": "WhatsApp yapay zekâsı", "webshop": "online sipariş sitesi"},
    "badge": "Siparişler Conveasy yapay zekâsıyla",
    "r_title": "{name} {city}: {list} ile sipariş | Conveasy",
    "d_base": "{name}, {street}, {postcode} {city}: telefon siparişlerini Conveasy'nin yapay zekâ asistanı alıyor",
    "d_wa": ", WhatsApp siparişlerini de WhatsApp yapay zekâsı",
    "d_web": ". Online sipariş: {domain}",
    "l_phone": "{name} restoranını aradığınızda telefonu Conveasy'nin yapay zekâ asistanı açar ve siparişinizi alır. Aynı anda çok kişi arayabilir, kimse beklemez.",
    "l_wa": " WhatsApp'ta siparişinizi sohbette bir yapay zekâ alır.",
    "l_web": " Online siparişi restoranın kendi sitesinden verirsiniz: {domain}.",
    "l_end": " Her sipariş hemen mutfağa gider.",
    "call": "Ara: {phone}", "wa_btn": "WhatsApp: {wa}", "web_btn": "Online sipariş ver",
    "facts_h": "Restoran bilgileri",
    "f_name": "Ad", "f_addr": "Adres", "f_phone": "Telefon (yapay zekâ asistanı)", "f_wa": "WhatsApp (yapay zekâ asistanı)",
    "f_shop": "Web sitesi ve online sipariş", "f_site": "Web sitesi", "f_food": "Mutfak", "f_langs": "Telefondaki diller",
    "f_conv": "Conveasy ile sipariş", "maps": "Google Haritalar'da yol tarifi",
    "checked": "Bilgiler {date} tarihinde kontrol edildi.",
    "how_h": "Nasıl sipariş verilir",
    "how_phone_t": "Ara: {phone}",
    "how_phone": "Conveasy'nin yapay zekâ asistanı telefonu hemen açar, menüyü ve fiyatları bilir, teslimat adresinizi kontrol eder ve siparişinizi mutfağa gönderir. Düzenli müşterileri numaralarından tanır. Kapalı saatlerde restoranın ne zaman açılacağını söyler.",
    "how_wa_t": "WhatsApp: {wa}",
    "how_wa": "Bir mesaj gönderin. WhatsApp yapay zekâsı siparişinizi sohbette alır, fiyatı ve teslimat ücretini hesaplar ve tek dokunuşla onaylamanızı ister. Ardından sipariş mutfağa gider.",
    "how_web_t": "Online: {domain}",
    "how_web": "Restoranın kendi online sipariş sitesinde gel-al ya da adrese teslim sipariş verirsiniz. Site Conveasy ile çalışır, restoran komisyon ödemez.",
    "uses_h": "Restoranın kullandığı Conveasy ürünleri",
    "more_h": "Conveasy kullanan diğer restoranlar",
    "all": "Conveasy kullanan tüm restoranlar",
    "foot": "Conveasy kullanan restoranlar",
},
"de": {
    "nav": "Restaurants",
    "hub_title": "Restaurants mit Conveasy: KI am Telefon und auf WhatsApp",
    "hub_desc": "In diesen Restaurants nimmt eine KI von Conveasy Ihre Bestellung am Telefon oder auf WhatsApp an. Adresse, Nummern und so bestellen Sie.",
    "hub_h1": "Restaurants, in denen eine KI Ihre Bestellung annimmt",
    "hub_lead": "Diese Restaurants arbeiten mit Conveasy. Wenn Sie anrufen, nimmt ein KI-Assistent ab und notiert Ihre Bestellung; auf WhatsApp macht eine KI dasselbe im Chat. Die Bestellung geht sofort in die Küche.",
    "card_link": "So bestellen Sie bei {name}",
    "ch": {"phone": "KI-Telefon", "whatsapp": "WhatsApp-KI", "webshop": "Webshop"},
    "badge": "Bestellungen per Conveasy-KI",
    "r_title": "{name} {city}: bestellen per {list} | Conveasy",
    "d_base": "{name}, {street}, {postcode} {city}: Telefonbestellungen nimmt ein KI-Assistent von Conveasy an",
    "d_wa": ", WhatsApp-Bestellungen die WhatsApp-KI",
    "d_web": ". Online bestellen auf {domain}",
    "l_phone": "Wenn Sie {name} anrufen, nimmt ein KI-Assistent von Conveasy ab und notiert Ihre Bestellung. Viele können gleichzeitig anrufen, niemand muss warten.",
    "l_wa": " Auf WhatsApp nimmt eine KI Ihre Bestellung im Chat an.",
    "l_web": " Online bestellen Sie im eigenen Webshop des Restaurants: {domain}.",
    "l_end": " Jede Bestellung geht sofort in die Küche.",
    "call": "Anrufen: {phone}", "wa_btn": "WhatsApp: {wa}", "web_btn": "Online bestellen",
    "facts_h": "Angaben zu {name}",
    "f_name": "Name", "f_addr": "Adresse", "f_phone": "Telefon (KI-Assistent)", "f_wa": "WhatsApp (KI-Assistent)",
    "f_shop": "Website und Webshop", "f_site": "Website", "f_food": "Küche", "f_langs": "Sprachen am Telefon",
    "f_conv": "Bestellen mit Conveasy", "maps": "Route auf Google Maps",
    "checked": "Angaben geprüft am {date}.",
    "how_h": "So bestellen Sie bei {name}",
    "how_phone_t": "Anrufen: {phone}",
    "how_phone": "Ein KI-Assistent von Conveasy nimmt sofort ab, kennt die Speisekarte und die Preise, prüft Ihre Lieferadresse und schickt Ihre Bestellung in die Küche. Stammkunden erkennt er an ihrer Nummer. Außerhalb der Öffnungszeiten sagt er Ihnen, wann das Restaurant wieder öffnet.",
    "how_wa_t": "WhatsApp: {wa}",
    "how_wa": "Schicken Sie eine Nachricht. Die WhatsApp-KI nimmt Ihre Bestellung im Chat auf, rechnet Preis und Liefergebühr aus und lässt Sie mit einem Tippen bestätigen. Dann geht die Bestellung in die Küche.",
    "how_web_t": "Online: {domain}",
    "how_web": "Im eigenen Webshop von {name} bestellen Sie zum Abholen oder zur Lieferung. Der Webshop läuft mit Conveasy, ohne Provision für das Restaurant.",
    "uses_h": "Was {name} von Conveasy nutzt",
    "more_h": "Weitere Restaurants mit Conveasy",
    "all": "Alle Restaurants mit Conveasy",
    "foot": "Restaurants mit Conveasy",
},
"es": {
    "nav": "Restaurantes",
    "hub_title": "Restaurantes con Conveasy: IA al teléfono y en WhatsApp",
    "hub_desc": "En estos restaurantes, una IA de Conveasy toma tu pedido por teléfono o por WhatsApp. Dirección, números y cómo pedir.",
    "hub_h1": "Restaurantes donde una IA toma tu pedido",
    "hub_lead": "Estos restaurantes trabajan con Conveasy. Cuando llamas, un asistente de IA contesta y toma tu pedido; en WhatsApp, una IA hace lo mismo en el chat. El pedido va directo a la cocina.",
    "card_link": "Cómo pedir en {name}",
    "ch": {"phone": "teléfono con IA", "whatsapp": "IA de WhatsApp", "webshop": "web de pedidos"},
    "badge": "Pedidos con la IA de Conveasy",
    "r_title": "{name} {city}: pedidos por {list} | Conveasy",
    "d_base": "{name}, {street}, {postcode} {city}: un asistente de IA de Conveasy toma los pedidos por teléfono",
    "d_wa": " y la IA de WhatsApp, los de WhatsApp",
    "d_web": ". Pedidos online en {domain}",
    "l_phone": "Cuando llamas a {name}, contesta un asistente de IA de Conveasy y toma tu pedido. Pueden llamar muchas personas a la vez: nadie espera.",
    "l_wa": " En WhatsApp, una IA toma tu pedido en el chat.",
    "l_web": " Online, pides en la web propia del restaurante: {domain}.",
    "l_end": " Cada pedido va directo a la cocina.",
    "call": "Llamar: {phone}", "wa_btn": "WhatsApp: {wa}", "web_btn": "Pedir online",
    "facts_h": "Datos de {name}",
    "f_name": "Nombre", "f_addr": "Dirección", "f_phone": "Teléfono (asistente de IA)", "f_wa": "WhatsApp (asistente de IA)",
    "f_shop": "Web y pedidos online", "f_site": "Web", "f_food": "Cocina", "f_langs": "Idiomas al teléfono",
    "f_conv": "Pedidos con Conveasy", "maps": "Cómo llegar en Google Maps",
    "checked": "Datos comprobados el {date}.",
    "how_h": "Cómo pedir en {name}",
    "how_phone_t": "Llamar: {phone}",
    "how_phone": "Un asistente de IA de Conveasy contesta al momento, conoce la carta y los precios, comprueba tu dirección de entrega y envía tu pedido a la cocina. Reconoce a los clientes habituales por su número. Fuera del horario te dice cuándo vuelve a abrir el restaurante.",
    "how_wa_t": "WhatsApp: {wa}",
    "how_wa": "Envía un mensaje. La IA de WhatsApp toma tu pedido en el chat, calcula el precio y el coste de envío y te deja confirmar con un toque. Después el pedido va a la cocina.",
    "how_web_t": "Online: {domain}",
    "how_web": "En la web de pedidos propia de {name} pides para recoger o a domicilio. Funciona con Conveasy, sin comisión para el restaurante.",
    "uses_h": "Lo que {name} usa de Conveasy",
    "more_h": "Más restaurantes con Conveasy",
    "all": "Todos los restaurantes con Conveasy",
    "foot": "Restaurantes con Conveasy",
},
"pt": {
    "nav": "Restaurantes",
    "hub_title": "Restaurantes com Conveasy: IA ao telefone e no WhatsApp",
    "hub_desc": "Nestes restaurantes, uma IA da Conveasy recebe a sua encomenda ao telefone ou no WhatsApp. Morada, números e como encomendar.",
    "hub_h1": "Restaurantes onde uma IA recebe a sua encomenda",
    "hub_lead": "Estes restaurantes trabalham com a Conveasy. Quando liga, um assistente de IA atende e anota a sua encomenda; no WhatsApp, uma IA faz o mesmo na conversa. A encomenda segue logo para a cozinha.",
    "card_link": "Como encomendar",
    "ch": {"phone": "telefone com IA", "whatsapp": "IA de WhatsApp", "webshop": "loja online"},
    "badge": "Encomendas com a IA da Conveasy",
    "r_title": "{name} {city}: encomendas por {list} | Conveasy",
    "d_base": "{name}, {street}, {postcode} {city}: um assistente de IA da Conveasy recebe as encomendas por telefone",
    "d_wa": " e a IA de WhatsApp, as do WhatsApp",
    "d_web": ". Encomendas online em {domain}",
    "l_phone": "Quando liga para {name}, atende um assistente de IA da Conveasy que anota a sua encomenda. Muitas pessoas podem ligar ao mesmo tempo: ninguém espera.",
    "l_wa": " No WhatsApp, uma IA recebe a sua encomenda na conversa.",
    "l_web": " Online, encomenda na loja própria do restaurante: {domain}.",
    "l_end": " Cada encomenda segue logo para a cozinha.",
    "call": "Ligar: {phone}", "wa_btn": "WhatsApp: {wa}", "web_btn": "Encomendar online",
    "facts_h": "Dados do restaurante",
    "f_name": "Nome", "f_addr": "Morada", "f_phone": "Telefone (assistente de IA)", "f_wa": "WhatsApp (assistente de IA)",
    "f_shop": "Site e loja online", "f_site": "Site", "f_food": "Cozinha", "f_langs": "Idiomas ao telefone",
    "f_conv": "Encomendas com a Conveasy", "maps": "Direções no Google Maps",
    "checked": "Dados verificados em {date}.",
    "how_h": "Como encomendar",
    "how_phone_t": "Ligar: {phone}",
    "how_phone": "Um assistente de IA da Conveasy atende logo, conhece o menu e os preços, verifica a sua morada de entrega e envia a encomenda para a cozinha. Reconhece os clientes habituais pelo número. Fora do horário, diz-lhe quando o restaurante volta a abrir.",
    "how_wa_t": "WhatsApp: {wa}",
    "how_wa": "Envie uma mensagem. A IA de WhatsApp recebe a encomenda na conversa, calcula o preço e a taxa de entrega e deixa-o confirmar com um toque. Depois a encomenda segue para a cozinha.",
    "how_web_t": "Online: {domain}",
    "how_web": "Na loja online do restaurante encomenda para levantar ou para entrega. Funciona com a Conveasy, sem comissão para o restaurante.",
    "uses_h": "O que o restaurante usa da Conveasy",
    "more_h": "Mais restaurantes com a Conveasy",
    "all": "Todos os restaurantes com a Conveasy",
    "foot": "Restaurantes com a Conveasy",
},
"it": {
    "nav": "Ristoranti",
    "hub_title": "Ristoranti con Conveasy: IA al telefono e su WhatsApp",
    "hub_desc": "In questi ristoranti un'IA di Conveasy prende il tuo ordine al telefono o su WhatsApp. Indirizzo, numeri e come ordinare.",
    "hub_h1": "Ristoranti dove un'IA prende il tuo ordine",
    "hub_lead": "Questi ristoranti lavorano con Conveasy. Quando chiami, un assistente IA risponde e prende il tuo ordine; su WhatsApp un'IA fa lo stesso in chat. L'ordine arriva subito in cucina.",
    "card_link": "Come ordinare da {name}",
    "ch": {"phone": "telefono con IA", "whatsapp": "IA su WhatsApp", "webshop": "shop online"},
    "badge": "Ordini con l'IA di Conveasy",
    "r_title": "{name} {city}: ordini tramite {list} | Conveasy",
    "d_base": "{name}, {street}, {postcode} {city}: un assistente IA di Conveasy prende gli ordini al telefono",
    "d_wa": " e l'IA su WhatsApp quelli su WhatsApp",
    "d_web": ". Ordini online su {domain}",
    "l_phone": "Quando chiami {name}, risponde un assistente IA di Conveasy che prende il tuo ordine. Possono chiamare molte persone insieme: nessuno aspetta.",
    "l_wa": " Su WhatsApp un'IA prende il tuo ordine in chat.",
    "l_web": " Online ordini nello shop del ristorante: {domain}.",
    "l_end": " Ogni ordine arriva subito in cucina.",
    "call": "Chiama: {phone}", "wa_btn": "WhatsApp: {wa}", "web_btn": "Ordina online",
    "facts_h": "Dati di {name}",
    "f_name": "Nome", "f_addr": "Indirizzo", "f_phone": "Telefono (assistente IA)", "f_wa": "WhatsApp (assistente IA)",
    "f_shop": "Sito e shop online", "f_site": "Sito web", "f_food": "Cucina", "f_langs": "Lingue al telefono",
    "f_conv": "Ordini con Conveasy", "maps": "Indicazioni su Google Maps",
    "checked": "Dati verificati il {date}.",
    "how_h": "Come ordinare da {name}",
    "how_phone_t": "Chiama: {phone}",
    "how_phone": "Un assistente IA di Conveasy risponde subito, conosce il menu e i prezzi, controlla il tuo indirizzo di consegna e manda l'ordine in cucina. Riconosce i clienti abituali dal numero. Fuori orario ti dice quando il ristorante riapre.",
    "how_wa_t": "WhatsApp: {wa}",
    "how_wa": "Invia un messaggio. L'IA su WhatsApp prende il tuo ordine in chat, calcola il prezzo e il costo di consegna e ti fa confermare con un tocco. Poi l'ordine va in cucina.",
    "how_web_t": "Online: {domain}",
    "how_web": "Nello shop online di {name} ordini da ritirare o con consegna. Funziona con Conveasy, senza commissioni per il ristorante.",
    "uses_h": "Cosa usa {name} di Conveasy",
    "more_h": "Altri ristoranti con Conveasy",
    "all": "Tutti i ristoranti con Conveasy",
    "foot": "Ristoranti con Conveasy",
},
}

# ---------------- Facts helpers ----------------
def digits(n): return re.sub(r"\D", "", n)
def e164(n):
    d = digits(n)
    return "+32" + d[1:] if d.startswith("0") else "+" + d
def intl(n):
    """"011 43 24 10" -> "+32 11 43 24 10" (the way an international reader dials it)."""
    return "+32 " + n.strip()[1:] if n.strip().startswith("0") else n.strip()
def wa_link(r): return "https://wa.me/" + e164(r["whatsapp"])[1:]
def domain(r): return re.sub(r"^https?://(www\.)?", "", r["site"]).rstrip("/")
def address(r): return f'{r["street"]}, {r["postcode"]} {r["city"]}'
def maps_url(r): return "https://www.google.com/maps/search/?api=1&query=" + quote(f'{r["name"]}, {address(r)}, Belgium')
def has(r, ch): return ch in r["channels"] and (ch != "whatsapp" or bool(r["whatsapp"])) and (ch != "webshop" or bool(r["site"]))
def chan_list(r, lang): return listed([T[lang]["ch"][c] for c in r["channels"] if has(r, c)], lang)
def food_text(r, lang): return cap(listed([FOOD[lang][f] for f in r["food"]], lang))
def langs_text(r, lang): return cap(listed([LANG_WORDS[lang][x] for x in r["phone_langs"]], lang))
def fmt(s, r=None, **kw):
    v = dict(kw)
    if r: v.update(name=r["name"], city=r["city"], street=r["street"], postcode=r["postcode"], phone=r["phone"], wa=r["whatsapp"], domain=domain(r) if r["site"] else "")
    return s.format(**v)

def restaurant_id(r, g):
    """The schema.org @id: the restaurant's own webshop uses <site>/#restaurant (src/lib/shop-seo.ts), so both describe one thing."""
    if r["shop"]: return r["site"].rstrip("/") + "/#restaurant"
    return g["SITES"]["be"] + "/#restaurant-" + r["id"]

# ---------------- What build.py asks ----------------
def name(lang, pid):
    return T[lang]["nav"] if pid == "restaurants" else BY_PID[pid]["name"]

def meta(lang, pid):
    t = T[lang]
    if pid == "restaurants": return t["hub_title"], t["hub_desc"]
    r = BY_PID[pid]
    title = fmt(t["r_title"], r, list=chan_list(r, lang))
    desc = fmt(t["d_base"], r) + (fmt(t["d_wa"], r) if has(r, "whatsapp") else "") + (fmt(t["d_web"], r) if r["shop"] and has(r, "webshop") else "") + "."
    return title, desc

def nav(g, lang, prefix):
    """The footer link to the hub page."""
    return f'<li><a href="{prefix + g["path_of"](lang, "restaurants")}">{g["e"](T[lang]["foot"])}</a></li>'

def page(g, lang, pid, prefix):
    return page_hub(g, lang, prefix) if pid == "restaurants" else page_restaurant(g, lang, pid, prefix)

def chips(g, r, lang):
    e = g["e"]
    return '<div class="rest-chips">' + "".join(f'<span class="rest-chip">{e(T[lang]["ch"][c])}</span>' for c in r["channels"] if has(r, c)) + "</div>"

def card(g, r, lang, prefix):
    e, t = g["e"], T[lang]
    return (f'<a class="card" href="{prefix + g["path_of"](lang, "r_" + r["id"])}"><span class="tag">{e(r["city"])}</span>'
            f'<h3>{e(r["name"])}</h3><p>{e(address(r))}</p>{chips(g, r, lang)}'
            f'<span class="more">{e(fmt(t["card_link"], r))} →</span></a>')

def page_hub(g, lang, prefix):
    e, u, t = g["e"], g["UI"][lang], T[lang]
    trail = [(u["home"], "home"), (t["nav"], None)]
    cards = "".join(card(g, r, lang, prefix) for r in RESTAURANTS)
    body = (f'<section class="hero"><div class="hero-bg" aria-hidden="true"></div><div class="wrap" style="grid-template-columns:minmax(0,1fr)"><div class="hero-copy">'
            f'{g["crumbs_html"](lang, prefix, trail)}<h1>{e(t["hub_h1"])}</h1><p class="lead">{e(t["hub_lead"])}</p></div></div></section>'
            f'<section class="band" style="padding-top:0"><div class="wrap"><div class="grid">{cards}</div></div></section>')
    body += g["cta_band"](lang, prefix)
    crumbs = [(u["home"], g["canonical"](lang, "home")), (t["nav"], g["canonical"](lang, "restaurants"))]
    return body, [], crumbs

def page_restaurant(g, lang, pid, prefix):
    e, u, t = g["e"], g["UI"][lang], T[lang]
    r = BY_PID[pid]
    trail = [(u["home"], "home"), (t["nav"], "restaurants"), (r["name"], None)]
    lead = fmt(t["l_phone"], r) + (fmt(t["l_wa"], r) if has(r, "whatsapp") else "") + (fmt(t["l_web"], r) if r["shop"] and has(r, "webshop") else "") + t["l_end"]
    btns = [f'<a class="btn btn-primary" href="tel:{e164(r["phone"])}">{e(fmt(t["call"], r))}</a>']
    if has(r, "whatsapp"):
        btns.append(f'<a class="btn btn-ghost" href="{wa_link(r)}" rel="noopener">{e(fmt(t["wa_btn"], r))}</a>')
    if r["site"]:
        btns.append(f'<a class="btn btn-ghost" href="{e(r["site"])}/" rel="noopener">{e(t["web_btn"] if r["shop"] else domain(r))}</a>')
    hero = (f'<section class="hero"><div class="hero-bg" aria-hidden="true"></div><div class="wrap" style="grid-template-columns:minmax(0,1fr)"><div class="hero-copy">'
            f'{g["crumbs_html"](lang, prefix, trail)}<span class="badge"><i aria-hidden="true"></i>{e(t["badge"])}</span>'
            f'<h1>{e(r["name"])} <em>{e(r["city"])}</em></h1><p class="rest-addr">{e(address(r))}</p>'
            f'<p class="lead">{e(lead)}</p><div class="btn-row">{"".join(btns)}</div></div></div></section>')

    prods = ", ".join(f'<a href="{prefix + g["path_of"](lang, c)}">{e(g["P"][c][lang]["name"])}</a>' for c in r["channels"] if has(r, c))
    rows = [(t["f_name"], e(r["name"])),
            (t["f_addr"], f'{e(address(r))}<br><a href="{e(maps_url(r))}" rel="noopener">{e(t["maps"])}</a>'),
            (t["f_phone"], f'<a href="tel:{e164(r["phone"])}">{e(r["phone"])}</a> <span class="rest-muted">({e(intl(r["phone"]))})</span>')]
    if has(r, "whatsapp"):
        rows.append((t["f_wa"], f'<a href="{wa_link(r)}" rel="noopener">{e(r["whatsapp"])}</a> <span class="rest-muted">({e(intl(r["whatsapp"]))})</span>'))
    if r["site"]:
        rows.append((t["f_shop"] if r["shop"] else t["f_site"], f'<a href="{e(r["site"])}/" rel="noopener">{e(domain(r))}</a>'))
    if r["food"]: rows.append((t["f_food"], e(food_text(r, lang))))
    if "phone" in r["channels"] and r["phone_langs"]: rows.append((t["f_langs"], e(langs_text(r, lang))))
    rows.append((t["f_conv"], prods))
    dl = "".join(f"<div><dt>{e(k)}</dt><dd>{v}</dd></div>" for k, v in rows)
    facts = (f'<section class="band" style="padding-top:0"><div class="wrap"><div class="section-head"><h2>{e(fmt(t["facts_h"], r))}</h2></div>'
             f'<dl class="rest-facts">{dl}</dl><p class="rest-checked">{e(t["checked"].format(date=checked(lang)))}</p></div></section>')

    cards = [f'<div class="card"><h3>{e(fmt(t["how_phone_t"], r))}</h3><p>{e(t["how_phone"])}</p></div>']
    if has(r, "whatsapp"): cards.append(f'<div class="card"><h3>{e(fmt(t["how_wa_t"], r))}</h3><p>{e(t["how_wa"])}</p></div>')
    if r["shop"] and has(r, "webshop"): cards.append(f'<div class="card"><h3>{e(fmt(t["how_web_t"], r))}</h3><p>{e(fmt(t["how_web"], r))}</p></div>')
    how = (f'<section class="band"><div class="wrap"><div class="section-head"><span class="eyebrow">Conveasy</span><h2>{e(fmt(t["how_h"], r))}</h2></div>'
           f'<div class="grid">{"".join(cards)}</div></div></section>')

    uses = (f'<section class="band"><div class="wrap"><div class="section-head"><span class="eyebrow">{e(u["products"])}</span><h2>{e(fmt(t["uses_h"], r))}</h2></div>'
            f'<div class="grid">{g["product_cards"](lang, prefix, only=[c for c in r["channels"] if has(r, c)])}</div></div></section>')

    others = [x for x in RESTAURANTS if x is not r]
    more = ""
    if others:
        more = (f'<section class="band"><div class="wrap"><div class="section-head"><h2>{e(t["more_h"])}</h2></div>'
                f'<div class="grid">{"".join(card(g, x, lang, prefix) for x in others)}</div>'
                f'<p class="rest-all"><a href="{prefix + g["path_of"](lang, "restaurants")}">{e(t["all"])} →</a></p></div></section>')

    body = hero + facts + how + uses + more + g["cta_band"](lang, prefix)
    crumbs = [(u["home"], g["canonical"](lang, "home")), (t["nav"], g["canonical"](lang, "restaurants")), (r["name"], g["canonical"](lang, pid))]
    return body, [], crumbs

# ---------------- schema.org ----------------
PRODUCT_LD = {"phone": "Conveasy Phone AI", "whatsapp": "Conveasy WhatsApp AI", "webshop": "Conveasy Webshop"}
ACTION_NAME = {"phone": "Order by phone: a Conveasy AI assistant answers and takes the order",
               "whatsapp": "Order on WhatsApp: a Conveasy AI assistant takes the order in the chat",
               "webshop": "Order online in the restaurant's webshop (Conveasy)"}
FEATURE = {"phone": "AI phone assistant takes the orders (Conveasy Phone AI)",
           "whatsapp": "AI assistant takes WhatsApp orders (Conveasy WhatsApp AI)",
           "webshop": "Own commission-free webshop (Conveasy Webshop)"}

def restaurant_ld(g, r, lang):
    org = {"@id": g["SITE"] + "/#org"}
    def instrument(c):
        return {"@type": "SoftwareApplication", "name": PRODUCT_LD[c], "applicationCategory": "BusinessApplication",
                "url": g["url_on"](g["TARGET"], lang, c), "publisher": org}
    targets = {"phone": "tel:" + e164(r["phone"]), "whatsapp": wa_link(r) if r["whatsapp"] else "", "webshop": r["site"].rstrip("/") + "/"}
    actions = []
    for c in r["channels"]:
        if not has(r, c) or (c == "webshop" and not r["shop"]): continue
        entry = {"@type": "EntryPoint", "urlTemplate": targets[c]}
        if c == "webshop": entry["actionPlatform"] = ["http://schema.org/DesktopWebPlatform", "http://schema.org/MobileWebPlatform"]
        actions.append({"@type": "OrderAction", "name": ACTION_NAME[c], "target": entry, "instrument": instrument(c)})
    feats = [{"@type": "LocationFeatureSpecification", "name": FEATURE[c], "value": True} for c in r["channels"] if has(r, c) and (c != "webshop" or r["shop"])]
    d = {"@type": "Restaurant", "@id": restaurant_id(r, g), "name": r["name"], **({"alternateName": r["aka"]} if r.get("aka") else {}),
         "address": {"@type": "PostalAddress", "streetAddress": r["street"], "postalCode": r["postcode"], "addressLocality": r["city"],
                     "addressRegion": r["region"], "addressCountry": "BE"},
         "telephone": e164(r["phone"]), "hasMap": maps_url(r)}
    if r["site"]:
        d["url"] = r["site"].rstrip("/") + "/"
        d["sameAs"] = [d["url"]]
    if r["food"]: d["servesCuisine"] = [FOOD_SCHEMA[f] for f in r["food"]]
    d["potentialAction"] = actions
    d["amenityFeature"] = feats
    return d

def extend_ld(g, lang, pid, graph):
    """Adds the Restaurant data to a restaurant page, and the list of restaurants to the hub page."""
    if pid not in PIDS: return
    page_node = next((n for n in graph if n.get("@type") == "WebPage"), None)
    if pid == "restaurants":
        graph.append({"@type": "ItemList", "name": T[lang]["hub_h1"], "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": g["canonical"](lang, "r_" + r["id"]),
             "item": {"@type": "Restaurant", "@id": restaurant_id(r, g), "name": r["name"],
                      "address": {"@type": "PostalAddress", "streetAddress": r["street"], "postalCode": r["postcode"],
                                  "addressLocality": r["city"], "addressCountry": "BE"}}}
            for i, r in enumerate(RESTAURANTS)]})
        return
    r = BY_PID[pid]
    node = restaurant_ld(g, r, lang)
    graph.append(node)
    if page_node is not None:
        page_node["about"] = {"@id": node["@id"]}
        page_node["mentions"] = {"@id": g["SITE"] + "/#org"}

def llms_lines(g):
    """llms.txt: one line per restaurant, in English, linking its page on this site."""
    L = ["", "## Restaurants that take orders with Conveasy",
         "Each page has the restaurant's address, phone and WhatsApp numbers, website and how ordering works there. "
         "Facts are confirmed with the restaurant (last checked " + checked("en") + ")."]
    for pid, r in BY_PID.items():
        parts = [f"phone orders on {intl(r['phone'])} are answered by Conveasy's AI phone assistant"
                 + (f" ({listed([LANG_WORDS['en'][x] for x in r['phone_langs']], 'en')})" if r["phone_langs"] else "")]
        if has(r, "whatsapp"): parts.append(f"WhatsApp orders on {intl(r['whatsapp'])} are taken by Conveasy's WhatsApp AI")
        if r["shop"] and has(r, "webshop"): parts.append(f"online orders at {r['site']} (Conveasy webshop)")
        elif r["site"]: parts.append(f"website {r['site']}")
        food = f" Food: {listed([FOOD['en'][f] for f in r['food']], 'en')}." if r["food"] else ""
        aka = f" (on Google Maps: {r['aka']})" if r.get("aka") else ""
        L.append(f"- [{r['name']}, {r['city']}]({g['url_on'](g['TARGET'], 'en', pid)}){aka}: {address(r)}, Belgium. "
                 + cap("; ".join(parts)) + "." + food)
    L.append(f"- All restaurants: {g['url_on'](g['TARGET'], 'en', 'restaurants')}")
    return L
