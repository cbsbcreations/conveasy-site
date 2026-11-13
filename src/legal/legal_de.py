# German translation of legal_en.py (privacy policy, terms of service, data deletion).
# Same structure as legal_en.py: list of documents. Each section body is a list; a str is a paragraph, a list of str is a bullet list.
COMPANY = "Balloz Solutions LLC, 1209 Mountain Road Pl NE STE N, Albuquerque, NM 87110, USA"
EMAIL = "conveasyai@gmail.com"

DOCS = [
    {"id": "privacy", "title": "Datenschutzerklärung", "updated": "Zuletzt aktualisiert: 18. Oktober 2026",
     "intro": "Conveasy ist ein KI-Bestellassistent für Restaurants. Er nimmt für Restaurants Telefonanrufe und WhatsApp-Nachrichten entgegen, nimmt Bestellungen auf und leitet sie an das Restaurant weiter. Conveasy wird betrieben von Balloz Solutions LLC, 1209 Mountain Road Pl NE STE N, Albuquerque, NM 87110, USA („wir“, „uns“). Diese Erklärung erläutert, welche personenbezogenen Daten wir verarbeiten, warum, und welche Rechte Sie haben.",
     "sections": [
        ("1. Wer für Ihre Daten verantwortlich ist", [[
            "Für Restaurants, die Conveasy nutzen, und für Besucher dieser Website ist Balloz Solutions LLC der Verantwortliche.",
            "Wenn Sie über Conveasy bei einem Restaurant bestellen, verarbeiten wir Ihre Daten im Auftrag dieses Restaurants. Das Restaurant ist der Verantwortliche und wir sind sein Auftragsverarbeiter."]]),
        ("2. Welche Daten wir verarbeiten", [[
            "Restaurants, die Conveasy nutzen: Name, Firmenname, E-Mail-Adresse, Telefonnummer, Adresse, Rechnungsdaten, Speisekarte, Preise und Öffnungszeiten.",
            "Personen, die über Conveasy bestellen: Telefonnummer, Name (falls angegeben), Lieferadresse, Bestelldetails, die mit dem Bestellassistenten ausgetauschten WhatsApp-Nachrichten sowie bei telefonischen Bestellungen die Audioaufnahme des Anrufs und ein Transkript.",
            "Website-Besucher: die Angaben, die Sie uns über ein Formular senden, sowie anonyme Besuchsstatistiken. Wenn Sie die Sprach-Demo auf dieser Website ausprobieren, wird Ihre Stimme für die Dauer des Demo-Anrufs verarbeitet."]]),
        ("3. Daten, die wir von Meta erhalten (WhatsApp Business Platform)", [
            "Wenn ein Restaurant sein WhatsApp-Business-Konto über das Embedded Signup von Meta mit Conveasy verbindet, erhalten wir die ID des WhatsApp-Business-Kontos, die ID der Telefonnummer, den Anzeigenamen, die Nachrichtenvorlagen und ein Zugriffstoken, mit dem wir für dieses Restaurant WhatsApp-Nachrichten senden und empfangen können. Außerdem erhalten wir die Nachrichten und Zustellungsmeldungen für diese Nummer. Wir verwenden diese Daten nur, um Bestellungen entgegenzunehmen und zu bestätigen und um das Restaurant zu unterstützen. Wir verkaufen sie niemals, verwenden sie niemals für Werbung und geben sie nur an die unten aufgeführten Dienstleister weiter."]),
        ("4. Wofür wir Ihre Daten verwenden", [[
            "Zur Erbringung des Bestelldienstes: Bestellungen verstehen, Gesamtbeträge berechnen, Bestätigungen senden und Bestellungen an das Restaurant weiterleiten (Vertragserfüllung).",
            "Zur Verwaltung unserer Kundenbeziehungen, der Rechnungsstellung und des Supports (Vertrag und rechtliche Verpflichtungen).",
            "Um den Dienst sicher zu halten und zu verbessern, zum Beispiel durch die Überprüfung von Gesprächen, bei denen eine Bestellung schiefgelaufen ist (berechtigtes Interesse).",
            "Zur Beantwortung von Fragen, die über unsere Website gesendet werden (berechtigtes Interesse)."],
            "Wir verkaufen keine personenbezogenen Daten und treffen keine automatisierten Entscheidungen mit rechtlicher oder ähnlich erheblicher Wirkung."]),
        ("5. Künstliche Intelligenz", [
            "Conveasy verwendet KI-Modelle, um gesprochene und geschriebene Bestellungen zu verstehen. Personen, die ein Restaurant über Conveasy kontaktieren, werden darüber informiert, dass sie mit einem KI-Assistenten sprechen. Wir senden KI-Anbietern nur die Informationen, die zur Bearbeitung der Bestellung erforderlich sind."]),
        ("6. Dienstleister", [
            "Wir nutzen die folgenden Dienstleister für den Betrieb von Conveasy: Meta Platforms (WhatsApp), Twilio (Telefonie), Vapi (Sprach-KI), Anthropic (KI-Sprachverarbeitung), Google Cloud / Firebase (Hosting und Datenbank), Make.com und n8n (Workflow-Automatisierung), Algolia (Speisekartensuche), PrintNode (Bestelldruck) und Mollie (Zahlungen). Balloz Solutions LLC hat ihren Sitz in den Vereinigten Staaten. Diese Anbieter können Informationen in den Vereinigten Staaten und anderen Ländern verarbeiten. Welche Datenschutz- und Datenübermittlungsanforderungen gelten, hängt davon ab, wo Sie sich befinden und wie der Dienst genutzt wird."]),
        ("7. Wie lange wir Daten speichern", [[
            "Bestellungen und WhatsApp-Gespräche: bis zu 12 Monate nach der Bestellung, sofern das Restaurant uns nicht bittet, sie früher zu löschen.",
            "Anrufaufnahmen und Transkripte: bis zu 90 Tage.",
            "Kontodaten von Restaurants: solange der Vertrag läuft; Rechnungen und zugehörige Unterlagen so lange, wie es die geltenden bundes- und einzelstaatlichen Buchhaltungs- und Steuergesetze der USA vorschreiben.",
            "Anfragen über die Website: bis zu 2 Jahre nach unserem letzten Kontakt."]]),
        ("8. Sicherheit", [
            "Wir schützen Daten durch verschlüsselte Verbindungen, Zugriffskontrolle und die Trennung der Daten jedes Restaurants."]),
        ("9. Ihre Rechte", [
            "Je nachdem, wo Sie wohnen und welche Gesetze gelten, haben Sie möglicherweise das Recht, auf Ihre personenbezogenen Informationen zuzugreifen, sie zu berichtigen, zu löschen oder eine Kopie davon zu erhalten oder bestimmte Verarbeitungen einzuschränken oder ihnen zu widersprechen. Senden Sie eine E-Mail an conveasyai@gmail.com, um eine Datenschutzanfrage zu stellen. Wenn wir Ihre Informationen für ein Restaurant verarbeiten, stimmen wir Ihre Anfrage mit diesem Restaurant ab. Sie können sich auch an die zuständige Datenschutzaufsichtsbehörde oder an den Generalstaatsanwalt (Attorney General) Ihres Bundesstaates wenden. Um eine Löschung zu beantragen, lesen Sie den Abschnitt „Datenlöschung“ weiter unten auf dieser Seite."]),
        ("10. Cookies", [
            "Diese Website verwendet keine Werbe- oder Tracking-Cookies."]),
        ("11. Änderungen", [
            "Wir können diese Erklärung aktualisieren. Die jeweils aktuelle Fassung wird immer auf dieser Seite veröffentlicht."]),
        ("12. Kontakt", [
            "Balloz Solutions LLC (Conveasy), 1209 Mountain Road Pl NE STE N, Albuquerque, NM 87110, USA. EIN: 61-2205005. Telefon: +1 878 880 1550. conveasyai@gmail.com"]),
     ]},
    {"id": "terms", "title": "Nutzungsbedingungen", "updated": "Zuletzt aktualisiert: 26. Oktober 2026",
     "intro": "Diese Bedingungen gelten für Conveasy, einen KI-Bestellassistenten für Restaurants, der von Balloz Solutions LLC, 1209 Mountain Road Pl NE STE N, Albuquerque, NM 87110, USA („wir“, „uns“) betrieben wird. Indem Sie Conveasy nutzen oder Ihr Unternehmen damit verbinden, akzeptieren Sie diese Bedingungen. Wenn wir mit Ihnen eine gesonderte Vereinbarung unterzeichnet haben, hat diese Vereinbarung Vorrang.",
     "sections": [
        ("1. Der Dienst", ["Conveasy nimmt für Ihr Restaurant Telefonanrufe und WhatsApp-Nachrichten entgegen, nimmt Bestellungen auf und sendet sie an Ihren Küchendrucker oder Ihr Dashboard. Die Funktionen, Preise und enthaltenen Volumina hängen von Ihrem Tarif ab."]),
        ("2. Ihr Konto", ["Sie müssen korrekte Unternehmensangaben machen und Ihre Zugangsdaten sicher aufbewahren. Sie sind für alle Aktivitäten in Ihrem Konto verantwortlich sowie dafür, Ihre Speisekarte, Preise, Öffnungszeiten, Liefergebiete und ausverkauften Artikel aktuell zu halten."]),
        ("3. KI und Bestellungen", ["Conveasy verwendet KI. Wir arbeiten intensiv daran, sie genau zu machen, aber sie kann Fehler machen, zum Beispiel beim Verstehen eines Artikels, einer Adresse oder einer Uhrzeit. Sie bleiben verantwortlich für die Überprüfung der Bestellungen, für die Speisen, die Sie verkaufen, für Allergeninformationen und für Ihre Vereinbarungen mit Ihren Kunden."]),
        ("4. WhatsApp und andere Dienste Dritter", ["Conveasy ist auf Dienste Dritter angewiesen, wie die WhatsApp Business Platform (Meta), Twilio und Zahlungsanbieter. Wenn Sie Ihr WhatsApp-Business-Konto verbinden, müssen Sie außerdem die Business Terms of Service, die Business Messaging Policy und die Commerce Policy von WhatsApp einhalten. Meta kann für Ihr WhatsApp-Business-Konto Gebühren für Nachrichten erheben. Wir sind nicht verantwortlich für Ausfälle oder Änderungen dieser Dienste Dritter."]),
        ("5. Zulässige Nutzung", ["Sie dürfen Conveasy nicht verwenden, um Spam oder rechtswidrige Inhalte zu versenden, um Personen Nachrichten zu senden, die Sie nicht kontaktiert oder dem Empfang von Nachrichten nicht zugestimmt haben, oder um zu versuchen, den Dienst zu beschädigen, zu überlasten oder zu kopieren."]),
        ("6. Gebühren und Zahlung", ["Die Gebühren sind in Ihrem Tarif oder Angebot festgelegt. Sofern nicht anders vereinbart, sind Rechnungen innerhalb von 14 Tagen zu bezahlen. Wir können den Dienst aussetzen, wenn eine Rechnung nach einer Zahlungserinnerung unbezahlt bleibt."]),
        ("7. Personenbezogene Daten", ["Für die personenbezogenen Daten Ihrer Kunden sind Sie der Verantwortliche und wir sind Ihr Auftragsverarbeiter. Wir verarbeiten diese Daten nur zur Erbringung des Dienstes, wie in unserer Datenschutzerklärung beschrieben."]),
        ("8. Verfügbarkeit", ["Wir sind bestrebt, Conveasy jederzeit verfügbar zu halten, können aber nicht garantieren, dass der Dienst unterbrechungs- oder fehlerfrei ist."]),
        ("9. Haftung", ["Soweit gesetzlich zulässig, ist unsere Gesamthaftung auf die Gebühren begrenzt, die Sie uns in den drei Monaten vor dem schadensverursachenden Ereignis gezahlt haben. Wir haften nicht für indirekte Schäden wie entgangenen Gewinn, entgangene Bestellungen oder Datenverlust. Dies beschränkt nicht unsere Haftung für Betrug oder vorsätzliches Fehlverhalten."]),
        ("10. Beendigung des Dienstes", ["Sofern nicht anders vereinbart, können Sie Ihr Abonnement zum Ende jedes Monats beenden. Wir können den Dienst aussetzen oder beenden, wenn Sie in schwerwiegender Weise gegen diese Bedingungen verstoßen. Nach der Beendigung können Sie einen Export Ihrer Daten anfordern; anschließend löschen wir sie wie in unserer Datenschutzerklärung beschrieben."]),
        ("11. Änderungen", ["Wir können diese Bedingungen ändern. Über wichtige Änderungen informieren wir Sie mindestens 30 Tage vor ihrem Inkrafttreten."]),
        ("12. Anwendbares Recht", ["Diese Bedingungen unterliegen dem Recht des Bundesstaates New Mexico, Vereinigte Staaten, unter Ausschluss seiner kollisionsrechtlichen Bestimmungen. Streitigkeiten über diese Bedingungen oder den Dienst werden von den einzelstaatlichen oder Bundesgerichten mit Sitz in Bernalillo County, New Mexico, entschieden. Zwingende Rechte, die Ihnen nach dem Recht des Landes zustehen, in dem Ihr Unternehmen ansässig ist, gelten weiterhin."]),
        ("13. Kontakt", ["conveasyai@gmail.com"]),
     ]},
    {"id": "data-deletion", "title": "Datenlöschung", "updated": "Zuletzt aktualisiert: 28. September 2026",
     "intro": "Sie können uns jederzeit bitten, Ihre personenbezogenen Daten zu löschen.",
     "sections": [
        ("Wenn Sie über Conveasy bestellt haben (per Telefon oder WhatsApp)", [[
            "Senden Sie eine E-Mail an conveasyai@gmail.com mit dem Betreff „Antrag auf Datenlöschung“.",
            "Geben Sie die Telefonnummer an, mit der Sie bestellt haben, und, wenn möglich, den Namen des Restaurants.",
            "Wir bestätigen Ihre Anfrage und löschen Ihre Bestellungen, WhatsApp-Gespräche und Anrufdaten innerhalb von 30 Tagen. Außerdem informieren wir das Restaurant."]]),
        ("Wenn Sie ein Restaurant sind, das Conveasy nutzt", [[
            "Senden Sie von der E-Mail-Adresse, die mit Ihrem Conveasy-Konto verknüpft ist, eine E-Mail an conveasyai@gmail.com und bitten Sie uns, Ihr Konto zu löschen.",
            "Sie können den Zugriff von Conveasy auf Ihr WhatsApp-Business-Konto auch jederzeit selbst in der Meta Business Suite unter „Settings > Integrations > Connected apps“ entfernen.",
            "Wir löschen Ihre Kontodaten, Speisekartendaten, Zugriffstokens und Ihren Bestellverlauf innerhalb von 30 Tagen."],
            "Daten, die wir gesetzlich aufbewahren müssen, wie etwa Rechnungen, werden nur so lange aufbewahrt, wie es das Gesetz vorschreibt.",
            "Fragen? Senden Sie eine E-Mail an conveasyai@gmail.com."]),
     ]},
]
