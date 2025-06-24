
SISTEM FUZZY MAMDANI - EVALUASI KUALITAS TANAH

Visualisasi fungsi keanggotaan berhasil dibuat

:: STEP-BY-STEP PERHITUNGAN DATA 1.0

:: DETAIL FUZZIFIKASI
[PH]
  - Asam (trapezoid [4, 4, 5.5, 6.0]):
    x = 6.5
    Karena x <= 4 atau x >= 6.0, maka μ = 0.0
  - Normal (triangular [5.5, 6.5, 7.5]):
    x = 6.5
    Karena 6.5 <= x < 7.5, maka μ = (7.5 - x) / (7.5 - 6.5) = (7.5 - 6.5) / 1.0 = 1.000
  - Basa (trapezoid [6.5, 7.0, 9, 9]):
    x = 6.5
    Karena x <= 6.5 atau x >= 9, maka μ = 0.0

[NUTRISI]
  - Rendah (triangular [0, 0, 150]):
    x = 150.0
    Karena x <= 0 atau x >= 150, maka μ = 0.0
  - Sedang (triangular [50, 150, 250]):
    x = 150.0
    Karena 150 <= x < 250, maka μ = (250 - x) / (250 - 150) = (250 - 150.0) / 100 = 1.000
  - Tinggi (triangular [150, 350, 350]):
    x = 150.0
    Karena x <= 150 atau x >= 350, maka μ = 0.0

[LOGAM BERAT]
  - Rendah (triangular [0, 0, 15]):
    x = 12.0
    Karena 0 <= x < 15, maka μ = (15 - x) / (15 - 0) = (15 - 12.0) / 15 = 0.200
  - Sedang (triangular [5, 15, 25]):
    x = 12.0
    Karena 5 < x < 15, maka μ = (x - 5) / (15 - 5) = (12.0 - 5) / 10 = 0.700
  - Tinggi (triangular [15, 30, 30]):
    x = 12.0
    Karena x <= 15 atau x >= 30, maka μ = 0.0

[BAHAN ORGANIK]
  - Rendah (triangular [0, 0, 3]):
    x = 3.0
    Karena x <= 0 atau x >= 3, maka μ = 0.0
  - Sedang (triangular [1, 3.5, 6]):
    x = 3.0
    Karena 1 < x < 3.5, maka μ = (x - 1) / (3.5 - 1) = (3.0 - 1) / 2.5 = 0.800
  - Tinggi (triangular [4, 10, 10]):
    x = 3.0
    Karena x <= 4 atau x >= 10, maka μ = 0.0

Ringkasan Derajat Keanggotaan:
╭───────────────┬─────────┬───────────────┬─────────────────┬───────────────╮
│ Variabel      │   Nilai │   Rendah/Asam │   Sedang/Normal │   Tinggi/Basa │
├───────────────┼─────────┼───────────────┼─────────────────┼───────────────┤
│ pH            │   6.500 │         0.000 │           1.000 │         0.000 │
├───────────────┼─────────┼───────────────┼─────────────────┼───────────────┤
│ Nutrisi       │ 150.000 │         0.000 │           1.000 │         0.000 │
├───────────────┼─────────┼───────────────┼─────────────────┼───────────────┤
│ Logam Berat   │  12.000 │         0.200 │           0.700 │         0.000 │
├───────────────┼─────────┼───────────────┼─────────────────┼───────────────┤
│ Bahan Organik │   3.000 │         0.000 │           0.800 │         0.000 │
╰───────────────┴─────────┴───────────────┴─────────────────┴───────────────╯

