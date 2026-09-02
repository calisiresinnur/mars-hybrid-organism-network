"""
Katman A — "tardigrade'den katalaz ekleme" fikrinin testi: SONUÇ = GEREKSİZ.

## Arka plan

Kullanıcı, tardigrade'lerde bakteriyel HGT ile doğrulanmış katalaz genini
(Yoshida ve ark. 2017, bkz. data/katman_b_genler.csv) Cyanothece bazına
"eklemeyi" istedi. Modeli kontrol edince ortaya çıktı ki: Cyanothece'nin
KENDİ katalazı (`r_CAT`) ve süperoksit dismutazı (`r_SOD`, gen: cce_1620)
ZATEN VAR, sınırsız kapasiteyle (0-1000 mmol/gDW/h) — bu beklenir, çünkü
fotosentez kendi başına ROS üretir, siyanobakteriler bu savunmayı evrimsel
olarak zaten taşır. "Ekleyecek" bir kapasite eksikliği yok.

Gerçek soru: modelde ışık/radyasyonu ROS üretimine bağlayan hiçbir
mekanizma yok (varsayılan akış = 0). Bu yüzden "Mars radyasyonu ->
zorunlu H2O2 üretimi" baskısını EKLEYİP mevcut CAT/SOD kapasitesinin
buna yetip yetmediğini test ettik.

## Türetme (fizik-temelli, ama katmanlı varsayımlar içerir — hepsi aşağıda)

1. G(H2O2) = 1.1×10⁻⁷ mol/J — su radyolizinde H2O2 verimi, gama ışınımı
   için birden fazla bağımsız çalışmada 1.0-1.2×10⁻⁷ mol/J aralığında
   tutarlı bir fizik sabiti (radyasyon kimyası literatürü).
2. Mars yüzey radyasyon dozu = 0.64 mSv/gün (Hassler ve ark. 2014,
   Science — bu proje ailesinde zaten kullanılan bir değer).
3. VARSAYIM (açıkça işaretli): Sv≈Gy (kalite faktörü QF≈1). Mars'ın
   karışık GCR alanında gerçek QF muhtemelen >1 (ağır iyon bileşeni
   var) — yani bu bir ALT SINIR/muhafazakar tahmin, gerçek H2O2 üretimi
   muhtemelen biraz daha yüksek olabilir.
4. VARSAYIM: hücre ~%75 su (yaş ağırlık), kuru ağırlık yaş ağırlığın
   ~%25'i -> 1 gDW ~ 0.004 kg yaş/sulu doku.

Sonuç: **1.17×10⁻¹¹ mmol H2O2/gDW/saat** — model kapasitesinin
(1000 mmol/gDW/h) **14 büyüklük mertebesi altında**.

## Test sonucu

| Zorlanan H2O2 akışı | Büyüme | Yorum |
|---|---|---|
| 0 (kontrol) | 0.0144755285133900 | — |
| 1.17e-11 (Mars ortam dozu, türetilmiş) | 0.0144755285133874 | Fark yok (13. ondalık basamakta) |
| 1.0 (Mars'tan ~10¹¹ kat büyük, varsayımsal) | 0.0144755285133901 | Hâlâ fark yok |
| 500 (CAT/SOD kapasitesinin yarısı) | 0.0144755285133899 | Hâlâ fark yok |
| 999 (kapasite tavanına yakın) | 0.0083883 | Gerçek maliyet başlıyor (%58 referans) |
| 1001 (kapasiteyi aşıyor) | infeasible | Sert sınır |

## Sonuç ve yorum

Mars'ın ORTAM (arka plan) radyasyon dozunun ürettiği ROS baskısı, bu
modelde herhangi bir ölçülebilir etki yaratmıyor — mevcut native
katalaz/SOD kapasitesi bunu fazlasıyla karşılıyor. **"Tardigrade'den
ekstra katalaz" fikri bu tehdit modeli altında hiçbir fayda sağlamaz.**

Bu, radyasyon direncinin önemsiz olduğu anlamına GELMİYOR — sadece bu
spesifik mekanizma (ROS/oksidatif stres) için, ORTAM doz seviyesinde,
sıradan bakteriyel/siyanobakteriyel antioksidan makinesi zaten yeterli.
Mars radyasyonunun asıl tehdidi muhtemelen DOĞRUDAN DNA hasarı (zaten
`bakım_carpani` ile ATPM üzerinden proxy'lendi) — akut yüksek-doz olaylar
(güneş parçacık olayları/SPE gibi) burada TEST EDİLMEDİ, farklı bir
senaryo, ayrı bir literatür taraması gerektirir.

NOT: 999 testindeki "gerçek maliyet" bulgusu, modelin kendi 1000
üst-sınırının (rastgele bir "big-M" varsayılan değeri, ampirik bir
fizyolojik tavan değil) yakınına dayanmanın bir sonucu — bu sınırın
kendisi gerçek bir biyolojik kapasite ölçümü değil, bu yüzden 999
civarındaki bulgu dikkatli yorumlanmalı.
"""

import cobra

from mars_fba import modeli_yukle, referans_ortami_uygula

# Türetilmiş Mars ortam radyasyon dozu H2O2 baskısı (bkz. modül docstring'i)
H2O2_MARS_MMOL_GDW_SAAT = 1.1733e-11


def h2o2_baskisi_ekle(model, zorunlu_akis):
    """Radyasyon kaynaklı H2O2 üretimini modele ekler (gen-ilişkisiz --
    su radyolizi bir enzimatik reaksiyon değil, fiziksel bir süreç)."""
    h2o2 = model.metabolites.get_by_id("m_h2o2_c")
    rxn = cobra.Reaction("r_RADYASYON_H2O2")
    rxn.name = "Radyasyon kaynaklı H2O2 üretimi (su radyolizi)"
    rxn.add_metabolites({h2o2: 1.0})
    rxn.bounds = (zorunlu_akis, zorunlu_akis)
    model.add_reactions([rxn])
    return model


def test(zorunlu_akis, etiket):
    model = modeli_yukle()
    referans_ortami_uygula(model)
    h2o2_baskisi_ekle(model, zorunlu_akis)
    sol = model.optimize(raise_error=False)
    durum = model.solver.status
    buyume = sol.objective_value if durum == "optimal" else None
    cat_flux = model.reactions.r_CAT.flux if durum == "optimal" else None
    print(f"{etiket}: durum={durum} büyüme={buyume} r_CAT_flux={cat_flux}")
    return durum, buyume


def main():
    test(0, "Baskısız (kontrol)")
    test(H2O2_MARS_MMOL_GDW_SAAT, "Mars ortam radyasyonu (türetilmiş)")
    test(1.0, "Varsayımsal: 1.0 mmol/gDW/saat")
    test(500, "Varsayımsal: 500 (kapasitenin yarısı)")
    test(999, "Varsayımsal: 999 (kapasite tavanına yakın)")
    test(1001, "Varsayımsal: 1001 (kapasiteyi aşıyor)")
    print("\nSonuç: Mars ortam dozu -> ölçülebilir etki YOK. Detay: modül docstring'i.")


if __name__ == "__main__":
    main()
