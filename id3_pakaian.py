import math
from collections import Counter

# Data pakaian: (Warna, Ukuran, Bahan, Kategori)
ATRIBUT = ["Warna", "Ukuran", "Bahan"]
TARGET = "Kategori"
DATA = [
    ("Merah",  "S", "Katun", "Casual"),
    ("Biru",   "M", "Sutra", "Formal"),
    ("Hijau",  "L", "Wol",   "Casual"),
    ("Kuning", "S", "Sutra", "Casual"),
    ("Merah",  "M", "Katun", "Casual"),
    ("Biru",   "L", "Wol",   "Formal"),
    ("Hijau",  "S", "Katun", "Casual"),
    ("Kuning", "M", "Sutra", "Formal"),
]
BARIS = [dict(zip(ATRIBUT + [TARGET], r)) for r in DATA]

def entropy(baris):
    """Entropy kelas Kategori pada sekumpulan baris."""
    n = len(baris)
    hitung = Counter(b[TARGET] for b in baris)
    return -sum((c / n) * math.log2(c / n) for c in hitung.values())

def gain(baris, atribut):
    """Information Gain jika data dipecah berdasarkan atribut."""
    n = len(baris)
    sisa = 0.0
    for nilai in sorted({b[atribut] for b in baris}):
        sub = [b for b in baris if b[atribut] == nilai]
        sisa += len(sub) / n * entropy(sub)
    return entropy(baris) - sisa

def mayoritas(baris):
    return Counter(b[TARGET] for b in baris).most_common(1)[0][0]

def bangun_id3(baris, atribut, level=0):
    kelas = {b[TARGET] for b in baris}
    if len(kelas) == 1:                      # simpul murni -> daun
        return kelas.pop()
    if not atribut:                          # atribut habis -> suara terbanyak
        return mayoritas(baris)

    print(f"{'  ' * level}Simpul dengan {len(baris)} data, "
          f"Entropy = {entropy(baris):.4f}")
    nilai_gain = {a: gain(baris, a) for a in atribut}
    for a, g in nilai_gain.items():
        print(f"{'  ' * level}  Gain({a}) = {g:.4f}")
    terbaik = max(nilai_gain, key=nilai_gain.get)   # tie -> atribut paling awal
    print(f"{'  ' * level}  -> atribut terpilih: {terbaik}\n")

    sisa = [a for a in atribut if a != terbaik]
    cabang = {}
    for nilai in sorted({b[terbaik] for b in baris}):
        sub = [b for b in baris if b[terbaik] == nilai]
        cabang[nilai] = bangun_id3(sub, sisa, level + 1)
    return {terbaik: cabang}

def prediksi(pohon, contoh):
    while isinstance(pohon, dict):
        atribut = next(iter(pohon))
        nilai = contoh[atribut]
        if nilai not in pohon[atribut]:
            return None                      # kombinasi tidak pernah terlihat
        pohon = pohon[atribut][nilai]
    return pohon

def cetak_pohon(pohon, indent=0):
    if not isinstance(pohon, dict):
        print(" " * indent + f"=> {pohon}")
        return
    atribut = next(iter(pohon))
    for nilai, anak in pohon[atribut].items():
        print(" " * indent + f"[{atribut} = {nilai}]")
        cetak_pohon(anak, indent + 4)

if __name__ == "__main__":
    print(f"Entropy awal S = {entropy(BARIS):.4f}\n")
    pohon = bangun_id3(BARIS, ATRIBUT)

    print("=== POHON KEPUTUSAN ID3 ===")
    cetak_pohon(pohon)

    print("\n=== PREDIKSI TIAP DATA ===")
    print(f"{'No':<3}{'Warna':<8}{'Ukuran':<8}{'Bahan':<7}", end="")
    print(f"{'Aktual':<8}{'Prediksi':<9}Cocok")
    benar = 0
    for i, b in enumerate(BARIS, 1):
        p = prediksi(pohon, b)
        benar += p == b[TARGET]
        print(f"{i:<3}{b['Warna']:<8}{b['Ukuran']:<8}{b['Bahan']:<7}"
              f"{b[TARGET]:<8}{p:<9}{'ya' if p == b[TARGET] else 'tidak'}")
    print(f"\nAkurasi = {benar}/{len(BARIS)} = {benar / len(BARIS):.0%}")
