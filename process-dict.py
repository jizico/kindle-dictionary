import time
import nltk
from deep_translator import GoogleTranslator

# Download the English dictionary word list (only needs to run once)
nltk.download('words', quiet=True)
from nltk.corpus import words

# Create a fast lookup set of valid English words
english_dictionary = set(words.words())

def is_valid_word(word):
    """Check if the word is a valid English word and not just gibberish."""
    if not word.isalpha():
        return False
    # Filter out random single letters except 'a' and 'i'
    if len(word) == 1 and word not in ['a', 'i']:
        return False
    return word in english_dictionary

def process_and_translate(input_filename, output_filename):
    translator = GoogleTranslator(source='en', target='id')

    print("Starting processing... This may take a while for large files.")

    with open(input_filename, 'r', encoding='utf-8') as infile, \
         open(output_filename, 'w', encoding='utf-8') as outfile:

        # Keep track of words we've already done to avoid duplicates
        processed_words = set()

        for line in infile:
            word = line.strip().lower()

            # 1. Normalize and Filter
            if word not in processed_words and is_valid_word(word):
                processed_words.add(word)

                try:
                    # 2. Translate
                    translation = translator.translate(word).lower()

                    # 3. Format Output: word <tab> translation
                    outfile.write(f"{word}\t{translation}\n")

                    print(f"Saved: {word} -> {translation}")

                    # Pause slightly so Google Translate doesn't block our IP
                    time.sleep(0.3)

                except Exception as e:
                    print(f"Error translating '{word}': {e}")
                    time.sleep(2) # Wait a bit longer if there's an error

if __name__ == "__main__":
    # Make sure 'english-final.txt' is in the same folder as this script
    process_and_translate('english-final.txt', 'translated-dictionary.txt')
    print("Finished! Check the 'translated-dictionary.txt' file.")
