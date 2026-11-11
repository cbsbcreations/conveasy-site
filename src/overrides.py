# Round 3 edits (Nov 10): "Marketing AI" instead of "Content & Marketing AI",
# no mention of an own shop, 24/7 reservations via phone AI and WhatsApp AI,
# and copy for the extra app visuals (sample data only).
# build.py applies this after the extra languages are loaded.

OV = {
"nl": {
    "home_desc": "Conveasy neemt bestellingen en reservaties aan via telefoon, WhatsApp, je eigen webshop en kiosk. 24/7, in 60+ talen, zonder commissie.",
    "made_by": "Ook tafelreservaties, 24/7.",
    "story": ("Gemaakt voor de drukte", "Conveasy is gebouwd voor zaken waar de telefoon rinkelt terwijl de friteuse vol zit. De AI neemt bestellingen en reservaties aan, zodat jij en je team kunnen koken."),
    "about": {"title": "Over Conveasy | AI-bestelsoftware voor restaurants",
              "desc": "Conveasy maakt AI-software die bestellingen en reservaties aanneemt via telefoon, WhatsApp, webshop en kiosk, voor frituren, snackbars, pizzeria's en burgerzaken.",
              "h1": "Gemaakt voor de drukte in je zaak",
              "lead": "Je kent het: de telefoon rinkelt terwijl de friteuse vol zit. Conveasy neemt die bestellingen en reservaties voor je aan, zodat jij kan koken.",
              "blocks": [("Waarom Conveasy", "Als het druk is, gaan telefoonbestellingen verloren, en platforms nemen een groot deel van elke bestelling. Conveasy neemt de telefoon op, beantwoordt WhatsApp en geeft je een eigen webshop en kiosk."),
                         ("Eén systeem voor alles", "Alle bestellingen en reservaties komen in één dashboard en op je keukenscherm of printer, wat het kanaal ook is."),
                         ("Eerst directe bestellingen", "Geen commissie op je eigen kanalen. Klanten bestellen bij jou, niet via een platform.")]},
    "snack0": ("Snacks met veel opties", "Zonder ui, extra look, saus apart: de AI zet elke opmerking juist op het ticket."),
    "marketing": {"name": "Marketing AI", "sub": "Meer klanten via advertenties, Google en AI", "badge": "Nieuw",
                  "title": "Marketing AI voor restaurants | Conveasy",
                  "desc": "Conveasy Marketing AI test advertenties met jouw budget en helpt je zaak gevonden te worden op Google en in AI-assistenten zoals ChatGPT.",
                  "h1": "Meer bestellingen via advertenties, Google en AI-assistenten",
                  "lead": "Conveasy Marketing AI test advertenties met jouw budget en zorgt dat je zaak gevonden wordt op Google en in ChatGPT, Gemini en Claude. Zo komen er meer directe bestellingen binnen.",
                  "card": "Advertenties, vindbaarheid op Google en aanbevolen worden door AI.",
                  "faq": [("Hoe begin ik met Marketing AI?", "Vraag een demo aan, dan bekijken we wat Marketing AI voor jouw zaak kan doen."),
                          ("Wat kost het?", "{{PH:prijs van Marketing AI}}"),
                          ("Op welke bestellingen focust Marketing AI?", "Op bestellingen bij jou zelf, via telefoon, WhatsApp en je webshop, niet op platforms met commissie.")]},
    "mkt_feats": ["Advertenties testen", "Vindbaar op Google", "Zichtbaar in AI-assistenten"],
    "mkt_mock": ("Deze week", [("Facebook", "Advertentie A/B-test"), ("Instagram", "Advertentie in je buurt"), ("Google", "Openingsuren en menu bijgewerkt"), ("AI-zoeken", "Menu leesbaar voor ChatGPT")]),
    "resv": {"eyebrow": "Reservaties 24/7", "title": "Ook reservaties, dag en nacht",
             "text": "Klanten reserveren een tafel via de telefoon of WhatsApp, ook als je gesloten bent. De AI vraagt naam, datum, uur en aantal personen en zet de reservatie meteen in je dashboard.",
             "points": ["Via telefoon AI en WhatsApp AI", "Naam, datum, uur en aantal personen", "Alles in je dashboard"],
             "feat": ("Reservaties 24/7", "Klanten reserveren een tafel via de telefoon of WhatsApp, ook 's nachts. De reservatie komt in je dashboard."),
             "faq": ("Kan de AI ook reservaties aannemen?", "Ja. Via de telefoon AI en de WhatsApp AI reserveren klanten 24/7 een tafel. De AI noteert naam, datum, uur en aantal personen en zet de reservatie in je dashboard. Reservaties zijn inbegrepen in de prijs, zonder meerprijs."),
             "card": ("Reservaties 24/7", "Klanten reserveren een tafel via de telefoon AI of de WhatsApp AI, dag en nacht.")},
    "gallery": ("In de app", "Zo ziet het eruit", "Alle bestellingen en reservaties komen samen in je dashboard en op het keukenscherm. Voorbeelden met fictieve gegevens."),
    "cap": {"dash": "Dashboard: alle bestellingen live, per kanaal", "kds": "Keukenscherm: nieuw, in bereiding, klaar",
            "resv": "Reservaties via telefoon en WhatsApp", "web": "Je eigen webshop op de gsm van je klant",
            "kiosk": "Kiosk: klanten bestellen en betalen zelf", "chat": "Bestellen via WhatsApp", "ticket": "Ticket op de keukenprinter"},
    "kds": ("Keuken", ["Nieuw", "In bereiding", "Klaar"], [
        (0, "#1046", "WhatsApp · Afhalen", ["1x Grote friet", "1x Bicky burger"], "20:05"),
        (0, "#1047", "Kiosk · Ter plaatse", ["2x Frikandel", "1x Cola"], "nu"),
        (1, "#1044", "Webshop · Levering", ["1x Pizza margherita", "1x Tiramisu"], "20:10"),
        (2, "#1042", "Telefoon · Levering", ["2x Grote friet", "1x Stoofvleessaus"], "19:55")]),
    "resv_mock": ("Reservaties", "Vandaag", [("19:00", "2 pers.", "Janssens", "Telefoon"), ("19:30", "4 pers.", "Yilmaz", "WhatsApp"), ("20:30", "6 pers.", "Dubois", "Telefoon"), ("21:00", "3 pers.", "Peeters", "WhatsApp")], "Nieuw via WhatsApp: zaterdag 19:00, 4 pers."),
    "web": ("Jouw zaak", "Afhalen of levering", ["Friet", "Snacks", "Burgers", "Dranken"], [("Grote friet", "€4,20"), ("Bicky burger", "€5,50"), ("Frikandel", "€2,80")], "Bestellen · €12,50"),
},
"fr": {
    "home_desc": "Conveasy prend les commandes et les réservations par téléphone, WhatsApp, votre boutique en ligne et votre borne. 24h/24, dans plus de 60 langues, sans commission.",
    "made_by": "Les réservations de table aussi, 24h/24.",
    "story": ("Conçu pour le rush", "Conveasy est conçu pour les établissements où le téléphone sonne alors que la friteuse est pleine. L'IA prend les commandes et les réservations, pour que vous et votre équipe puissiez cuisiner."),
    "about": {"title": "À propos de Conveasy | Logiciel de commande IA pour restaurants",
              "desc": "Conveasy crée un logiciel IA qui prend les commandes et les réservations par téléphone, WhatsApp, boutique en ligne et borne, pour friteries, snacks, pizzerias et burgers.",
              "h1": "Conçu pour le rush de votre établissement",
              "lead": "Vous connaissez ça : le téléphone sonne alors que la friteuse est pleine. Conveasy prend ces commandes et réservations pour vous, pour que vous puissiez cuisiner.",
              "blocks": [("Pourquoi Conveasy", "Pendant le rush, des commandes téléphoniques se perdent, et les plateformes prennent une grande partie de chaque commande. Conveasy décroche le téléphone, répond sur WhatsApp et vous donne votre propre boutique en ligne et votre borne."),
                         ("Un seul système pour tout", "Toutes les commandes et réservations arrivent dans un seul tableau de bord et sur votre écran cuisine ou imprimante, quel que soit le canal."),
                         ("Les commandes directes d'abord", "Aucune commission sur vos propres canaux. Les clients commandent chez vous, pas via une plateforme.")]},
    "snack0": ("Des snacks avec beaucoup d'options", "Sans oignons, extra ail, sauce à part : l'IA met chaque remarque correctement sur le ticket."),
    "marketing": {"name": "Marketing IA", "sub": "Plus de clients via la publicité, Google et l'IA", "badge": "Nouveau",
                  "title": "Marketing IA pour restaurants | Conveasy",
                  "desc": "Conveasy Marketing IA teste des publicités avec votre budget et aide votre établissement à être trouvé sur Google et par les assistants IA comme ChatGPT.",
                  "h1": "Plus de commandes via la publicité, Google et les assistants IA",
                  "lead": "Conveasy Marketing IA teste des publicités avec votre budget et aide votre établissement à être trouvé sur Google et dans ChatGPT, Gemini et Claude. Pour plus de commandes directes.",
                  "card": "Publicités, visibilité sur Google et recommandations par l'IA.",
                  "faq": [("Comment commencer avec Marketing IA ?", "Demandez une démo, et nous regardons ce que Marketing IA peut faire pour votre établissement."),
                          ("Combien ça coûte ?", "{{PH:prix de Marketing IA}}"),
                          ("Sur quelles commandes Marketing IA se concentre-t-il ?", "Sur les commandes passées chez vous, par téléphone, WhatsApp et votre boutique en ligne, pas sur les plateformes à commission.")]},
    "mkt_feats": ["Tests de publicités", "Trouvé sur Google", "Visible dans les assistants IA"],
    "mkt_mock": ("Cette semaine", [("Facebook", "Test A/B de publicité"), ("Instagram", "Publicité dans votre quartier"), ("Google", "Horaires et carte à jour"), ("Recherche IA", "Carte lisible par ChatGPT")]),
    "resv": {"eyebrow": "Réservations 24h/24", "title": "Les réservations aussi, jour et nuit",
             "text": "Vos clients réservent une table par téléphone ou sur WhatsApp, même quand vous êtes fermé. L'IA demande le nom, la date, l'heure et le nombre de personnes, puis place la réservation directement dans votre tableau de bord.",
             "points": ["Par téléphone IA et WhatsApp IA", "Nom, date, heure et nombre de personnes", "Tout dans votre tableau de bord"],
             "feat": ("Réservations 24h/24", "Vos clients réservent une table par téléphone ou sur WhatsApp, même la nuit. La réservation arrive dans votre tableau de bord."),
             "faq": ("L'IA peut-elle aussi prendre des réservations ?", "Oui. Avec le téléphone IA et le WhatsApp IA, vos clients réservent une table 24h/24. L'IA note le nom, la date, l'heure et le nombre de personnes et place la réservation dans votre tableau de bord. Les réservations sont incluses dans le prix, sans supplément."),
             "card": ("Réservations 24h/24", "Vos clients réservent une table via le téléphone IA ou le WhatsApp IA, jour et nuit.")},
    "gallery": ("Dans l'application", "Voici à quoi ça ressemble", "Toutes les commandes et réservations arrivent dans votre tableau de bord et sur l'écran cuisine. Exemples avec des données fictives."),
    "cap": {"dash": "Tableau de bord : toutes les commandes en direct, par canal", "kds": "Écran cuisine : nouvelles, en préparation, prêtes",
            "resv": "Réservations par téléphone et WhatsApp", "web": "Votre boutique en ligne sur le téléphone du client",
            "kiosk": "Borne : les clients commandent et paient eux-mêmes", "chat": "Commander via WhatsApp", "ticket": "Ticket sur l'imprimante cuisine"},
    "kds": ("Cuisine", ["Nouvelles", "En préparation", "Prêtes"], [
        (0, "#1046", "WhatsApp · À emporter", ["1x Grande frite", "1x Bicky burger"], "20:05"),
        (0, "#1047", "Borne · Sur place", ["2x Fricadelle", "1x Cola"], "maint."),
        (1, "#1044", "En ligne · Livraison", ["1x Pizza margherita", "1x Tiramisu"], "20:10"),
        (2, "#1042", "Téléphone · Livraison", ["2x Grande frite", "1x Sauce carbonnade"], "19:55")]),
    "resv_mock": ("Réservations", "Aujourd'hui", [("19:00", "2 pers.", "Janssens", "Téléphone"), ("19:30", "4 pers.", "Yilmaz", "WhatsApp"), ("20:30", "6 pers.", "Dubois", "Téléphone"), ("21:00", "3 pers.", "Peeters", "WhatsApp")], "Nouvelle via WhatsApp : samedi 19:00, 4 pers."),
    "web": ("Votre établissement", "À emporter ou livraison", ["Frites", "Snacks", "Burgers", "Boissons"], [("Grande frite", "4,20 €"), ("Bicky burger", "5,50 €"), ("Fricadelle", "2,80 €")], "Commander · 12,50 €"),
},
"en": {
    "home_desc": "Conveasy takes orders and reservations by phone, WhatsApp, your own webshop and kiosk. 24/7, in 60+ languages, no commission.",
    "made_by": "Table reservations too, 24/7.",
    "story": ("Made for the rush", "Conveasy is built for restaurants where the phone rings while the fryer is full. The AI takes orders and reservations, so you and your team can cook."),
    "about": {"title": "About Conveasy | AI ordering software for restaurants",
              "desc": "Conveasy makes AI software that takes orders and reservations by phone, WhatsApp, webshop and kiosk, for fry shops, snack bars, pizzerias and burger restaurants.",
              "h1": "Made for the rush in your restaurant",
              "lead": "You know the feeling: the phone rings while the fryer is full. Conveasy takes those orders and reservations for you, so you can cook.",
              "blocks": [("Why Conveasy", "During the rush, phone orders get lost, and platforms take a big share of every order. Conveasy answers the phone, replies on WhatsApp and gives you your own webshop and kiosk."),
                         ("One system for everything", "All orders and reservations land in one dashboard and on your kitchen screen or printer, whatever the channel."),
                         ("Direct orders first", "No commission on your own channels. Customers order from you, not through a platform.")]},
    "snack0": ("Snacks with lots of options", "No onions, extra garlic, sauce on the side: the AI puts every note correctly on the ticket."),
    "marketing": {"name": "Marketing AI", "sub": "More customers from ads, Google and AI", "badge": "New",
                  "title": "Marketing AI for restaurants | Conveasy",
                  "desc": "Conveasy Marketing AI tests ads with your budget and helps your restaurant get found on Google and by AI assistants like ChatGPT.",
                  "h1": "More orders from ads, Google and AI assistants",
                  "lead": "Conveasy Marketing AI tests ads with your budget and helps your restaurant get found on Google and in ChatGPT, Gemini and Claude. So more direct orders come in.",
                  "card": "Ads, visibility on Google, and recommendations by AI.",
                  "faq": [("How do I start with Marketing AI?", "Book a demo, and we'll look at what Marketing AI can do for your restaurant."),
                          ("What does it cost?", "{{PH:Marketing AI price}}"),
                          ("Which orders does Marketing AI focus on?", "Orders placed with you, by phone, WhatsApp and your webshop, not on commission platforms.")]},
    "mkt_feats": ["Ad testing", "Found on Google", "Visible in AI assistants"],
    "mkt_mock": ("This week", [("Facebook", "Ad A/B test"), ("Instagram", "Ad in your area"), ("Google", "Opening hours and menu updated"), ("AI search", "Menu readable by ChatGPT")]),
    "resv": {"eyebrow": "Reservations 24/7", "title": "Reservations too, day and night",
             "text": "Customers book a table by phone or on WhatsApp, even when you're closed. The AI asks for name, date, time and party size and puts the reservation straight into your dashboard.",
             "points": ["Through phone AI and WhatsApp AI", "Name, date, time and party size", "Everything in your dashboard"],
             "feat": ("Reservations 24/7", "Customers book a table by phone or on WhatsApp, even at night. The reservation lands in your dashboard."),
             "faq": ("Can the AI take reservations too?", "Yes. With the phone AI and the WhatsApp AI, customers book a table 24/7. The AI notes name, date, time and party size and puts the reservation in your dashboard. Reservations are included in the price, at no extra cost."),
             "card": ("Reservations 24/7", "Customers book a table through the phone AI or the WhatsApp AI, day and night.")},
    "gallery": ("In the app", "Here's what it looks like", "All orders and reservations come together in your dashboard and on the kitchen screen. Examples with sample data."),
    "cap": {"dash": "Dashboard: every order live, by channel", "kds": "Kitchen screen: new, preparing, ready",
            "resv": "Reservations by phone and WhatsApp", "web": "Your own webshop on your customer's phone",
            "kiosk": "Kiosk: customers order and pay themselves", "chat": "Ordering on WhatsApp", "ticket": "Ticket on the kitchen printer"},
    "kds": ("Kitchen", ["New", "Preparing", "Ready"], [
        (0, "#1046", "WhatsApp · Pickup", ["1x Large fries", "1x Bicky burger"], "20:05"),
        (0, "#1047", "Kiosk · Eat in", ["2x Frikandel", "1x Cola"], "now"),
        (1, "#1044", "Webshop · Delivery", ["1x Pizza margherita", "1x Tiramisu"], "20:10"),
        (2, "#1042", "Phone · Delivery", ["2x Large fries", "1x Stew sauce"], "19:55")]),
    "resv_mock": ("Reservations", "Today", [("19:00", "2 ppl", "Janssens", "Phone"), ("19:30", "4 ppl", "Yilmaz", "WhatsApp"), ("20:30", "6 ppl", "Dubois", "Phone"), ("21:00", "3 ppl", "Peeters", "WhatsApp")], "New via WhatsApp: Saturday 19:00, 4 ppl"),
    "web": ("Your restaurant", "Pickup or delivery", ["Fries", "Snacks", "Burgers", "Drinks"], [("Large fries", "€4.20"), ("Bicky burger", "€5.50"), ("Frikandel", "€2.80")], "Order · €12.50"),
},
"tr": {
    "home_desc": "Conveasy telefondan, WhatsApp'tan, kendi sipariş sitenden ve kiosktan sipariş ve rezervasyon alır. 7/24, 60'tan fazla dilde, komisyonsuz.",
    "made_by": "Masa rezervasyonları da, 7/24.",
    "story": ("Yoğunluk için yapıldı", "Conveasy, fritöz doluyken telefonun çaldığı işletmeler için yapıldı. Yapay zekâ siparişleri ve rezervasyonları alır, sen ve ekibin yemeğe odaklanırsınız."),
    "about": {"title": "Conveasy hakkında | Restoranlar için yapay zekâ sipariş yazılımı",
              "desc": "Conveasy, telefon, WhatsApp, online sipariş sitesi ve kiosk üzerinden sipariş ve rezervasyon alan yapay zekâ yazılımı yapar. Frituur, snack bar, pizzeria ve burgerciler için.",
              "h1": "İşletmendeki yoğunluk için yapıldı",
              "lead": "Bilirsin: fritöz doluyken telefon çalar. Conveasy bu siparişleri ve rezervasyonları senin yerine alır, sen de yemeğe odaklanırsın.",
              "blocks": [("Neden Conveasy", "Yoğun saatlerde telefon siparişleri kaybolur, platformlar da her siparişten büyük pay alır. Conveasy telefonu açar, WhatsApp'a cevap verir ve sana kendi online sipariş siteni ve kioskunu verir."),
                         ("Her şey tek sistemde", "Kanal ne olursa olsun tüm siparişler ve rezervasyonlar tek panoya ve mutfak ekranına ya da yazıcına gelir."),
                         ("Önce doğrudan siparişler", "Kendi kanallarında komisyon yok. Müşteriler platformdan değil, doğrudan senden sipariş verir.")]},
    "snack0": ("Çok seçenekli atıştırmalıklar", "Soğansız, ekstra sarımsak, sos ayrı: yapay zekâ her notu fişe doğru yazar."),
    "marketing": {"name": "Pazarlama YZ", "sub": "Reklam, Google ve yapay zekâdan daha fazla müşteri", "badge": "Yeni",
                  "title": "Restoranlar için Pazarlama Yapay Zekâsı | Conveasy",
                  "desc": "Conveasy Pazarlama YZ senin bütçenle reklamları test eder, restoranının Google'da ve ChatGPT gibi yapay zekâ asistanlarında bulunmasına yardım eder.",
                  "h1": "Reklam, Google ve yapay zekâ asistanlarından daha fazla sipariş",
                  "lead": "Conveasy Pazarlama YZ senin bütçenle reklamları test eder ve restoranının Google'da ve ChatGPT, Gemini ve Claude'da bulunmasına yardım eder. Böylece daha fazla doğrudan sipariş gelir.",
                  "card": "Reklamlar, Google'da görünürlük ve yapay zekânın önerileri.",
                  "faq": [("Pazarlama YZ ile nasıl başlarım?", "Demo iste, Pazarlama YZ'nin restoranın için neler yapabileceğine birlikte bakalım."),
                          ("Ücreti ne kadar?", "{{PH:Pazarlama YZ fiyatı}}"),
                          ("Pazarlama YZ hangi siparişlere odaklanır?", "Komisyonlu platformlara değil, telefonla, WhatsApp'tan ve online sipariş sitenden doğrudan sana verilen siparişlere.")]},
    "mkt_feats": ["Reklam testleri", "Google'da bulunma", "Yapay zekâ asistanlarında görünürlük"],
    "mkt_mock": ("Bu hafta", [("Facebook", "Reklam A/B testi"), ("Instagram", "Bölgendeki reklam"), ("Google", "Açılış saatleri ve menü güncellendi"), ("Yapay zekâ arama", "Menü ChatGPT için okunabilir")]),
    "resv": {"eyebrow": "7/24 rezervasyon", "title": "Rezervasyonlar da, gece gündüz",
             "text": "Müşterilerin telefonla veya WhatsApp'tan masa ayırtır, kapalı olsan bile. Yapay zekâ isim, tarih, saat ve kişi sayısını sorar ve rezervasyonu hemen panona ekler.",
             "points": ["Telefon YZ ve WhatsApp YZ ile", "İsim, tarih, saat ve kişi sayısı", "Hepsi panonda"],
             "feat": ("7/24 rezervasyon", "Müşterilerin telefonla veya WhatsApp'tan masa ayırtır, gece bile. Rezervasyon panona düşer."),
             "faq": ("Yapay zekâ rezervasyon da alabilir mi?", "Evet. Telefon YZ ve WhatsApp YZ ile müşterilerin 7/24 masa ayırtır. Yapay zekâ isim, tarih, saat ve kişi sayısını not eder ve rezervasyonu panona ekler. Rezervasyonlar fiyata dahildir, ek ücret yok."),
             "card": ("7/24 rezervasyon", "Müşterilerin Telefon YZ veya WhatsApp YZ ile gece gündüz masa ayırtır.")},
    "gallery": ("Uygulamada", "Böyle görünüyor", "Tüm siparişler ve rezervasyonlar panonda ve mutfak ekranında toplanır. Örnek verilerle gösterilmiştir."),
    "cap": {"dash": "Pano: tüm siparişler canlı, kanala göre", "kds": "Mutfak ekranı: yeni, hazırlanıyor, hazır",
            "resv": "Telefon ve WhatsApp ile rezervasyonlar", "web": "Müşterinin telefonunda kendi online sipariş siten",
            "kiosk": "Kiosk: müşteriler kendisi sipariş verir ve öder", "chat": "WhatsApp'tan sipariş", "ticket": "Mutfak yazıcısında fiş"},
    "kds": ("Mutfak", ["Yeni", "Hazırlanıyor", "Hazır"], [
        (0, "#1046", "WhatsApp · Gel al", ["1x Büyük patates", "1x Bicky burger"], "20:05"),
        (0, "#1047", "Kiosk · Restoranda", ["2x Frikandel", "1x Kola"], "şimdi"),
        (1, "#1044", "Online · Paket servis", ["1x Pizza margherita", "1x Tiramisu"], "20:10"),
        (2, "#1042", "Telefon · Paket servis", ["2x Büyük patates", "1x Et sosu"], "19:55")]),
    "resv_mock": ("Rezervasyonlar", "Bugün", [("19:00", "2 kişi", "Janssens", "Telefon"), ("19:30", "4 kişi", "Yılmaz", "WhatsApp"), ("20:30", "6 kişi", "Dubois", "Telefon"), ("21:00", "3 kişi", "Peeters", "WhatsApp")], "WhatsApp'tan yeni: cumartesi 19:00, 4 kişi"),
    "web": ("Restoranın", "Gel al veya paket servis", ["Patates", "Atıştırmalık", "Burger", "İçecek"], [("Büyük patates", "€4,20"), ("Bicky burger", "€5,50"), ("Frikandel", "€2,80")], "Sipariş ver · €12,50"),
},
"de": {
    "home_desc": "Conveasy nimmt Bestellungen und Reservierungen per Telefon, WhatsApp, Webshop und Kiosk an. 24/7, in über 60 Sprachen, ohne Provision.",
    "made_by": "Auch Tischreservierungen, 24/7.",
    "story": ("Gemacht für die Stoßzeit", "Conveasy ist für Restaurants gebaut, in denen das Telefon klingelt, während die Fritteuse voll ist. Die KI nimmt Bestellungen und Reservierungen an, damit Sie und Ihr Team kochen können."),
    "about": {"title": "Über Conveasy | KI-Bestellsoftware für Restaurants",
              "desc": "Conveasy entwickelt KI-Software, die Bestellungen und Reservierungen per Telefon, WhatsApp, Webshop und Kiosk annimmt, für Frittenbuden, Imbisse, Pizzerien und Burgerläden.",
              "h1": "Gemacht für die Stoßzeit in Ihrem Restaurant",
              "lead": "Sie kennen das: Das Telefon klingelt, während die Fritteuse voll ist. Conveasy nimmt diese Bestellungen und Reservierungen für Sie an, damit Sie kochen können.",
              "blocks": [("Warum Conveasy", "Zur Stoßzeit gehen Telefonbestellungen verloren, und Plattformen nehmen einen großen Teil jeder Bestellung. Conveasy nimmt das Telefon ab, antwortet auf WhatsApp und gibt Ihnen einen eigenen Webshop und Kiosk."),
                         ("Ein System für alles", "Alle Bestellungen und Reservierungen landen in einem Dashboard und auf Ihrem Küchenbildschirm oder Drucker, egal über welchen Kanal."),
                         ("Direktbestellungen zuerst", "Keine Provision auf Ihren eigenen Kanälen. Gäste bestellen bei Ihnen, nicht über eine Plattform.")]},
    "snack0": ("Snacks mit vielen Optionen", "Ohne Zwiebeln, extra Knoblauch, Soße extra: Die KI schreibt jede Anmerkung richtig auf den Bon."),
    "marketing": {"name": "Marketing-KI", "sub": "Mehr Kunden über Anzeigen, Google und KI", "badge": "Neu",
                  "title": "Marketing-KI für Restaurants | Conveasy",
                  "desc": "Conveasy Marketing-KI testet Anzeigen mit Ihrem Budget und sorgt dafür, dass Ihr Restaurant auf Google und bei KI-Assistenten wie ChatGPT gefunden wird.",
                  "h1": "Mehr Bestellungen über Anzeigen, Google und KI-Assistenten",
                  "lead": "Conveasy Marketing-KI testet Anzeigen mit Ihrem Budget und sorgt dafür, dass Ihr Restaurant auf Google und in ChatGPT, Gemini und Claude gefunden wird. So kommen mehr Direktbestellungen herein.",
                  "card": "Anzeigen, Sichtbarkeit auf Google und Empfehlungen durch KI.",
                  "faq": [("Wie starte ich mit der Marketing-KI?", "Fordern Sie eine Demo an, dann schauen wir, was die Marketing-KI für Ihr Restaurant tun kann."),
                          ("Was kostet es?", "{{PH:Preis für Marketing-KI}}"),
                          ("Auf welche Bestellungen setzt die Marketing-KI?", "Auf Bestellungen direkt bei Ihnen, per Telefon, WhatsApp und über Ihren Webshop, nicht auf Plattformen mit Provision.")]},
    "mkt_feats": ["Anzeigen testen", "Auf Google gefunden", "Sichtbar bei KI-Assistenten"],
    "mkt_mock": ("Diese Woche", [("Facebook", "Anzeigen A/B-Test"), ("Instagram", "Anzeige in Ihrer Umgebung"), ("Google", "Öffnungszeiten und Speisekarte aktualisiert"), ("KI-Suche", "Speisekarte lesbar für ChatGPT")]),
    "resv": {"eyebrow": "Reservierungen 24/7", "title": "Auch Reservierungen, Tag und Nacht",
             "text": "Ihre Gäste reservieren einen Tisch per Telefon oder WhatsApp, auch wenn Sie geschlossen haben. Die KI fragt nach Name, Datum, Uhrzeit und Personenzahl und trägt die Reservierung direkt in Ihr Dashboard ein.",
             "points": ["Über Telefon-KI und WhatsApp-KI", "Name, Datum, Uhrzeit und Personenzahl", "Alles in Ihrem Dashboard"],
             "feat": ("Reservierungen 24/7", "Gäste reservieren einen Tisch per Telefon oder WhatsApp, auch nachts. Die Reservierung landet in Ihrem Dashboard."),
             "faq": ("Kann die KI auch Reservierungen annehmen?", "Ja. Über die Telefon-KI und die WhatsApp-KI reservieren Gäste rund um die Uhr einen Tisch. Die KI notiert Name, Datum, Uhrzeit und Personenzahl und trägt die Reservierung in Ihr Dashboard ein. Reservierungen sind im Preis inbegriffen, ohne Aufpreis."),
             "card": ("Reservierungen 24/7", "Gäste reservieren einen Tisch über die Telefon-KI oder die WhatsApp-KI, Tag und Nacht.")},
    "gallery": ("In der App", "So sieht es aus", "Alle Bestellungen und Reservierungen laufen in Ihrem Dashboard und auf dem Küchenbildschirm zusammen. Beispiele mit fiktiven Daten."),
    "cap": {"dash": "Dashboard: alle Bestellungen live, nach Kanal", "kds": "Küchenbildschirm: neu, in Zubereitung, fertig",
            "resv": "Reservierungen per Telefon und WhatsApp", "web": "Ihr eigener Webshop auf dem Handy Ihrer Gäste",
            "kiosk": "Kiosk: Gäste bestellen und bezahlen selbst", "chat": "Bestellen über WhatsApp", "ticket": "Bon auf dem Küchendrucker"},
    "kds": ("Küche", ["Neu", "In Zubereitung", "Fertig"], [
        (0, "#1046", "WhatsApp · Abholung", ["1x Große Pommes", "1x Bicky Burger"], "20:05"),
        (0, "#1047", "Kiosk · Vor Ort", ["2x Frikandel", "1x Cola"], "jetzt"),
        (1, "#1044", "Webshop · Lieferung", ["1x Pizza Margherita", "1x Tiramisu"], "20:10"),
        (2, "#1042", "Telefon · Lieferung", ["2x Große Pommes", "1x Gulaschsoße"], "19:55")]),
    "resv_mock": ("Reservierungen", "Heute", [("19:00", "2 Pers.", "Janssens", "Telefon"), ("19:30", "4 Pers.", "Yilmaz", "WhatsApp"), ("20:30", "6 Pers.", "Dubois", "Telefon"), ("21:00", "3 Pers.", "Peeters", "WhatsApp")], "Neu über WhatsApp: Samstag 19:00, 4 Pers."),
    "web": ("Ihr Restaurant", "Abholung oder Lieferung", ["Pommes", "Snacks", "Burger", "Getränke"], [("Große Pommes", "4,20 €"), ("Bicky Burger", "5,50 €"), ("Frikandel", "2,80 €")], "Bestellen · 12,50 €"),
},
}


