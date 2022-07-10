# -*- coding: utf-8 -*-
"""NLP_FinalProject.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zjqE3KPCaWXX0WK1ZpwxKAr21NTzv-xZ
"""

from google.colab import drive
drive.mount('/content/drive')

"""# Import Requirements"""

from pandas import read_csv
from sklearn.model_selection import train_test_split
import numpy as np
!pip install transformers
from transformers import pipeline
from transformers import TFAutoModel
!pip install datasets
from datasets import Dataset, DatasetDict
!pip install tensorflow
from tensorflow.keras.layers import LSTM, Bidirectional, TimeDistributed, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import Sequential
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

"""# Load Data"""

df = read_csv('drive/MyDrive/NPL-Project-Data/dataset.csv')
df = df.dropna()
train_df, test_df = train_test_split(df, train_size=0.8, shuffle=True)

"""# Noisy Channel"""

import nltk
from nltk.corpus import words
nltk.download('words')
nltk.download('punkt')

!pip install wordfreq
from wordfreq import word_frequency

import operator

# A Space efficient Dynamic Programming
# based Python3 program to find minimum
# number operations to convert str1 to str2
def edit_distance(str1, str2):
	
	len1 = len(str1)
	len2 = len(str2)

	# Create a DP array to memoize result
	# of previous computations
	DP = [[0 for i in range(len1 + 1)]
			for j in range(2)];

	# Base condition when second String
	# is empty then we remove all characters
	for i in range(0, len1 + 1):
		DP[0][i] = i

	# Start filling the DP
	# This loop run for every
	# character in second String
	for i in range(1, len2 + 1):
		
		# This loop compares the char from
		# second String with first String
		# characters
		for j in range(0, len1 + 1):

			# If first String is empty then
			# we have to perform add character
			# operation to get second String
			if (j == 0):
				DP[i % 2][j] = i

			# If character from both String
			# is same then we do not perform any
			# operation . here i % 2 is for bound
			# the row number.
			elif(str1[j - 1] == str2[i-1]):
				DP[i % 2][j] = DP[(i - 1) % 2][j - 1]
			
			# If character from both String is
			# not same then we take the minimum
			# from three specified operation
			else:
				DP[i % 2][j] = (1 + min(DP[(i - 1) % 2][j],
									min(DP[i % 2][j - 1],
								DP[(i - 1) % 2][j - 1])))
			
	# After complete fill the DP array
	# if the len2 is even then we end
	# up in the 0th row else we end up
	# in the 1th row so we take len2 % 2
	# to get row
	return DP[len2 % 2][len1]

# to find closest options for a token
english_words_set = set(words.words())

def min_distants(token):
  min_dist = len(token)
  candidates = []
  candidate_distants = []
  for w in english_words_set:
    d = edit_distance(token, w)
    if d<min_dist:
      candidates.append(w)
      candidate_distants.append(d)
      min_dist = d
  if len(candidates)==0:
    return token
  
  min_dist = min(candidate_distants)
  final_candidates = []
  for i in range(len(candidate_distants)):
    if candidate_distants[i] == min_dist:
      final_candidates.append(candidates[i])
  return final_candidates

# return the item that is most frequent
def correct_token(token):
  if token in english_words_set:
    return token
  
  candidates = min_distants(token)
  if len(candidates)==1:
    return candidates[0]


  candidates_frequency = {}
  for c in candidates:
    candidates_frequency[c] = word_frequency(c, 'en')
  return max(candidates_frequency.items(), key=operator.itemgetter(1))[0]

def spell_correction(text):
  tokenizer = nltk.tokenize.TreebankWordTokenizer()
  tokens = tokenizer.tokenize(text)
  new_tokens = [correct_token(t) for t in tokens]
  return ' '.join(new_tokens)

spell_correction("I don't need that guyy!")

"""# RNNs

## Data Pre-processing
"""

# Create a dictionary to convert the vocabulary (characters) to integers
vocab_to_int = {}
count = 0
for row in df['noise_sentence']:
    for character in row:
        if character not in vocab_to_int:
            vocab_to_int[character] = count
            count += 1

# Check the size of vocabulary and all of the values
vocab_size = len(vocab_to_int)
print("The vocabulary contains {} characters.".format(vocab_size))
print(sorted(vocab_to_int))

