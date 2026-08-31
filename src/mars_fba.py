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


## Referans (Dünya benzeri) ortam kalibrasyonu
#
# Modelin varsayılan (tam açık) ortamı yanıltıcı -- tüm organik/kompleks
# besinler (amino asitler, şekerler vb.) de açık bırakıldığında model
# ağırlıkla HETEROTROFİK/mikst yollarla büyüyor (CO2 net SALGILANIYOR,
# tüketilmiyor -- fotoototrofi değil). Bu proje için "referans" ortam,
# organizmanın gerçek ekolojik nişini yansıtan KALİBRE EDİLMİŞ fotoototrofik
# ortam: SADECE ışık + CO2 + N2 (gaz, fiksasyon yoluyla) + mineraller açık,
# tüm organik/kompleks besinler kapalı (bkz. mars-minimal-cell-network'teki
# aynı mantık -- ama orada infeasible çıkmıştı, burada feasible).
#
# Foton sınırı, gerçek literatür büyüme oranına (Cyanothece 51142, 12s
# ışık/12s karanlık döngüsünde çiftlenme süresi ~48 saat -- Reed ve ark.
# çalışmaları, bkz. README) karşılık gelecek şekilde KALİBRE EDİLDİ:
# foton_sinir=8.5 -> büyüme=0.014476/saat (hedef ln2/48=0.014441, ~%0.2 fark).
EARTH_FOTON_SINIRI = 8.5  # kalibre edilmiş "Dünya benzeri" ışık üst sınırı

INORGANIK_ACIK = {
    "EX_m_co2_b", "EX_m_n2_b", "EX_m_h2o_b", "EX_m_h_b",
    "EX_m_photon_psii_b", "EX_m_photon_psi_b",
    "EX_m_ca2_b", "EX_m_cu2_b", "EX_m_fe2_b", "EX_m_fe3_b", "EX_m_k_b",
    "EX_m_mg2_b", "EX_m_mn2_b", "EX_m_na1_b", "EX_m_ni2_b", "EX_m_pi_b",
    "EX_m_so4_b", "EX_m_zn2_b", "EX_m_cobalt2_b", "EX_m_mobd_b", "EX_m_wo4_b",
    "EX_m_o2_b", "EX_m_hco3_b",
}


def referans_ortami_uygula(model, foton_sinir=EARTH_FOTON_SINIRI):
    """Organik/kompleks besinleri kapatır, sadece inorganik kaynakları +
    kalibre edilmiş ışığı açık bırakır. Bkz. modül docstring'i."""
    for r in model.reactions:
        if r.id.startswith("EX_m_") and r.id.endswith("_b") and r.id not in INORGANIK_ACIK:
            r.lower_bound = 0
    model.reactions.EX_m_photon_psii_b.lower_bound = -foton_sinir
    model.reactions.EX_m_photon_psi_b.lower_bound = -foton_sinir
    return model


def referans_buyume(model):
    baseline = model.optimize(raise_error=False)
    durum = model.solver.status
    print(f"Referans (kalibre edilmiş fotoototrofik ortam) büyüme oranı (1/saat): "
          f"{baseline.objective_value if durum == 'optimal' else 'TANIMSIZ'} | durum: {durum}")
    return baseline


def bakim_reaksiyonunu_bul(model):
    """NGAM: r_ATPM -- iYO844'teki ATPM ile birebir aynı sözleşme (sabit,
    gen-ilişkisiz). ATPase (JCVI-syn3A) 'dakiği yön çevirme/paradoks'
    sorunlarının HİÇBİRİ burada yok."""
    atpm = model.reactions.get_by_id("r_ATPM")
    print(f"Bakım (NGAM/ATPM) reaksiyonu: {atpm.id} | mevcut sınırlar: {atpm.bounds}")
    return atpm


