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

## Noise Generator

## Statistics

The `statistics.py` script processes the data and calculates some statistics metrics such as

- Number of data units

- Number of sentences 

- Number of words

- Number of unique words

It also plots some graphs to show the result.
