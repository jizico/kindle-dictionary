import fs from 'fs/promises';
import { existsSync } from 'fs';

const META_URL = 'https://dl.fbaipublicfiles.com/arrival/dictionaries/en-id.txt';
const META_FILE = 'meta_en_id_dict.txt';
const NLTK_FILE = 'kamus-offline-id.txt'; // The file your Python script generated
const OUTPUT_FILE = 'ultimate_kindle_dictionary.txt';

async function mergeDictionaries() {
    console.log('Starting the ultimate dictionary merger...');
    const masterDictionary = new Map();

    // 1. Load the NLTK WordNet translations
    if (existsSync(NLTK_FILE)) {
        console.log('Loading your Python NLTK dictionary...');
        const nltkText = await fs.readFile(NLTK_FILE, 'utf-8');

        for (const line of nltkText.split('\n')) {
            const parts = line.split('\t');
            if (parts.length === 2) {
                const word = parts[0].trim().toLowerCase();
                const translations = parts[1].trim().split(',').map(t => t.trim());

                masterDictionary.set(word, new Set(translations));
            }
        }
        console.log(`Loaded ${masterDictionary.size} words from NLTK.`);
    } else {
        console.error(`ERROR: Cannot find ${NLTK_FILE}. Run your Python script first!`);
        process.exit(1);
    }

    // 2. Download Meta dataset if missing
    if (!existsSync(META_FILE)) {
        console.log('Downloading Meta EN-ID dataset...');
        const response = await fetch(META_URL);
        const text = await response.text();
        await fs.writeFile(META_FILE, text);
    }

    // 3. Merge the Meta dataset into our master dictionary
    console.log('Merging Meta dataset...');
    const metaText = await fs.readFile(META_FILE, 'utf-8');
    let newWordsAdded = 0;

    for (const line of metaText.split('\n')) {
        const parts = line.trim().split(/\s+/);
        if (parts.length >= 2) {
            const word = parts[0].toLowerCase();
            const translation = parts.slice(1).join(' ');

            if (!masterDictionary.has(word)) {
                masterDictionary.set(word, new Set());
                newWordsAdded++;
            }
            masterDictionary.get(word).add(translation);
        }
    }
    console.log(`Added ${newWordsAdded} brand new words from Meta.`);

    // 4. Format and export the final merged dictionary
    console.log('Formatting the final output...');
    const outputLines = [];

    // Sort alphabetically for clean Kindle processing
    const sortedWords = Array.from(masterDictionary.keys()).sort();

    for (const word of sortedWords) {
        const translations = Array.from(masterDictionary.get(word)).join(', ');
        outputLines.push(`${word}\t${translations}`);
    }

    await fs.writeFile(OUTPUT_FILE, outputLines.join('\n'));
    console.log(`\nSUCCESS! Your ultimate dictionary is ready: ${OUTPUT_FILE}`);
    console.log(`Total unique words compiled: ${masterDictionary.size}`);
}

mergeDictionaries();