Firing Strength (α) Setiap Aturan:
╭──────┬──────────────────────────────────────────────────────────┬─────┬──────────╮
│   No │ Rule                                                     │   α │ Output   │
├──────┼──────────────────────────────────────────────────────────┼─────┼──────────┤
│    1 │ pH normal ∧ nutrisi tinggi ∧ logam rendah → Baik         │ 0   │ Baik     │
├──────┼──────────────────────────────────────────────────────────┼─────┼──────────┤
│    2 │ (pH asam ∨ basa) ∧ nutrisi rendah ∧ logam tinggi → Buruk │ 0   │ Buruk    │
├──────┼──────────────────────────────────────────────────────────┼─────┼──────────┤
│    3 │ pH normal ∧ nutrisi sedang ∧ logam sedang → Sedang       │ 0.7 │ Sedang   │
├──────┼──────────────────────────────────────────────────────────┼─────┼──────────┤
│    4 │ bahan organik tinggi → Baik                              │ 0   │ Baik     │
├──────┼──────────────────────────────────────────────────────────┼─────┼──────────┤
│    5 │ bahan organik rendah ∧ logam tinggi → Buruk              │ 0   │ Buruk    │
├──────┼──────────────────────────────────────────────────────────┼─────┼──────────┤
│    6 │ pH normal ∧ nutrisi tinggi ∧ logam sedang → Sedang       │ 0   │ Sedang   │
╰──────┴──────────────────────────────────────────────────────────┴─────┴──────────╯

Agregasi α:
  α_buruk  = max(0.000, 0.000) = 0.000
  α_sedang = max(0.700, 0.000) = 0.700
  α_baik   = max(0.000, 0.000) = 0.000

Defuzzifikasi (Metode Centroid):
  Skor akhir = (α_buruk × z_buruk + α_sedang × z_sedang + α_baik × z_baik) / (α_buruk + α_sedang + α_baik)

Defuzzifikasi (skor akhir dari library): 50.00
Kategori: Sedang


:: STEP-BY-STEP PERHITUNGAN DATA 2.0

:: DETAIL FUZZIFIKASI
[PH]
  - Asam (trapezoid [4, 4, 5.5, 6.0]):
    x = 7.5
    Karena x <= 4 atau x >= 6.0, maka μ = 0.0
  - Normal (triangular [5.5, 6.5, 7.5]):
    x = 7.5
    Karena x <= 5.5 atau x >= 7.5, maka μ = 0.0
  - Basa (trapezoid [6.5, 7.0, 9, 9]):
    x = 7.5
    Karena 7.0 <= x <= 9, maka μ = 1.0

[NUTRISI]
  - Rendah (triangular [0, 0, 150]):
    x = 250.0
    Karena x <= 0 atau x >= 150, maka μ = 0.0
  - Sedang (triangular [50, 150, 250]):
    x = 250.0
    Karena x <= 50 atau x >= 250, maka μ = 0.0
  - Tinggi (triangular [150, 350, 350]):
    x = 250.0
    Karena 150 < x < 350, maka μ = (x - 150) / (350 - 150) = (250.0 - 150) / 200 = 0.500

[LOGAM BERAT]
  - Rendah (triangular [0, 0, 15]):
    x = 5.0
    Karena 0 <= x < 15, maka μ = (15 - x) / (15 - 0) = (15 - 5.0) / 15 = 0.667
  - Sedang (triangular [5, 15, 25]):
    x = 5.0
    Karena x <= 5 atau x >= 25, maka μ = 0.0
  - Tinggi (triangular [15, 30, 30]):
    x = 5.0
    Karena x <= 15 atau x >= 30, maka μ = 0.0

[BAHAN ORGANIK]
  - Rendah (triangular [0, 0, 3]):
    x = 6.0
    Karena x <= 0 atau x >= 3, maka μ = 0.0
  - Sedang (triangular [1, 3.5, 6]):
    x = 6.0
    Karena x <= 1 atau x >= 6, maka μ = 0.0
  - Tinggi (triangular [4, 10, 10]):
    x = 6.0
    Karena 4 < x < 10, maka μ = (x - 4) / (10 - 4) = (6.0 - 4) / 6 = 0.333

