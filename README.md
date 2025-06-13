# 📦 File-Compressor – Huffman-Based File Compressor (Images & Text)

**File-Compressor** adalah aplikasi berbasis web yang memungkinkan pengguna untuk mengompresi dan mendekompresi file gambar (**JPG, PNG**) serta file teks (**.txt, .csv**) menggunakan **algoritma Huffman Coding**. Semua proses kompresi dan dekompresi dilakukan menggunakan implementasi manual (tanpa library built-in).

Proyek ini dibuat sebagai bagian dari tugas akhir praktikum mata kuliah **Analisis Algoritma**.

---

## 🚀 Fitur Utama

- ✅ Kompresi file teks dan gambar menggunakan algoritma Huffman (Greedy Algorithm)
- ✅ Dukungan format: `.jpg`, `.jpeg`, `.png`, `.txt`, `.csv`
- ✅ Ukuran file sebelum dan sesudah kompresi ditampilkan
- ✅ Download hasil kompresi (.huff) dan dekompresi (file asli)
- ✅ Antarmuka interaktif berbasis Streamlit
- ✅ Struktur kode modular dan terbuka untuk dikembangkan

---

## 🧠 Teknologi yang Digunakan

- **Python 3.10+**
- **Streamlit** – UI web
- **Pillow (PIL)** – pembacaan file gambar
- **NumPy** – bantuan manipulasi data
- **Huffman Coding** – kompresi lossless (greedy algorithm)

---

## 📁 Struktur Proyek

---

# File-Compressor

A simple application for compressing and decompressing files using the Huffman coding algorithm.

# File-Compressor

A simple application for compressing and decompressing files using the Huffman coding algorithm.

## Cara Menjalankan Aplikasi Secara Lokal

Ikuti langkah-langkah berikut untuk menjalankan aplikasi **File-Compressor** secara lokal di mesin Anda:

### 1. **Clone Repositori dari GitHub**

   Pertama, Anda perlu meng-clone repositori ke komputer lokal Anda. Buka terminal atau command prompt dan jalankan perintah berikut:

   git clone https://github.com/dzackyahmad/File-Compressor.git
   cd File-Compressor
   
Catatan: Pastikan Anda mengganti https://github.com/dzackyahmad/File-Compressor.git dengan URL repositori GitHub Anda.

2. Buat dan Aktivasi Virtual Environment
Setelah repositori berhasil di-clone, buatlah virtual environment untuk mengisolasi dependensi aplikasi. Jalankan perintah berikut di terminal:

Untuk Windows:
python -m venv venv
venv\Scripts\activate
Untuk macOS/Linux:
python3 -m venv venv
source venv/bin/activate
Setelah menjalankan perintah ini, Anda akan berada di dalam virtual environment yang terisolasi, yang memungkinkan Anda untuk menginstal dependensi tanpa mempengaruhi sistem Python global Anda.

3. Install Dependensi
Setelah virtual environment diaktifkan, instal semua dependensi yang diperlukan dengan menjalankan:

pip install -r requirements.txt
Perintah ini akan menginstal semua library yang diperlukan yang tercantum di dalam file requirements.txt.

4. Jalankan Aplikasi
Setelah instalasi selesai, Anda dapat menjalankan aplikasi menggunakan Streamlit dengan perintah berikut:

streamlit run app.py
Aplikasi akan berjalan di localhost, dan Anda akan melihat URL di terminal yang biasanya terlihat seperti ini:

Local URL:  http://localhost:8501
Network URL:  http://<your-ip>:8501
Buka URL tersebut di browser Anda untuk mengakses aplikasi.

Lisensi

Distribusi ini dilisensikan di bawah MIT License. Lihat file LICENSE untuk informasi lebih lanjut.


You can copy this and paste it into a `README.md` file in your project folder. Let me know if you need
