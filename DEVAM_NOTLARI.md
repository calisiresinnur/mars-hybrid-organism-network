# Proje Devam Notları — mars-hybrid-organism-network

Son güncelleme: 2026-08-31

Bu dosya `mars-minimal-cell-network/DEVAM_NOTLARI.md`'nin devamıdır —
JCVI-syn3A'nın auxotrofi tuzağından sonra AYRI, üçüncü bir proje olarak
açıldı. Geçmiş için önce oradaki (ve mars-minimal-gene-network'teki)
notlara bak.

## Bu oturumda yapılanlar

1. **Baz organizma araştırması ve seçimi**: Deinococcus radiodurans,
   Chroococcidiopsis, Pelagibacter ubique, Rubrobacter/Kineococcus
   araştırıldı — hiçbirinin GEM'i yok. Cyanothece sp. ATCC 51142
   (iCce806, Vu ve ark. 2012 PLoS Comput Biol) seçildi: doğrulanmış
   prototrofik + fotoototrof + diazotrof, tek hücreli.
2. **Model indirildi, doğrulandı**: 806 gen (makaleyle birebir), 771
   reaksiyon, 689 metabolit. `data/models/iCce806.xml.gz`.
3. **Eski SBML formatı sorunu çözüldü**: objective KineticLaw'da eski
   usul kodlanmış, cobra otomatik almıyor — `modeli_yukle()` `r_CYANOBM`'i
   açıkça objective yapıyor.
4. **Kritik doğrulama testi yapıldı**: TÜM organik/kompleks exchange
   reaksiyonları (amino asitler, şekerler, NH4/NO2/NO3 dahil) kapatılıp
   SADECE ışık+CO2+N2(gaz, fiksasyon)+mineral açık bırakıldığında model
   **feasible** (büyüme=1.35/saat) — JCVI-syn3A'daki auxotrofi tuzağı
   burada YOK, bağımsız olarak doğrulandı.
5. **İki katmanlı mimari netleştirildi** (kullanıcı + başka bir sohbetteki
   teknik değerlendirme birlikte): Katman A (metabolik, FBA ile
   çalıştırılır, bu repo) vs Katman B (yapısal/koruyucu -- Dsup, CAHS/
   SAHS/MAHS, HSP70/20, DNA onarım genleri -- FBA'da temsil edilemez,
   literatür kanıt-seviyesiyle ayrı izlenecek). Gerekçe: JCVI-syn3.0'da
   transpozon mutajenezi (%92 in vivo, deneysel) vs FBA (%79 in silico) --
   fark tam olarak metabolik-olmayan esansiyel fonksiyonlar.
   ÖNEMLİ DÜZELTME NOTU: trehaloz biyosentezi bir metabolik modül olarak
   eklenecekse kaynağı "tardigrade" DEĞİL, Artemia/maya olmalı --
   R. varieornatus'ta (Dsup'ın kaynağı tardigrade) trehaloz üretimi
   düşük/önemsiz, asıl mekanizma CAHS/SAHS/MAHS (yapısal, Katman B).

## Henüz yapılmadı / sıradaki somut adımlar

1. Gerçekçi Mars ortamı kalibrasyonu — ışık şiddeti (Mars'ta Dünya'nın
   ~%43'ü güneş ışığı alır, bunu ayrı araştırıp foton exchange sınırına
   çevirmek gerekecek), CO2/N2 kısmi basınçları (Cortesão 2019'daki
   %95.54 CO2/%0.03'e karşı ~2% N2), su kısıtı, radyasyon→bakım enerjisi
   (NGAM'a eşdeğer bir reaksiyon bu modelde bulunup bulunmadığı henüz
   kontrol edilmedi).
2. Duyarlılık analizi + gen esansiyellik/silme analizi
   (SOLVER_TOLERANCE=1e-9'dan başlayarak, önceki projelerdeki
   metodoloji + dersler tekrar uygulanarak -- özellikle solver
   artefaktlarına karşı REPEATED-verification disiplinini sürdür).
3. Katman A'ya isteğe bağlı metabolik modüller (antioksidan enzimler,
   trehaloz -- doğru kaynak organizmasıyla etiketlenerek) eklenmesi --
   kullanıcıyla ayrıca netleştirilecek, henüz karar verilmedi.
4. **Katman B literatür taraması** (büyük iş, ayrı bir oturum
   gerektirebilir): Dsup (Ramazzottius varieornatus), CAHS/SAHS/MAHS
   proteinleri, HSP70/HSP20, DNA onarım genleri (RecA benzeri) -- her
   biri için kaynak organizma + kanıt seviyesi (knockdown/RNAi ile
   esansiyellik kanıtlanmış / sadece korunmuşluk / sadece upregülasyon)
   etiketli bir tablo.
5. GitHub'a push (kullanıcıdan ayrıca izin istenecek -- yeni repo
   oluşturma, önceki iki projedeki gibi).
6. Üç/dört projenin karşılaştırmalı bulgu tablosu (B. subtilis su-kısıtlı
   uçurum / Salinibacter uçurumsuz-doğrusal / JCVI-syn3A auxotrofi-engeli
   / Cyanothece hibrit-tasarım).

## Genel hatırlatmalar (önceki projelerden taşınan, hâlâ geçerli)

- Windows Unicode kullanıcı adı → gzip+string SBML yükleme yöntemi.
- Solver tolerance: essentiality/gen silme analizlerinde MUTLAKA 1e-9'a
  çek; düşük-büyüme Mars senaryolarında solver artefaktları AGRESİF
  çıkabiliyor (mars-minimal-cell-network'te canlı yakalandı, birden
  fazla kez) -- her kritik sonucu 5x bağımsız (taze model) tekrarla
  doğrula.
- Essentiality mantığında infeasible KO'ları HER ZAMAN açıkça essential
  say -- NaN/status kontrolü atlanırsa "0 essential gen" gibi imkânsız
  sonuçlar çıkabiliyor (mars-minimal-cell-network'te canlı yakalandı).
- Bir "düzeltme" literatürle örtüşmeye başladığında, örtüşmenin gerekçeyi
  mi doğurduğu yoksa gerekçenin örtüşmeden bağımsız var olup olmadığı
  MUTLAKA ayrıca sorgulanmalı, sıralama şeffaf belgelenmeli (kullanıcı
  uyarısı, mars-minimal-cell-network'te).
- Kullanıcı Türkçe konuşuyor, dürüst/kaynaklı/"bulunamadı"yı da rapor
  eden üslup — literatür atıflarını asla hafızadan yazma, her zaman
  WebSearch/WebFetch ile çapraz doğrula.
