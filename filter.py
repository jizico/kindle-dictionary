# filter_real_words.py
from enchant import Dict  # pip install pyenchant

d = Dict("en_US")

with open("dictionary.txt", "r", encoding="utf-8") as fin, \
     open("real_words.txt", "w", encoding="utf-8") as fout, \
     open("skipped.txt", "w", encoding="utf-8") as fskip:

    for line in fin:
        line = line.strip()
        if "\t" in line:
            word, translation = line.split("\t", 1)
            if d.check(word):
                fout.write(line + "\n")
            else:
                fskip.write(line + "\n")

print("Done filtering!")
