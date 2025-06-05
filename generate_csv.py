import csv

# Buat file bernama 'contoh_data.csv'
with open("contoh_input.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Header kolom
    writer.writerow(["Nama", "Umur", "Kota", "Profesi"])

    # Data baris (bisa diperbanyak untuk tes ukuran)
    for i in range(1, 15001):  # 1000 baris data
        writer.writerow([
            f"Nama{i}",
            20 + (i % 30),
            f"Kota{i % 10}",
            f"Profesi{i % 5}"
        ])

print("✅ File 'contoh_data.csv' berhasil dibuat.")
