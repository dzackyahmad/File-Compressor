import heapq
import collections
import pickle

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_tree(data):
    freq = collections.Counter(data)
    heap = [Node(ch, fr) for ch, fr in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]

def build_codes(root):
    codes = {}
    def generate_codes(node, code=""):
        if node:
            if node.char is not None:
                codes[node.char] = code
            generate_codes(node.left, code + "0")
            generate_codes(node.right, code + "1")
    generate_codes(root)
    return codes

def compress(data):
    root = build_tree(data)
    codes = build_codes(root)
    encoded_data = ''.join([codes[byte] for byte in data])
    padded = encoded_data + '0' * ((8 - len(encoded_data) % 8) % 8)
    b = bytearray()
    for i in range(0, len(padded), 8):
        byte = padded[i:i+8]
        b.append(int(byte, 2))
    tree_data = pickle.dumps(root)
    tree_size = len(tree_data).to_bytes(4, 'big')
    return tree_size + tree_data + bytes(b), root

def decompress(data):
    tree_size = int.from_bytes(data[:4], 'big')
    tree_data = data[4:4+tree_size]
    root = pickle.loads(tree_data)
    encoded_data = data[4+tree_size:]
    bit_string = ''.join(f"{byte:08b}" for byte in encoded_data)

    decoded_bytes = bytearray()
    node = root
    for bit in bit_string:
        node = node.left if bit == '0' else node.right
        if node.char is not None:
            decoded_bytes.append(node.char)
            node = root

    return bytes(decoded_bytes)
