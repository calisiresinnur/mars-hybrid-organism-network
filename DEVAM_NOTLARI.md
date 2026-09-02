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

## Devam — 2026-08-31 (aynı gün, ikinci tur: ilk Mars kısıt testi)

**TAMAMLANDI**: Işık kalibrasyonu (Mars %59 güneş ışını) + N2 kısmi
basınç kısıtı (~1/6500) + Mars kısıtlarının uygulanması. NGAM = `r_ATPM`
bulundu (B. subtilis'teki ATPM ile birebir aynı sözleşme, sabit 2.8,
gen-ilişkisiz -- JCVI-syn3A'daki ATPase paradoksu burada yok).

**Referans kalibrasyonu**: foton_sınırı=8.5 → büyüme=0.014476/saat,
gerçek literatür değerine (Cyanothece 51142, 12s ışık/12s karanlık,
çiftlenme ~48 saat → hedef ln2/48=0.014441) ~%0.2 farkla örtüşüyor.

**İlk Mars bulgusu** (bakım çarpanı henüz taranmadı, sabit 1.0):
Mars koşulunda büyüme referansın **%51'i** (0.00737/saat), infeasible
DEĞİL, keskin uçurum YOK. İzole kısıt testi: **sadece ışık kısıtı**
tüm-kısıtlarla BİREBİR aynı sonucu veriyor -- N2 (kısmi basınç ~6500x
azalsa bile) ve su hiç belirleyici değil. Yani bu organizmanın Mars
canlılığı TAMAMEN ışığa bağlı. Bu, projedeki dördüncü net "darboğaz
profili" (B. subtilis=su, Salinibacter=yok/doğrusal, JCVI-syn3A=
auxotrofi/imkânsız, Cyanothece=ışık/orta azalma). Detay: README >
"Mars kısıtları — ilk bulgu".

## Devam — 2026-08-31 (üçüncü tur: duyarlılık + gen esansiyellik analizi)

**TAMAMLANDI**: `src/mars_duyarlilik.py` ve `src/mars_gen_silme.py`.

Duyarlılık: büyüme bakım çarpanına göre DÜZGÜN azalıyor (uçurum yok),
×4.0'da infeasible. Küçük değerler (×3.5, %1.6) 5x tekrarla doğrulandı,
JCVI-syn3A'daki gibi bir kırılganlık YOK.

Gen esansiyellik: referans 282/806 (%35), Mars ×1.5/×2.5'te DEĞİŞMİYOR,
×3.5'te (en aşırı senaryo) **+15 yeni esansiyel gen** — hepsi solunum/
fotosentez elektron taşıma zincirine ait (NDH-1 kompleksi, FNR, sitokrom
oksidaz/redüktaz). r_ATPM gen-ilişkisiz olduğu için JCVI-syn3A'daki
essentiality-paradoksu burada hiç oluşmadı, ekstra düzeltme gerekmedi.
Detay: README > "Gen esansiyellik/silme analizi".

## Devam — 2026-09-01 (dördüncü tur: Katman B literatür taraması, ilk tur)

**TAMAMLANDI (ilk tur)**: Dsup, CAHS, SAHS, MAHS, HSP70, küçük HSP ailesi
(HSP17-38), RecA/Rad51/Ku/umuC/Ada (DNA onarım, HGT), TRID1/TDR1, DODA1
araştırıldı. Tablo: `data/katman_b_genler.csv` (kaynak organizma +
mekanizma + kanıt seviyesi + kaynak + notlar sütunlarıyla).

