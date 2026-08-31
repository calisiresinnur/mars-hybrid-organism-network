"""
Mars kısıt şiddetine duyarlılık analizi (sensitivity analysis) — Cyanothece.

mars-minimal-gene-network/mars-minimal-cell-network'teki AYNI yöntem
(şiddet ekseni t: 0=sert ilk varsayım, 1=ılımlı uç) kullanılıyor.

İlk (README'deki) bulgu: bu organizmada baskın kısıt IŞIK -- N2 (kısmi
basınç ~6500x azalsa bile) ve su tek başına belirleyici değil. Bu script
bakım çarpanının (radyasyon onarımı) etkisini de tarayarak bu bulguyu
sistematik olarak doğruluyor/görselleştiriyor.
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from mars_fba import (
    bakim_reaksiyonunu_bul,
    mars_kisitlarini_uygula,
    modeli_yukle,
    referans_buyume,
    referans_ortami_uygula,
)

PROJE_KOKU = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SONUC_KLASORU = os.path.join(PROJE_KOKU, "results")

# t=0: ilk sert varsayım (README'deki), t=1: ılımlı uç (kısıtlar tamamen gevşetilmiş).
SERT = dict(foton=0.59, n2=0.0002, h2o=1.0)
ILIMLI = dict(foton=1.0, n2=1.0, h2o=1000.0)

BAKIM_CARPANLARI = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
T_DEGERLERI = [round(i * 0.02, 2) for i in range(51)]


def kisit_degerleri(t):
    foton = SERT["foton"] + t * (ILIMLI["foton"] - SERT["foton"])
    n2 = SERT["n2"] + t * (ILIMLI["n2"] - SERT["n2"])
    h2o = SERT["h2o"] + t * (ILIMLI["h2o"] - SERT["h2o"])
    return foton, n2, h2o


def tek_nokta_calistir(model, atpm, atpm_taban, t, bakim_carpani):
    foton, n2, h2o = kisit_degerleri(t)
    mars_kisitlarini_uygula(
        model, atpm, foton_carpani=foton, n2_carpani=n2, h2o_cap=h2o,
        bakim_carpani=bakim_carpani, bakim_taban=atpm_taban, sessiz=True,
    )
    sol = model.optimize(raise_error=False)
    durum = model.solver.status
    buyume = sol.objective_value if durum == "optimal" else None
    return durum, buyume, foton, n2, h2o


def tarama_yap(model, atpm, atpm_taban):
    satirlar = []
    for bakim_x in BAKIM_CARPANLARI:
        for t in T_DEGERLERI:
            durum, buyume, foton, n2, h2o = tek_nokta_calistir(model, atpm, atpm_taban, t, bakim_x)
            satirlar.append(dict(
                bakim_carpani=bakim_x, t=t, foton_carpani=foton, n2_carpani=n2,
                h2o_cap=h2o, durum=durum, buyume=buyume,
            ))
    return pd.DataFrame(satirlar)


def grafik_ciz(df, baseline_buyume, dosya_yolu):
    fig, ax = plt.subplots(figsize=(8, 5))
    for bakim_x, grup in df.groupby("bakim_carpani"):
        gecerli = grup.dropna(subset=["buyume"]).sort_values("t")
        ax.plot(gecerli["t"], 100 * gecerli["buyume"] / baseline_buyume, marker=".", label=f"bakım ×{bakim_x}")
    ax.set_xlabel("Şiddet ekseni t  (0 = sert ilk varsayım, 1 = ılımlı uç)")
    ax.set_ylabel("Büyüme oranı (referansa göre %)")
    ax.set_title("Mars kısıt şiddetine duyarlılık analizi — Cyanothece (iCce806)")
    ax.legend(title="Bakım çarpanı")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(dosya_yolu, dpi=150)
    plt.close(fig)
    print(f"Grafik kaydedildi: {dosya_yolu}")


def main():
    os.makedirs(SONUC_KLASORU, exist_ok=True)

    model = modeli_yukle()
    referans_ortami_uygula(model)
    baseline = referans_buyume(model)
    atpm = bakim_reaksiyonunu_bul(model)
    atpm_taban = atpm.lower_bound

    df = tarama_yap(model, atpm, atpm_taban)

    csv_yolu = os.path.join(SONUC_KLASORU, "duyarlilik_sonuclari.csv")
    df.to_csv(csv_yolu, index=False)
    print(f"\nSonuçlar kaydedildi: {csv_yolu} ({len(df)} satır)")

    grafik_yolu = os.path.join(SONUC_KLASORU, "buyume_vs_siddet.png")
    grafik_ciz(df, baseline.objective_value, grafik_yolu)

    print("\n--- Özet: her bakım çarpanı için t=0 (en sert) büyüme ---")
    for bakim_x, grup in df.groupby("bakim_carpani"):
        sert_nokta = grup[grup["t"] == 0.0].iloc[0]
        durum = sert_nokta["durum"]
        buyume = sert_nokta["buyume"]
        if durum == "optimal":
            pct = 100 * buyume / baseline.objective_value
            print(f"bakım ×{bakim_x}: t=0 -> büyüme={buyume:.6f} (%{pct:.1f} referans)")
        else:
            print(f"bakım ×{bakim_x}: t=0 -> {durum}")


if __name__ == "__main__":
    main()
