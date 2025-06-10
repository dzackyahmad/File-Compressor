import streamlit as st
from utils.huffman import huffmanCoding_steps  # Import fungsi untuk proses Huffman dari file huffman.py
from utils.visualizer import visualize_partial_tree, get_decode_trace, visualize_huffman_step  # Import fungsi visualisasi tree dari file visualizer.py
from utils.huffman_code import compress, decompress, build_codes, build_tree
from utils.image_handler import image_to_bytes, bytes_to_image
from utils.file_utils import read_text_file

import os
import tempfile
from PIL import Image

st.set_page_config(page_title="File-Compressor", layout="centered")
st.title("📦 File-Compressor using Huffman Coding Algorithm")

# Tab Layout: Hanya ada 2 tab sekarang
tab1, tab2 = st.tabs(["🗜️ File Compressor", "📊 Huffman Visualizer"])


# === TAB 1: FILE COMPRESSOR ===
with tab1:
    st.markdown("<h2 style='text-align:center;'>🗜️ File Compressor </h2>", unsafe_allow_html=True)
    # Mode dipilih di dalam tab, bukan di sidebar
    mode = st.radio("Pilih Mode:", ("Compress", "Decompress"), key="file_compressor_mode_tab1")
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

                # Calculate compressed bitstream size (excluding tree)
                root = build_tree(data)
                codes = build_codes(root)
                bitstream = ''.join(codes[byte] for byte in data)

                # Pad bits to make full bytes
                padding = (8 - len(bitstream) % 8) % 8
                padded_bitstream = bitstream + '0' * padding
                bitstream_bytes = len(padded_bitstream) // 8
            
                st.image(image, caption="Original Image", use_column_width=True)
                st.write(f"Ukuran Asli: {original_size} bytes")
                st.write(f"Ukuran Setelah Kompresi: {compressed_size} bytes")
                st.write(f"Ukuran Bitstream Saja (tanpa metadata pohon): {bitstream_bytes} bytes")
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
            else:
                st.warning("Tipe file tidak didukung untuk kompresi.")


        elif mode == "Decompress":
            if file_type == "huff":
                try:
                    binary_data = uploaded_file.read()
                    decoded_data = decompress(binary_data)

                    # Determine if it's an image or text/csv
                    # Check for common image magic numbers (PNG: \x89PNG, JPEG: \xff\xd8)
                    if decoded_data[:4] == b'\x89PNG' or decoded_data[:2] == b'\xff\xd8':
                        image = bytes_to_image(decoded_data)
                        st.image(image, caption="Hasil Dekompresi", use_column_width=True)
                        # Save to a temporary file for download
                        tmp_path = os.path.join(tempfile.gettempdir(), "decompressed_image.png")
                        image.save(tmp_path)
                        with open(tmp_path, "rb") as f:
                            st.download_button("⬇️ Download Gambar", f.read(), "decompressed.png")
                    else:
                        text = decoded_data.decode(errors="ignore") # Use errors="ignore" for robustness
                        st.text_area("Hasil Dekompresi:", text, height=300)
                        st.download_button("⬇️ Download Teks", text, "decompressed.txt")

                except Exception as e:
                    st.error(f"Gagal mendekompresi file: {e}. Pastikan file .huff yang diunggah valid dan cocok dengan format aslinya.")
            else:
                st.warning("Untuk dekompresi, harap unggah file berformat `.huff`.")

