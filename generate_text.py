with open("contoh_input.txt", "w", encoding="utf-8") as f:
    base_text = (
        "Alice was beginning to get very tired of sitting by her sister on the bank, "
        "and of having nothing to do: once or twice she had peeped into the book her sister was reading, "
        "but it had no pictures or conversations in it, 'and what is the use of a book,' thought Alice "
        "'without pictures or conversation?'\n"
    )
    for _ in range(15000):  # Menulis ulang teks agar ukuran besar (~100 KB)
        f.write(base_text)