INCLUDED = {'nl': 'Reservaties inbegrepen', 'fr': 'Réservations incluses', 'en': 'Reservations included', 'tr': 'Rezervasyon dahil', 'de': 'Reservierungen inklusive'}  # Sammy, Nov 10: reservations included in phone AI and WhatsApp AI price

def apply(ns):
    """Apply the round-3 copy to build.py's globals (ns)."""
    P, S, HOME, ABOUT, PRICING, MKT = ns["P"], ns["S"], ns["HOME"], ns["ABOUT"], ns["PRICING"], ns["MKT"]
    for l, o in OV.items():
        if l not in HOME:
            continue
        # Marketing AI: keep the ads, Google, AI and direct-order features; drop content creation
        m = P["marketing"][l]
        old_feats = m["features"]
        m.update(o["marketing"])
        m["features"] = old_feats[1:]
        PRICING[l]["mkt_feats"] = o["mkt_feats"]
        PRICING[l]["stamp_price"] = "49"
        PRICING[l]["tier_feats"] = list(PRICING[l]["tier_feats"]) + [INCLUDED[l] + " 24/7"]
        PRICING[l]["wa_feats"] = list(PRICING[l]["wa_feats"]) + [INCLUDED[l] + " 24/7"]
        o["resv"]["points"] = list(o["resv"]["points"])[:2] + [INCLUDED[l]]  # Sammy, Nov 10: digital stamp card EUR 49 a month
        MKT[l] = o["mkt_mock"]
        # No own-shop story
        h = HOME[l]
        h["desc"] = o["home_desc"]
        h["made_by"] = o["made_by"]
        h["story_title"], h["story_text"] = o["story"]
        company = ABOUT[l]["blocks"][-1]
        ABOUT[l].update({k: v for k, v in o["about"].items() if k != "blocks"})
        ABOUT[l]["blocks"] = list(o["about"]["blocks"]) + [company]
        S["snackbar"][l]["pains"][0] = o["snack0"]
        # 24/7 reservations via phone AI and WhatsApp AI
        r = o["resv"]
        for pid in ("phone", "whatsapp"):
            P[pid][l]["features"] = [r["feat"]] + list(P[pid][l]["features"])
            P[pid][l]["faq"] = list(P[pid][l]["faq"]) + [r["faq"]]
        h["faq"] = list(h["faq"]) + [r["faq"]]
    # Sammy, Nov 10: show 24/7 clearly on the phone AI and WhatsApp AI (badge on cards and hero, and in the headline)
    for l, (badge, h_phone, h_wa) in ALWAYS_ON.items():
        if l not in HOME:
            continue
        P["phone"][l]["badge"] = badge
        P["whatsapp"][l]["badge"] = badge
        P["phone"][l]["h1"] = h_phone
        P["whatsapp"][l]["h1"] = h_wa

    # Sammy, Nov 10: live within 10 days at most. Also answered on the pricing page.
    for l, q in LIVE10.items():
        if l in HOME:
            PRICING[l]["faq"] = [q] + list(PRICING[l]["faq"])


