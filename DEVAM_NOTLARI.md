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

## Henüz yapılmadı / sıradaki somut adımlar

1. Katman B taraması derinleştirilmeli: CAHS/SAHS'ın test edilen
   spesifik gen ID'leri makalenin orijinal metninden netleştirilmeli;
   RecA/Rad51 HGT bulgusunun literatürdeki tartışmalı durumu (bazı takip
   çalışmaları kontaminasyon iddia etti) kontrol edilmeli.
2. Katman A'ya isteğe bağlı metabolik modüller (antioksidan enzimler,
   trehaloz -- doğru kaynak organizmasıyla, örn. trehaloz için Artemia/
   maya, etiketlenerek) ve DODA1 (betalain) yolunun eklenmesi --
   kullanıcıyla ayrıca netleştirilecek, henüz karar verilmedi.
3. Dört projenin karşılaştırmalı bulgu tablosu (B. subtilis su-kısıtlı
   uçurum / Salinibacter uçurumsuz-doğrusal / JCVI-syn3A auxotrofi-engeli
   / Cyanothece ışık-kısıtlı+elektron-taşıma-zinciri).

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