Ringkasan Derajat Keanggotaan:
╭───────────────┬─────────┬───────────────┬─────────────────┬───────────────╮
│ Variabel      │   Nilai │   Rendah/Asam │   Sedang/Normal │   Tinggi/Basa │
├───────────────┼─────────┼───────────────┼─────────────────┼───────────────┤
│ pH            │   7.500 │         0.000 │           0.000 │         1.000 │
├───────────────┼─────────┼───────────────┼─────────────────┼───────────────┤
│ Nutrisi       │ 250.000 │         0.000 │           0.000 │         0.500 │
├───────────────┼─────────┼───────────────┼─────────────────┼───────────────┤
│ Logam Berat   │   5.000 │         0.667 │           0.000 │         0.000 │
├───────────────┼─────────┼───────────────┼─────────────────┼───────────────┤
│ Bahan Organik │   6.000 │         0.000 │           0.000 │         0.333 │
╰───────────────┴─────────┴───────────────┴─────────────────┴───────────────╯

Firing Strength (α) Setiap Aturan:
╭──────┬──────────────────────────────────────────────────────────┬───────┬──────────╮
│   No │ Rule                                                     │     α │ Output   │
├──────┼──────────────────────────────────────────────────────────┼───────┼──────────┤
│    1 │ pH normal ∧ nutrisi tinggi ∧ logam rendah → Baik         │ 0     │ Baik     │
├──────┼──────────────────────────────────────────────────────────┼───────┼──────────┤
│    2 │ (pH asam ∨ basa) ∧ nutrisi rendah ∧ logam tinggi → Buruk │ 0     │ Buruk    │
├──────┼──────────────────────────────────────────────────────────┼───────┼──────────┤
│    3 │ pH normal ∧ nutrisi sedang ∧ logam sedang → Sedang       │ 0     │ Sedang   │
├──────┼──────────────────────────────────────────────────────────┼───────┼──────────┤
│    4 │ bahan organik tinggi → Baik                              │ 0.333 │ Baik     │
├──────┼──────────────────────────────────────────────────────────┼───────┼──────────┤
│    5 │ bahan organik rendah ∧ logam tinggi → Buruk              │ 0     │ Buruk    │
├──────┼──────────────────────────────────────────────────────────┼───────┼──────────┤
│    6 │ pH normal ∧ nutrisi tinggi ∧ logam sedang → Sedang       │ 0     │ Sedang   │
╰──────┴──────────────────────────────────────────────────────────┴───────┴──────────╯

Agregasi α:
  α_buruk  = max(0.000, 0.000) = 0.000
  α_sedang = max(0.000, 0.000) = 0.000
  α_baik   = max(0.000, 0.333) = 0.333

Defuzzifikasi (Metode Centroid):
  Skor akhir = (α_buruk × z_buruk + α_sedang × z_sedang + α_baik × z_baik) / (α_buruk + α_sedang + α_baik)

Defuzzifikasi (skor akhir dari library): 78.93
Kategori: Baik


:: STEP-BY-STEP PERHITUNGAN DATA 3.0

:: DETAIL FUZZIFIKASI
[PH]
  - Asam (trapezoid [4, 4, 5.5, 6.0]):
    x = 5.5
    Karena 4 <= x <= 5.5, maka μ = 1.0
  - Normal (triangular [5.5, 6.5, 7.5]):
    x = 5.5
    Karena x <= 5.5 atau x >= 7.5, maka μ = 0.0
  - Basa (trapezoid [6.5, 7.0, 9, 9]):
    x = 5.5
    Karena x <= 6.5 atau x >= 9, maka μ = 0.0

[NUTRISI]
  - Rendah (triangular [0, 0, 150]):
    x = 50.0
    Karena 0 <= x < 150, maka μ = (150 - x) / (150 - 0) = (150 - 50.0) / 150 = 0.667
  - Sedang (triangular [50, 150, 250]):
    x = 50.0
    Karena x <= 50 atau x >= 250, maka μ = 0.0
  - Tinggi (triangular [150, 350, 350]):
    x = 50.0
    Karena x <= 150 atau x >= 350, maka μ = 0.0

