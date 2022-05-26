from typing import List
from collections import Counter

import csv
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import numpy as np

nltk.download('stopwords')


def load_word_list() -> List[str]:
    with open('data/wordlist.txt', 'r') as word_list_file:
        word_data = word_list_file.read()
        return [w for w in word_data.split('\n') if len(w) != 0]


def load_wikipedia_units(words) -> List[str]:
    units = []
    for w in words:
        try:
            with open(f'data/wikipedia_raw/{w}.txt', 'r') as wiki_raw_file:
                raw_data = wiki_raw_file.read()
                units.extend(raw_data.split('\n'))
        except Exception as err:
            print(f"can not find the file {w}.txt, error: {err}")

    return units


def plot_word_counter(words, counts):
    labels = words[:20]
    words_counts = counts[:20]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, words_counts, width, label='Number of repeat')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Words')
    ax.set_title('20 Top repeated words')
    ax.set_xticks(x, labels)
    ax.legend()

    ax.bar_label(rects1, padding=3)

    fig.tight_layout()

    plt.show()


def load_samples(path: str) -> List[str]:
    samples = []
    try:
        with open(path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            # Ignore the header (first line of the csv file)
            line_number = 0
            for row in csv_reader:
                # Add the correct sentence to the list
                if line_number == 0:
                    line_number += 1
                    continue
                samples.append(row[1])
                line_number += 1
    except Exception as err:
        print(f"can not open dataset file, error: {err}")

    return samples


if __name__ == '__main__':
    # Load words list
    print("Loading the wordlist.txt...")
    word_list = load_word_list()
    if word_list is None:
        print("can not read the word list. exiting...")
        exit(1)

    # Wikipedia raw data (To calculate the the number of units)
    print("Loading Wikipedia raw data...")
    wikipedia_units = load_wikipedia_units(word_list)

    # Sample Data
    print("Reading the dataset.csv file...")
    csv_samples = load_samples('data/dataset.csv')

    # Create the word list
    print("Calculating the word list for the dataset...")
    whole_text = " ".join(csv_samples).lower()
    whole_words = whole_text.split()
    word_counter = dict(Counter(whole_words))

    # Calculate the statistics metrics
    print("Calculating statistics...")
    statistics = {
        "n_of_units": len(wikipedia_units),
        "n_of_sentences": len(csv_samples),
        "n_of_words": len(whole_words),
        "n_of_unique_words": len(word_counter.keys()),
    }
    print(statistics)

    # Sorting
    print("Sorting the word counter...")
    word_counter_sorted = sorted(word_counter.items(), key=lambda item: item[1], reverse=True)
    sorted_words = [w[0] for w in word_counter_sorted]
    sorted_counts = [w[1] for w in word_counter_sorted]

    # Plotting the unique words
    print("Plotting the unique words")
    plot_word_counter(sorted_words, sorted_counts)

    # Plotting the unique words (ignoring stop words)
    print("Plotting the unique words (ignoring stop words)")
    stop_words = stopwords.words('english')
    stop_words_removed_dic = [(k, v) for k, v in word_counter_sorted if k not in stop_words]
    sorted_words = [w[0] for w in stop_words_removed_dic]
    sorted_counts = [w[1] for w in stop_words_removed_dic]
    plot_word_counter(sorted_words, sorted_counts)
