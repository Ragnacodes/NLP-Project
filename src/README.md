# Source

It contains the code files for this project. They're generally for

- Crawling
- Preprocessing
- Generating noise
- Statistics calculations

## Crawler

The script aggregates and cleans up some data and saves them in the `data/` directory. You need to download your wordlist to execute this code. (default: `data/wordlist.txt`)

### Wikipedia

The `crawler.py` script reads the given word list and uses Wikipedia SDK to fetch the content related to given words. The crawler saves the Wikipedia files to the `data/wikipedia_raw/`.

### Kaggle Spell list

The `crawler.py` script reads the Kaggle spell list files (.txt format) and parses the content of that file. In the end, It generates a CSV output file `data/kaggle_spell_dataset.csv`.

## Preprocessing

The `preprocessing.py` script reads the whole .txt files and then create clean data from row data. This file steps are sentence tokenization, word tokenization, remove unclean tokens and remove very short sentences. different steps has saved on different files (.csv format) and the last one is `data/english_tokens.csv`.

## Noise Generator

The `noise_generation.py` script reads the preprocessed csv file and then creates some misspelled words among any sentence. This script does that by 4 noise algorithms and each has different possibility. even selecting the noisy tokens of a sentence has specific algorithm. After running this script, we will have our dataset (`data\dataset.csv`) which has 2 columns. first column is a sentence with some noises and the second column is correct sentences (labels).

## Statistics

The `statistics.py` script processes the data and calculates some statistics metrics such as

- Number of data units

- Number of sentences 

- Number of words

- Number of unique words

It also plots some graphs to show the result.
