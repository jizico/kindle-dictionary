import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import re

# Download modul tambahan untuk mencari akar kata
print("Menyiapkan database AI...")
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

def is_reasonably_valid(word):
    """Filter pintar agar 'aaaa' terbuang, tapi nama dan istilah medis tetap masuk."""
    if not re.match(r"^[a-z\-']+$", word): return False
    if len(word) == 1 and word not in ['a', 'i']: return False
    if not re.search(r'[aeiouy]', word): return False
    if re.search(r'(.)\1\1', word): return False
    return True

def build_fast_dict():
    """Memindahkan seluruh kamus ke RAM agar prosesnya instan."""
    en_id = {}
    for syn in wn.all_synsets():
        ind_lemmas = [l.replace('_', ' ') for l in syn.lemma_names('ind')]
        if ind_lemmas:
            for lemma in syn.lemmas():
                word = lemma.name().lower()
                if word not in en_id:
                    en_id[word] = set()
                en_id[word].update(ind_lemmas)
    return en_id

def process_massive_offline(input_file, output_file):
    print("Membangun kamus ke dalam Memori... (mohon tunggu sebentar)")
    en_id_dict = build_fast_dict()
    lemmatizer = WordNetLemmatizer()

    print("Mulai memproses ratusan ribu kata...")
    valid_count = 0

    with open(input_file, 'r', encoding='utf-8') as f, \
         open(output_file, 'w', encoding='utf-8') as out:

        processed = set()

        for line in f:
            word = line.strip().lower()

            # Buang sampah seperti "aaac", tapi biarkan sisanya
            if word in processed or not is_reasonably_valid(word):
                continue

            processed.add(word)

            # 1. Coba terjemahkan secara langsung
            if word in en_id_dict:
                meanings = ", ".join(sorted(en_id_dict[word]))
                out.write(f"{word}\t{meanings}\n")
                valid_count += 1
                continue

            # 2. Jika tidak ada, cari KATA DASARNYA (Lemmatization)
            # Cek sebagai Kata Benda (n), Kerja (v), Sifat (a), Keterangan (r)
            found_translation = False
            for pos in ['n', 'v', 'a', 'r']:
                lemma = lemmatizer.lemmatize(word, pos=pos)
                if lemma in en_id_dict:
                    meanings = ", ".join(sorted(en_id_dict[lemma]))
                    out.write(f"{word}\t{meanings}\n")
                    found_translation = True
                    valid_count += 1
                    break

            # 3. Jika tetap tidak ada (berarti itu Nama Orang, Kota, atau Istilah Medis)
            # Biarkan saja aslinya (Contoh: aachen -> aachen) agar kamus tetap lengkap!
            if not found_translation:
                out.write(f"{word}\t{word}\n")
                valid_count += 1

            # Tampilkan progress
            if valid_count % 50000 == 0:
                print(f"Berhasil memproses {valid_count} kata...")

    print(f"\nSELESAI LUAR BIASA! Total kosakata Anda sekarang: {valid_count} kata.")

if __name__ == "__main__":
    process_massive_offline('english-final.txt', 'kamus-raksasa-id.txt')
