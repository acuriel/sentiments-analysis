# -*-coding: UTF-8 -*-

from app import Analizer_SVM, Analizer_random, save, load
from test import Test, Percent_test, Random_test, Intelligent_test
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm

from os import linesep

# ====================test 0====================

# path = 'BD/medium_db.csv'
# sentiments = ['alegria', 'sorpresa', 'anticipacion', 'disgusto', 'tristeza', 'confianza', 'miedo']
# dummy_test = Test(sentiments, path, Analizer_random)
# dummy_test.train()
# print (dummy_test.test())
#
# dummy_test = Test(sentiments, path, Analizer_SVM)
# dummy_test.train()
# print (dummy_test.test())

# ====================test 1====================
path = 'BD/text_emotion_short.csv'
sentiments = ['worry', 'happiness', 'sadness', 'love', 'surprise', 'hate']
sets = [0, 1, 0, 1, None, 0]

# 'neutral', 'relief', 'empty', 'enthusiasm', 'boredom', 'anger,'fun']

# path = 'BD/medium_db.csv'
# sentiments = ['sorpresa', 'anticipacion', 'alegria', 'disgusto', 'tristeza', 'ira', 'miedo']

# # Random
# dummy_test = Test(sentiments, path, Analizer_random)
# dummy_test.train()
# print('Random')
# print(dummy_test.test())

# # SVM
# dummy_test = Test(sentiments, path, Analizer_SVM)
# dummy_test.train()
# print('SVM')
# print(dummy_test.test())

# # SVM
# percent_test = Percent_test(sentiments, path, Analizer_SVM, 4, 5)
# percent_test.train()
# print('SVM, porciento')
# print(percent_test.test())

# # SVM
# percent_test = Random_test(sentiments, path, Analizer_SVM, 15)
# percent_test.train()
# print('SVM, proceinto random')
# print(percent_test.test())

percent = float(input("Test Data Percent >> "))
print('test data percent : ' + str(percent))

# SVM
percent_test = Intelligent_test(sentiments, path, Analizer_SVM, percent, sets=sets)
percent_test.train()  #
print('SVM, inteligente')
print('test data percent : ' + str(percent))
print(percent_test.test())
save(percent_test.analizer_svm, 'machine065')


 # todo hablar en el informe de cuando se considera correcto un rsultado y poner ejemolos particulares de love y happiness
