# French (Belgium) translation of legal_en.py (privacy policy, terms of service, data deletion).
# Same structure as legal_en.py: list of documents. Each section body is a list; a str is a paragraph,
# a list of str is a bullet list. Keep this file in sync with legal_en.py.
COMPANY = "Balloz Solutions LLC, 1209 Mountain Road Pl NE STE N, Albuquerque, NM 87110, États-Unis"
EMAIL = "conveasyai@gmail.com"

DOCS = [
    {"id": "privacy", "title": "Politique de confidentialité", "updated": "Dernière mise à jour : 18 octobre 2026",
     "intro": "Conveasy est un assistant de commande IA pour les restaurants. Il répond aux appels téléphoniques et aux messages WhatsApp pour les restaurants, prend les commandes et les transmet au restaurant. Conveasy est exploité par Balloz Solutions LLC, 1209 Mountain Road Pl NE STE N, Albuquerque, NM 87110, États-Unis (« nous »). Cette politique explique quelles données à caractère personnel nous traitons, pourquoi, et quels sont vos droits.",
     "sections": [
        ("1. Qui est responsable de vos données", [[
            "Pour les restaurants qui utilisent Conveasy et pour les visiteurs de ce site web, Balloz Solutions LLC est le responsable du traitement.",
            "Lorsque vous commandez auprès d’un restaurant via Conveasy, nous traitons vos données pour le compte de ce restaurant. Le restaurant est le responsable du traitement et nous sommes son sous-traitant."]]),
        ("2. Quelles données nous traitons", [[
            "Restaurants utilisant Conveasy : nom, nom de l’entreprise, adresse e-mail, numéro de téléphone, adresse, données de facturation, menu, prix et heures d’ouverture.",
            "Personnes qui commandent via Conveasy : numéro de téléphone, nom (s’il est communiqué), adresse de livraison, détails de la commande, messages WhatsApp échangés avec l’assistant de commande et, pour les commandes par téléphone, l’audio de l’appel et une transcription.",
            "Visiteurs du site web : les données que vous nous envoyez via un formulaire, et des statistiques de visite anonymes. Si vous essayez la démo vocale sur ce site web, votre voix est traitée pendant la durée de l’appel de démonstration."]]),
        ("3. Données que nous recevons de Meta (WhatsApp Business Platform)", [
            "Lorsqu’un restaurant connecte son WhatsApp Business Account à Conveasy via l’Embedded Signup de Meta, nous recevons l’identifiant du WhatsApp Business Account, l’identifiant du numéro de téléphone, le nom d’affichage, les modèles de messages et un jeton d’accès qui nous permet d’envoyer et de recevoir des messages WhatsApp pour ce restaurant. Nous recevons également les messages et les mises à jour de statut de distribution pour ce numéro. Nous utilisons ces données uniquement pour prendre et confirmer des commandes et pour assister le restaurant. Nous ne les vendons jamais, ne les utilisons jamais à des fins publicitaires et ne les partageons qu’avec les prestataires de services énumérés ci-dessous."]),
        ("4. Pourquoi nous utilisons vos données", [[
            "Pour fournir le service de commande : comprendre les commandes, calculer les totaux, envoyer les confirmations et transmettre les commandes au restaurant (exécution d’un contrat).",
            "Pour gérer nos relations clients, la facturation et le support (contrat et obligations légales).",
            "Pour assurer la sécurité du service et l’améliorer, par exemple en vérifiant les conversations dans lesquelles une commande s’est mal passée (intérêt légitime).",
            "Pour répondre aux questions envoyées via notre site web (intérêt légitime)."],
            "Nous ne vendons pas de données à caractère personnel et nous ne prenons pas de décisions automatisées produisant des effets juridiques ou des effets significatifs similaires."]),
        ("5. Intelligence artificielle", [
            "Conveasy utilise des modèles d’IA pour comprendre les commandes orales et écrites. Les personnes qui contactent un restaurant via Conveasy sont informées qu’elles parlent à un assistant IA. Nous n’envoyons aux fournisseurs d’IA que les informations nécessaires au traitement de la commande."]),
        ("6. Prestataires de services", [
            "Nous faisons appel aux prestataires de services suivants pour faire fonctionner Conveasy : Meta Platforms (WhatsApp), Twilio (téléphonie), Vapi (IA vocale), Anthropic (traitement du langage par IA), Google Cloud / Firebase (hébergement et base de données), Make.com et n8n (automatisation des flux de travail), Algolia (recherche dans le menu), PrintNode (impression des commandes) et Mollie (paiements). Balloz Solutions LLC est établie aux États-Unis. Ces prestataires peuvent traiter des informations aux États-Unis et dans d’autres pays. Les exigences applicables en matière de protection de la vie privée et de transfert de données dépendent de l’endroit où vous vous trouvez et de la manière dont le service est utilisé."]),
        ("7. Durée de conservation des données", [[
            "Commandes et conversations WhatsApp : jusqu’à 12 mois après la commande, sauf si le restaurant nous demande de les supprimer plus tôt.",
            "Audio des appels et transcriptions : jusqu’à 90 jours.",
            "Données du compte restaurant : pendant toute la durée du contrat ; les factures et les documents connexes aussi longtemps que l’exigent les lois fédérales et des États américains applicables en matière de comptabilité et de fiscalité.",
            "Demandes envoyées via le site web : jusqu’à 2 ans après notre dernier contact."]]),
        ("8. Sécurité", [
            "Nous protégeons les données au moyen de connexions chiffrées, d’un contrôle d’accès et de la séparation des données de chaque restaurant."]),
        ("9. Vos droits", [
            "Selon l’endroit où vous vivez et les lois applicables, vous pouvez avoir le droit d’accéder à vos informations personnelles, de les rectifier, de les supprimer ou d’en obtenir une copie, ou de limiter certains traitements ou de vous y opposer. Envoyez un e-mail à conveasyai@gmail.com pour introduire une demande relative à la vie privée. Si nous traitons vos informations pour un restaurant, nous coordonnerons votre demande avec ce restaurant. Vous pouvez également contacter l’autorité de protection des données compétente ou le procureur général (attorney general) de votre État. Pour demander la suppression, consultez « Suppression des données » ci-dessous sur cette page."]),
        ("10. Cookies", [
            "Ce site web n’utilise pas de cookies publicitaires ni de cookies de suivi."]),
        ("11. Modifications", [
            "Nous pouvons mettre à jour cette politique. La version la plus récente est toujours publiée sur cette page."]),
        ("12. Contact", [
            "Balloz Solutions LLC (Conveasy), 1209 Mountain Road Pl NE STE N, Albuquerque, NM 87110, États-Unis. EIN : 61-2205005. Téléphone : +1 878 880 1550. conveasyai@gmail.com"]),
     ]},
    {"id": "terms", "title": "Conditions d’utilisation", "updated": "Dernière mise à jour : 26 octobre 2026",
     "intro": "Les présentes conditions s’appliquent à Conveasy, un assistant de commande IA pour les restaurants exploité par Balloz Solutions LLC, 1209 Mountain Road Pl NE STE N, Albuquerque, NM 87110, États-Unis (« nous »). En utilisant Conveasy ou en y connectant votre établissement, vous acceptez les présentes conditions. Si nous avons signé un contrat distinct avec vous, ce contrat prévaut.",
     "sections": [
        ("1. Le service", ["Conveasy répond aux appels téléphoniques et aux messages WhatsApp pour votre restaurant, prend les commandes et les envoie à l’imprimante de votre cuisine ou à votre tableau de bord. Les fonctionnalités, les prix et les volumes inclus dépendent de votre formule."]),
        ("2. Votre compte", ["Vous devez fournir des informations exactes sur votre entreprise et conserver vos identifiants de connexion en lieu sûr. Vous êtes responsable de toute activité sur votre compte et de la mise à jour de votre menu, de vos prix, de vos heures d’ouverture, de vos zones de livraison et des articles épuisés."]),
        ("3. IA et commandes", ["Conveasy utilise l’IA. Nous nous efforçons de la rendre précise, mais elle peut commettre des erreurs, par exemple dans la compréhension d’un article, d’une adresse ou d’une heure. Vous restez responsable de la vérification des commandes, des aliments que vous vendez, des informations sur les allergènes et de vos accords avec vos clients."]),
        ("4. WhatsApp et autres services tiers", ["Conveasy repose sur des services tiers tels que la WhatsApp Business Platform (Meta), Twilio et des prestataires de paiement. Si vous connectez votre WhatsApp Business Account, vous devez également respecter les Business Terms of Service, la Business Messaging Policy et la Commerce Policy de WhatsApp. Meta peut facturer des frais de messagerie pour votre WhatsApp Business Account. Nous ne sommes pas responsables des pannes ou des modifications de ces services tiers."]),
        ("5. Utilisation acceptable", ["Vous ne pouvez pas utiliser Conveasy pour envoyer du spam ou des contenus illicites, pour envoyer des messages à des personnes qui ne vous ont pas contacté ou n’ont pas accepté de recevoir des messages, ni pour tenter de perturber, de surcharger ou de copier le service."]),
        ("6. Frais et paiement", ["Les frais sont fixés dans votre formule ou votre devis. Sauf accord contraire, les factures doivent être payées dans un délai de 14 jours. Nous pouvons suspendre le service si une facture reste impayée après un rappel."]),
        ("7. Données à caractère personnel", ["Pour les données à caractère personnel de vos clients, vous êtes le responsable du traitement et nous sommes votre sous-traitant. Nous traitons ces données uniquement pour fournir le service, comme décrit dans notre politique de confidentialité."]),
        ("8. Disponibilité", ["Nous nous efforçons de maintenir Conveasy disponible en permanence, mais nous ne pouvons pas garantir qu’il fonctionnera sans interruption ni erreur."]),
        ("9. Responsabilité", ["Dans la mesure permise par la loi, notre responsabilité totale est limitée aux frais que vous nous avez payés au cours des trois mois précédant l’événement à l’origine du dommage. Nous ne sommes pas responsables des dommages indirects tels que le manque à gagner, la perte de commandes ou la perte de données. Cela ne limite pas notre responsabilité en cas de fraude ou de faute intentionnelle."]),
        ("10. Fin du service", ["Sauf accord contraire, vous pouvez mettre fin à votre abonnement à la fin de chaque mois. Nous pouvons suspendre le service ou y mettre fin si vous enfreignez gravement les présentes conditions. Après la fin, vous pouvez demander une exportation de vos données ; nous les supprimons ensuite comme décrit dans notre politique de confidentialité."]),
        ("11. Modifications", ["Nous pouvons modifier les présentes conditions. Nous vous informerons au moins 30 jours avant l’entrée en vigueur de modifications importantes."]),
        ("12. Droit applicable", ["Les présentes conditions sont régies par le droit de l’État du Nouveau-Mexique, États-Unis, sans égard à ses règles de conflit de lois. Tout litige relatif aux présentes conditions ou au service sera porté devant les tribunaux d’État ou fédéraux situés dans le comté de Bernalillo, Nouveau-Mexique. Les droits impératifs dont vous disposez en vertu du droit du pays où votre entreprise est établie restent applicables."]),
        ("13. Contact", ["conveasyai@gmail.com"]),
     ]},
    {"id": "data-deletion", "title": "Suppression des données", "updated": "Dernière mise à jour : 28 septembre 2026",
     "intro": "Vous pouvez nous demander de supprimer vos données à caractère personnel à tout moment.",
     "sections": [
        ("Si vous avez commandé via Conveasy (par téléphone ou WhatsApp)", [[
            "Envoyez un e-mail à conveasyai@gmail.com avec pour objet « Demande de suppression des données ».",
            "Indiquez le numéro de téléphone avec lequel vous avez commandé et, si possible, le nom du restaurant.",
            "Nous confirmerons votre demande et supprimerons vos commandes, vos conversations WhatsApp et vos données d’appel dans un délai de 30 jours. Nous en informerons également le restaurant."]]),
        ("Si vous êtes un restaurant qui utilise Conveasy", [[
            "Envoyez un e-mail à conveasyai@gmail.com depuis l’adresse e-mail liée à votre compte Conveasy et demandez-nous de supprimer votre compte.",
            "Vous pouvez également retirer vous-même à tout moment l’accès de Conveasy à votre WhatsApp Business Account dans Meta Business Suite, sous « Settings > Integrations > Connected apps ».",
            "Nous supprimons les données de votre compte, les données de votre menu, les jetons d’accès et l’historique de vos commandes dans un délai de 30 jours."],
            "Les données que nous sommes légalement tenus de conserver, comme les factures, ne sont conservées que pendant la durée exigée par la loi.",
            "Des questions ? Envoyez un e-mail à conveasyai@gmail.com."]),
     ]},
]
