def read_text_file(uploaded_file):
    return uploaded_file.read().decode("utf-8")

def save_text_file(data, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)