[LOGAM BERAT]
  - Rendah (triangular [0, 0, 15]):
    x = 25.0
    Karena x <= 0 atau x >= 15, maka μ = 0.0
  - Sedang (triangular [5, 15, 25]):
    x = 25.0
    Karena x <= 5 atau x >= 25, maka μ = 0.0
  - Tinggi (triangular [15, 30, 30]):
    x = 25.0
    Karena 15 < x < 30, maka μ = (x - 15) / (30 - 15) = (25.0 - 15) / 15 = 0.667

[BAHAN ORGANIK]
  - Rendah (triangular [0, 0, 3]):
    x = 1.0
    Karena 0 <= x < 3, maka μ = (3 - x) / (3 - 0) = (3 - 1.0) / 3 = 0.667
  - Sedang (triangular [1, 3.5, 6]):
    x = 1.0
    Karena x <= 1 atau x >= 6, maka μ = 0.0
  - Tinggi (triangular [4, 10, 10]):
    x = 1.0
    Karena x <= 4 atau x >= 10, maka μ = 0.0

Ringkasan Derajat Keanggotaan:
╭───────────────┬─────────┬───────────────┬─────────────────┬───────────────╮
│ Variabel      │   Nilai │   Rendah/Asam │   Sedang/Normal │   Tinggi/Basa │
├───────────────┼─────────┼───────────────┼─────────────────┼───────────────┤
│ pH            │   5.500 │         1.000 │           0.000 │         0.000 │
├───────────────┼─────────┼───────────────┼─────────────────┼───────────────┤
│ Nutrisi       │  50.000 │         0.667 │           0.000 │         0.000 │
├───────────────┼─────────┼───────────────┼─────────────────┼───────────────┤
│ Logam Berat   │  25.000 │         0.000 │           0.000 │         0.667 │
├───────────────┼─────────┼───────────────┼─────────────────┼───────────────┤
│ Bahan Organik │   1.000 │         0.667 │           0.000 │         0.000 │
╰───────────────┴─────────┴───────────────┴─────────────────┴───────────────╯

Firing Strength (α) Setiap Aturan:
╭──────┬──────────────────────────────────────────────────────────┬───────┬──────────╮
│   No │ Rule                                                     │     α │ Output   │
├──────┼──────────────────────────────────────────────────────────┼───────┼──────────┤
│    1 │ pH normal ∧ nutrisi tinggi ∧ logam rendah → Baik         │ 0     │ Baik     │
├──────┼──────────────────────────────────────────────────────────┼───────┼──────────┤
│    2 │ (pH asam ∨ basa) ∧ nutrisi rendah ∧ logam tinggi → Buruk │ 0.667 │ Buruk    │
├──────┼──────────────────────────────────────────────────────────┼───────┼──────────┤
│    3 │ pH normal ∧ nutrisi sedang ∧ logam sedang → Sedang       │ 0     │ Sedang   │
├──────┼──────────────────────────────────────────────────────────┼───────┼──────────┤
│    4 │ bahan organik tinggi → Baik                              │ 0     │ Baik     │
├──────┼──────────────────────────────────────────────────────────┼───────┼──────────┤
│    5 │ bahan organik rendah ∧ logam tinggi → Buruk              │ 0.667 │ Buruk    │
├──────┼──────────────────────────────────────────────────────────┼───────┼──────────┤
│    6 │ pH normal ∧ nutrisi tinggi ∧ logam sedang → Sedang       │ 0     │ Sedang   │
╰──────┴──────────────────────────────────────────────────────────┴───────┴──────────╯

Agregasi α:
  α_buruk  = max(0.667, 0.667) = 0.667
  α_sedang = max(0.000, 0.000) = 0.000
  α_baik   = max(0.000, 0.000) = 0.000

Defuzzifikasi (Metode Centroid):
  Skor akhir = (α_buruk × z_buruk + α_sedang × z_sedang + α_baik × z_baik) / (α_buruk + α_sedang + α_baik)

Defuzzifikasi (skor akhir dari library): 18.06
Kategori: Buruk


:: STEP-BY-STEP PERHITUNGAN DATA 4.0

