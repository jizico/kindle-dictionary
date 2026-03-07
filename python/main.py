import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import re

# Download database yang dibutuhkan
print("Menyiapkan database WordNet...")
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

def get_indonesian_meanings(synsets):
    """Fungsi pembantu untuk mengambil terjemahan bahasa Indonesia dari synsets."""
    meanings = set()
    for syn in synsets:
        for lemma in syn.lemma_names('ind'):
            meanings.add(lemma.replace('_', ' '))
    return meanings

def translate_100k_valid(input_filename, output_filename):
    print("Memulai proses pembuatan kamus 100k+ kata valid...")
    lemmatizer = WordNetLemmatizer()

    with open(input_filename, 'r', encoding='utf-8') as infile, \
         open(output_filename, 'w', encoding='utf-8') as outfile:

        processed_words = set()
        valid_count = 0

        for line in infile:
            word = line.strip().lower()

            # Filter dasar: pastikan hanya berisi huruf/tanda hubung, bukan simbol aneh
            if not word or word in processed_words or not re.match(r"^[a-z\-']+$", word):
                continue

            processed_words.add(word)

            # Cek apakah kata ini adalah bahasa Inggris yang valid di WordNet
            synsets = wn.synsets(word, lang='eng')

            # Jika synsets kosong, coba cari akar katanya (siapa tahu ini bentuk jamak/lampau)
            if not synsets:
                lemma = lemmatizer.lemmatize(word)
                if lemma != word:
                    synsets = wn.synsets(lemma, lang='eng')

            # Jika kata tersebut VALID (ada di kamus Inggris WordNet)
            if synsets:
                # 1. Coba cari bahasa Indonesianya secara langsung
                indonesian_meanings = get_indonesian_meanings(synsets)

                # 2. Jika tidak ada, coba cari bahasa Indonesia dari akar katanya (Lemmatization)
                if not indonesian_meanings:
                    for pos in ['n', 'v', 'a', 'r']:
                        lemma = lemmatizer.lemmatize(word, pos=pos)
                        if lemma != word:
                            lemma_synsets = wn.synsets(lemma, lang='eng')
                            indonesian_meanings.update(get_indonesian_meanings(lemma_synsets))

                # 3. Tentukan hasil akhir yang akan ditulis ke file
                final_meaning = ""
                if indonesian_meanings:
                    # Jika ada terjemahan Indonesia, gabungkan
                    final_meaning = ", ".join(sorted(indonesian_meanings))
                else:
                    # Jika sama sekali tidak ada di database Indonesia,
                    # gunakan definisi bahasa Inggrisnya sebagai cadangan!
                    # [EN] menandakan bahwa ini adalah definisi bahasa Inggris
                    definition = synsets[0].definition()
                    final_meaning = f"[EN] {definition}"

                # Simpan ke file (Kata <TAB> Arti/Definisi)
                outfile.write(f"{word}\t{final_meaning}\n")
                valid_count += 1

                if valid_count % 15000 == 0:
                    print(f"Berhasil merangkai {valid_count} kata bahasa Inggris valid...")

    print(f"\nSELESAI! Total kosakata Anda sekarang: {valid_count} kata murni tanpa kata sampah.")

if __name__ == "__main__":
    translate_100k_valid('english-final.txt', 'kamus-100k-bersih.txt')
