# visualizer.py

from graphviz import Digraph  # Import library untuk membuat visualisasi graf

def visualize_partial_tree(root):
    dot = Digraph()  # Membuat objek Digraph baru

    def add_nodes_edges(node, parent_id=None, edge_label=""):
        if node is None:  # Jika node kosong, keluar dari fungsi
            return

        node_id = str(id(node))  # Menggunakan id unik dari node sebagai node_id
        if node.char is not None:  # Jika node memiliki karakter (leaf node)
            label = f"{node.char} ({node.data})"  # Label berisi karakter dan frekuensi
        else:
            label = f"{node.data}"  # Jika bukan leaf, hanya tampilkan frekuensi
        dot.node(node_id, label, shape="circle", style="filled", fillcolor="lightblue")  # Tambahkan node ke graf

        if parent_id is not None:  # Jika ada parent, tambahkan edge dari parent ke node ini
            dot.edge(parent_id, node_id, label=edge_label)

        add_nodes_edges(node.left, node_id, "0")  # Rekursi ke anak kiri dengan label edge "0"
        add_nodes_edges(node.right, node_id, "1")  # Rekursi ke anak kanan dengan label edge "1"

    add_nodes_edges(root)  # Mulai rekursi dari root
    return dot  # Kembalikan objek Digraph

def visualize_huffman_step(root, active_path_bits):
    dot = Digraph()
    node_counter = [0]
    node_map = {}

    def traverse(node, path=""):
        idx = node_counter[0]
        node_id = f"n{idx}"
        label = (
            chr(node.char) if node.char is not None and isinstance(node.char, int) and 32 <= node.char <= 126
            else str(node.data)
        )
        color = "red" if path == active_path_bits else "black"
        shape = "circle" if node.char is None else "box"
        dot.node(node_id, label=label, color=color, shape=shape)
        node_map[id(node)] = node_id
        node_counter[0] += 1

        if node.left:
            left_path = path + "0"
            left_id = traverse(node.left, left_path)
            dot.edge(node_id, left_id, label="0")
        if node.right:
            right_path = path + "1"
            right_id = traverse(node.right, right_path)
            dot.edge(node_id, right_id, label="1")

        return node_id

    traverse(root)
    return dot

def get_decode_trace(root, bitstring):
    trace = []
    node = root
    path = ""
    for bit in bitstring:
        node = node.left if bit == "0" else node.right
        path += bit
        if node.char is not None:
            trace.append((path, node.char if isinstance(node.char, str) else chr(node.char)))
            node = root
            path = ""
    return trace
