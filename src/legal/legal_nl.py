# Dutch (Flanders) translation of legal_en.py (privacy policy, terms of service, data deletion).
# Same structure as legal_en.py: list of documents. Each section body is a list; a str is a paragraph,
# a list of str is a bullet list. Keep this file in sync with legal_en.py.
COMPANY = "Balloz Solutions LLC, 1209 Mountain Road Pl NE STE N, Albuquerque, NM 87110, Verenigde Staten"
EMAIL = "conveasyai@gmail.com"

DOCS = [
    {"id": "privacy", "title": "Privacybeleid", "updated": "Laatst bijgewerkt: 18 oktober 2026",
     "intro": "Conveasy is een AI-bestelassistent voor restaurants. Conveasy beantwoordt telefoongesprekken en WhatsApp-berichten voor restaurants, neemt bestellingen op en stuurt ze door naar het restaurant. Conveasy wordt uitgebaat door Balloz Solutions LLC, 1209 Mountain Road Pl NE STE N, Albuquerque, NM 87110, Verenigde Staten (“wij”, “ons”). Dit beleid legt uit welke persoonsgegevens we verwerken, waarom, en wat je rechten zijn.",
     "sections": [
        ("1. Wie is verantwoordelijk voor je gegevens", [[
            "Voor restaurants die Conveasy gebruiken en voor bezoekers van deze website is Balloz Solutions LLC de verwerkingsverantwoordelijke.",
            "Wanneer je via Conveasy bij een restaurant bestelt, verwerken wij je gegevens in opdracht van dat restaurant. Het restaurant is de verwerkingsverantwoordelijke en wij zijn de verwerker van het restaurant."]]),
        ("2. Welke gegevens we verwerken", [[
            "Restaurants die Conveasy gebruiken: naam, bedrijfsnaam, e-mailadres, telefoonnummer, adres, factuurgegevens, menu, prijzen en openingsuren.",
            "Mensen die via Conveasy bestellen: telefoonnummer, naam (indien opgegeven), leveringsadres, bestelgegevens, de WhatsApp-berichten die met de bestelassistent worden uitgewisseld en, bij telefonische bestellingen, de audio van het gesprek en een transcriptie.",
            "Websitebezoekers: de gegevens die je ons via een formulier stuurt, en anonieme bezoekstatistieken. Als je de spraakdemo op deze website uitprobeert, wordt je stem verwerkt voor de duur van het demogesprek."]]),
        ("3. Gegevens die we van Meta ontvangen (WhatsApp Business Platform)", [
            "Wanneer een restaurant zijn WhatsApp Business Account via de Embedded Signup van Meta aan Conveasy koppelt, ontvangen we de ID van het WhatsApp Business Account, de ID van het telefoonnummer, de weergavenaam, de berichtsjablonen en een toegangstoken waarmee we voor dat restaurant WhatsApp-berichten kunnen versturen en ontvangen. We ontvangen ook de berichten en de afleveringsupdates voor dat nummer. We gebruiken deze gegevens alleen om bestellingen op te nemen en te bevestigen en om het restaurant te ondersteunen. We verkopen ze nooit, gebruiken ze nooit voor reclame en delen ze alleen met de hieronder vermelde dienstverleners."]),
        ("4. Waarvoor we je gegevens gebruiken", [[
            "Om de bestelservice te leveren: bestellingen begrijpen, totalen berekenen, bevestigingen versturen en bestellingen doorgeven aan het restaurant (uitvoering van een overeenkomst).",
            "Om onze klantrelaties, facturatie en ondersteuning te beheren (overeenkomst en wettelijke verplichtingen).",
            "Om de dienst veilig te houden en te verbeteren, bijvoorbeeld door gesprekken na te kijken waarin een bestelling is misgelopen (gerechtvaardigd belang).",
            "Om vragen te beantwoorden die via onze website worden verstuurd (gerechtvaardigd belang)."],
            "We verkopen geen persoonsgegevens en we nemen geen geautomatiseerde beslissingen met rechtsgevolgen of vergelijkbare aanzienlijke gevolgen."]),
        ("5. Artificiële intelligentie", [
            "Conveasy gebruikt AI-modellen om gesproken en geschreven bestellingen te begrijpen. Mensen die via Conveasy contact opnemen met een restaurant, krijgen te horen dat ze met een AI-assistent praten. We sturen AI-aanbieders alleen de informatie die nodig is om de bestelling af te handelen."]),
        ("6. Dienstverleners", [
            "We gebruiken de volgende dienstverleners om Conveasy te laten werken: Meta Platforms (WhatsApp), Twilio (telefonie), Vapi (spraak-AI), Anthropic (AI-taalverwerking), Google Cloud / Firebase (hosting en database), Make.com en n8n (workflowautomatisering), Algolia (zoeken in het menu), PrintNode (afdrukken van bestellingen) en Mollie (betalingen). Balloz Solutions LLC is gevestigd in de Verenigde Staten. Deze dienstverleners kunnen informatie verwerken in de Verenigde Staten en in andere landen. Welke vereisten inzake privacy en gegevensdoorgifte van toepassing zijn, hangt af van waar je je bevindt en hoe de dienst wordt gebruikt."]),
        ("7. Hoe lang we gegevens bewaren", [[
            "Bestellingen en WhatsApp-gesprekken: tot 12 maanden na de bestelling, tenzij het restaurant ons vraagt ze eerder te verwijderen.",
            "Gespreksaudio en transcripties: tot 90 dagen.",
            "Accountgegevens van restaurants: zolang de overeenkomst loopt; facturen en bijbehorende documenten zolang de toepasselijke Amerikaanse federale wetgeving en wetgeving van de staten inzake boekhouding en belastingen dat vereist.",
            "Vragen via de website: tot 2 jaar na ons laatste contact."]]),
        ("8. Beveiliging", [
            "We beschermen gegevens met versleutelde verbindingen, toegangscontrole en scheiding van de gegevens van elk restaurant."]),
        ("9. Je rechten", [
            "Afhankelijk van waar je woont en welke wetten van toepassing zijn, kun je het recht hebben om je persoonsgegevens in te zien, te corrigeren, te verwijderen of er een kopie van te krijgen, of om bepaalde verwerkingen te beperken of er bezwaar tegen te maken. Mail naar conveasyai@gmail.com om een privacyverzoek in te dienen. Als we je gegevens voor een restaurant verwerken, stemmen we je verzoek af met dat restaurant. Je kunt ook contact opnemen met de bevoegde privacytoezichthouder of met de procureur-generaal (attorney general) van je staat. Om verwijdering aan te vragen, zie “Verwijdering van gegevens” hieronder op deze pagina."]),
        ("10. Cookies", [
            "Deze website gebruikt geen advertentie- of trackingcookies."]),
        ("11. Wijzigingen", [
            "We kunnen dit beleid bijwerken. De meest recente versie wordt altijd op deze pagina gepubliceerd."]),
        ("12. Contact", [
            "Balloz Solutions LLC (Conveasy), 1209 Mountain Road Pl NE STE N, Albuquerque, NM 87110, Verenigde Staten. EIN: 61-2205005. Telefoon: +1 878 880 1550. conveasyai@gmail.com"]),
     ]},
    {"id": "terms", "title": "Gebruiksvoorwaarden", "updated": "Laatst bijgewerkt: 26 oktober 2026",
     "intro": "Deze voorwaarden gelden voor Conveasy, een AI-bestelassistent voor restaurants die wordt uitgebaat door Balloz Solutions LLC, 1209 Mountain Road Pl NE STE N, Albuquerque, NM 87110, Verenigde Staten (“wij”, “ons”). Door Conveasy te gebruiken of je zaak eraan te koppelen, aanvaard je deze voorwaarden. Als we met jou een afzonderlijke overeenkomst hebben ondertekend, heeft die overeenkomst voorrang.",
     "sections": [
        ("1. De dienst", ["Conveasy beantwoordt telefoongesprekken en WhatsApp-berichten voor je restaurant, neemt bestellingen op en stuurt ze naar je keukenprinter of dashboard. De functies, prijzen en inbegrepen volumes hangen af van je abonnement."]),
        ("2. Je account", ["Je moet correcte bedrijfsgegevens verstrekken en je inloggegevens veilig bewaren. Je bent verantwoordelijk voor alle activiteit in je account en voor het up-to-date houden van je menu, prijzen, openingsuren, leveringszones en uitverkochte artikelen."]),
        ("3. AI en bestellingen", ["Conveasy gebruikt AI. We werken hard om die nauwkeurig te maken, maar ze kan fouten maken, bijvoorbeeld bij het begrijpen van een product, een adres of een tijdstip. Je blijft verantwoordelijk voor het controleren van bestellingen, voor het eten dat je verkoopt, voor informatie over allergenen en voor je afspraken met je klanten."]),
        ("4. WhatsApp en andere diensten van derden", ["Conveasy steunt op diensten van derden, zoals het WhatsApp Business Platform (Meta), Twilio en betaalproviders. Als je je WhatsApp Business Account koppelt, moet je ook de Business Terms of Service, de Business Messaging Policy en de Commerce Policy van WhatsApp naleven. Meta kan berichtkosten aanrekenen voor je WhatsApp Business Account. We zijn niet verantwoordelijk voor storingen of wijzigingen van deze diensten van derden."]),
        ("5. Aanvaardbaar gebruik", ["Je mag Conveasy niet gebruiken om spam of onrechtmatige inhoud te versturen, om berichten te sturen naar mensen die geen contact met je hebben opgenomen of niet hebben ingestemd met het ontvangen van berichten, of om te proberen de dienst te ontregelen, te overbelasten of te kopiëren."]),
        ("6. Vergoedingen en betaling", ["De vergoedingen staan in je abonnement of offerte. Tenzij anders overeengekomen, moeten facturen binnen 14 dagen worden betaald. We kunnen de dienst opschorten als een factuur na een herinnering onbetaald blijft."]),
        ("7. Persoonsgegevens", ["Voor de persoonsgegevens van je klanten ben jij de verwerkingsverantwoordelijke en zijn wij je verwerker. We verwerken deze gegevens alleen om de dienst te leveren, zoals beschreven in ons privacybeleid."]),
        ("8. Beschikbaarheid", ["We streven ernaar Conveasy altijd beschikbaar te houden, maar we kunnen niet garanderen dat de dienst ononderbroken of foutloos zal werken."]),
        ("9. Aansprakelijkheid", ["Voor zover wettelijk toegestaan, is onze totale aansprakelijkheid beperkt tot de vergoedingen die je ons hebt betaald in de drie maanden vóór de gebeurtenis die de schade heeft veroorzaakt. We zijn niet aansprakelijk voor indirecte schade zoals gederfde winst, gemiste bestellingen of verloren gegevens. Dit beperkt onze aansprakelijkheid voor fraude of opzettelijk wangedrag niet."]),
        ("10. Beëindiging van de dienst", ["Tenzij anders overeengekomen, kun je je abonnement aan het einde van elke maand opzeggen. We kunnen de dienst opschorten of beëindigen als je deze voorwaarden ernstig schendt. Na de beëindiging kun je een export van je gegevens vragen; daarna verwijderen we ze zoals beschreven in ons privacybeleid."]),
        ("11. Wijzigingen", ["We kunnen deze voorwaarden wijzigen. We brengen je minstens 30 dagen voordat belangrijke wijzigingen van kracht worden op de hoogte."]),
        ("12. Toepasselijk recht", ["Op deze voorwaarden is het recht van de staat New Mexico, Verenigde Staten, van toepassing, zonder rekening te houden met de conflictregels van dat recht. Elk geschil over deze voorwaarden of de dienst wordt behandeld door de staats- of federale rechtbanken in Bernalillo County, New Mexico. Dwingende rechten die je hebt op grond van het recht van het land waar je zaak gevestigd is, blijven van toepassing."]),
        ("13. Contact", ["conveasyai@gmail.com"]),
     ]},
    {"id": "data-deletion", "title": "Verwijdering van gegevens", "updated": "Laatst bijgewerkt: 28 september 2026",
     "intro": "Je kunt ons op elk moment vragen om je persoonsgegevens te verwijderen.",
     "sections": [
        ("Als je via Conveasy hebt besteld (telefonisch of via WhatsApp)", [[
            "Mail naar conveasyai@gmail.com met als onderwerp “Verzoek tot verwijdering van gegevens”.",
            "Vermeld het telefoonnummer waarmee je hebt besteld en, als je kunt, de naam van het restaurant.",
            "We bevestigen je verzoek en verwijderen je bestellingen, WhatsApp-gesprekken en gespreksgegevens binnen 30 dagen. We brengen ook het restaurant op de hoogte."]]),
        ("Als je een restaurant bent dat Conveasy gebruikt", [[
            "Mail naar conveasyai@gmail.com vanaf het e-mailadres dat aan je Conveasy-account gekoppeld is en vraag ons om je account te verwijderen.",
            "Je kunt de toegang van Conveasy tot je WhatsApp Business Account ook op elk moment zelf intrekken in Meta Business Suite, onder “Settings > Integrations > Connected apps”.",
            "We verwijderen je accountgegevens, menugegevens, toegangstokens en bestelgeschiedenis binnen 30 dagen."],
            "Gegevens die we wettelijk moeten bewaren, zoals facturen, bewaren we enkel zolang de wet dat vereist.",
            "Vragen? Mail naar conveasyai@gmail.com."]),
     ]},
]
