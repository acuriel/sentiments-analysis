# -*-coding: UTF-8 -*-

from app import Analizer_SVM
from csv import *

from sklearn import cross_validation

from random import uniform


class Test(object):
    # Lo que hace es entrenar y consultar con el mismo conjunto
    def __init__(self, sentiments, path, analizer, lang='english', sets = None):
        self.analizer_svm = analizer(sentiments, path, lang, sets = sets)
        self.total_cases = 0
        self.correct_cases = 0
        self.sentiments = sentiments
        self.path = path
        self.db_text = []
        self.db_sentiments = []

        self.__read_db()

        self.train_set = []
        self.train_result = []
        self.test_set = []
        self.test_result = []

    def __read_db(self):
        db = open(self.path)
        db_reader = reader(db)
        first = True

        # crear texto de prueba a partir del path
        for row in db_reader:
            if first:
                first = False
                continue

            self.db_sentiments.append(row[0])
            self.db_text.append(row[1])

    def train(self):
        self.train_set = self.db_text
        self.train_result = self.db_sentiments
        self.test_set = self.db_text
        self.test_result = self.db_sentiments

        self.analizer_svm.train(self.train_set, self.train_result)

    def test(self):
        # crear texto de prueba a partir del path
        for i in range(0, len(self.test_set)):
            result, prob = self.analizer_svm.consult([self.test_set[i]])
            # print result
            if len(result) > 0 and self.test_result[i] in result:  # result[0] == self.test_result[i]:
                print(self.test_result[i] + ' ' + str(result) + ' ' + str(prob))
                self.correct_cases += 1

            self.total_cases += 1

        return self.correct_cases, self.total_cases

    def particular_test(self, text):
        return self.analizer_svm.consult([text])


class Percent_test(Test):
    # Selecciona como conjunto de prueba el porciento que se le da acomo parametro a partir de la posicion que se le pasa como parametro
    def __init__(self, sentiments, path, analizer, percent, start_position):
        super(Percent_test, self).__init__(sentiments, path, analizer)

        self.percent = percent
        self.start_position = start_position
        self.count_test = int(len(self.db_text) * percent / 100)
        self.count_train = len(self.db_text) - self.count_test

    def train(self):
        for i in range(0, len(self.db_text)):
            if i >= self.start_position and len(self.test_set) <= self.count_test:
                self.test_set.append(self.db_text[i])
                self.test_result.append(self.db_sentiments[i])
            else:
                self.train_set.append(self.db_text[i])
                self.train_result.append(self.db_sentiments[i])

        self.analizer_svm.train(self.train_set, self.train_result)


class Random_test(Test):
    # recibe un porciento y coge ese porciento de a bd de forma random para hacer testing
    def __init__(self, sentiments, path, analizer, percent):
        super(Random_test, self).__init__(sentiments, path, analizer)
        self.percent = percent
        self.count_test = int(len(self.db_text) * percent / 100)
        self.count_train = len(self.db_text) - self.count_test

    def train(self):
        possible = []
        for i in range(0, len(self.db_text)):
            possible.append(i)

        while len(self.test_set) < self.count_test:
            rand = int(round(uniform(0, len(possible) - 1)))
            pos = possible[rand]
            self.test_set.append(self.db_text[pos])
            self.test_result.append(self.db_sentiments[pos])
            possible.remove(pos)

        for i in possible:
            self.train_set.append(self.db_text[i])
            self.train_result.append(self.db_sentiments[i])

        self.analizer_svm.train(self.train_set, self.train_result)


class Intelligent_test(Test):
    # recibe un porciento y coge ese porciento para testing
    # pero en el conjunto de entrenamiento para cada svm intenta que los datos de cada clase sean mas o menos la misma cantidad
    def __init__(self, sentiments, path, analizer, percent, sets = None):
        super(Intelligent_test, self).__init__(sentiments, path, analizer, sets = sets)
        self.percent = percent
        self.count_test = int(len(self.db_text) * percent / 100)
        self.count_train = len(self.db_text) - self.count_test

    def train(self):
        possible = []
        for i in range(0, len(self.db_text)):
            possible.append(i)

        while len(self.test_set) < self.count_test:
            rand = int(round(uniform(0, len(possible) - 1)))
            pos = possible[rand]
            self.test_set.append(self.db_text[pos])
            self.test_result.append(self.db_sentiments[pos])
            possible.remove(pos)

        for i in possible:
            self.train_set.append(self.db_text[i])
            self.train_result.append(self.db_sentiments[i])

        self.analizer_svm.individual_fit(self.train_set)

        for j in range(0, self.analizer_svm.sentiments_count):
            # entrenar cada svm
            possible_1_data = []
            possible_1_result = []
            possible_0_data = []
            possible_0_result = []
            for i in range(0, len(self.train_set)):
                if self.train_result[i] == self.analizer_svm.sentiments[j].name:
                    possible_1_data.append(self.train_set[i])
                    possible_1_result.append(self.train_result[i])
                else:
                    possible_0_data.append(self.train_set[i])
                    possible_0_result.append(self.train_result[i])

            if len(possible_0_data) > len(possible_1_data) * 1 / 2:
                index = int(len(possible_1_data) * 1 / 2)
                possible_1_data.extend(possible_0_data[0:index])
                possible_1_result.extend(possible_0_result[0:index])
            else:
                possible_1_data.extend(possible_0_data)
                possible_1_result.extend(possible_0_result)

            self.analizer_svm.train_pos(possible_1_data, possible_1_result, j)

            # if len(possible_1_data) < len(possible_0_data):
            #     # recortar el array de los valores 0
            #     lenght = len(possible_1_data)
            #     possible_1_data.extend(possible_0_data[0:lenght])
            #     possible_1_result.extend(possible_0_result[0:lenght])
            #     self.analizer_svm.train_pos(possible_1_data, possible_1_result, j)
            #
            # else:
            #     # recortar el array de los valores 1
            #     lenght = len(possible_0_data)
            #     possible_0_data.extend(possible_1_data[0:lenght])
            #     possible_0_result.extend(possible_1_result[0:lenght])
            #     self.analizer_svm.train_pos(possible_0_data, possible_0_result, j)
