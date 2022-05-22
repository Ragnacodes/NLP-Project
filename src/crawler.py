import wikipediaapi
from alive_progress import alive_bar
from time import sleep


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
    with alive_bar(len(word_list), bar = 'bubbles', spinner = 'notes2') as bar:
        for word in word_list:
                try:
                        page_py = wiki_wiki.page(word)
                        raw_wikipedia_data[word] = page_py.text
                except:
                        print(f'Can not fetch word:\"{word}\"')
                bar()

    # Save the Wikipedia data in multiple files
    with alive_bar(len(raw_wikipedia_data.keys()), bar = 'bubbles', spinner = 'notes2') as bar:
        for word in word_list:
                with open(f'./data/wikipedia_raw/{word}.txt', 'w') as f:
                        content = raw_wikipedia_data[word]
                        f.write(content)
                        bar()
