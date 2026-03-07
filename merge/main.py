import os

def merge_dictionaries(file1_path, file2_path, output_path):
    # We use a dictionary where the key is the English word,
    # and the value is a 'set' to automatically prevent duplicate meanings.
    merged_dict = {}

    def process_file(filepath):
        if not os.path.exists(filepath):
            print(f"Error: Could not find {filepath}")
            return

        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                # Split the line by the <Tab> character
                parts = line.split('\t')

                # Make sure the line actually has a word and a meaning
                if len(parts) == 2:
                    word = parts[0].strip().lower()
                    meanings_raw = parts[1].strip()

                    # Split the meanings by comma and clean up any extra spaces
                    meanings = [m.strip() for m in meanings_raw.split(',') if m.strip()]

                    # If it's a new word, initialize its set
                    if word not in merged_dict:
                        merged_dict[word] = set()

                    # Add all meanings to the set (duplicates are ignored automatically)
                    merged_dict[word].update(meanings)

    print(f"Processing first file: {file1_path}...")
    process_file(file1_path)

    print(f"Processing second file: {file2_path}...")
    process_file(file2_path)

    print(f"Writing merged data to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        # Sort words alphabetically for a clean final dictionary
        for word in sorted(merged_dict.keys()):
            # Sort the individual meanings alphabetically, then join them back with a comma
            meanings_str = ", ".join(sorted(merged_dict[word]))
            f.write(f"{word}\t{meanings_str}\n")

    print("\nMERGE COMPLETE!")
    print(f"Total unique words compiled: {len(merged_dict)}")

if __name__ == "__main__":
    # Change these to match the actual names of your txt files
    FILE_1 = 'file1.txt'
    FILE_2 = 'file2.txt'
    OUTPUT_FILE = 'ultimate_merged_dictionary.txt'

    merge_dictionaries(FILE_1, FILE_2, OUTPUT_FILE)
