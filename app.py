import streamlit as st
from utils.huffman_code import compress, decompress
from utils.image_handler import image_to_bytes, bytes_to_image
from utils.file_utils import read_text_file, save_text_file
import os
import tempfile
from PIL import Image

st.set_page_config(page_title="File-Compressor", layout="centered")
st.title("📦 File-Compressor using Huffman Coding Algorithm")

# Tab Layout
tab1, tab2 = st.tabs(["🗜️ File Compressor", "📊 Huffman Visualizer"])

# === TAB 1: FILE COMPRESSOR ===
with tab1:
    mode = st.sidebar.radio("Pilih Mode:", ("Compress", "Decompress"))
    uploaded_file = st.file_uploader("Upload file:", type=["jpg", "jpeg", "png", "txt", "csv", "huff"])

    if uploaded_file:
        file_name = uploaded_file.name
        file_type = file_name.split(".")[-1].lower()

        if mode == "Compress":
            if file_type in ["jpg", "jpeg", "png"]:
                image = Image.open(uploaded_file)
                data = image_to_bytes(image)
                encoded_data, _ = compress(data)
                original_size = len(data)
                compressed_size = len(encoded_data)
                compression_ratio = compressed_size / original_size
                saving = (1 - compression_ratio) * 100

                st.image(image, caption="Original Image", use_column_width=True)
                st.write(f"Ukuran Asli: {original_size} bytes")
                st.write(f"Ukuran Setelah Kompresi: {compressed_size} bytes")
                st.write(f"Rasio Kompresi: {compression_ratio:.2f}")
                st.write(f"Penghematan: {saving:.2f}%")

                st.download_button("⬇️ Download File Kompresi", encoded_data, file_name + ".huff")

            elif file_type in ["txt", "csv"]:
                text_data = read_text_file(uploaded_file)
                data = text_data.encode()
                encoded_data, _ = compress(data)
                original_size = len(data)
                compressed_size = len(encoded_data)
                compression_ratio = compressed_size / original_size
                saving = (1 - compression_ratio) * 100

                st.text_area("Isi File:", text_data, height=200)
                st.write(f"Ukuran Asli: {original_size} bytes")
                st.write(f"Ukuran Setelah Kompresi: {compressed_size} bytes")
                st.write(f"Rasio Kompresi: {compression_ratio:.2f}")
                st.write(f"Penghematan: {saving:.2f}%")

                st.download_button("⬇️ Download File Kompresi", encoded_data, file_name + ".huff")

        elif mode == "Decompress" and file_type == "huff":
            try:
                binary_data = uploaded_file.read()
                decoded_data = decompress(binary_data)

                if decoded_data[:4] == b'\x89PNG' or decoded_data[:2] == b'\xff\xd8':
                    image = bytes_to_image(decoded_data)
                    st.image(image, caption="Hasil Dekompresi", use_column_width=True)
                    tmp_path = os.path.join(tempfile.gettempdir(), "decompressed_image.png")
                    image.save(tmp_path)
                    with open(tmp_path, "rb") as f:
                        st.download_button("⬇️ Download Gambar", f.read(), "decompressed.png")
                else:
                    text = decoded_data.decode(errors="ignore")
                    st.text_area("Hasil Dekompresi:", text, height=300)
                    st.download_button("⬇️ Download Teks", text, "decompressed.txt")

            except Exception as e:
                st.error(f"Gagal mendekompresi file: {e}")

# === TAB 2: VISUALIZER (Kosong dulu) ===
with tab2:
    st.subheader("📊 Visualisasi Huffman Tree dan Encoding")
    st.info("Visualisasi algoritma akan tersedia di sini. (Coming soon...)")
