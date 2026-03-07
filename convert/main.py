import os

INPUT_FILE = 'kamus-offline-id.txt'
HTML_FILE = 'kamus.html'
OPF_FILE = 'kamus.opf'

def generate_kindle_files():
    print("Membuat format HTML untuk Kindle...")

    with open(INPUT_FILE, 'r', encoding='utf-8') as f, \
         open(HTML_FILE, 'w', encoding='utf-8') as out:

        out.write('<html><head><meta charset="utf-8"></head><body>\n')
        out.write('<mbp:frameset>\n')

        count = 0
        for line in f:
            parts = line.strip().split('\t')
            # Memastikan baris memiliki kata dan arti
            if len(parts) >= 2:
                word = parts[0]
                meaning = parts[1]

                # Tag khusus agar Kindle mengenali ini sebagai kamus
                out.write(f'<idx:entry name="english">\n')
                out.write(f'  <idx:orth value="{word}"><h2><b>{word}</b></h2></idx:orth>\n')
                out.write(f'  <p>{meaning}</p>\n')
                out.write(f'</idx:entry>\n<hr/>\n')
                count += 1

        out.write('</mbp:frameset>\n')
        out.write('</body></html>\n')

    opf_content = """<?xml version="1.0" encoding="utf-8"?>
<package unique-identifier="uid">
  <metadata>
    <dc-metadata xmlns:dc="http://purl.org/metadata/dublin_core" xmlns:oebpackage="http://openebook.org/namespaces/oeb-package/1.0/">
      <dc:Title>Kamus Inggris-Indonesia (Offline)</dc:Title>
      <dc:Language>en</dc:Language>
      <dc:Identifier id="uid">kamus_en_id_offline</dc:Identifier>
    </dc-metadata>
    <x-metadata>
      <DictionaryInLanguage>en</DictionaryInLanguage>
      <DictionaryOutLanguage>id</DictionaryOutLanguage>
      <DefaultLookupIndex>english</DefaultLookupIndex>
    </x-metadata>
  </metadata>
  <manifest>
    <item id="dictionary0" href="kamus.html" media-type="text/x-oeb1-document"/>
  </manifest>
  <spine>
    <itemref idref="dictionary0"/>
  </spine>
</package>
"""
    with open(OPF_FILE, 'w', encoding='utf-8') as f:
        f.write(opf_content)

    print(f"Selesai! {count} kata telah diformat.")
    print("File 'kamus.html' dan 'kamus.opf' berhasil dibuat!")

if __name__ == "__main__":
    generate_kindle_files()
