import fs from "fs/promises";
import { wiktionary } from "@wordlist/english-wiktionary";

const INPUT_FILE = "input.txt";
const OUTPUT_FILE = "valid_english_words.txt";

async function filterValidWords() {
  console.log("Loading the Wiktionary validation list...");
  // Create a Set from the wiktionary array for high-speed, instant lookups
  const validWordsSet = new Set(wiktionary);

  console.log(`Reading your input file: ${INPUT_FILE}...`);
  try {
    const rawText = await fs.readFile(INPUT_FILE, "utf-8");

    // Split by line, trim spaces, convert to lowercase, and remove empty lines
    const inputWords = rawText
      .split("\n")
      .map((w) => w.trim().toLowerCase())
      .filter((w) => w);

    console.log(`Filtering ${inputWords.length} words...`);
    const validWords = [];

    for (const word of inputWords) {
      // Check if the word exists in the Wiktionary Set
      if (validWordsSet.has(word)) {
        validWords.push(word);
      }
    }

    console.log(
      `Writing ${validWords.length} valid words to ${OUTPUT_FILE}...`,
    );
    await fs.writeFile(OUTPUT_FILE, validWords.join("\n"));

    console.log("Process complete!");
  } catch (error) {
    console.error(`Error processing files: ${error.message}`);
  }
}

filterValidWords();
