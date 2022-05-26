# NLP-Project

Natural Processing Language Project - IUST 2022

## Overview

Spelling correction is **a well-known task in Natural Language Processing (NLP)**. Automatic spelling correction is essential for many NLP applications like web search engines, text summarization, sentiment analysis, etc.

## Directories

- [Data Directory](data/README.md)
- [Source Directory](src/README.md)

## Report Files

You can open the markdown file or download the PDF files.

| The phase of the project | Markdown file                | PDF file              |
| ------------------------ | ---------------------------- | --------------------- |
| P1                       | [Open](reports/P1_Report.md) | [Open](P1_Report.pdf) |

## Run the code

### Update the dataset

To update the dataset from scratch, you need to follow these steps:

- Crawl the raw data.

- Preprocess the data.

- Add noise to the data.

You can run these steps by a single command.

```bash
# First of all, you need to provide your wordlist.
# The default wordlist is `data/wordlist.txt`,
# You can download English dictionary by running ./src/download_wordlist.sh
./run.sh
```

In the end, it will report some metrics and plot the histogram.