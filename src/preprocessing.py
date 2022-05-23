from nltk import sent_tokenize
from nltk.tokenize import TreebankWordTokenizer
import csv
import random
import string
import re
import os

def tokenizer(sentence):
    return TreebankWordTokenizer().tokenize(sentence)


def remove_extra_tokens(tokens):
    # Remove unclean tokens which have non-english characters
    return [token for token in tokens if not re.search('[^a-zA-Z]', token)]


def list_to_string(o):
    # Storing data as lists is not available in .csv files so we need to change their type to string
    if isinstance(o, list):
        o = ' '.join(o)
    return o


def save_csv(path, column_names, first_column, second_column=False):
    rows = []
    for i in range(len(first_column)):
        # Handle both single column and multi column csv files
        if second_column:
            rows.append([list_to_string(first_column[i]), list_to_string(second_column[i])])
        else:
            rows.append([list_to_string(first_column[i])])

    # Write the list on inputted csv path
    with open(path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(column_names)
        writer.writerows(rows)


def preprocess(text):
    sentences = sent_tokenize(text)
    # Store separated sentences as the first preprocessing step
    save_csv(path='sentences.csv', column_names=['sentence'], first_column=sentences)
    print('sentences.csv file saved!')

    tokenized = []
    for sent in sentences:
        tokens = tokenizer(sent)
        # Eliminate short sentences
        if len(tokens) > 5:
            new_tokens = remove_extra_tokens(tokens)
            tokenized.append(new_tokens)

    # Store separated english tokens as the second preprocessing step
    save_csv(path='english_tokens.csv', column_names=['tokens'], first_column=tokenized)
    print('english_tokens.csv file saved!')

    return tokenized


def change_token(token):
    random_index = random.randint(0, len(token) - 1)
    c = token[random_index]
    new_char = c
    while c == new_char:
        new_char = random.choice(string.ascii_letters)

    new_token = token[:random_index] + new_char + token[random_index + 1:]
    return new_token


def noisy_text(tokens, noisy_token_rate=0.3):
    for i, token in enumerate(tokens):
        if random.random() < noisy_token_rate:
            tokens[i] = change_token(token)
    return tokens


if __name__ == '__main__':
    # Read all text files and concat them in a single long string
    print('data is loading ...')
    DATA_DIRECTORY = '..\\data\\wikipedia_raw'
    text = ''
    i = 0
    for file_path in os.listdir(DATA_DIRECTORY):
        if file_path.endswith('.txt'):
            i += 1
            text += open(os.path.join(DATA_DIRECTORY, file_path), mode='r', encoding='utf-8').read() + '\n'

        if i>100:
            break
    print('data loaded successfully.')

    english_tokenized = preprocess(text)

    noisy_tokenized = [noisy_text(tokens.copy()) for tokens in english_tokenized]
    save_csv(path='dataset.csv', column_names=['noise_sentence', 'label'],
             first_column=noisy_tokenized, second_column=english_tokenized)
    print('the final noisy sentences and their labels are available in dataset.csv file!')
