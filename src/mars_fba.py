"""
Mars Yüzey Koşulları İçin Hibrit (Fotoototrof + Azot-Fikse Edici) Organizma —
Katman A: Metabolik Baz Model + Mars Kısıtları FBA

mars-hybrid-organism-network — mars-minimal-gene-network ve
mars-minimal-cell-network'ün devamı/üçüncü kardeş projesi.

## Bu projenin arka planı ve iki katmanlı mimarisi

mars-minimal-cell-network'te (JCVI-syn3A) bulunan bir tuzak nedeniyle bu
proje ayrı açıldı: JCVI-syn3A ve tüm Mycoplasma soyu, amino asit/
nükleotid/vitamin/lipid biyosentezinden TAMAMEN yoksun (evrimsel bir
özellik, minimizasyonla ilgisi yok) — desteksiz Mars yüzeyinde yapısal
olarak imkânsız. Bu projede aynı tuzağa düşmemek için PROTOTROFİK
(kendi amino asit/nükleotid ihtiyacını karşılayabilen), tercihen
FOTOOTOTROF (CO2'den kendi karbonunu üretebilen — Mars atmosferinin
%95.5'i CO2) bir baz organizma seçildi.

Ayrıca kullanıcıyla yapılan bir tartışma sonucunda ("tardigrade genlerini
ekleyebilir miyiz" sorusu), FBA'nın matematiksel bir sınırı olduğu netleşti:
FBA, S·v=0 stokiyometrik matrisini çözen bir yöntem -- sadece bir REAKSİYONU
KATALİZE EDEN genler modele girebilir (GPR kuralı üzerinden). Dsup gibi
DNA'ya fiziksel olarak bağlanan koruyucu proteinler, ya da CAHS/SAHS/MAHS
gibi yapısal intrinsically-disordered proteinler hiçbir reaksiyonu
katalize etmediği için FBA'da temsil EDİLEMEZ. Bu, gerçek JCVI-syn3.0
projesinde de görülmüş bir olgu: transpozon mutajenezi (deneysel, TÜM
gen kategorilerini kapsar) %92 in vivo esansiyellik buluyor, ama FBA
(Breuer ve ark. 2019) sadece %79 in silico esansiyellik yakalıyor --
aradaki fark tam olarak metabolik-olmayan ama esansiyel fonksiyonlar.

Bu yüzden proje İKİ AYRI KATMAN olarak tasarlandı:

  KATMAN A (bu dosya ve src/'deki diğer FBA script'leri): metabolik ağ,
  COBRApy ile ÇALIŞTIRILIR, tek-gen silme ile essentiality DOĞRUDAN
  simüle edilir. Baz organizma + üstüne eklenecek metabolik modüller
  (antioksidan enzimler, trehaloz biyosentezi vb. -- gerçek kaynak
  organizmasıyla birlikte etiketlenerek) burada yer alır.

  KATMAN B (henüz başlanmadı -- bir sonraki oturumun konusu): yapısal/
  koruyucu genler (Dsup, CAHS/SAHS/MAHS, HSP70/20, DNA onarım genleri).
  FBA ile ÇALIŞTIRILMAZ -- literatür kanıt-seviyesi ile (knockdown/RNAi
  ile esansiyelliği kanıtlanmış / sadece korunmuş / sadece upregüle)
  ayrı bir tabloda izlenir.

  Nihai "minimal gen ağı" = Katman A (FBA-esansiyel) ∪ Katman B
  (literatür-esansiyel) -- HER ZAMAN hangi genin hangi katmandan,
  hangi yöntemle geldiği açıkça etiketlenerek sunulacak, tek homojen
  bir liste gibi DEĞİL.

## Katman A baz organizma: Cyanothece sp. ATCC 51142 (iCce806)

Model kaynağı: Vu TT, Stolyar SM, Pinchuk GE, et al. (2012) "Genome-Scale
Modeling of Light-Driven Reductant Partitioning and Carbon Fluxes in
Diazotrophic Unicellular Cyanobacterium Cyanothece sp. ATCC 51142."
PLoS Comput Biol 8(4):e1002460. DOI: 10.1371/journal.pcbi.1002460
(açık erişim). Model dosyası (Dataset S1, SBML):
https://doi.org/10.1371/journal.pcbi.1002460.s001

806 gen, 771 reaksiyon (SBML'den yüklenince; makale 667 rapor ediyor --
fark muhtemelen exchange reaksiyon sayımı farkı), 689 metabolit. cobra
ile yüklenip 806 gen sayısı BİREBİR doğrulandı.

Seçim gerekçesi: (1) DOĞRULANMIŞ prototrofik -- fotoototrof (CO2+ışıktan
kendi karbonunu üretir) + diazotrof (N2'den kendi azotunu üretir), yani
JCVI-syn3A'yı batıran auxotrofi tuzağı yapısal olarak yok; (2) TEK
HÜCRELİ (fotosentez/N-fiksasyonu aynı hücrede zamansal olarak ayırıyor,
gündüz/gece döngüsü) -- Anabaena/Trichodesmium'un çok-hücre-tipli
("iki hücreli") modellerinden çok daha basit, standart tek-kompartmanlı
FBA yöntemimize doğrudan uyuyor; (3) Mars'ın en bol iki kaynağıyla
(CO2 %95.5, N2 ~%2) doğrudan çalışıyor.

## Bilinen teknik özellik: eski SBML (Level 2) formatı

Model SBML Level 2 formatında (modern FBC paketi yok), objective
katsayısı KineticLaw içinde eski usul kodlanmış -- cobra.io.read_sbml_model
bunu OTOMATİK algılamıyor (model.objective boş/0 geliyor, optimize()
sessizce 0 döndürüyor -- YANLIŞ bir "büyüme yok" sonucu gibi görünebilir,
ama gerçekte objective ayarlanmadığı için). Bu yüzden modeli_yukle()
biyokütle reaksiyonunu (`r_CYANOBM`, "Average_biomass_formation_equation")
BULUP AÇIKÇA objective olarak ayarlıyor.

Windows Unicode kullanıcı adı sorunu: aynı gzip+string çözümü burada da
geçerli (bkz. mars-minimal-gene-network/mars-minimal-cell-network).
"""