ALWAYS_ON = {
    "nl": ("24/7 bereikbaar",
           "Een AI die 24/7 je telefoon opneemt en de bestelling aanneemt",
           "Je klanten bestellen 24/7 via WhatsApp. De AI doet de rest."),
    "fr": ("Disponible 24h/24, 7j/7",
           "Une IA qui décroche le téléphone 24h/24, 7j/7 et prend la commande",
           "Vos clients commandent via WhatsApp, 24h/24 et 7j/7. L'IA s'occupe du reste."),
    "en": ("Available 24/7",
           "An AI that answers your phone 24/7 and takes the order",
           "Your customers order on WhatsApp, 24/7. The AI does the rest."),
    "tr": ("7/24 açık",
           "Telefonunu 7/24 açan ve siparişi alan bir yapay zekâ",
           "Müşterilerin WhatsApp'tan 7/24 sipariş verir. Gerisini yapay zekâ halleder."),
    "de": ("Rund um die Uhr, 24/7",
           "Eine KI, die Ihr Telefon 24/7 annimmt und die Bestellung aufnimmt",
           "Ihre Kunden bestellen über WhatsApp, 24/7. Die KI erledigt den Rest."),
}


LIVE10 = {
    "nl": ("Hoe snel kan ik starten?", "Je stuurt je menu en wij zetten alles op. Binnen maximaal 10 dagen ben je live."),
    "fr": ("En combien de temps puis-je démarrer ?", "Vous envoyez votre carte et nous installons tout. Vous êtes en ligne en 10 jours maximum."),
    "en": ("How fast can I start?", "You send your menu and we set everything up. You're live within 10 days at most."),
    "tr": ("Ne kadar hızlı başlayabilirim?", "Menünü gönderirsin, her şeyi biz kurarız. En geç 10 gün içinde yayındasın."),
    "de": ("Wie schnell kann ich starten?", "Sie senden Ihre Speisekarte, und wir richten alles ein. Sie sind in höchstens 10 Tagen live."),
}