**En önemli bulgu**: Sadece **CAHS ve SAHS** gerçek knockdown/RNAi
kanıtı taşıyor (Boothby ve ark. 2017, Mol Cell — susturulunca kuruma
direnci gerçekten düşüyor). Geri kalanların (Dsup, MAHS, HSP70, TRID1,
RecA/Rad51 HGT) HEPSİ sadece kazanım-fonksiyonu (insan hücresine
transfeksiyon) veya korelasyon/genom-analizi seviyesinde -- tardigrade'in
KENDİSİNDE knockdown kanıtı YOK. Kök neden: tardigrade'lerde CRISPR-Cas9
ile gen inaktivasyonu HENÜZ mümkün değil (TRID1 makalesinin yazarlarının
kendi ifadesi) -- bu yüzden RNAi'nin çalıştığı birkaç gen dışında çoğu
iddia doğrudan test edilemiyor. Bu, Katman B'nin "literatür kanıt-
seviyesiyle izlenecek" tasarımının TAM olarak neden gerekli olduğunu
gösteren somut bir örnek.

**Önemli düzeltme/uyarı**: küçük HSP ailesinde (HSP17-38) TÜM üyeler
aynı şekilde davranmıyor -- HSP21/24.6/25.1/38 koruyucu bulunurken
HSP17/19/20 TEST EDİLİP koruyucu ETKİSİ OLMADIĞI bulunmuş. "HSP ailesi"
diye toptan genelleme yapmak YANLIŞ -- gen-spesifik olunmalı (aynı
titizlik CAHS/SAHS için de geçerli: hangi 2 CAHS geni test edildi, henüz
netleştirilmedi).

**Yan bulgu**: DODA1 (betalain sentezi, yatay gen transferiyle
kazanılmış) aslında METABOLİK bir yol (küçük molekül biyosentezi) --
Katman B değil, Katman A'ya (FBA'ya eklenebilir) aday. Henüz eklenmedi.

## Devam — 2026-09-01 (beşinci tur: RecA/Rad51 HGT derinleştirmesi)

**TAMAMLANDI**: RecA/Rad51/Ku/umuC/Ada HGT iddiasının kaynağı araştırıldı
ve ÇÖKTÜĞÜ bulundu. Zincir: Boothby ve ark. 2015 (PNAS) → %17.5 HGT iddia
etti → Koutsovoulos ve ark. 2016 (PNAS) bunun büyük ölçüde KONTAMİNASYON
ARTEFAKTI olduğunu gösterdi (düzeltilmiş: ~%0.4) → Yoshida ve ark. 2017
(PLOS Biol) yüksek kaliteli, temiz genomla ~%2.3 GERÇEK HGT doğruladı,
ama RecA/Rad51/Ku/umuC/Ada bu doğrulanmış listede YOK. Sonuç: bu satır
Katman B tablosundan (`data/katman_b_genler.csv`) çıkarıldı, ❌ olarak
işaretlendi (silinmedi -- şeffaflık için "geçersiz bulundu" notuyla
tutuluyor).

**Yan bulgu (önemli)**: Aynı derinleştirme sırasında **katalazın**
GERÇEKTEN doğrulanmış bir HGT geni olduğu bulundu (Yoshida 2017 --
tüm katalaz lokusları bakteriyel kökenli). Bu METABOLİK bir enzim
(2 H2O2 -> 2 H2O + O2) -- DODA1'den bile daha sağlam kanıt tabanlı bir
Katman A adayı (gerçek reaksiyon + gerçek doğrulanmış HGT kaynağı).
Henüz eklenmedi.

**CAHS/SAHS tam gen ID'leri**: Bu turda da doğrulanamadı -- Boothby 2017
Mol Cell'in tam metnine birden fazla yoldan (Elsevier, PubMed, UNC
kurumsal deposu) erişim denendi, hepsi engellendi/başarısız (ödeme
duvarı veya ağ sorunu). Sayısal bağlam netleşti: H. dujardini'de 17 CAHS
transkripti var, 11'i ifade ediliyor, 4'ü kuruma sırasında yüksek-
indükleniyor (13-22 kat), bu 4'ten 2'si RNAi ile test edildi. İsimler
(ör. "CAHS1/CAHS8" gibi) hâlâ eksik -- kurumsal erişimle tekrar
denenmeli.

## Devam — 2026-09-01 (altıncı tur: katalaz testi -- SONUÇ negatif)