import gzip
import io
import os

import cobra

PROJE_KOKU = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_ONBELLEK = os.path.join(PROJE_KOKU, "data", "models", "iCce806.xml.gz")
BIYOKUTLE_ID = "r_CYANOBM"

SOLVER_TOLERANCE = 1e-9  # bkz. önceki iki projedeki kritik ders


def modeli_yukle():
    if not os.path.exists(MODEL_ONBELLEK):
        raise FileNotFoundError(
            f"Model önbellekte bulunamadı: {MODEL_ONBELLEK}\n"
            "Kaynak: https://doi.org/10.1371/journal.pcbi.1002460.s001 "
            "(Vu ve ark. 2012, PLoS Comput Biol, Dataset S1)"
        )
    with gzip.open(MODEL_ONBELLEK, "rt", encoding="utf-8") as f:
        sbml_metni = f.read()
    model = cobra.io.read_sbml_model(io.StringIO(sbml_metni))

    # KRİTİK: eski SBML L2 formatı objective'i otomatik taşımıyor -- açıkça ayarla
    # (bkz. modül docstring'i "Bilinen teknik özellik").
    if model.objective.expression == 0 or str(model.objective.expression) == "0":
        model.objective = BIYOKUTLE_ID

    model.solver.configuration.tolerances.feasibility = SOLVER_TOLERANCE
    print(f"Model yüklendi: {len(model.reactions)} reaksiyon, {len(model.genes)} gen, "
          f"{len(model.metabolites)} metabolit | objective: {model.objective.expression}")
    return model


def referans_buyume(model):
    baseline = model.optimize(raise_error=False)
    durum = model.solver.status
    print(f"Referans (yayınlanmış/varsayılan ortam) büyüme oranı (1/saat): "
          f"{baseline.objective_value if durum == 'optimal' else 'TANIMSIZ'} | durum: {durum}")
    return baseline


def main():
    model = modeli_yukle()
    referans_buyume(model)


if __name__ == "__main__":
    main()
