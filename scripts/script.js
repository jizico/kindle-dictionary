import fs from "fs/promises";
import { existsSync } from "fs";

const DICT_URL =
  "https://dl.fbaipublicfiles.com/arrival/dictionaries/en-id.txt";
const DICT_FILE = "meta_en_id_dict.txt";
const INPUT_FILE = "input.txt";
const OUTPUT_FILE = "kamus-offline-id.txt";

async function translateOffline() {
  console.log("Starting OFFLINE translation process...");
  console.log("This will finish in just a few seconds, not hours!");

  // 1. Download the offline dictionary database (Meta dataset instead of WordNet)
  if (!existsSync(DICT_FILE)) {
    console.log("Downloading offline dictionary database...");
    const response = await fetch(DICT_URL);
    const text = await response.text();
    await fs.writeFile(DICT_FILE, text);
  }

  // 2. Load dictionary into a Map for instant lookups
  const dictText = await fs.readFile(DICT_FILE, "utf-8");
  const dictionaryMap = new Map();

  for (const line of dictText.split("\n")) {
    const parts = line.trim().split(/\s+/);
    if (parts.length >= 2) {
      const word = parts[0].toLowerCase();
      // Replace underscores with spaces just like your Python script
      const translation = parts.slice(1).join(" ").replace(/_/g, " ");

      if (!dictionaryMap.has(word)) {
        dictionaryMap.set(word, new Set());
      }
      dictionaryMap.get(word).add(translation);
    }
  }

  // 3. Process the input file
  if (!existsSync(INPUT_FILE)) {
    console.error(`ERROR: Please ensure ${INPUT_FILE} is in the same folder.`);
    process.exit(1);
  }

  const rawText = await fs.readFile(INPUT_FILE, "utf-8");
  const processedWords = new Set();
  const outputLines = [];
  let translatedCount = 0;

  for (const line of rawText.split("\n")) {
    const word = line.trim().toLowerCase();

    // Skip if the word has already been processed or is empty
    if (!word || processedWords.has(word)) continue;
    processedWords.add(word);

    // Find the word meaning
    if (dictionaryMap.has(word)) {
      // Combine with commas and sort alphabetically
      const meaningsStr = Array.from(dictionaryMap.get(word)).sort().join(", ");

      // Format: word <TAB> meaning1, meaning2
      outputLines.push(`${word}\t${meaningsStr}`);
      translatedCount++;

      // Display progress to prevent terminal lag
      if (translatedCount % 10000 === 0) {
        console.log(
          `Successfully translated ${translatedCount} valid words...`,
        );
      }
    }
  }

  // 4. Save to output file
  await fs.writeFile(OUTPUT_FILE, outputLines.join("\n"));
  console.log(
    `DONE! A total of ${translatedCount} words were successfully translated and saved.`,
  );
}

translateOffline();