**TAMAMLANDI**: Kullanıcı "en sağlam kanıtlıdan başla" dedi -> katalaz.
Modeli kontrol edince ortaya çıktı: Cyanothece'nin KENDİ katalazı
(`r_CAT`) ve SOD'u (`r_SOD`, gen cce_1620) ZATEN VAR, sınırsız
kapasiteyle -- "tardigrade'den ekleme" fikri anlamsızlaştı (eklenecek
kapasite eksikliği yok).

Bunun yerine gerçek soruyu test ettik: modelde radyasyon->ROS bağlantısı
yok, bu yüzden fizik-temelli (G-değeri, su radyolizi, 1.1e-7 mol/J) bir
"Mars radyasyonu -> zorunlu H2O2 üretimi" baskısı türetildi (0.64 mSv/gün
x G-değeri x hücre-su-oranı varsayımları -> 1.17e-11 mmol/gDW/saat) ve
test edildi: `src/katman_a_ros_testi.py`.

**SONUÇ: negatif/gereksiz**. Mars ortam dozu, model kapasitesinin
(1000) 14 büyüklük mertebesi altında -- büyümede ÖLÇÜLEBİLİR HİÇBİR ETKİ
yok. Gerçek maliyet ancak kapasite tavanına (999-1000) çok yakın
zorlanan akışlarda başlıyor, Mars'ın gerçek dozundan ~10^14 kat uzakta.
Yorum: bu tehdit modelinde ekstra katalaz FAYDASIZ; radyasyonun asıl
tehdidi muhtemelen doğrudan DNA hasarı (zaten bakım_carpani ile
proxy'leniyor), akut yüksek-doz olaylar (SPE) ayrı, test edilmedi.

Bu, "en sağlam kanıtlı olandan başla" stratejisinin DEĞERİNİ gösteren
bir örnek: erken bir negatif sonuç, zaman kaybını (DODA1/trehaloz gibi
daha karmaşık eklemelere geçmeden önce) önledi.

## Devam — 2026-09-01 (yedinci tur: DODA1 araştırması + dört-proje karşılaştırma tablosu)

**DODA1 araştırması**: Betalamik asit üretimi (DODA enzimi) gerçekten
**Anabaena cylindrica adlı bir siyanobakteride** (Cyanothece ile aynı
filum) klonlanıp karakterize edilmiş bulundu ("AcDODA", 17.8 kDa
homodimer) -- bitkiden ödünç almaya göre çok daha savunulabilir bir
kaynak. Ama tirozin->DOPA adımı hâlâ bitki kaynaklı (CYP76AD1) olurdu.
Kullanıcıyla karar: katalaz testi zaten negatif çıktığı (Mars ortam
radyasyonunun ROS baskısı ihmal edilebilir) için DODA1 de muhtemelen
aynı sonucu verir -- **DODA1 BEKLEMEDE**, öncelik dört-proje
karşılaştırma tablosuna verildi.

**TAMAMLANDI**: `KARSILASTIRMA.md` -- dört modelin (B. subtilis/
Salinibacter/JCVI-syn3A/Cyanothece) bulgularını bir araya getiren sentez
belgesi. ÖNEMLİ metodolojik uyarı: dört model FARKLI referans-ortam
konvansiyonu kullandığı için MUTLAK sayılar (büyüme oranı, esansiyel gen
YÜZDESİ) modeller arası karşılaştırılamaz -- sadece KALİTATİF darboğaz
profili karşılaştırılabilir. Ana senteze bkz. o dosya.

## Henüz yapılmadı / sıradaki somut adımlar

1. CAHS/SAHS'ın tam gen ID'leri (kurumsal erişim veya farklı kaynakla
   tekrar denenmeli).
2. DODA1 (beklemede, düşük öncelik) ve isteğe bağlı trehaloz modülü.
3. `KARSILASTIRMA.md`'ye üç kardeş projenin README/DEVAM_NOTLARI'ndan
   referans eklenmesi (mars-minimal-gene-network,
   mars-minimal-cell-network).

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
