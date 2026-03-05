import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import re

# Download database AI Premium
print("Menyiapkan database AI Premium...")
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# Mapping tag WordNet ke tampilan yang rapi
POS_MAP = {
    'n': '[Noun/Kata Benda]',
    'v': '[Verb/Kata Kerja]',
    'a': '[Adjective/Kata Sifat]',
    's': '[Adjective/Kata Sifat]', 
    'r': '[Adverb/Kata Keterangan]'
}

# TARGET KATA: 500.000 KOSAKATA
TARGET_WORDS = 500000

def is_reasonably_valid(word):
    """Filter pintar untuk membuang sampah murni tapi mempertahankan kata asli & nama."""
    if not re.match(r"^[a-z\-']+$", word): return False
    if len(word) == 1 and word not in ['a', 'i']: return False
    if not re.search(r'[aeiouy]', word): return False
    if re.search(r'(.)\1\1', word): return False
    return True

def build_fast_dict():
    """Membangun database kamus ke dalam RAM agar secepat kilat."""
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

def process_massive_premium_dictionary(input_file, output_file):
    print(f"Membangun Kamus Premium (Target: {TARGET_WORDS} Kata)...")
    en_id_dict = build_fast_dict()
    lemmatizer = WordNetLemmatizer()
    valid_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as f, \
         open(output_file, 'w', encoding='utf-8') as out:
        
        processed = set()
        
        for line in f:
            word = line.strip().lower()
            
            # Berhenti otomatis jika target 500.000 kata tercapai
            if valid_count >= TARGET_WORDS:
                break
            
            # Filter kata sampah
            if word in processed or not is_reasonably_valid(word):
                continue
                
            processed.add(word)
            
            found_translation = False
            formatted_meanings = []
            
            # 1. Cari langsung di database
            synsets = wn.synsets(word, lang='eng')
            if synsets:
                meanings_by_pos = {}
                for syn in synsets:
                    pos_tag = POS_MAP.get(syn.pos(), '[Other]')
                    for lemma in syn.lemma_names('ind'):
                        clean_lemma = lemma.replace('_', ' ')
                        if pos_tag not in meanings_by_pos:
                            meanings_by_pos[pos_tag] = set()
                        meanings_by_pos[pos_tag].add(clean_lemma)
                
                if meanings_by_pos:
                    for pos, meanings in meanings_by_pos.items():
                        joined_meanings = ", ".join(sorted(meanings))
                        formatted_meanings.append(f"{pos} {joined_meanings}")
                    found_translation = True
            
            # 2. Jika tidak ketemu, cari menggunakan akar kata (Lemmatization)
            if not found_translation:
                meanings_by_pos = {}
                for pos_code, pos_name in zip(['n', 'v', 'a', 'r'], ['[Noun/Kata Benda]', '[Verb/Kata Kerja]', '[Adjective/Kata Sifat]', '[Adverb/Kata Keterangan]']):
                    lemma = lemmatizer.lemmatize(word, pos=pos_code)
                    if lemma in en_id_dict:
                        if pos_name not in meanings_by_pos:
                            meanings_by_pos[pos_name] = set()
                        meanings_by_pos[pos_name].update(en_id_dict[lemma])
                        found_translation = True
                
                if found_translation:
                    for pos, meanings in meanings_by_pos.items():
                        joined_meanings = ", ".join(sorted(meanings))
                        formatted_meanings.append(f"{pos} {joined_meanings}")
            
            # 3. Tulis hasilnya ke dalam file
            if found_translation:
                final_translation = " | ".join(formatted_meanings)
                out.write(f"{word}\t{final_translation}\n")
            else:
                # Menjaga istilah asing, nama kota, dan sains tetap masuk untuk memenuhi kuota
                out.write(f"{word}\t[Istilah/Nama] {word}\n")
            
            valid_count += 1
            
            if valid_count > 0 and valid_count % 50000 == 0:
                print(f"Progress: {valid_count} / {TARGET_WORDS} kata...")

    print(f"\nSELESAI! Kamus Ekstra Besar Anda siap dengan total tepat {valid_count} kosakata.")

if __name__ == "__main__":
    process_massive_premium_dictionary('english-final.txt', 'kamus-500k-id.txt')