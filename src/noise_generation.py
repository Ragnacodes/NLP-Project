import random
import string
from preprocessing import save_csv
import csv


keyboard_rows = [["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", ""],
                 ["", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", ""],
                 ["", "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "", "", ""],
                 ["", "z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "", "", ""],
                 ["", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "{", "}", "|"],
                 ["","A", "S", "D", "F", "G", "H", "J", "K", "L", ":", "", "", ""],
                 ["", "Z", "X", "C", "V", "B", "N", "M", "<", ">", "?", "", "", ""]]


def find_keyboard_coordinates(char, my_list=keyboard_rows):
    for sub_list in my_list:
        if char in sub_list:
            return my_list.index(sub_list), sub_list.index(char)


def find_adjacents(char):
    x, y = find_keyboard_coordinates(char)
    adjacents = []
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            try:
                adjacents.append(keyboard_rows[i][j])
            except:
                continue
    adjacents.remove(char)
    return adjacents


def replace_noise(token, random_index):
    c = token[random_index]
    c_adjacents = find_adjacents(c)
    new_char = random.choice(c_adjacents)
    return token[:random_index] + new_char + token[random_index + 1:]


def extra_noise(token, random_index):
    new_char = random.choice(string.ascii_letters)
    return token[:random_index] + new_char + token[random_index + 1:]


def eliminate_noise(token, random_index):
    return token[:random_index] + token[random_index + 1:]


def transposition_noise(token, random_index):
    if random_index == 0:
        random_index = random.randint(1, len(token) - 1)
    return token[:random_index-1] + token[random_index] + token[random_index-1]+token[random_index+1:]


def change_token(token):
    choices = ['replace', 'extra', 'eliminate', 'transposition']
    choices_possibilities = [50, 15, 15, 20]
    noise_type = random.choices(choices, weights=choices_possibilities)[0]

    random_index = random.randint(0, len(token) - 1)

    if noise_type == 'replace':
        return replace_noise(token, random_index)
    elif noise_type == 'extra':
        return extra_noise(token, random_index)
    elif noise_type == 'eliminate':
        return eliminate_noise(token, random_index)
    else:
        return transposition_noise(token, random_index)


def noisy_text(tokens, maximum_noisy_token_rate=0.3):
    for i, token in enumerate(tokens):
        noise_possibility = min(maximum_noisy_token_rate, len(token) / 15)
        if len(token) > 1 and random.random() < noise_possibility:
            tokens[i] = change_token(token)
    return tokens


if __name__ == '__main__':
    # Load pre-processed data
    with open('data/english_tokens.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)[1:]
    english_tokenized = [row[0].split(' ') for row in data]
    print('noise generation started ...')

    # Generate some noise on dataset records to make incorrect words
    noisy_tokenized = [noisy_text(tokens.copy()) for tokens in english_tokenized]
    save_csv(path='data/dataset.csv', column_names=['noise_sentence', 'label'],
             first_column=noisy_tokenized, second_column=english_tokenized)
    print('The final noisy sentences and their labels are available in data/dataset.csv file.')
