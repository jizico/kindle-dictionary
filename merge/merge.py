file1 = "file1.txt"
file2 = "file2.txt"
output = "merged.txt"

data = {}

# Load file2 first (priority)
with open(file2, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        word, meaning = line.split("\t", 1)
        data[word] = meaning

# Add file1 only if word not already in file2
with open(file1, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        word, meaning = line.split("\t", 1)
        if word not in data:
            data[word] = meaning

# Write merged result
with open(output, "w", encoding="utf-8") as f:
    for word in sorted(data):
        f.write(f"{word}\t{data[word]}\n")

print("Merged dictionary saved to", output)
