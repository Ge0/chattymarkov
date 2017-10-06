#!/usr/bin/env python3
from chattymarkov import ChattyMarkov
from chattymarkov.database import MemoryDatabase

db = MemoryDatabase()
markov = ChattyMarkov(db)
markov.learn("My favorite animal is the crocodile")
markov.learn("The word animal is six letters long")
print(markov.generate())