# Create another dictionary to convert integers to their respective characters
int_to_vocab = {}
for character, value in vocab_to_int.items():
    int_to_vocab[value] = character

# This method convert sentences to integers
def create_int_sentences(sentences, max_length = 100):
  int_sentences = []
  for sentence in sentences:
    int_sentence = []
    count = 0
    for character in sentence:
        if count>=max_length:
          break
        int_sentence.append(vocab_to_int[character])
        count+=1
    if len(int_sentence)<max_length:
      int_sentence = int_sentence + ([vocab_to_int[' ']]*(max_length-len(int_sentence)))
    int_sentences.append([int_sentence])
  return np.array(int_sentences)

x_train = create_int_sentences(train_df['noise_sentence'][:180000])
y_train = create_int_sentences(train_df['label'][:180000])
x_test = create_int_sentences(test_df['noise_sentence'][:45000])
y_test = create_int_sentences(test_df['label'][:45000])

"""## Build model"""

input_size = 100
output_size = 100
dropout = 0.5
batch_size = 8
is_load = True

if is_load:
  model = load_model('/content/drive/MyDrive/NPL-Project-Data/lstm_model.h5')
else:
  model = Sequential()
  model.add(Bidirectional(LSTM(output_size, activation='relu', return_sequences=True, dropout=dropout),
                          merge_mode='sum',
                          input_shape=(None, input_size)))
  model.add(Bidirectional(LSTM(output_size, activation='relu', return_sequences=True,
                              dropout=dropout), merge_mode='sum'))
  model.add(Bidirectional(LSTM(output_size, activation='relu', return_sequences=True,
                              dropout=dropout), merge_mode='sum'))
  model.compile(loss='mse', optimizer=Adam(learning_rate=0.001), metrics=['mse'])

model.summary()

history = model.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test), batch_size=batch_size)
model.save('/content/drive/MyDrive/NPL-Project-Data/lstm_model.h5')
plt.plot(history.epoch, history.history['loss'], 'g', 'Training loss')

train_df['noise_sentence'][12]

x_train[12]

sample = x_train[12].reshape((1,1,100))
res = ''
for i in np.squeeze(sample):
  res+=int_to_vocab[i]
print(res)

res = ''
for i in np.squeeze(model.predict(sample)):
  res+=int_to_vocab[round(i)]
print(res)

"""# Transformers"""

my_dataset = DatasetDict()
train_ds = Dataset.from_pandas(train_df)
test_ds = Dataset.from_pandas(test_df, split='test')
my_dataset['train'] = train_ds
my_dataset['test'] = test_ds
my_dataset

from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

def my_tokenize_function(examples):
    return tokenizer(examples["noise_sentence"], padding="max_length", truncation=True)

my_tokenized_datasets = my_dataset.map(my_tokenize_function, batched=True)

from transformers import DefaultDataCollator

data_collator = DefaultDataCollator(return_tensors="tf")

tf_train_dataset = my_tokenized_datasets["train"].to_tf_dataset(
    columns=["attention_mask", "input_ids", "token_type_ids"],
    label_cols=["label"],
    shuffle=True,
    batch_size=8,
)

tf_test_dataset = my_tokenized_datasets["test"].to_tf_dataset(
    columns=["attention_mask", "input_ids", "token_type_ids"],
    label_cols=["label"],
    shuffle=False,
    batch_size=8,
)

my_model = TFAutoModel.from_pretrained('murali1996/bert-base-cased-spell-correction', from_pt=True)

# Import generic wrappers
from transformers import AutoModel, AutoTokenizer 


# Define the model repo
model_name = "murali1996/bert-base-cased-spell-correction" 


# Download pytorch model
model = TFAutoModel.from_pretrained('murali1996/bert-base-cased-spell-correction', from_pt=True)
tokenizer = AutoTokenizer.from_pretrained(model_name)


# Transform input tokens 
inputs = tokenizer("Hello world! I am Arman and I really want to introduce you someting", return_tensors="tf")

# Model apply
outputs = model(**inputs)

optimizer = tf.keras.optimizers.Adam(learning_rate=5e-5)
model.compile(optimizer=optimizer, loss=model.compute_loss) # can also use any keras loss fn
model.fit(tf_train_dataset, epochs=3, batch_size=16)