import pickle

from preproc.proc_queue import ProcQueue
from preproc.modules import *
from csv import *

from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm

from random import uniform

import string


# text = "This is a sample sentence, showing off the stop words filtration and the tokenization :)."
# print(text)
# queue = ProcQueue()
# queue.enqueue(RemoveStopwordsModule)
# queue.enqueue(SnowballStemmerModule)
#
# print(queue.execQ(text))

class Sentiment:
    def __init__(self, name):
        self.name = name
        self.result = []
        self.count = 0

    def match(self, string):
        # recibe un string y si el nombre del sentimiento es igual al string adiciona a la lista de resultados 1, sino adiciona 0
        if self.name == string:
            self.result.append(1)
            self.count += 1
        else:
            self.result.append(0)


class Analizer_SVM:
    def __init__(self, sentiments, path, lang='english', threshold=0.75, sets=None):
        self.sentiments = []
        self.SVMs = []
        self.sentiments_mapped = {}
        self.sentiments_count = len(sentiments)
        # self.path = path
        # self.vectorizer = CountVectorizer(ngram_range=(1, 2))
        self.vectorizer = CountVectorizer()
        self.total_queries = 0
        self.count_per_sentiment = []

        self.text_process = ProcQueue(lang=lang)
        # self.text_process.enqueue(RemoveUserHashtag)
        self.text_process.enqueue(RemoveStopwordsModule)
        self.text_process.enqueue(SnowballStemmerModule)

        if sets is not None:
            self.sets = {}
            self.count_sets = 0
            i = 0
            for s in sets:
                if not s in self.sets.values() and s is not None:
                    self.count_sets += 1
                self.sets[sentiments[i]] = s
                i += 1

        self.threshold = threshold

        for i in range(0, len(sentiments)):
            self.sentiments_mapped[i] = sentiments[i]
            self.sentiments.append(Sentiment(sentiments[i]))

            self.SVMs.append(svm.SVC(kernel='linear', probability=True))

            self.count_per_sentiment.append(0)

    def put_results(self, results):
        for r in results:
            for s in self.sentiments:
                s.match(r)

    def train(self, text, results):
        print('training...')
        self.put_results(results)
        vectors = self.__text_modification__(text)
        # SVM
        for i in range(0, self.sentiments_count):
            self.SVMs[i].fit(vectors, self.sentiments[i].result)

    def consult(self, text):
        # debe retornar una lista con los sentimeintos, NO con el mapeo de estos
        result = []
        prob = []
        text_modification = self.__text_modification__(text, fit=False)

        for i in range(0, self.sentiments_count):
            s = self.SVMs[i].predict_proba(text_modification)[0][1]
            if s > 0.75:  # self.threshold:
                prob.append(s)
                result.append(self.sentiments_mapped[i])
                self.count_per_sentiment[i] += 1

        self.total_queries += 1

        s = ''
        for c in text:
            s += c
        s += ':'
        for c in result:
            s += c

        if len(result) > 1 and self.sets is not None:
            # initializing total sum and average arrays
            aux_prom = []
            aux_total = []
            for i in range(0, self.count_sets):
                aux_prom.append(0)
                aux_total.append(0)

            # updating arrays
            i = 0
            for c in result:
                if self.sets[c] != None:
                    aux_prom[self.sets[c]] += prob[i]
                    aux_total[self.sets[c]] += 1

                i += 1

            # calculating average per set
            for i in range(0, len(aux_prom)):
                if aux_prom[i] != 0:
                    aux_prom[i] /= aux_total[i]

            # removing sentiments if average per set is less than 0.5 between sets
            sets_to_remove = []
            for i in range(0, len(aux_prom)):
                for j in range(0, len(aux_prom)):
                    s = aux_prom[j] - aux_prom[i]
                    if aux_prom[j] - aux_prom[i] > 0.05 and aux_prom[j] != 0 and aux_prom[i] != 0:
                        if not sets_to_remove.__contains__(i):
                            sets_to_remove.append(i)

            true_result = []
            true_prob = []
            i = 0
            for c in result:
                if sets_to_remove.__contains__(self.sets[c]):
                    continue

                true_result.append(c)
                true_prob.append(prob[i])
                i += 1

            return true_result, true_prob

        return result, prob

    def __text_modification__(self, text, fit=True):
        # Text Modification
        mod_text = (self.text_process.exec_list(text))

        # mod_text = text

        # Bag of Words
        if fit:
            self.vectorizer.fit(mod_text)
        vectors = self.vectorizer.transform(mod_text)

        return vectors

    def reset(self, sentiments, path):
        self.__init__(sentiments, path)

    def individual_fit(self, text):
        # Text Modification
        mod_text = (self.text_process.exec_list(text))

        # Bag of Words
        self.vectorizer.fit(mod_text)

    def train_pos(self, text, results, pos):
        print('training ' + str(pos))
        mapped_results = []
        for r in results:
            if r == self.sentiments[pos].name:
                mapped_results.append(1)
            else:
                mapped_results.append(0)

        vectors = self.__text_modification__(text, False)

        # SVM
        self.SVMs[pos].fit(vectors, mapped_results)


class Analizer_random:
    def __init__(self, sentiments, path, lang):
        self.sentiments = sentiments

    def train(self, text, results):
        pass

    def consult(self, text):
        return [self.sentiments[int(uniform(0, len(self.sentiments) - 1))]]


def save(self, name):
    with open(name + '.pkl', 'wb') as file:
        pickle.dump(self, file)


def load(name):
    try:
        with open(name + '.pkl', 'rb') as file:
            return pickle.load(file)
    except:
        pass
