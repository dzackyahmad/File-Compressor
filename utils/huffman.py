class Node:
    def __init__(self, data, char=None):
        self.data = data
        self.char = char          # Harus int (karakter dalam byte)
        self.left = None
        self.right = None

class PriorityQueue:
    def __init__(self):
        self.items = []

    def push(self, node):
        self.items.append(node)
        self.items.sort(key=lambda x: x.data)

    def popMin(self):
        return self.items.pop(0)

    def size(self):
        return len(self.items)

def generate_code(node, current_code, code_dict):
    if node.left is None and node.right is None:
        code_dict[node.char] = current_code  # char harus integer
        return
    generate_code(node.left, current_code + "0", code_dict)
    generate_code(node.right, current_code + "1", code_dict)

def build_frequency_table(data_bytes):
    freq = {}
    for byte in data_bytes:  # byte: int 0–255
        freq[byte] = freq.get(byte, 0) + 1
    return freq

def huffmanCoding_steps(text_input):
    # ✅ Langkah penting: ubah string ke bytes dulu
    data = text_input.encode()  # b'aaaa...' ➜ list of int
    freq_table = build_frequency_table(data)

    pq = PriorityQueue()
    for byte, freq in freq_table.items():
        pq.push(Node(freq, byte))  # Simpan byte sebagai int

    steps = []
    step_descriptions = []

    while pq.size() > 1:
        left = pq.popMin()
        right = pq.popMin()
        merged = Node(left.data + right.data)
        merged.left = left
        merged.right = right
        pq.push(merged)

        desc = f"Menggabungkan node "
        desc += f"'{chr(left.char)}' ({left.data})" if left.char is not None and 32 <= left.char <= 126 else f"({left.data})"
        desc += " dan "
        desc += f"'{chr(right.char)}' ({right.data})" if right.char is not None and 32 <= right.char <= 126 else f"({right.data})"
        desc += f" menjadi node ({merged.data})"
        step_descriptions.append(desc)
        steps.append(merged)

    root = pq.popMin()
    code_dict = {}
    generate_code(root, "", code_dict)

    return steps, code_dict, freq_table, step_descriptions
