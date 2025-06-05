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

## 💡 Cara Menjalankan Aplikasi

Ikuti langkah-langkah berikut untuk menjalankan aplikasi File-Compressor secara lokal:

### 1. Clone repositori dari GitHub

```bash
git clone https://github.com/username/File-Compressor.git
cd File-Compressor

```

### 2. run venv dan activate

### python -m venv venv

### venv\Scripts\activate

### 3. pip install -r requirements.txt

### 4. streamlit run app.py
