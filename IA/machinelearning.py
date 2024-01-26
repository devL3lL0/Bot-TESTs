# -*- coding: utf-8 -*-
"""MachineLearning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13XMGDWw3dTYKVu10V_4VmDPkC-D99iHQ
"""

#import os

#esecuzione = os.popen("pip install git+https://github.com/tflearn/tflearn.git")
#risultato = esecuzione.read()
#risultato

import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tensorflow
import random
import json
import tflearn

nltk.download('punkt')

words = []
labels = []
docs_x = []
docs_y = []

with open("./train.json") as file:
  data = json.load(file)

for intent in data["intents"]:
  for pattern in intent["patterns"]:
    wrds = nltk.word_tokenize(pattern)
    words.extend(wrds)
    docs_x.append(wrds)
    docs_y.append(intent["tag"])

  if intent["tag"] not in labels:
    labels.append(intent["tag"])

stemmer = LancasterStemmer()

words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))
labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
  bag = []

  wrds = [stemmer.stem(w.lower()) for w in doc]

  for w in words:
    if w in wrds:
      bag.append(1)
    else:
      bag.append(0)

  output_row = out_empty[:]
  output_row[labels.index(docs_y[x])] = 1

  training.append(bag)
  output.append(output_row)

def bag_of_words(input,l):
  bag = []
  array = []
  wrds = [stemmer.stem(w.lower()) for w in input.split(" ")]
  for w in l:
    if w in wrds:
      bag.append(1)
    else:
      bag.append(0)
  array.append(bag)
  return np.array(array)

training = np.array(training)
output = np.array(output)

#tensorflow.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net, len(output[0]),activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

model.load("model.tflearn")

print("Inizia a parlare con il tuo bot (exit per uscire)!")
while True:
  inp = input("You: ")
  if inp.lower() == "exit":
    break

  results = model.predict(bag_of_words(inp,words))
  results_index = np.argmax(results)
  tag = labels[results_index]

  for tg in data["intents"]:
    if tg["tag"] == tag:
      responses = tg["responses"]

  print(random.choice(responses))
