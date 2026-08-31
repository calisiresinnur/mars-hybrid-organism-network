# mars-hybrid-organism-network

Mars yüzey koşullarında hayatta kalabilecek **teorik bir hibrit
organizma** için minimal gen ağını hesaplamalı incelemek — IAC 2026 ·
IAF/IAA Space Life Sciences Symposium (A1), Paper ID 114761 kapsamındaki
araştırmanın üçüncü ve son aşaması. Yazar: Esinnur Çalışır, İstanbul
Üniversitesi.

Bu proje, [mars-minimal-gene-network](https://github.com/calisiresinnur/mars-minimal-gene-network)
(B. subtilis, Salinibacter) ve
[mars-minimal-cell-network](https://github.com/calisiresinnur/mars-minimal-cell-network)
(JCVI-syn3A) projelerinin devamıdır.

## Neden bu proje ayrı açıldı: JCVI-syn3A tuzağı

mars-minimal-cell-network'te, JCVI-syn3A'nın (ve TÜM Mycoplasma soyunun)
amino asit/nükleotid/vitamin/lipid biyosentezinden **tamamen yoksun**
olduğu bulundu — bu, sentetik minimizasyonla ilgisi olmayan, onlarca
milyon yıllık bir evrimsel özellik. Desteksiz Mars yüzeyinde bu organizma
kategorik olarak imkânsız. Bu projede aynı tuzağa düşmemek için
**doğrulanmış prototrofik + fotoototrof** bir baz organizma seçildi
(detay aşağıda).

## İki katmanlı mimari

Kullanıcıyla yapılan bir tartışma ("tardigrade genlerini ekleyebilir
miyiz") sırasında FBA'nın matematiksel bir sınırı netleşti: FBA, S·v=0
stokiyometrik matrisini çözüyor — sadece bir REAKSİYONU KATALİZE EDEN
genler modele girebilir. Dsup gibi DNA'ya fiziksel bağlanan koruyucu
proteinler, ya da CAHS/SAHS/MAHS gibi yapısal intrinsically-disordered
proteinler hiçbir reaksiyonu katalize etmediği için FBA'da **temsil
edilemez**. Bu, gerçek JCVI-syn3.0/Breuer 2019 hikayesinde de görülüyor:
transpozon mutajenezi (deneysel, tüm genleri kapsar) %92 in vivo
esansiyellik buluyor, FBA ise sadece %79 in silico esansiyellik
yakalıyor — fark tam olarak metabolik-olmayan ama esansiyel fonksiyonlar.

Bu yüzden proje **iki ayrı katman** olarak tasarlandı:

- **Katman A** (bu repo, `src/`): metabolik ağ, COBRApy ile ÇALIŞTIRILIR,
  tek-gen silme ile essentiality doğrudan simüle edilir.
- **Katman B** (henüz başlanmadı): yapısal/koruyucu genler (Dsup,
  CAHS/SAHS/MAHS, HSP70/20, DNA onarım genleri). FBA ile çalıştırılmaz —
  literatür kanıt-seviyesiyle (knockdown/RNAi ile kanıtlanmış / sadece
  korunmuş / sadece upregüle) ayrı bir tabloda izlenir.

Nihai "minimal gen ağı" = Katman A (FBA-esansiyel) ∪ Katman B
(literatür-esansiyel) — her gen HANGİ katmandan, HANGİ yöntemle geldiği
açıkça etiketlenerek sunulacak, tek homojen bir liste gibi DEĞİL.

## Katman A baz organizması: Cyanothece sp. ATCC 51142 (iCce806)

**Kaynak**: Vu TT, Stolyar SM, Pinchuk GE, et al. (2012) "Genome-Scale
Modeling of Light-Driven Reductant Partitioning and Carbon Fluxes in
Diazotrophic Unicellular Cyanobacterium *Cyanothece* sp. ATCC 51142."
*PLoS Comput Biol* 8(4):e1002460. DOI:
[10.1371/journal.pcbi.1002460](https://doi.org/10.1371/journal.pcbi.1002460)
(açık erişim). Model dosyası (Dataset S1, SBML):
<https://doi.org/10.1371/journal.pcbi.1002460.s001>

**806 gen, 771 reaksiyon, 689 metabolit** (cobra ile yüklenince; makale
667 reaksiyon rapor ediyor, muhtemelen exchange sayım farkı — gen sayısı
806 birebir örtüşüyor).

### Seçim gerekçesi (adaylarla karşılaştırma)

Araştırılan diğer adaylar: Deinococcus radiodurans, Chroococcidiopsis,
Pelagibacter ubique, Rubrobacter/Kineococcus — hiçbirinin kullanılabilir
bir GEM'i yok (kapsamlı bir extremofil-GEM derlemesinde bile: Noirungsee
ve ark. 2024, PMC10866088). Cyanothece 51142 seçildi çünkü:

1. **Doğrulanmış prototrofik + fotoototrof + diazotrof** — aşağıdaki
   test bunu bağımsız olarak kanıtlıyor.
2. **Tek hücreli** (fotosentez/N-fiksasyonu aynı hücrede zamansal olarak
   ayırıyor — gündüz/gece döngüsü), Anabaena/Trichodesmium'un
   çok-hücre-tipli ("iki hücreli") modellerinden çok daha basit —
   standart tek-kompartmanlı FBA yöntemimize doğrudan uyuyor.
3. Mars'ın en bol iki kaynağıyla (CO2 %95.5, N2 ~%2) doğrudan çalışıyor.

### Doğrulama testi — organik besin OLMADAN büyüme

Modelin tüm exchange reaksiyonları (amino asitler, şekerler, organik
asitler, hatta NH4/NO2/NO3) kapatılıp SADECE ışık + CO2 + N2 (gaz
halinde, azot fiksasyonu yoluyla) + mineraller (Ca/Fe/K/Mg/Mn/Na/Zn/S/
Co/Mo/W — Mars regolitinde mevcut) açık bırakıldığında:

```
SADECE ışık+CO2+N2+mineral ile durum: optimal
Büyüme: 1.3477568611114878 (1/saat)
```

**Feasible.** JCVI-syn3A'yı batıran auxotrofi tuzağı burada yapısal
olarak yok — organizma gerçekten kendi karbonunu ve azotunu sıfırdan
üretebiliyor.

### Bilinen teknik özellik: eski SBML formatı

Model SBML Level 2 formatında (modern FBC paketi yok), objective
katsayısı KineticLaw içinde eski usul kodlanmış — `cobra.io.read_sbml_model`
bunu otomatik algılamıyor (`model.objective` boş geliyor, `optimize()`
sessizce 0 döndürüyor). `src/mars_fba.py`'deki `modeli_yukle()` biyokütle
reaksiyonunu (`r_CYANOBM`) bulup açıkça objective olarak ayarlıyor.

## Kurulum

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/mars_fba.py
```

## Repo yapısı

```
.
├── README.md
├── DEVAM_NOTLARI.md
├── requirements.txt
├── data/
│   └── models/
│       └── iCce806.xml.gz     # Cyanothece 51142 modeli (Vu ve ark. 2012, Dataset S1)
├── results/
└── src/
    └── mars_fba.py            # Model yükleme + referans büyüme (Katman A, ilk aşama)
```

## Mars kısıtları — ilk bulgu

`src/mars_fba.py`, referans olarak yukarıdaki kalibre edilmiş
fotoototrofik ortamı (foton_sınırı=8.5, gerçek 48 saatlik çiftlenme
süresine göre kalibre edildi: 0.014476/saat, hedef ln2/48=0.014441 ile
~%0.2 fark) kullanıyor. NGAM: `r_ATPM` — B. subtilis'teki ATPM ile
birebir aynı sözleşme (sabit 2.8, gen-ilişkisiz) — JCVI-syn3A'daki
ters-yön/gen-paradoksu sorunlarının HİÇBİRİ burada yok.

**Mars kısıtları** (ilk, gerekçeli varsayımlar — kesin ölçüm değil):
- Işık: Mars'ta maksimum güneş ışını Dünya'nın ~%59'u (590 W/m² vs
  1000 W/m²).
- N2: Mars'ta N2'nin MUTLAK kısmi basıncı Dünya'nınkinin ~1/6500'ü
  (Mars: %1.9 N2 × ~0.636 kPa toplam basınç ≈ 0.0121 kPa; Dünya: %78 ×
  ~101.3 kPa ≈ 79 kPa).
- CO2: Mars'ta bol (%95.5) — kısıtlayıcı değil.
- Su: önceki projelerle aynı ilk varsayım (±1.0).

**Sonuç — izole edilmiş kısıt testi**:

| Senaryo | Büyüme | Referansa göre |
|---|---|---|
| Tüm kısıtlar | 0.00737 | %51 |
| Sadece foton kısıtlı | 0.00737 | %51 (tüm kısıtlarla BİREBİR AYNI) |
| Sadece N2 kısıtlı | 0.01448 | %100 (fark yok) |
| Sadece su kısıtlı | 0.01448 | %100 (fark yok) |

**Yorum**: Bu organizmanın Mars'taki canlılığı **tamamen ışığa bağlı** —
N2 kısmi basıncı ~6500 kat azalsa bile (kendi azot fiksasyonu yeterli
geliyor) ve su kısıtlansa bile büyüme etkilenmiyor. Bu, projedeki
dördüncü ve net bir "kısıtlayıcı darboğaz" profili:

| Proje | Darboğaz profili |
|---|---|
| B. subtilis (iYO844) | Su-kısıtlı, keskin uçurum |
| Salinibacter (iMB631) | Uçurum yok, doğrusal |
| JCVI-syn3A (iMMSYN) | Auxotrofi — kategorik olarak imkânsız |
| **Cyanothece (iCce806)** | **Işık-kısıtlı, orta düzey azalma (%51), uçurum yok** |

**Henüz yapılmadı (bir sonraki oturum)**: bakım çarpanının (radyasyon)
etkisi henüz taranmadı (bu ilk testte carpani=1.0 sabit tutuldu); tam
duyarlılık analizi + gen esansiyellik analizi de bekliyor.

## Duyarlılık analizi

`src/mars_duyarlilik.py`, önceki projelerle aynı şiddet-ekseni (t: 0=sert,
1=ılımlı) ve bakım-çarpanı listesini kullanıyor. Sonuç: büyüme, bakım
çarpanı arttıkça **düzgün ve kademeli** azalıyor (uçurum yok) —
bakım×1.0'da referansın %51'i, ×2.0'da %31, ×3.0'da %11.5, ×3.5'te %1.6,
**×4.0'da infeasible**. Bu, B. subtilis'teki keskin uçurumdan farklı,
Salinibacter'in tam doğrusallığından da farklı — "kademeli aşınma +
sonunda sert bir sınır" profili. Küçük büyüme değerleri (×3.5, %1.6) 5x
bağımsız tekrarla doğrulandı, kararlı (JCVI-syn3A'daki gibi bir sınır
kırılganlığı YOK). Sonuçlar: `results/duyarlilik_sonuclari.csv`,
`results/buyume_vs_siddet.png`.

## Gen esansiyellik/silme analizi

`src/mars_gen_silme.py`, referans + üç Mars senaryosu (t=0 sabit, bakım
×1.5/×2.5/×3.5) için 806 genin tek tek silinmesini test etti. `r_ATPM`
gen-ilişkisiz olduğu için JCVI-syn3A'daki essentiality-paradoksu (silinen
NGAM geninin büyümeyi artırması) burada YAPISAL OLARAK oluşmuyor —
ayrı bir istisna/düzeltme listesi gerekmedi.

**Sonuç**:

| Senaryo | Esansiyel gen | Referansa göre |
|---|---|---|
| Referans | 282/806 (%35.0) | — |
| Mars ×1.5 | 282/806 | Değişim yok |
| Mars ×2.5 | 282/806 | Değişim yok |
| Mars ×3.5 | 297/806 (%36.8) | **+15 yeni esansiyel gen** |

**Ana bulgu — 15 yeni esansiyel gen, tamamı TEK bir biyolojik sisteme
ait**: solunum/fotosentez **elektron taşıma zinciri**:
- `cce_1176/1763/1764/2221-2224/2317-2319/4717` — **NDH-1 kompleksi**
  (proton-pompalayan NADH dehidrogenaz, Kompleks I)
- `cce_0994` — ferredoxin-NADP+ redüktaz (FNR)
- `cce_1975/1976/1977` — sitokrom c oksidaz/redüktaz kompleksleri

Yorum: ışık son derece kısıtlı VE bakım yükü en yüksekken (en aşırı
senaryo), hücre kalan az miktardaki enerjiyi eksiksiz hasat etmek için
elektron taşıma zincirinin HER bileşenine muhtaç hale geliyor — herhangi
birinin kaybı artık telafi edilemiyor. Bu, JCVI-syn3A'daki PDH→PTA→ACK
bulgusuyla (enerji darboğazının ek ATP-üretim yollarını kritikleştirmesi)
aynı ailede ama farklı bir mekanizma: orada tek bir yedek yol, burada
TÜM ana enerji-hasat makinesi kritikleşiyor. Sadece en aşırı senaryoda
(×3.5) ortaya çıkması, bu duyarlılığın gerçekten bir "son sınır" etkisi
olduğunu, ara senaryolarda (×1.5/×2.5) henüz devreye girmediğini gösteriyor.

Sonuçlar: `results/gen_silme_sonuclari.csv`,
`results/mars_yeni_esansiyel_genler.csv`, `results/mars_dispanse_olan_genler.csv`
(bu proje için de boş — hiçbir gen dispanse olmuyor).

## Katman B — yapısal/koruyucu genler (literatür taraması, ilk tur)

Dsup, CAHS/SAHS/MAHS, HSP, DNA onarım genleri ve TRID1 araştırıldı; her
biri için kaynak organizma, mekanizma ve **kanıt seviyesi** açıkça
etiketlendi (bkz. `data/katman_b_genler.csv`). Bu genler FBA ile
ÇALIŞTIRILMIYOR — hiçbiri bir metabolik reaksiyonu katalize etmiyor
(bkz. proje docstring'i). Özet:

| Protein/gen | Kanıt seviyesi |
|---|---|
| **CAHS** (2/4 test edilen gen) | ✅ **Knockdown-kanıtlı esansiyel** (Boothby ve ark. 2017, RNAi ile susturulunca kuruma direnci gerçekten düşüyor) |
| **SAHS** (1 test edilen gen) | ✅ **Knockdown-kanıtlı esansiyel** (aynı çalışma) |
| Dsup | ⚠️ Sadece kazanım-fonksiyonu (insan hücresi) — tardigrade'in kendisinde knockdown YOK |
| MAHS | ⚠️ Sadece kazanım-fonksiyonu (insan hücresi) — knockdown YOK |
| HSP70 | ⚠️ Sadece upregülasyon/korelasyon — knockdown YOK |
| HSP21/24.6/25.1/38 | ⚠️ Heterolog (bakteri) kanıt — tardigrade'de knockdown YOK. **DİKKAT**: aynı ailenin HSP17/19/20 üyeleri test edilip koruyucu etkisi OLMADIĞI bulunmuş — "HSP ailesi" diye toptan genelleme YANLIŞ |
| RecA/Rad51/Ku/umuC/Ada (HGT) | ⚠️ Sadece genom-analizi/korunmuşluk — knockdown YOK. Bu HGT bulgusu literatürde kısmen tartışmalı (bazı takip çalışmaları kontaminasyon iddia etti) — doğrulanmalı |
| TRID1/TDR1 | ⚠️ Sadece korelasyon + insan hücresinde kazanım-kanıtı — tardigrade'de CRISPR HENÜZ mümkün değil (yazarların kendi ifadesi) |
| DODA1 (betalain sentezi) | 🔄 **Bu METABOLİK bir yol — Katman A'ya aday**, Katman B değil |

**Genel gözlem**: Şu ana kadar sadece CAHS/SAHS gerçek knockdown kanıtı
taşıyor — geri kalan çoğu "gösterge/aday" seviyesinde (kazanım-fonksiyonu
veya korelasyon). Bunun nedeni kısmen metodolojik: tardigrade'lerde
CRISPR-Cas9 ile gen inaktivasyonu **henüz mümkün değil** (TRID1
makalesinin yazarlarının kendi ifadesi) — bu yüzden RNAi'nin çalıştığı
birkaç gen dışında çoğu iddia knockout/knockdown ile doğrudan test
edilemiyor.

**Henüz yapılmadı**: CAHS/SAHS için test edilen spesifik gen ID'lerinin
makale orijinal metninden netleştirilmesi; RecA/Rad51 HGT tartışmasının
derinlemesine kontrolü; DODA1'in Katman A'ya eklenip eklenmeyeceğine
karar verilmesi.

## Sıradaki adımlar

1. Katman A'ya antioksidan enzim / trehaloz gibi metabolik modüllerin
   (gerçek kaynak organizmasıyla — trehaloz için Artemia/maya, tardigrade
   DEĞİL — etiketlenerek) eklenmesi, ve DODA1 (betalain) yolunun
   değerlendirilmesi (isteğe bağlı, kullanıcıyla netleştirilecek).
2. Katman B taraması derinleştirilmeli: CAHS/SAHS'ın test edilen spesifik
   gen ID'leri, RecA/Rad51 HGT tartışmasının kontrolü.
3. Dört projenin (B. subtilis/Salinibacter/JCVI-syn3A/Cyanothece)
   karşılaştırmalı bulgu tablosu.

## Kaynaklar

- Vu TT, Stolyar SM, Pinchuk GE, et al. (2012) Genome-Scale Modeling of
  Light-Driven Reductant Partitioning and Carbon Fluxes in Diazotrophic
  Unicellular Cyanobacterium *Cyanothece* sp. ATCC 51142. *PLoS Comput
  Biol* 8(4):e1002460.
- Katman B kaynakları — tam liste ve kanıt seviyeleri için bkz.
  `data/katman_b_genler.csv`. Öne çıkanlar: Boothby ve ark. (2017) *Mol
  Cell* 65(6):975-984 (CAHS/SAHS knockdown); Hashimoto ve ark. (2016)
  *Nat Commun* 7:12808 (Dsup); Chavez ve ark. (2019) *eLife* 8:e47682
  (Dsup mekanizması); Tanaka ve ark. (2015) *PLOS ONE* 10(2):e0118272
  (MAHS); Boothby ve ark. (2015) *PNAS* 112(52):15976-15981 (DNA onarım
  genleri HGT, DODA1).
- Diğer Mars atmosfer/radyasyon kaynakları için bkz.
  [mars-minimal-gene-network README](https://github.com/calisiresinnur/mars-minimal-gene-network).
- JCVI-syn3A auxotrofi bulgusu için bkz.
  [mars-minimal-cell-network README](https://github.com/calisiresinnur/mars-minimal-cell-network).
