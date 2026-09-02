# Dört Model, Dört Farklı Mars Darboğazı — Karşılaştırmalı Bulgu Tablosu

IAC 2026 · IAF/IAA Space Life Sciences Symposium (A1), Paper ID 114761
kapsamındaki üç projenin (dört genom-ölçekli metabolik model) birleşik
bulguları. Yazar: Esinnur Çalışır, İstanbul Üniversitesi.

## Metodolojik uyarı — sayılar ARASINDA doğrudan karşılaştırma YAPILMAMALI

Dört model, dört FARKLI referans-ortam konvansiyonu kullanıyor (B.
subtilis/Salinibacter: tanımlı minimal ortam; JCVI-syn3A: yayınlanmış
zengin/tanımsız ortam; Cyanothece: kalibre edilmiş fotoototrofik ortam).
Bu yüzden **mutlak büyüme oranları veya esansiyel gen YÜZDELERİ modeller
arası karşılaştırılamaz** — her model sadece KENDİ referansına göre
yorumlanmalı. Karşılaştırılabilir olan şey **kalitatif darboğaz
profili** (hangi kısıt baskın, uçurum var mı, gen esansiyelliği Mars'ta
değişiyor mu).

## Özet tablo

| | **B. subtilis** (iYO844) | **Salinibacter** (iMB631) | **JCVI-syn3A** (iMMSYN) | **Cyanothece** (iCce806) |
|---|---|---|---|---|
| Proje | mars-minimal-gene-network | mars-minimal-gene-network | mars-minimal-cell-network | mars-hybrid-organism-network |
| Organizma tipi | Doğal bakteri, toprak | Doğal aşırı halofil | **Sentetik minimal hücre** | Doğal fotoototrof/diazotrof siyanobakteri |
| Gen/reaksiyon | 844 gen | ~630 gen | 155 gen / 338 rxn | 806 gen / 771 rxn |
| Referans ortam | Tanımlı minimal (glikoz) | Elle kalibre edilmiş minimal | Yayınlanmış zengin/tanımsız | Kalibre edilmiş fotoototrofik (organiksiz) |
| **Baskın Mars kısıtı** | **Su** | Yok (hiçbiri tek başına belirleyici) | **Glikoz** (organik karbon) | **Işık** |
| Feasibility profili | **Keskin uçurum** (eşik altı tamamen infeasible) | **Uçurum yok** — tamamen doğrusal | **Keskin uçurum** (glc_lb ≈-0.8/-0.75) | **Kademeli/düzgün azalma**, sadece aşırı uçta (×4.0) infeasible |
| Yapısal engel var mı | Yok | Yok | **VAR — amino asit/nükleotid/vitamin/ lipid biyosentezi TAMAMEN yok** (Mycoplasma soyunun evrimsel özelliği) → desteksiz Mars'ta **kategorik olarak imkânsız** | Yok — doğrulanmış prototrofik (organiksiz, sadece ışık+CO2+N2+mineralle feasible) |
| Gen esansiyelliği Mars'ta değişiyor mu | Hayır (171 esansiyel, değişmiyor; ilk "değişiyor" bulgusu solver-tolerance artefaktıydı, düzeltildi) | Hayır (148 esansiyel, değişmiyor) | **Evet — +4 yeni esansiyel** (referans %79.4→Mars %81.9) | **Evet, ama sadece en aşırı senaryoda — +15 yeni esansiyel** (referans %35→ ×3.5'te %36.8; ×1.5/×2.5'te değişim yok) |
| Yeni esansiyel gen(ler)in kimliği | — | — | pdhC/pta/ackA (PDH→PTA→ACK yolu — ek ATP üretimi, substrat düzeyinde fosforilasyon) | NDH-1 kompleksi + FNR + sitokrom oksidaz/redüktaz (solunum/fotosentez **elektron taşıma zinciri**) |
| Yeni esansiyel genlerin ortak teması | — | — | Enerji darboğazında **alternatif bir ATP-üretim yolu** vazgeçilmez hale geliyor | Enerji darboğazında **ana enerji-hasat makinesinin TAMAMI** kritikleşiyor |
| Model sınırlaması/dürüstlük notu | `dltABCD` genleri modelde her koşulda esansiyel ama gerçek biyolojide ölümcül değil (iYO844'ün bilinen eksikliği) | Model kürasyon kalitesi B. subtilis'ten düşük — dayanıklılığın ne kadarı gerçek halofil biyolojisi ne kadarı model esnekliği ayırt edilemiyor | NGAM'a bağlı 9 gen (ATPase×8+Protein_degrad) standart knockout'ta paradoksal davranıyor (silinince büyüme artıyor) — makale Table 4 ile çapraz kontrol edilip düzeltildi | Katalaz/SOD zaten native — "tardigrade'den ekleme" fikri gereksiz çıktı; Mars ORTAM radyasyonunun ROS baskısı fizik-temelli hesapla ihmal edilebilir bulundu (14 büyüklük mertebesi altında) |

## Dört modelin anlattığı ortak hikaye

1. **"Su kısıtlı" ve "glikoz kısıtlı" uçurumlar farklı organizmalarda farklı
   kaynaklardan geliyor** — B. subtilis'te su, JCVI-syn3A'da glikoz (organik
   karbon) baskın. Cyanothece'de ise hiçbiri değil, **ışık** baskın — çünkü
   bu tek fotoototrof model, karbon/su kısıtlarına Salinibacter gibi
   duyarsız ama enerji girdisine (ışık) çok duyarlı.
2. **Model kalitesi/organizma seçimi sonucu kökten değiştiriyor** — bu,
   B. subtilis vs Salinibacter karşılaştırmasıyla ilk kez gösterildi, JCVI-
   syn3A vs Cyanothece karşılaştırmasıyla EN ÇARPICI haliyle doğrulandı:
   aynı "Mars'ta minimal gen seti" sorusu, organizma seçimine göre
   "kategorik olarak imkânsız" (JCVI-syn3A) ile "orta düzey zorlanma"
   (Cyanothece) arasında değişebiliyor.
3. **Mars'ın enerji darboğazı, genelde TEK bir alternatif yolu değil,
   organizmanın MİMARİSİNE göre değişen bir set geni kritikleştiriyor** —
   JCVI-syn3A'da dar bir yol (4 gen), Cyanothece'de geniş bir sistem
   (15 gen, tüm elektron taşıma zinciri).
4. **Sentetik minimal hücre yaklaşımı (JCVI-syn3A) ile doğal prototrofik
   organizma yaklaşımı (Cyanothece) TAMAMEN FARKLI riskler taşıyor** —
   minimal hücre "az gen = kırılgan" değil, "az gen = yanlış ortam
   varsayımıyla tasarlanmış, o ortam dışında YAPISAL OLARAK imkânsız"
   riski taşıyor. Cyanothece gibi doğal prototroflar bu riski taşımıyor
   ama kendi doğal sınırlamalarına (ışık ihtiyacı) sahip.

## Henüz yapılmadı

- Bu tablo, üç projenin README/DEVAM_NOTLARI dosyalarına da referans
  olarak eklenmeli.
- Katman B (Cyanothece'nin yapısal/koruyucu gen taraması) henüz sadece
  bu projede var — B. subtilis/Salinibacter/JCVI-syn3A için eşdeğeri
  yapılmadı (yapılması gerekip gerekmediği ayrı bir karar).
