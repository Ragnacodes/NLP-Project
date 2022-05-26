# Report

## Dataset resources

There are various wordlists across the internet. We choose a 3K word list and save it in `data/wordlist.txt`. 

### Wikipedia

We need lots of sentences to create our dataset. Wikipedia is a free encyclopedia in that we can get lots of content by giving a single word. We get the content of Wikipedia for every single word in our `wordlist.txt` and save these raw data in `data/wikipedia_raw/`.

### Kaggle spell wordlist

Aside from Wikipedia, We use the `data/kaggle_spell_list/` files and make it cleaner by generating a CSV file (`data/kaggle_spell_dataset.csv`).

You can download the dataset in this [link](https://www.kaggle.com/datasets/bittlingmayer/spelling).

## Process of collecting the dataset

We use the `crawler.py` script to aggregate these data.

The script aggregates and cleans up some data and saves them in the `data/` directory. You need to download your wordlist to execute this code. (default: `data/wordlist.txt`)

### Steps

1. Download the wordlist.

2. Read the wordlist.

3. Download the Wikipedia content for every single word in the wordlist.

4. Save all of these contents in separate files in `data/wikipedia_raw/`.

5. Read the Kaggle spell list.

6. Parse and clean the Kaggle spell list.

7. Save the Kaggle spell list in a CSV file `data/kaggle_spell_dataset.csv`.

### Tools

- Wikipedia SDK: This crawler uses the Wikipedia SDK tool to fetch the content of Wikipedia.

- Alive progress: It is just a progress bar for showing the status.

```python
import wikipediaapi
from alive_progress import alive_bar

if __name__ == '__main__':
    print('Downloading Wikipedia data...')
    # Use Wikipedia API to fetch the summary of the word
    with alive_bar(len(word_list), bar='bubbles', spinner='notes2') as bar:
        for word in word_list:
            try:
                page_py = wiki_wiki.page(word)
                raw_wikipedia_data[word] = page_py.text
            except Exception as err:
                print(f'Can not fetch word:\"{word}\", err: {err}')
            bar()
```

### How to run crawler

```bash
python3 src/crawler.py
# Reading word list...
# Downloading Wikipedia data...
# <●●●●●●●●●●●●●●●●●●●                     > ♫♬  ♪♫♬ ♩♪♫♬ 1428/2999 [48%] in 6:29 (3.7/s, eta: 7:08) 
```

After running this, the generated files under `data/` directory look like this.

```bash
tree .
# The output
# ├── README.md
# ├── data
# │   ├── kaggle_spell_dataset.csv
# │   ├── wikipedia_raw
# │   │   ├── AIDS.txt
# │   │   ├── AM.txt
# │   │   ├── African-American.txt
# │   │   ├── African.txt
# │   │   ├── American.txt
# │   │   ├── ...
# │   │   ├── ...
```

It should be about 45MB with the default wordlist.

## ## Project Structure

- `src/` - for the scripts

- `data/` - a directory for all kinds of data
  
  - `data/wikipedia_raw/` - the downloaded pages of Wikipedia
  
  - `data/kaggle_spell_list/` - Kaggle spell correction data set. You can download the dataset in this [link](https://www.kaggle.com/datasets/bittlingmayer/spelling).
  
  - `data/wordlist.txt` - It is the main wordlist. You can change this file.

- `run.sh` - a file for generating the data set files. (It starts crawling, preprocessing, ...)

### Datasets

- Wikipedia dataset: It is a CSV file; the first column is a sentence with some spell correction errors. The second column is the sentence with the correct format.

- Kaggle spell dataset: It is a CSV file; the first column is a correct word. The second column is the word with a dictation issue.

## Preprocessing

`empty for now.`

## Labeling unit

We merged all of the contents of Wikipedia and considered every single sentence a unit. We manipulated the words by adding noise to these sentences.

### Adding noise to data

`empty for now.`

## Statistics

The `statistics.py` script processes the data and calculates some statistics metrics such as

- Number of data units

- Number of sentences

- Number of words

- Number of unique words

It also plots some graphs to show the result.

To run the statistics script:

```bash
python3 src/statistics.py 
# Here is the result for our dataset:
# [nltk_data] Downloading package stopwords to /Users/snapp/nltk_data...
# [nltk_data]   Package stopwords is already up-to-date!
# Loading the wordlist.txt...
# Loading Wikipedia raw data...
# Reading the dataset.csv file...
# Calculating the word list for the dataset...
# Calculating statistics...
# {'n_of_units': 255800, 'n_of_sentences': 226355, 'n_of_words': 5593836, 'n_of_unique_words': 103351}
# Sorting the word counter...
# Plotting the unique words
# Plotting the unique words (ignoring stop words)
```

These are the statistics metrics for our dataset.

- There are 255800 data units in our dataset.

- There are 255800 sentences in our dataset.

- There are 5593836 words in our dataset.

- There are 103351 unique words in our dataset.

The histogram with stop words.

<img src="images/histogram_with_stopwords.png" title="" alt="histogram_with_stopwords.png" data-align="center">

The histogram without stop words.

<img src="images/histogram_without_stopwords.png" title="" alt="histogram_without_stopwords.png" data-align="center">

We consider as many different words as we can to collect various contents. As you can see, It is evident that the most repeated words are some frequent and common words in texts.
