# -*-coding: UTF-8 -*-

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


class PreprocModule:
    """Base class for text pre-processing modules"""

    def __init__(self, tokens):
        self.tokens = tokens

    def process(self, *args, **kwargs):
        return self.tokens


class RemoveStopwordsModule(PreprocModule):
    """Remove the stop words receiving a tokenized text"""

    def process(self, *args, **kwargs):
        lang = 'english' if 'lang' not in kwargs else kwargs['lang']
        stop_words = set(stopwords.words(lang))
        result = [w for w in self.tokens if w not in stop_words]
        return result


class SnowballStemmerModule(PreprocModule):
    """Generic stemmer for a tokenized text"""

    def process(self, *args, **kwargs):
        lang = 'english' if 'lang' not in kwargs else kwargs['lang']
        stemmer = SnowballStemmer(lang)
        result = [str(stemmer.stem(token)) for token in self.tokens]
        return result

