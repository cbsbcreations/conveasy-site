# Turkish translation of legal_en.py (privacy policy, terms of service, data deletion).
# Same structure as legal_en.py: list of documents. Each section body is a list; a str is a paragraph, a list of str is a bullet list.
COMPANY = "Balloz Solutions LLC, 1209 Mountain Rd Pl NE STE N, Albuquerque, NM 87110, ABD"
EMAIL = "conveasyai@gmail.com"

DOCS = [
    {"id": "privacy", "title": "Gizlilik politikası", "updated": "Son güncelleme: 18 Ekim 2026",
     "intro": "Conveasy, restoranlar için bir yapay zekâ sipariş asistanıdır. Restoranlar adına telefon aramalarını ve WhatsApp mesajlarını yanıtlar, siparişleri alır ve restorana iletir. Conveasy, Balloz Solutions LLC, 1209 Mountain Rd Pl NE STE N, Albuquerque, NM 87110, ABD (“biz”, “bize”) tarafından işletilmektedir. Bu politika, hangi kişisel verileri neden işlediğimizi ve haklarının neler olduğunu açıklar.",
     "sections": [
        ("1. Verilerinden kim sorumludur", [[
            "Conveasy kullanan restoranlar ve bu web sitesinin ziyaretçileri için veri sorumlusu Balloz Solutions LLC’dir.",
            "Conveasy üzerinden bir restorandan sipariş verdiğinde, verilerini o restoran adına işleriz. Veri sorumlusu restorandır, biz ise onun veri işleyeniyiz."]]),
        ("2. Hangi verileri işliyoruz", [[
            "Conveasy kullanan restoranlar: ad, işletme adı, e-posta adresi, telefon numarası, adres, fatura bilgileri, menü, fiyatlar ve çalışma saatleri.",
            "Conveasy üzerinden sipariş veren kişiler: telefon numarası, ad (verilmişse), teslimat adresi, sipariş ayrıntıları, sipariş asistanıyla yapılan WhatsApp yazışmaları ve telefonla verilen siparişlerde aramanın ses kaydı ile bir transkripti.",
            "Web sitesi ziyaretçileri: bir form aracılığıyla bize gönderdiğin bilgiler ve anonim ziyaret istatistikleri. Bu web sitesindeki sesli demoyu denersen, sesin demo araması süresince işlenir."]]),
        ("3. Meta’dan aldığımız veriler (WhatsApp Business Platform)", [
            "Bir restoran, WhatsApp Business Hesabını Meta’nın Embedded Signup özelliği aracılığıyla Conveasy’ye bağladığında; WhatsApp Business Hesap kimliğini (ID), telefon numarası kimliğini (ID), görünen adı, mesaj şablonlarını ve o restoran adına WhatsApp mesajları göndermemizi ve almamızı sağlayan bir erişim belirtecini (access token) alırız. Ayrıca o numaraya ait mesajları ve teslim durumu güncellemelerini de alırız. Bu verileri yalnızca siparişleri almak ve onaylamak ve restorana destek olmak için kullanırız. Bu verileri asla satmayız, asla reklam amacıyla kullanmayız ve yalnızca aşağıda listelenen hizmet sağlayıcılarla paylaşırız."]),
        ("4. Verilerini neden kullanıyoruz", [[
            "Sipariş hizmetini sunmak için: siparişleri anlamak, toplam tutarları hesaplamak, onay mesajları göndermek ve siparişleri restorana iletmek (sözleşmenin ifası).",
            "Müşteri ilişkilerimizi, faturalandırmayı ve desteği yönetmek için (sözleşme ve yasal yükümlülükler).",
            "Hizmeti güvenli tutmak ve geliştirmek için, örneğin bir siparişin yanlış gittiği konuşmaları inceleyerek (meşru menfaat).",
            "Web sitemiz üzerinden gönderilen sorulara yanıt vermek için (meşru menfaat)."],
            "Kişisel verileri satmayız ve hukuki ya da benzer şekilde önemli etkiler doğuran otomatik kararlar almayız."]),
        ("5. Yapay zekâ", [
            "Conveasy, sözlü ve yazılı siparişleri anlamak için yapay zekâ modelleri kullanır. Bir restoranla Conveasy üzerinden iletişime geçen kişilere, bir yapay zekâ asistanıyla konuştukları bildirilir. Yapay zekâ sağlayıcılarına yalnızca siparişi işlemek için gereken bilgileri göndeririz."]),
        ("6. Hizmet sağlayıcılar", [
            "Conveasy’yi çalıştırmak için şu hizmet sağlayıcıları kullanıyoruz: Meta Platforms (WhatsApp), Twilio (telefon hizmetleri), Vapi (sesli yapay zekâ), Anthropic (yapay zekâ ile dil işleme), Google Cloud / Firebase (barındırma ve veritabanı), Make.com ve n8n (iş akışı otomasyonu), Algolia (menü arama), PrintNode (sipariş yazdırma) ve Mollie (ödemeler). Balloz Solutions LLC, Amerika Birleşik Devletleri’nde yerleşiktir. Bu sağlayıcılar bilgileri Amerika Birleşik Devletleri’nde ve diğer ülkelerde işleyebilir. Geçerli gizlilik ve veri aktarımı gereklilikleri, nerede bulunduğuna ve hizmetin nasıl kullanıldığına bağlıdır."]),
        ("7. Verileri ne kadar süre saklıyoruz", [[
            "Siparişler ve WhatsApp yazışmaları: restoran bunları daha önce silmemizi istemedikçe, siparişten sonra en fazla 12 ay.",
            "Arama ses kayıtları ve transkriptler: en fazla 90 gün.",
            "Restoran hesap verileri: sözleşme sürdüğü müddetçe; faturalar ve ilgili kayıtlar, geçerli ABD federal ve eyalet muhasebe ve vergi yasalarının gerektirdiği süre boyunca.",
            "Web sitesi üzerinden gelen talepler: son iletişimimizden sonra en fazla 2 yıl."]]),
        ("8. Güvenlik", [
            "Verileri şifreli bağlantılar, erişim kontrolü ve her restoranın verilerinin birbirinden ayrılmasıyla koruruz."]),
        ("9. Hakların", [
            "Nerede yaşadığına ve hangi yasaların geçerli olduğuna bağlı olarak; kişisel bilgilerine erişme, bunları düzeltme, silme veya bir kopyasını alma ya da belirli işlemleri kısıtlama veya bunlara itiraz etme hakların olabilir. Bir gizlilik talebi göndermek için conveasyai@gmail.com adresine e-posta gönder. Bilgilerini bir restoran adına işliyorsak, talebini o restoranla koordine ederiz. Ayrıca ilgili gizlilik denetim kurumuna veya eyaletinin başsavcısına (attorney general) da başvurabilirsin. Silme talebinde bulunmak için bu sayfada aşağıdaki “Veri silme” bölümüne bak."]),
        ("10. Çerezler", [
            "Bu web sitesi reklam veya izleme çerezleri kullanmaz."]),
        ("11. Değişiklikler", [
            "Bu politikayı güncelleyebiliriz. En güncel sürüm her zaman bu sayfada yayımlanır."]),
        ("12. İletişim", [
            "Balloz Solutions LLC (Conveasy), 1209 Mountain Rd Pl NE STE N, Albuquerque, NM 87110, ABD. conveasyai@gmail.com"]),
     ]},
    {"id": "terms", "title": "Hizmet şartları", "updated": "Son güncelleme: 26 Ekim 2026",
     "intro": "Bu şartlar, Balloz Solutions LLC, 1209 Mountain Rd Pl NE STE N, Albuquerque, NM 87110, ABD (“biz”, “bize”) tarafından işletilen, restoranlar için bir yapay zekâ sipariş asistanı olan Conveasy için geçerlidir. Conveasy’yi kullanarak veya işletmeni ona bağlayarak bu şartları kabul etmiş olursun. Seninle ayrı bir sözleşme imzalamışsak, o sözleşme önceliklidir.",
     "sections": [
        ("1. Hizmet", ["Conveasy, restoranın için telefon aramalarını ve WhatsApp mesajlarını yanıtlar, siparişleri alır ve bunları mutfak yazıcına veya paneline (dashboard) gönderir. Özellikler, fiyatlar ve dahil olan hacimler planına bağlıdır."]),
        ("2. Hesabın", ["Doğru işletme bilgileri vermeli ve giriş bilgilerini güvende tutmalısın. Hesabındaki tüm etkinliklerden ve menünü, fiyatlarını, çalışma saatlerini, teslimat bölgelerini ve tükenen ürünleri güncel tutmaktan sen sorumlusun."]),
        ("3. Yapay zekâ ve siparişler", ["Conveasy yapay zekâ kullanır. Doğru çalışması için çok çaba gösteriyoruz, ancak örneğin bir ürünü, bir adresi veya bir saati anlarken hata yapabilir. Siparişleri kontrol etmekten, sattığın yiyeceklerden, alerjen bilgilerinden ve müşterilerinle yaptığın anlaşmalardan sorumlu olmaya devam edersin."]),
        ("4. WhatsApp ve diğer üçüncü taraf hizmetleri", ["Conveasy, WhatsApp Business Platform (Meta), Twilio ve ödeme sağlayıcıları gibi üçüncü taraf hizmetlerine dayanır. WhatsApp Business Hesabını bağlarsan, WhatsApp’ın Business Terms of Service, Business Messaging Policy ve Commerce Policy belgelerine de uymalısın. Meta, WhatsApp Business Hesabın için mesajlaşma ücretleri talep edebilir. Bu üçüncü taraf hizmetlerindeki kesintilerden veya değişikliklerden sorumlu değiliz."]),
        ("5. Kabul edilebilir kullanım", ["Conveasy’yi spam veya yasa dışı içerik göndermek, seninle iletişime geçmemiş ya da mesaj almayı kabul etmemiş kişilere mesaj göndermek veya hizmeti bozmaya, aşırı yüklemeye ya da kopyalamaya çalışmak için kullanamazsın."]),
        ("6. Ücretler ve ödeme", ["Ücretler planında veya teklifinde belirtilir. Aksi kararlaştırılmadıkça faturalar 14 gün içinde ödenmelidir. Bir fatura hatırlatmadan sonra da ödenmemiş kalırsa hizmeti askıya alabiliriz."]),
        ("7. Kişisel veriler", ["Müşterilerinin kişisel verileri bakımından veri sorumlusu sensin; biz ise senin veri işleyenin olarak hareket ederiz. Bu verileri yalnızca hizmeti sunmak için, gizlilik politikamızda açıklandığı şekilde işleriz."]),
        ("8. Kullanılabilirlik", ["Conveasy’nin her zaman kullanılabilir olmasını hedefliyoruz, ancak kesintisiz veya hatasız olacağını garanti edemeyiz."]),
        ("9. Sorumluluk", ["Yasaların izin verdiği ölçüde, toplam sorumluluğumuz, zarara yol açan olaydan önceki üç ay içinde bize ödediğin ücretlerle sınırlıdır. Kâr kaybı, sipariş kaybı veya veri kaybı gibi dolaylı zararlardan sorumlu değiliz. Bu, dolandırıcılık veya kasıtlı suistimal durumundaki sorumluluğumuzu sınırlamaz."]),
        ("10. Hizmetin sona ermesi", ["Aksi kararlaştırılmadıkça aboneliğini herhangi bir ayın sonunda sona erdirebilirsin. Bu şartları ciddi şekilde ihlal edersen hizmeti askıya alabilir veya sona erdirebiliriz. Sona ermenin ardından verilerinin dışa aktarımını isteyebilirsin; ardından bunları gizlilik politikamızda açıklandığı şekilde sileriz."]),
        ("11. Değişiklikler", ["Bu şartları değiştirebiliriz. Önemli değişiklikler yürürlüğe girmeden en az 30 gün önce seni bilgilendiririz."]),
        ("12. Uygulanacak hukuk", ["Bu şartlar, kanunlar ihtilafı kurallarına bakılmaksızın Amerika Birleşik Devletleri, New Mexico Eyaleti yasalarına tabidir. Bu şartlar veya hizmetle ilgili her türlü uyuşmazlık, New Mexico, Bernalillo County’de bulunan eyalet veya federal mahkemelerde görülür. İşletmenin bulunduğu ülkenin yasaları kapsamında sahip olduğun emredici haklar yine de geçerlidir."]),
        ("13. İletişim", ["conveasyai@gmail.com"]),
     ]},
    {"id": "data-deletion", "title": "Veri silme", "updated": "Son güncelleme: 28 Eylül 2026",
     "intro": "Kişisel verilerini silmemizi istediğin zaman bizden isteyebilirsin.",
     "sections": [
        ("Conveasy üzerinden sipariş verdiysen (telefonla veya WhatsApp ile)", [[
            "conveasyai@gmail.com adresine “Veri silme talebi” konulu bir e-posta gönder.",
            "Sipariş verirken kullandığın telefon numarasını ve mümkünse restoranın adını ekle.",
            "Talebini onaylayacak ve siparişlerini, WhatsApp yazışmalarını ve arama verilerini 30 gün içinde sileceğiz. Restoranı da bilgilendireceğiz."]]),
        ("Conveasy kullanan bir restoransan", [[
            "Conveasy hesabına bağlı e-posta adresinden conveasyai@gmail.com adresine e-posta gönder ve hesabını silmemizi iste.",
            "Ayrıca Conveasy’nin WhatsApp Business Hesabına erişimini istediğin zaman Meta Business Suite’te “Settings > Integrations > Connected apps” bölümünden kendin kaldırabilirsin.",
            "Hesap verilerini, menü verilerini, erişim belirteçlerini ve sipariş geçmişini 30 gün içinde sileriz."],
            "Faturalar gibi yasal olarak saklamakla yükümlü olduğumuz veriler, yalnızca yasanın gerektirdiği süre boyunca saklanır.",
            "Soruların mı var? conveasyai@gmail.com adresine e-posta gönder."]),
     ]},
]
