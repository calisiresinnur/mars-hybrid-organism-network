"""
Tekli gen silme (single gene deletion) analizi — Cyanothece (iCce806).

Referans (kalibre edilmiş fotoototrofik ortam) + üç Mars senaryosu için
modelin 806 geninin her biri tek tek "silinip" büyüme oranı yeniden
hesaplanıyor. mars-minimal-cell-network'te canlı yakalanan İKİ kritik
derse burada baştan uyuluyor:

1. infeasible KO'larda `growth` NaN gelir -> "growth_efektif" ile 0'a
   sabitlenip esansiyellik buna göre hesaplanıyor (NaN < eşik HER ZAMAN
   False döner, bu YANLIŞLIKLA "esansiyel değil" sayar -- düzeltildi).
2. r_ATPM zaten gen-ilişkisiz (bkz. mars_fba.py) -- JCVI-syn3A'daki
   ATPase-knockout paradoksu (silinince büyüme artması) burada
   YAPISAL OLARAK oluşamaz, ayrı bir istisna listesi gerekmiyor.

Mars senaryoları, mars_duyarlilik.py sonuçlarından seçildi: t=0 (en sert
ilk varsayım) sabit tutulup üç farklı bakım çarpanı (%41, %21, %1.6
referans büyüme) test edildi -- hepsi 5x bağımsız tekrarla "optimal"
tutarlılığı doğrulanmış noktalar (bkz. DEVAM_NOTLARI.md).
"""

import os

import pandas as pd
from cobra.flux_analysis import single_gene_deletion

from mars_fba import bakim_reaksiyonunu_bul, mars_kisitlarini_uygula, modeli_yukle, referans_ortami_uygula

PROJE_KOKU = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SONUC_KLASORU = os.path.join(PROJE_KOKU, "results")

ESANSIYELLIK_ESIGI = 0.01
ISLEMCI_SAYISI = 1  # bkz. mars-minimal-cell-network'teki temkinli tercih
SOLVER_TOLERANCE = 1e-9

MARS_SENARYOLARI = [
    dict(etiket="Mars_bakim_x1.5", t=0.0, foton=0.59, n2=0.0002, h2o=1.0, bakim_carpani=1.5),
    dict(etiket="Mars_bakim_x2.5", t=0.0, foton=0.59, n2=0.0002, h2o=1.0, bakim_carpani=2.5),
    dict(etiket="Mars_bakim_x3.5", t=0.0, foton=0.59, n2=0.0002, h2o=1.0, bakim_carpani=3.5),
]


def senaryo_calistir(etiket, kisit_uygula):
    model = modeli_yukle()
    model.solver.configuration.tolerances.feasibility = SOLVER_TOLERANCE
    referans_ortami_uygula(model)
    if kisit_uygula is not None:
        kisit_uygula(model)

    wt = model.optimize(raise_error=False)
    print(f"{etiket}: WT büyüme = {wt.objective_value} (durum: {model.solver.status})")
    if model.solver.status != "optimal":
        raise RuntimeError(f"{etiket}: WT durumu optimal değil ({model.solver.status}) -- senaryo geçersiz")

    sonuc = single_gene_deletion(model, processes=ISLEMCI_SAYISI)
    sonuc = sonuc.reset_index(drop=True)
    sonuc["gen_id"] = sonuc["ids"].apply(lambda s: next(iter(s)) if s else None)
    sonuc["senaryo"] = etiket
    sonuc["wt_buyume"] = wt.objective_value
    # bkz. modül docstring'i madde 1 -- infeasible KO'lar growth_efektif=0 kabul edilir
    sonuc["growth_efektif"] = sonuc["growth"].where(sonuc["status"] == "optimal", 0.0)
    sonuc["oran"] = sonuc["growth_efektif"] / wt.objective_value
    sonuc["esansiyel"] = sonuc["oran"] < ESANSIYELLIK_ESIGI
    return sonuc[["gen_id", "senaryo", "growth", "wt_buyume", "oran", "status", "esansiyel"]]


def mars_kisiti(senaryo):
    def uygula(model):
        atpm = bakim_reaksiyonunu_bul(model)
        mars_kisitlarini_uygula(
            model, atpm, foton_carpani=senaryo["foton"], n2_carpani=senaryo["n2"],
            h2o_cap=senaryo["h2o"], bakim_carpani=senaryo["bakim_carpani"], sessiz=True,
        )
    return uygula


def main():
    os.makedirs(SONUC_KLASORU, exist_ok=True)

    tum_sonuclar = [senaryo_calistir("Referans_fotoototrofik", None)]
    for s in MARS_SENARYOLARI:
        tum_sonuclar.append(senaryo_calistir(s["etiket"], mars_kisiti(s)))

    df = pd.concat(tum_sonuclar, ignore_index=True)
    csv_yolu = os.path.join(SONUC_KLASORU, "gen_silme_sonuclari.csv")
    df.to_csv(csv_yolu, index=False)
    print(f"\nHam sonuçlar kaydedildi: {csv_yolu} ({len(df)} satır)")

    pivot = df.pivot(index="gen_id", columns="senaryo", values="esansiyel")
    referans_esansiyel = pivot["Referans_fotoototrofik"]
    mars_kolonlari = [c for c in pivot.columns if c != "Referans_fotoototrofik"]

    mars_yeni_esansiyel = pivot[(~referans_esansiyel) & pivot[mars_kolonlari].any(axis=1)].copy()
    mars_yeni_esansiyel["kac_mars_senaryosunda"] = mars_yeni_esansiyel[mars_kolonlari].sum(axis=1)
    mars_yeni_esansiyel = mars_yeni_esansiyel.sort_values("kac_mars_senaryosunda", ascending=False)
    mars_yeni_esansiyel.to_csv(os.path.join(SONUC_KLASORU, "mars_yeni_esansiyel_genler.csv"))

    mars_dispanse = pivot[referans_esansiyel & (~pivot[mars_kolonlari]).any(axis=1)].copy()
    mars_dispanse["kac_mars_senaryosunda_dispanse"] = (~mars_dispanse[mars_kolonlari]).sum(axis=1)
    mars_dispanse = mars_dispanse.sort_values("kac_mars_senaryosunda_dispanse", ascending=False)
    mars_dispanse.to_csv(os.path.join(SONUC_KLASORU, "mars_dispanse_olan_genler.csv"))

    print("\n--- Özet ---")
    for kolon in pivot.columns:
        print(f"{kolon:24s}: {int(pivot[kolon].sum()):4d} esansiyel gen / {len(pivot)}")
    print(f"\nMars'a özgü YENİ esansiyel gen adayı: {len(mars_yeni_esansiyel)}")
    print(f"Mars'ta esansiyel OLMAKTAN ÇIKAN gen: {len(mars_dispanse)}")
    if len(mars_yeni_esansiyel) > 0:
        print("  Yeni esansiyel:", ", ".join(mars_yeni_esansiyel.index.tolist()))
    if len(mars_dispanse) > 0:
        print("  Dispanse olan:", ", ".join(mars_dispanse.index.tolist()))
    print("Kaydedildi: results/mars_yeni_esansiyel_genler.csv, results/mars_dispanse_olan_genler.csv")


if __name__ == "__main__":
    main()
