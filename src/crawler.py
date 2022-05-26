import os
import csv

import wikipediaapi
from alive_progress import alive_bar

if __name__ == '__main__':
    # Open word list
    print('Reading word list...')
    word_list = []
    with open('./data/wordlist.txt', 'r') as word_list_file:
        content = word_list_file.read()
        word_list = [w for w in content.split('\n') if w != '']

    print('Downloading Wikipedia data...')
    # Use Wikipedia API to fetch the summary of the word
    wiki_wiki = wikipediaapi.Wikipedia('en')
    raw_wikipedia_data = {}
    with alive_bar(len(word_list), bar='bubbles', spinner='notes2') as bar:
        for word in word_list:
            try:
                page_py = wiki_wiki.page(word)
                raw_wikipedia_data[word] = page_py.text
            except Exception as err:
                print(f'Can not fetch word:\"{word}\", err: {err}')
            bar()

    # Save the Wikipedia data in multiple files
    with alive_bar(len(raw_wikipedia_data.keys()), bar='bubbles', spinner='notes2') as bar:
        for word in word_list:
            with open(f'./data/wikipedia_raw/{word}.txt', 'w') as f:
                content = raw_wikipedia_data[word]
                f.write(content)
                bar()

    # Cleaning the kaggle spell set
    print("cleaning the kaggle spell set...")
    kaggle_spell_dic = {}
    # Iterate through all kaggle spell list files
    files = os.listdir('data/kaggle_spell_list')
    for file in files:
        with open(f"data/kaggle_spell_list/{file}", 'r') as f:
            content = f.read()
            records = content.split('\n')
            for record in records:
                # Ignore empty lines
                if record == "":
                    continue
                # Parse the correct and wrong items
                correct_word, wrong_words = record.split(": ")
                # Add the wrong words to the dictionary
                if kaggle_spell_dic.get(correct_word) is None:
                    kaggle_spell_dic[correct_word] = []
                for w_word in wrong_words.split():
                    kaggle_spell_dic[correct_word].append(w_word)

    # Create kaggle csv rows
    # In each row, there is only a correct word and a wrong word.
    # (correct_word, wrong_word)
    print("Creating kaggle csv rows...")
    kaggle_csv_rows = []
    for c_word, w_words in kaggle_spell_dic.items():
        for w_word in w_words:
            kaggle_csv_rows.append((c_word, w_word))

    # Saving the dictionary in csv format.
    print("Saving the kaggle spell csv file...")
    with open('data/kaggle_spell_dataset.csv', mode='w') as k_file:
        kaggle_writer = csv.writer(k_file, delimiter=',')
        kaggle_writer.writerows(kaggle_csv_rows)