:: DETAIL FUZZIFIKASI
[PH]
  - Asam (trapezoid [4, 4, 5.5, 6.0]):
    x = 6.8
    Karena x <= 4 atau x >= 6.0, maka μ = 0.0
  - Normal (triangular [5.5, 6.5, 7.5]):
    x = 6.8
    Karena 6.5 <= x < 7.5, maka μ = (7.5 - x) / (7.5 - 6.5) = (7.5 - 6.8) / 1.0 = 0.700
  - Basa (trapezoid [6.5, 7.0, 9, 9]):
    x = 6.8
    Karena 6.5 < x < 7.0, maka μ = (x - 6.5) / (7.0 - 6.5) = (6.8 - 6.5) / 0.5 = 0.600

[NUTRISI]
  - Rendah (triangular [0, 0, 150]):
    x = 180.0
    Karena x <= 0 atau x >= 150, maka μ = 0.0
  - Sedang (triangular [50, 150, 250]):
    x = 180.0
    Karena 150 <= x < 250, maka μ = (250 - x) / (250 - 150) = (250 - 180.0) / 100 = 0.700
  - Tinggi (triangular [150, 350, 350]):
    x = 180.0
    Karena 150 < x < 350, maka μ = (x - 150) / (350 - 150) = (180.0 - 150) / 200 = 0.150

[LOGAM BERAT]
  - Rendah (triangular [0, 0, 15]):
    x = 15.0
    Karena x <= 0 atau x >= 15, maka μ = 0.0
  - Sedang (triangular [5, 15, 25]):
    x = 15.0
    Karena 15 <= x < 25, maka μ = (25 - x) / (25 - 15) = (25 - 15.0) / 10 = 1.000
  - Tinggi (triangular [15, 30, 30]):
    x = 15.0
    Karena x <= 15 atau x >= 30, maka μ = 0.0

[BAHAN ORGANIK]
  - Rendah (triangular [0, 0, 3]):
    x = 4.0
    Karena x <= 0 atau x >= 3, maka μ = 0.0
  - Sedang (triangular [1, 3.5, 6]):
    x = 4.0
    Karena 3.5 <= x < 6, maka μ = (6 - x) / (6 - 3.5) = (6 - 4.0) / 2.5 = 0.800
  - Tinggi (triangular [4, 10, 10]):
    x = 4.0
    Karena x <= 4 atau x >= 10, maka μ = 0.0

Ringkasan Derajat Keanggotaan:
╭───────────────┬─────────┬───────────────┬─────────────────┬───────────────╮
│ Variabel      │   Nilai │   Rendah/Asam │   Sedang/Normal │   Tinggi/Basa │
├───────────────┼─────────┼───────────────┼─────────────────┼───────────────┤
│ pH            │   6.800 │         0.000 │           0.700 │         0.600 │
├───────────────┼─────────┼───────────────┼─────────────────┼───────────────┤
│ Nutrisi       │ 180.000 │         0.000 │           0.700 │         0.150 │
├───────────────┼─────────┼───────────────┼─────────────────┼───────────────┤
│ Logam Berat   │  15.000 │         0.000 │           1.000 │         0.000 │
├───────────────┼─────────┼───────────────┼─────────────────┼───────────────┤
│ Bahan Organik │   4.000 │         0.000 │           0.800 │         0.000 │
╰───────────────┴─────────┴───────────────┴─────────────────┴───────────────╯