# === TAB 2: HUFFMAN VISUALIZER (Menggabungkan Kompresi dan Dekompresi Visual) ===
with tab2:
    st.markdown("<h2 style='text-align:center;'>📊 Huffman Visualizer</h2>", unsafe_allow_html=True)
    
    # Pilih mode visualisasi (kompresi atau dekompresi)
    visualizer_mode = st.radio("Pilih Visualisasi:", 
                                ("Huffman Tree Compression Steps", "Huffman Tree Decompression Steps"), 
                                key="visualizer_mode_tab2")

    # Inisialisasi session state untuk visualisasi jika belum ada
    if "step_index" not in st.session_state:
        st.session_state.step_index = 0
    if "decomp_index" not in st.session_state:
        st.session_state.decomp_index = 0
    if "show_huffman_visual" not in st.session_state:
        st.session_state.show_huffman_visual = False
    if "show_decomp_visual" not in st.session_state:
        st.session_state.show_decomp_visual = False
    
    # Reset visualisasi ketika mode visualizer berubah
    if st.session_state.get('last_visualizer_mode') != visualizer_mode:
        st.session_state.show_huffman_visual = False
        st.session_state.show_decomp_visual = False 
        st.session_state.step_index = 0
        st.session_state.decomp_index = 0
        st.session_state.last_visualizer_mode = visualizer_mode


    if visualizer_mode == "Huffman Tree Compression Steps":
        st.markdown("<h3 style='text-align:center;'>🌲 Visualisasi Kompresi Huffman </h3>", unsafe_allow_html=True)
        
        with st.container():  # Container untuk input teks
            st.markdown("### ✍️ Masukkan Teks untuk Visualisasi Kompresi")  # Judul input
            user_input_compress_visual = st.text_area("", value="aaaaabbbbbbbbbccccccccccccdddddddddddddeeeeeeeeeeeeeeeefffffffffffffffffffffffffffffffffffffffffffff", key="compress_visual_input")  # Text area untuk input user

        if st.button("🔐 Kompresi Sekarang (Visual)", key="trigger_compress_visual"):
            if not user_input_compress_visual.strip():
                st.warning("Silakan masukkan teks terlebih dahulu.")
            else:
                steps, code_dict, freq_table, descriptions = huffmanCoding_steps(user_input_compress_visual)

                st.session_state["huffman_steps"] = steps
                st.session_state["huffman_code"] = code_dict
                st.session_state["huffman_freq"] = freq_table
                st.session_state["input_text"] = user_input_compress_visual
                st.session_state["step_descriptions"] = descriptions
                st.session_state.step_index = 0
                st.session_state.show_huffman_visual = True # Flag to show the visual elements
                st.session_state.show_decomp_visual = False # Pastikan dekompresi tidak tampil
                st.experimental_rerun() # Rerun immediately after processing

        if st.session_state.get("show_huffman_visual", False) and "huffman_code" in st.session_state:
            code_dict = st.session_state["huffman_code"]
            freq_table = st.session_state["huffman_freq"]
            user_input = st.session_state["input_text"]

            with st.expander("📊 Frekuensi Karakter", expanded=True):
                for char, freq in freq_table.items():
                    st.markdown(f"- **'{char}'** : {freq} kali")

            if "huffman_steps" in st.session_state:
                steps = st.session_state["huffman_steps"]
                current_step_idx = st.session_state.step_index
                
                # Safety checks for index bounds
                if current_step_idx >= len(steps):
                    current_step_idx = len(steps) - 1
                    st.session_state.step_index = current_step_idx
                if current_step_idx < 0:
                    current_step_idx = 0
                    st.session_state.step_index = current_step_idx

                st.markdown("---")
                col1, col2, col3 = st.columns([1, 5, 1])
                with col1:
                    if st.button("⬅️ Prev", key="huffman_prev") and current_step_idx > 0:
                        st.session_state.step_index -= 1
                        st.experimental_rerun() 
                with col3:
                    if st.button("Next ➡️", key="huffman_next") and current_step_idx < len(steps) - 1:
                        st.session_state.step_index += 1
                        st.experimental_rerun()

                st.markdown(f"<h3 style='text-align:center;'>🎬 Visualisasi Huffman Tree - Langkah {st.session_state.step_index + 1} dari {len(steps)}</h3>", unsafe_allow_html=True)
                desc_list = st.session_state["step_descriptions"]
                
                if st.session_state.step_index < len(desc_list):
                    st.info(desc_list[st.session_state.step_index])

                selected_root = steps[st.session_state.step_index]
                dot = visualize_partial_tree(selected_root)

                st.markdown("<div style='display: flex; justify-content: center; max-width: 800px; margin: auto;'>", unsafe_allow_html=True)
                st.graphviz_chart(dot.source, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("---")

            with st.expander("🔐 Kode Huffman Tiap Karakter", expanded=True):
                for char, code in code_dict.items():
                    st.markdown(f"- **'{char}'** → `{code}`")

            st.markdown("---")
            with st.container():
                st.markdown("### 📏 Perbandingan Ukuran")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("ASCII (8-bit)", f"{len(user_input)*8} bit")
                with col2:
                    total_huffman_bits = sum(freq_table[char] * len(code_dict[char]) for char in freq_table)
                    st.metric("Huffman", f"{total_huffman_bits} bit")
                compressed_percent = (1 - total_huffman_bits / (len(user_input)*8)) * 100
                st.success(f"Penghematan ukuran data: **{compressed_percent:.2f}%**")
    
    # === Huffman Tree Decompression Steps (UI Disamakan dengan Huffman Tree Compression Steps) ===
    elif visualizer_mode == "Huffman Tree Decompression Steps":
        st.markdown("<h3 style='text-align:center;'>🔍 Visualisasi Dekompresi Huffman</h3>", unsafe_allow_html=True)

        with st.container():
            st.markdown("### ✍️ Masukkan Teks untuk Visualisasi Dekompresi")  # Judul input
            user_input_decompress_visual = st.text_area("", value="aaaaabbbbbbbbbccccccccccccdddddddddddddeeeeeeeeeeeeeeeefffffffffffffffffffffffffffffffffffffffffffff", key="decode_input_visual_common")

        if st.button("🔐 Dekompresi Sekarang (Visual)", key="trigger_decompress_visual_common"):
            if not user_input_decompress_visual.strip():
                st.warning("Silakan masukkan teks terlebih dahulu.")
            else:
                data = user_input_decompress_visual.encode()
                # Proses kompresi untuk mendapatkan pohon dan kode yang akan digunakan untuk dekompresi
                steps_for_tree, code_dict_for_decomp, freq_table_for_decomp, _ = huffmanCoding_steps(user_input_decompress_visual)
                final_root = steps_for_tree[-1] # Ambil root terakhir dari proses kompresi untuk dekompresi
                bitstream = ''.join(code_dict_for_decomp[byte] for byte in data)
                decode_trace = get_decode_trace(final_root, bitstream) # Ini adalah algoritma dekompresi

                st.session_state["decomp_tree"] = final_root
                st.session_state["decomp_trace"] = decode_trace
                st.session_state["decomp_index"] = 0
                st.session_state["decomp_code"] = code_dict_for_decomp # Simpan code_dict untuk ditampilkan
                st.session_state["decomp_freq"] = freq_table_for_decomp # Simpan freq_table untuk ditampilkan
                st.session_state["decomp_input_text"] = user_input_decompress_visual # Simpan input text
                st.session_state.show_decomp_visual = True
                st.session_state.show_huffman_visual = False # Pastikan kompresi tidak tampil
                st.experimental_rerun()

        if st.session_state.get("show_decomp_visual", False) and "decomp_trace" in st.session_state:
            trace = st.session_state["decomp_trace"]
            root = st.session_state["decomp_tree"]
            code_dict = st.session_state["decomp_code"]
            freq_table = st.session_state["decomp_freq"]
            user_input = st.session_state["decomp_input_text"]

            with st.expander("📊 Frekuensi Karakter", expanded=True):
                for char, freq in freq_table.items():
                    st.markdown(f"- **'{char}'** : {freq} kali")

            current_decomp_idx = st.session_state.get("decomp_index", 0)
            
            # Safety checks for index bounds
            if current_decomp_idx >= len(trace):
                current_decomp_idx = len(trace) - 1
                st.session_state.decomp_index = current_decomp_idx
            if current_decomp_idx < 0:
                current_decomp_idx = 0
                st.session_state.decomp_index = current_decomp_idx

            st.markdown("---")
            col1, col2, col3 = st.columns([1, 5, 1])
            with col1:
                if st.button("⬅️ Prev", key="decomp_prev_btn_common") and current_decomp_idx > 0:
                    st.session_state.decomp_index -= 1
                    st.experimental_rerun()
            with col3:
                if st.button("Next ➡️", key="decomp_next_btn_common") and current_decomp_idx < len(trace) - 1:
                    st.session_state.decomp_index += 1
                    st.experimental_rerun()

            st.markdown(f"<h3 style='text-align:center;'>🎬 Langkah Dekompresi {st.session_state.decomp_index + 1} dari {len(trace)}</h3>", unsafe_allow_html=True)

            # Bagian info dekompresi spesifik
            current_bitpath, current_char = trace[st.session_state.decomp_index]
            st.info(f"**Bit dibaca:** `{current_bitpath}` → **Karakter:** `{current_char}`")

            arah = ' → '.join(['kanan' if b == '1' else 'kiri' for b in current_bitpath])
            desc = f"Menelusuri bit `{current_bitpath}` ({arah}), ditemukan karakter `{current_char}`"
            st.caption(f"🧭 {desc}")

            decoded_so_far = ''.join(c for _, c in trace[:st.session_state.decomp_index + 1])
            st.success(f"📝 Hasil Decode Sementara: `{decoded_so_far}`")

            # Visualisasi pohon dekompresi
            dot = visualize_huffman_step(root, current_bitpath) 
            st.markdown("<div style='display: flex; justify-content: center; max-width: 800px; margin: auto;'>", unsafe_allow_html=True)
            st.graphviz_chart(dot.source, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("---")

            with st.expander("🔐 Kode Huffman Tiap Karakter", expanded=True):
                for char, code in code_dict.items():
                    st.markdown(f"- **'{char}'** → `{code}`")

            st.markdown("---")
            with st.container():
                st.markdown("### 📏 Perbandingan Ukuran")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("ASCII (8-bit)", f"{len(user_input)*8} bit")
                with col2:
                    total_huffman_bits = sum(freq_table[char] * len(code_dict[char]) for char in freq_table)
                    st.metric("Huffman", f"{total_huffman_bits} bit")
                compressed_percent = (1 - total_huffman_bits / (len(user_input)*8)) * 100
                st.success(f"Penghematan ukuran data: **{compressed_percent:.2f}%**")