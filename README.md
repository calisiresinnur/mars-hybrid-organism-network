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

## Henüz yapılmadı (bir sonraki oturum)

1. Gerçekçi Mars ortamı kalibrasyonu (ışık şiddeti, CO2/N2 kısmi
   basınçları, su kısıtı, radyasyon→bakım enerjisi) — mars-minimal-*
   projelerindeki yöntemle.
2. Duyarlılık analizi + gen esansiyellik/silme analizi
   (SOLVER_TOLERANCE=1e-9 ile).
3. Katman A'ya antioksidan enzim / trehaloz gibi metabolik modüllerin
   (gerçek kaynak organizmasıyla — trehaloz için Artemia/maya, tardigrade
   DEĞİL — etiketlenerek) eklenmesi (isteğe bağlı, kullanıcıyla
   netleştirilecek).
4. Katman B: Dsup, CAHS/SAHS/MAHS, HSP70/20, DNA onarım genlerinin
   literatür taraması, kanıt-seviyesi tablosu.
5. Üç projenin (B. subtilis/Salinibacter/JCVI-syn3A/Cyanothece)
   karşılaştırmalı bulgu tablosu.

## Kaynaklar

- Vu TT, Stolyar SM, Pinchuk GE, et al. (2012) Genome-Scale Modeling of
  Light-Driven Reductant Partitioning and Carbon Fluxes in Diazotrophic
  Unicellular Cyanobacterium *Cyanothece* sp. ATCC 51142. *PLoS Comput
  Biol* 8(4):e1002460.
- Diğer Mars atmosfer/radyasyon kaynakları için bkz.
  [mars-minimal-gene-network README](https://github.com/calisiresinnur/mars-minimal-gene-network).
- JCVI-syn3A auxotrofi bulgusu için bkz.
  [mars-minimal-cell-network README](https://github.com/calisiresinnur/mars-minimal-cell-network).