Firing Strength (α) Setiap Aturan:
╭──────┬──────────────────────────────────────────────────────────┬──────┬──────────╮
│   No │ Rule                                                     │    α │ Output   │
├──────┼──────────────────────────────────────────────────────────┼──────┼──────────┤
│    1 │ pH normal ∧ nutrisi tinggi ∧ logam rendah → Baik         │ 0    │ Baik     │
├──────┼──────────────────────────────────────────────────────────┼──────┼──────────┤
│    2 │ (pH asam ∨ basa) ∧ nutrisi rendah ∧ logam tinggi → Buruk │ 0    │ Buruk    │
├──────┼──────────────────────────────────────────────────────────┼──────┼──────────┤
│    3 │ pH normal ∧ nutrisi sedang ∧ logam sedang → Sedang       │ 0.7  │ Sedang   │
├──────┼──────────────────────────────────────────────────────────┼──────┼──────────┤
│    4 │ bahan organik tinggi → Baik                              │ 0    │ Baik     │
├──────┼──────────────────────────────────────────────────────────┼──────┼──────────┤
│    5 │ bahan organik rendah ∧ logam tinggi → Buruk              │ 0    │ Buruk    │
├──────┼──────────────────────────────────────────────────────────┼──────┼──────────┤
│    6 │ pH normal ∧ nutrisi tinggi ∧ logam sedang → Sedang       │ 0.15 │ Sedang   │
╰──────┴──────────────────────────────────────────────────────────┴──────┴──────────╯

Agregasi α:
  α_buruk  = max(0.000, 0.000) = 0.000
  α_sedang = max(0.700, 0.150) = 0.700
  α_baik   = max(0.000, 0.000) = 0.000

Defuzzifikasi (Metode Centroid):
  Skor akhir = (α_buruk × z_buruk + α_sedang × z_sedang + α_baik × z_baik) / (α_buruk + α_sedang + α_baik)

Defuzzifikasi (skor akhir dari library): 50.00
Kategori: Sedang


:: STEP-BY-STEP PERHITUNGAN DATA 5.0

:: DETAIL FUZZIFIKASI
[PH]
  - Asam (trapezoid [4, 4, 5.5, 6.0]):
    x = 8.0
    Karena x <= 4 atau x >= 6.0, maka μ = 0.0
  - Normal (triangular [5.5, 6.5, 7.5]):
    x = 8.0
    Karena x <= 5.5 atau x >= 7.5, maka μ = 0.0
  - Basa (trapezoid [6.5, 7.0, 9, 9]):
    x = 8.0
    Karena 7.0 <= x <= 9, maka μ = 1.0

[NUTRISI]
  - Rendah (triangular [0, 0, 150]):
    x = 300.0
    Karena x <= 0 atau x >= 150, maka μ = 0.0
  - Sedang (triangular [50, 150, 250]):
    x = 300.0
    Karena x <= 50 atau x >= 250, maka μ = 0.0
  - Tinggi (triangular [150, 350, 350]):
    x = 300.0
    Karena 150 < x < 350, maka μ = (x - 150) / (350 - 150) = (300.0 - 150) / 200 = 0.750

[LOGAM BERAT]
  - Rendah (triangular [0, 0, 15]):
    x = 10.0
    Karena 0 <= x < 15, maka μ = (15 - x) / (15 - 0) = (15 - 10.0) / 15 = 0.333
  - Sedang (triangular [5, 15, 25]):
    x = 10.0
    Karena 5 < x < 15, maka μ = (x - 5) / (15 - 5) = (10.0 - 5) / 10 = 0.500
  - Tinggi (triangular [15, 30, 30]):
    x = 10.0
    Karena x <= 15 atau x >= 30, maka μ = 0.0

[BAHAN ORGANIK]
  - Rendah (triangular [0, 0, 3]):
    x = 7.0
    Karena x <= 0 atau x >= 3, maka μ = 0.0
  - Sedang (triangular [1, 3.5, 6]):
    x = 7.0
    Karena x <= 1 atau x >= 6, maka μ = 0.0
  - Tinggi (triangular [4, 10, 10]):
    x = 7.0
    Karena 4 < x < 10, maka μ = (x - 4) / (10 - 4) = (7.0 - 4) / 6 = 0.500

