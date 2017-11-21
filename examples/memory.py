#!/usr/bin/env python3
from chattymarkov import ChattyMarkov

markov = ChattyMarkov("memory://")
markov.learn("My favorite animal is the crocodile")
markov.learn("The word animal is six letters long")
print(markov.generate())
