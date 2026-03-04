import time
import re
from deep_translator import GoogleTranslator

def has_letters(word):
    """Memastikan baris tersebut memiliki setidaknya satu huruf (bukan cuma tanda baca/angka kosong)."""
    return bool(re.search('[a-z]', word))

def process_and_translate_all(input_filename, output_filename, batch_size=100):
    translator = GoogleTranslator(source='en', target='id')
    
    print("Memulai proses terjemahan MASSAL (900k+ kata)...")
    print("Estimasi waktu: ~5 jam. Silakan biarkan komputer Anda menyala.")
    
    with open(input_filename, 'r', encoding='utf-8') as infile, \
         open(output_filename, 'w', encoding='utf-8') as outfile:
        
        processed_words = set()
        batch_words = []
        total_translated = 0
        
        for line in infile:
            word = line.strip().lower()
            
            # 1. Pembersihan Dasar: Pastikan kata tidak kosong, belum diproses, dan memiliki huruf
            if word and word not in processed_words and has_letters(word):
                processed_words.add(word)
                batch_words.append(word)
                
                # 2. Terjemahkan jika batch sudah mencapai 100 kata
                if len(batch_words) >= batch_size:
                    _translate_and_save_batch(translator, batch_words, outfile)
                    total_translated += len(batch_words)
                    print(f"Total berhasil diproses: {total_translated} kata...")
                    
                    batch_words = [] # Kosongkan batch
                    time.sleep(1)    # Jeda 1 detik agar tidak diblokir IP-nya
        
        # 3. Terjemahkan sisa kata yang tidak mencapai 100 di akhir file
        if batch_words:
            _translate_and_save_batch(translator, batch_words, outfile)
            total_translated += len(batch_words)
            print(f"Total berhasil diproses: {total_translated} kata...")

def _translate_and_save_batch(translator, batch_words, outfile):
    try:
        # Terjemahkan seluruh batch (100 kata) sekaligus
        translations = translator.translate_batch(batch_words)
        
        # Simpan ke file dengan format: kata<TAB>arti
        for word, translation in zip(batch_words, translations):
            if translation:
                # Menghapus enter ekstra yang mungkin muncul dari hasil translate
                clean_translation = translation.lower().replace('\n', ' ').strip()
                outfile.write(f"{word}\t{clean_translation}\n")
                
    except Exception as e:
        print(f"Terjadi kesalahan pada batch, mencoba lagi... Error: {e}")
        # Jika gagal (misal karena jaringan), tunggu 5 detik lalu coba lagi
        time.sleep(5)
        try:
            translations = translator.translate_batch(batch_words)
            for word, translation in zip(batch_words, translations):
                if translation:
                    clean_translation = translation.lower().replace('\n', ' ').strip()
                    outfile.write(f"{word}\t{clean_translation}\n")
        except Exception as e2:
            print(f"Gagal menerjemahkan batch setelah mencoba lagi. Melewati batch ini...")

if __name__ == "__main__":
    # Pastikan nama file input sesuai dengan file Anda
    process_and_translate_all('english-final.txt', 'kamus-lengkap-id.txt', batch_size=100)
    print("Selesai! Silakan cek file 'kamus-lengkap-id.txt'.")