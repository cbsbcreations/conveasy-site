# English legal texts, copied from the live Framer site conveasy.be (/privacy, /terms, /data-deletion), read Nov 11, 2026.
# Adapted only: address STE N, email conveasyai@gmail.com, the cookie line (no Framer statistics on the new site),
# a line on the website voice demo, and links point to this site's own legal page.
# Structure: list of documents. Each section body is a list; a str is a paragraph, a list of str is a bullet list.
COMPANY = "Balloz Solutions LLC, 1209 Mountain Road Pl NE STE N, Albuquerque, NM 87110, USA"
EMAIL = "conveasyai@gmail.com"

DOCS = [
    {"id": "privacy", "title": "Privacy policy", "updated": "Last updated: October 18, 2026",
     "intro": "Conveasy is an AI ordering assistant for restaurants. It answers phone calls and WhatsApp messages for restaurants, takes orders and sends them to the restaurant. Conveasy is operated by Balloz Solutions LLC, 1209 Mountain Road Pl NE STE N, Albuquerque, NM 87110, USA (“we”, “us”). This policy explains which personal data we process, why, and what your rights are.",
     "sections": [
        ("1. Who is responsible for your data", [[
            "For restaurants that use Conveasy and for visitors of this website, Balloz Solutions LLC is the controller.",
            "When you order from a restaurant through Conveasy, we process your data on behalf of that restaurant. The restaurant is the controller and we are its processor."]]),
        ("2. Which data we process", [[
            "Restaurants using Conveasy: name, business name, email address, phone number, address, billing details, menu, prices and opening hours.",
            "People who order through Conveasy: phone number, name (if given), delivery address, order details, the WhatsApp messages exchanged with the ordering assistant, and for phone orders the call audio and a transcript.",
            "Website visitors: the details you send us through a form, and anonymous visit statistics. If you try the voice demo on this website, your voice is processed for the length of the demo call."]]),
        ("3. Data we receive from Meta (WhatsApp Business Platform)", [
            "When a restaurant connects its WhatsApp Business Account to Conveasy through Meta’s Embedded Signup, we receive the WhatsApp Business Account ID, phone number ID, display name, message templates and an access token that lets us send and receive WhatsApp messages for that restaurant. We also receive the messages and delivery updates for that number. We use this data only to take and confirm orders and to support the restaurant. We never sell it, never use it for advertising, and only share it with the service providers listed below."]),
        ("4. Why we use your data", [[
            "To provide the ordering service: understand orders, calculate totals, send confirmations and pass orders to the restaurant (performance of a contract).",
            "To manage our customer relationships, invoicing and support (contract and legal obligations).",
            "To keep the service secure and improve it, for example by checking conversations where an order went wrong (legitimate interest).",
            "To answer questions sent through our website (legitimate interest)."],
            "We do not sell personal data and we do not make automated decisions with legal or similarly significant effects."]),
        ("5. Artificial intelligence", [
            "Conveasy uses AI models to understand spoken and written orders. People who contact a restaurant through Conveasy are told that they are talking to an AI assistant. We only send AI providers the information needed to handle the order."]),
        ("6. Service providers", [
            "We use the following service providers to run Conveasy: Meta Platforms (WhatsApp), Twilio (telephony), Vapi (voice AI), Anthropic (AI language processing), Google Cloud / Firebase (hosting and database), Make.com and n8n (workflow automation), Algolia (menu search), PrintNode (order printing) and Mollie (payments). Balloz Solutions LLC is based in the United States. These providers may process information in the United States and other countries. Applicable privacy and data-transfer requirements depend on where you are located and how the service is used."]),
        ("7. How long we keep data", [[
            "Orders and WhatsApp conversations: up to 12 months after the order, unless the restaurant asks us to delete them earlier.",
            "Call audio and transcripts: up to 90 days.",
            "Restaurant account data: as long as the contract runs; invoices and related records for as long as required by applicable U.S. federal and state accounting and tax laws.",
            "Website enquiries: up to 2 years after our last contact."]]),
        ("8. Security", [
            "We protect data with encrypted connections, access control and separation of each restaurant’s data."]),
        ("9. Your rights", [
            "Depending on where you live and which laws apply, you may have rights to access, correct, delete or obtain a copy of your personal information, or to restrict or object to certain processing. Email conveasyai@gmail.com to submit a privacy request. If we process your information for a restaurant, we will coordinate your request with that restaurant. You may also contact the appropriate privacy regulator or your state attorney general. To request deletion, see “Data deletion” below on this page."]),
        ("10. Cookies", [
            "This website does not use advertising or tracking cookies."]),
        ("11. Changes", [
            "We may update this policy. The latest version is always published on this page."]),
        ("12. Contact", [
            "Balloz Solutions LLC (Conveasy), 1209 Mountain Road Pl NE STE N, Albuquerque, NM 87110, USA. EIN: 61-2205005. Phone: +1 878 880 1550. conveasyai@gmail.com"]),
     ]},
    {"id": "terms", "title": "Terms of service", "updated": "Last updated: October 26, 2026",
     "intro": "These terms apply to Conveasy, an AI ordering assistant for restaurants operated by Balloz Solutions LLC, 1209 Mountain Road Pl NE STE N, Albuquerque, NM 87110, USA (“we”, “us”). By using Conveasy or connecting your business to it, you accept these terms. If we have signed a separate agreement with you, that agreement takes precedence.",
     "sections": [
        ("1. The service", ["Conveasy answers phone calls and WhatsApp messages for your restaurant, takes orders and sends them to your kitchen printer or dashboard. The features, prices and included volumes depend on your plan."]),
        ("2. Your account", ["You must provide correct business information and keep your login details safe. You are responsible for all activity in your account and for keeping your menu, prices, opening hours, delivery areas and sold-out items up to date."]),
        ("3. AI and orders", ["Conveasy uses AI. We work hard to make it accurate, but it can make mistakes, for example when understanding an item, an address or a time. You remain responsible for checking orders, for the food you sell, for allergen information and for your agreements with your customers."]),
        ("4. WhatsApp and other third-party services", ["Conveasy relies on third-party services such as the WhatsApp Business Platform (Meta), Twilio and payment providers. If you connect your WhatsApp Business Account, you must also follow WhatsApp’s Business Terms of Service, Business Messaging Policy and Commerce Policy. Meta may charge messaging fees for your WhatsApp Business Account. We are not responsible for outages or changes of these third-party services."]),
        ("5. Acceptable use", ["You may not use Conveasy to send spam or unlawful content, to message people who have not contacted you or agreed to receive messages, or to try to break, overload or copy the service."]),
        ("6. Fees and payment", ["Fees are set out in your plan or quote. Unless agreed otherwise, invoices must be paid within 14 days. We may suspend the service if an invoice stays unpaid after a reminder."]),
        ("7. Personal data", ["For the personal data of your customers, you are the controller and we are your processor. We process this data only to provide the service, as described in our privacy policy."]),
        ("8. Availability", ["We aim to keep Conveasy available at all times, but we cannot guarantee that it will be uninterrupted or error-free."]),
        ("9. Liability", ["To the extent permitted by law, our total liability is limited to the fees you paid us in the three months before the event that caused the damage. We are not liable for indirect damage such as lost profit, lost orders or lost data. This does not limit our liability for fraud or intentional misconduct."]),
        ("10. Ending the service", ["Unless agreed otherwise, you can end your subscription at the end of any month. We may suspend or end the service if you seriously breach these terms. After the end, you can ask for an export of your data; we then delete it as described in our privacy policy."]),
        ("11. Changes", ["We may change these terms. We will inform you at least 30 days before important changes take effect."]),
        ("12. Governing law", ["These terms are governed by the laws of the State of New Mexico, United States, without regard to its conflict-of-law rules. Any dispute about these terms or the service will be handled by the state or federal courts located in Bernalillo County, New Mexico. Mandatory rights you have under the law of the country where your business is based still apply."]),
        ("13. Contact", ["conveasyai@gmail.com"]),
     ]},
    {"id": "data-deletion", "title": "Data deletion", "updated": "Last updated: September 28, 2026",
     "intro": "You can ask us to delete your personal data at any time.",
     "sections": [
        ("If you ordered through Conveasy (by phone or WhatsApp)", [[
            "Email conveasyai@gmail.com with the subject “Data deletion request”.",
            "Include the phone number you ordered with and, if you can, the name of the restaurant.",
            "We will confirm your request and delete your orders, WhatsApp conversations and call data within 30 days. We will also inform the restaurant."]]),
        ("If you are a restaurant using Conveasy", [[
            "Email conveasyai@gmail.com from the email address linked to your Conveasy account and ask us to delete your account.",
            "You can also remove Conveasy’s access to your WhatsApp Business Account yourself at any time in Meta Business Suite, under Settings > Integrations > Connected apps.",
            "We delete your account data, menu data, access tokens and order history within 30 days."],
            "Data that we are legally required to keep, such as invoices, is kept only as long as the law requires.",
            "Questions? Email conveasyai@gmail.com."]),
     ]},
]
