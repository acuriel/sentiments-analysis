# -*-coding: UTF-8 -*-

from .modules import *
from nltk.tokenize import word_tokenize, RegexpTokenizer, TweetTokenizer

import sklearn.semi_supervised as sk

import string

from nltk.tokenize.casual import EMOTICON_RE, URLS

import re


class ProcQueue:
    def __init__(self, lang='english'):
        self.queue = []
        self.lang = lang

    @property
    def count(self):
        return len(self.queue)

    def enqueue(self, preproc_module):
        self.queue.append(preproc_module)

    def dequeue(self):
        if self.count is 0:
            return None
        return self.queue.pop(0)

    def insert(self, index, preproc_module):
        self.queue.insert(index, preproc_module)

    def exec_simple(self, text):
        tweet = TweetTokenizer()
        # simple preprocessing
        new_text = text.lower()

        # tokenizing
        tokens = tweet.tokenize(new_text)

        # removing emoticons
        new_tokens = []
        for c in tokens:
            if EMOTICON_RE.fullmatch(c) is not None:  # deleting emoticons
                continue

            if c.startswith('#') or c.startswith('@'):  # deleting User names and Hashtags
                continue

            if re.sub(r"(http[s]?|ftp):\S+", "", c) == '':  # removing urls
                continue

            new_tokens.append(c)

        # negating from 'not' to next punctuation sign
        for i in range(0, len(new_tokens)):
            if new_tokens[i] == 'not' or new_tokens[i] == 'dont' or new_tokens[i].endswith('n\'t'):
                for j in range(i + 1, len(new_tokens)):
                    if new_tokens[j] not in string.punctuation:
                        new_tokens[j] = new_tokens[j] + '_neg'
                    else:
                        break

        # removing punctuation signs
        punctuation = '!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~]+'
        new_text = []
        found = False
        for c in new_tokens:
            for char in c:
                if char in punctuation:
                    found = True
                    break
                else:
                    break
            if found:
                found = False
                continue
            new_text.append(c)

        # print(tokens)
        for mod in self.queue:
            tokens = mod(new_text).process()

        str = ''
        for s in tokens:
            str += ' ' + s

        return str

    def exec_list(self, list):
        result = []

        for t in list:
            result.append(self.exec_simple(t))

        return result