def mars_kisitlarini_uygula(
    model, atpm, foton_carpani=0.59, n2_carpani=0.0002, h2o_cap=1.0,
    bakim_carpani=1.0, foton_sinir=EARTH_FOTON_SINIRI, bakim_taban=None, sessiz=False
):
    """
    Mars kısıtları (tümü ilk, gerekçeli varsayımlar -- kesin ölçüm değil,
    bkz. mars-minimal-gene-network'teki aynı dürüstlük notu):

    - foton_carpani=0.59: Mars yüzeyinde maksimum güneş ışını Dünya'nın
      ~%59'u (590 W/m² vs 1000 W/m², bkz. README > Kaynaklar).
    - n2_carpani=0.0002: Mars'ta N2'nin MUTLAK kısmi basıncı Dünya'nınkinin
      ~1/6500'ü (Mars: %1.9 N2 x ~0.636 kPa toplam basınç ≈ 0.0121 kPa;
      Dünya: %78 x ~101.3 kPa ≈ 79 kPa -- oran ≈0.000153). Bu SADECE bir
      kısmi-basınç oranı, akı sınırına birebir çevrilmesi bilimsel olarak
      kesin değil (mars-minimal-gene-network'teki O2 kısıtı notuyla aynı
      sınırlama) -- 0.0002 bu oranın gerekçeli, yuvarlak bir yaklaşığı.
    - h2o_cap=1.0: düşük su aktivitesi, önceki projelerle aynı ilk varsayım.
    - bakim_carpani: radyasyon onarımı için ek ATP -- r_ATPM'in sabit
      akışını çarpıyor (önceki projelerdeki "bakım çarpanı" yöntemiyle
      birebir aynı, r_ATPM zaten temiz/gen-ilişkisiz bir NGAM reaksiyonu).
    """
    model.reactions.EX_m_photon_psii_b.lower_bound = -foton_sinir * foton_carpani
    model.reactions.EX_m_photon_psi_b.lower_bound = -foton_sinir * foton_carpani
    model.reactions.EX_m_co2_b.lower_bound = -1000  # Mars'ta bol (%95.5) -- kısıtlayıcı olmasın
    model.reactions.EX_m_n2_b.lower_bound = -1000 * n2_carpani
    model.reactions.EX_m_h2o_b.bounds = (-h2o_cap, h2o_cap)

    taban = bakim_taban if bakim_taban is not None else atpm.lower_bound
    yeni_bakim = taban * bakim_carpani
    atpm.bounds = (yeni_bakim, yeni_bakim)
    if not sessiz:
        print(f"Mars kısıtları: foton_sinir={foton_sinir*foton_carpani:.3f}, "
              f"n2_sinir={1000*n2_carpani:.4f}, h2o_cap={h2o_cap}, "
              f"bakım(ATPM)={atpm.bounds}")
    return model


def mars_buyume(model):
    """Bkz. mars-minimal-cell-network'teki kritik ders: infeasible durumda
    objective_value ASLA gerçek bir büyüme oranı gibi raporlanmaz."""
    mars_solution = model.optimize(raise_error=False)
    durum = model.solver.status
    if durum != "optimal":
        print(f"Mars koşulunda büyüme oranı: TANIMSIZ (durum: {durum})")
    else:
        print(f"Mars koşulunda büyüme oranı (1/saat): {mars_solution.objective_value} | durum: {durum}")
    return mars_solution


def main():
    model = modeli_yukle()
    referans_ortami_uygula(model)
    baseline = referans_buyume(model)
    atpm = bakim_reaksiyonunu_bul(model)
    model = mars_kisitlarini_uygula(model, atpm)
    mars_solution = mars_buyume(model)

    print()
    print("--- Özet ---")
    print(f"Referans (kalibre edilmiş fotoototrofik ortam): {baseline.objective_value}")
    if model.solver.status == "optimal":
        print(f"Mars koşulu:                                    {mars_solution.objective_value}")
    else:
        print(f"Mars koşulu:                                    TANIMSIZ (infeasible)")


if __name__ == "__main__":
    main()
