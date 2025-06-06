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

# Tab Layout
tab1, tab2, tab3 = st.tabs(["🗜️ File Compressor", "📊 Huffman Visualizer", "🔍 Huffman Decompress Visual"])


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

# === TAB 2: VISUALIZER ===
with tab2:
    st.markdown("<h2 style='text-align:center;'>🌲 Huffman Tree Visualizer</h2>", unsafe_allow_html=True)

    with st.container():  # Container untuk input teks
        st.markdown("### ✍️ Masukkan Teks untuk Kompresi")  # Judul input
        user_input = st.text_area("", value="aaaaabbbbbbbbbccccccccccccdddddddddddddeeeeeeeeeeeeeeeefffffffffffffffffffffffffffffffffffffffffffff")  # Text area untuk input user


    if "step_index" not in st.session_state:
        st.session_state.step_index = 0

    if st.button("🔐 Kompresi Sekarang (Visual)"):
        if not user_input.strip():
            st.warning("Silakan masukkan teks terlebih dahulu.")
        else:

            steps, code_dict, freq_table, descriptions = huffmanCoding_steps(user_input)

            st.session_state["huffman_steps"] = steps
            st.session_state["huffman_code"] = code_dict
            st.session_state["huffman_freq"] = freq_table
            st.session_state["step_descriptions"] = descriptions
            st.session_state["input_text"] = user_input
            st.session_state.step_index = 0

    if "huffman_code" in st.session_state:
        code_dict = st.session_state["huffman_code"]
        freq_table = st.session_state["huffman_freq"]
        user_input = st.session_state["input_text"]

        with st.expander("📊 Frekuensi Karakter", expanded=True):
            for char, freq in freq_table.items():
                st.markdown(f"- **'{char}'** : {freq} kali")

        if "huffman_steps" in st.session_state:
            steps = st.session_state["huffman_steps"]
            step_index = st.session_state.step_index

            st.markdown("---")
            col1, col2, col3 = st.columns([1, 5, 1])
            with col1:
                if st.button("⬅️ Prev") and step_index > 0:
                    st.session_state.step_index -= 1
                    step_index = st.session_state.step_index
            with col3:
                if st.button("Next ➡️") and step_index < len(steps) - 1:
                    st.session_state.step_index += 1
                    step_index = st.session_state.step_index

            st.markdown(f"<h3 style='text-align:center;'>🎬 Visualisasi Huffman Tree - Langkah {step_index + 1} dari {len(steps)}</h3>", unsafe_allow_html=True)
            desc_list = st.session_state["step_descriptions"]
            step_idx = st.session_state.step_index

            if step_idx < len(desc_list):
                st.info(desc_list[step_idx])

            selected_root = steps[step_idx]
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

# === TAB 3: VISUAL DECOMPRESS ===
with tab3:
    st.markdown("<h2 style='text-align:center;'>🔍 Visualisasi Dekompresi Huffman</h2>", unsafe_allow_html=True)

    default_text = "aaaaabbbbbbbbbccccccccccccdddddddddddddeeeeeeeeeeeeeeeefffffffffffffffffffffffffffffffffffffffffffff"
    user_input = st.text_area("✍️ Masukkan teks untuk dikompres", value=default_text, key="decode_input")

    if st.button("🔐 Kompres & Visualisasi Dekompresi"):

        data = user_input.encode()
        steps, code_dict, freq_table, descriptions = huffmanCoding_steps(user_input)
        final_root = steps[-1]
        bitstream = ''.join(code_dict[byte] for byte in data)
        decode_trace = get_decode_trace(final_root, bitstream)

        st.session_state["decomp_tree"] = final_root
        st.session_state["decomp_trace"] = decode_trace
        st.session_state["decomp_index"] = 0

    if "decomp_trace" in st.session_state:
        trace = st.session_state["decomp_trace"]
        root = st.session_state["decomp_tree"]
        idx = st.session_state.get("decomp_index", 0)

        st.markdown("---")
        col1, col2, col3 = st.columns([1, 5, 1])
        with col1:
            if st.button("⬅️ Prev", key="decomp_prev") and idx > 0:
                st.session_state.decomp_index -= 1
                idx = st.session_state.decomp_index
        with col3:
            if st.button("Next ➡️", key="decomp_next") and idx < len(trace) - 1:
                st.session_state.decomp_index += 1
                idx = st.session_state.decomp_index

        st.markdown(f"<h3 style='text-align:center;'>🎬 Langkah Dekompresi {idx + 1} dari {len(trace)}</h3>", unsafe_allow_html=True)

        bitpath, char = trace[idx]
        st.info(f"**Bit dibaca:** `{bitpath}` → **Karakter:** `{char}`")

        # ✅ Deskripsi arah
        arah = ' → '.join(['kanan' if b == '1' else 'kiri' for b in bitpath])
        desc = f"Menelusuri bit `{bitpath}` ({arah}), ditemukan karakter `{char}`"
        st.caption(f"🧭 {desc}")

        # ✅ Tampilkan hasil decode sementara
        decoded_so_far = ''.join(c for _, c in trace[:idx + 1])
        st.success(f"📝 Hasil Decode Sementara: `{decoded_so_far}`")

        dot = visualize_huffman_step(root, bitpath)
        st.markdown("<div style='display: flex; justify-content: center; max-width: 800px; margin: auto;'>", unsafe_allow_html=True)
        st.graphviz_chart(dot.source, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")