Ringkasan Derajat Keanggotaan:
╭───────────────┬─────────┬───────────────┬─────────────────┬───────────────╮
│ Variabel      │   Nilai │   Rendah/Asam │   Sedang/Normal │   Tinggi/Basa │
├───────────────┼─────────┼───────────────┼─────────────────┼───────────────┤
│ pH            │   8.000 │         0.000 │           0.000 │         1.000 │
├───────────────┼─────────┼───────────────┼─────────────────┼───────────────┤
│ Nutrisi       │ 300.000 │         0.000 │           0.000 │         0.750 │
├───────────────┼─────────┼───────────────┼─────────────────┼───────────────┤
│ Logam Berat   │  10.000 │         0.333 │           0.500 │         0.000 │
├───────────────┼─────────┼───────────────┼─────────────────┼───────────────┤
│ Bahan Organik │   7.000 │         0.000 │           0.000 │         0.500 │
╰───────────────┴─────────┴───────────────┴─────────────────┴───────────────╯

Firing Strength (α) Setiap Aturan:
╭──────┬──────────────────────────────────────────────────────────┬─────┬──────────╮
│   No │ Rule                                                     │   α │ Output   │
├──────┼──────────────────────────────────────────────────────────┼─────┼──────────┤
│    1 │ pH normal ∧ nutrisi tinggi ∧ logam rendah → Baik         │ 0   │ Baik     │
├──────┼──────────────────────────────────────────────────────────┼─────┼──────────┤
│    2 │ (pH asam ∨ basa) ∧ nutrisi rendah ∧ logam tinggi → Buruk │ 0   │ Buruk    │
├──────┼──────────────────────────────────────────────────────────┼─────┼──────────┤
│    3 │ pH normal ∧ nutrisi sedang ∧ logam sedang → Sedang       │ 0   │ Sedang   │
├──────┼──────────────────────────────────────────────────────────┼─────┼──────────┤
│    4 │ bahan organik tinggi → Baik                              │ 0.5 │ Baik     │
├──────┼──────────────────────────────────────────────────────────┼─────┼──────────┤
│    5 │ bahan organik rendah ∧ logam tinggi → Buruk              │ 0   │ Buruk    │
├──────┼──────────────────────────────────────────────────────────┼─────┼──────────┤
│    6 │ pH normal ∧ nutrisi tinggi ∧ logam sedang → Sedang       │ 0   │ Sedang   │
╰──────┴──────────────────────────────────────────────────────────┴─────┴──────────╯

Agregasi α:
  α_buruk  = max(0.000, 0.000) = 0.000
  α_sedang = max(0.000, 0.000) = 0.000
  α_baik   = max(0.000, 0.500) = 0.500

Defuzzifikasi (Metode Centroid):
  Skor akhir = (α_buruk × z_buruk + α_sedang × z_sedang + α_baik × z_baik) / (α_buruk + α_sedang + α_baik)

Defuzzifikasi (skor akhir dari library): 80.59
Kategori: Baik

╭──────┬──────┬───────────┬───────────────┬─────────────────┬────────┬────────────╮
│   No │   pH │   Nutrisi │   Logam Berat │   Bahan Organik │   Skor │ Kualitas   │
├──────┼──────┼───────────┼───────────────┼─────────────────┼────────┼────────────┤
│    1 │  6.5 │       150 │            12 │               3 │   50   │ Sedang     │
├──────┼──────┼───────────┼───────────────┼─────────────────┼────────┼────────────┤
│    2 │  7.5 │       250 │             5 │               6 │   78.9 │ Baik       │
├──────┼──────┼───────────┼───────────────┼─────────────────┼────────┼────────────┤
│    3 │  5.5 │        50 │            25 │               1 │   18.1 │ Buruk      │
├──────┼──────┼───────────┼───────────────┼─────────────────┼────────┼────────────┤
│    4 │  6.8 │       180 │            15 │               4 │   50   │ Sedang     │
├──────┼──────┼───────────┼───────────────┼─────────────────┼────────┼────────────┤
│    5 │  8   │       300 │            10 │               7 │   80.6 │ Baik       │
╰──────┴──────┴───────────┴───────────────┴─────────────────┴────────┴────────────╯

Dibuat Oleh
Agil Ghani Istikmal (5220411040)

Keterangan Skor
:: 0-40   => Buruk
:: 40-70  => Sedang
:: 70-100 => Baik