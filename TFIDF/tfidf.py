import math
import re
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import os

class Calculator(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.__word_set = set()
        self.ranged_word_list = []

        self.main()

    # cигнал передающий сумму
    # обязательно даём название аргументу через arguments=['sum']
    # иначе нельзя будет его забрать в QML
    sumResult = pyqtSignal(int, arguments=['sum'])

    subResult = pyqtSignal(int, arguments=['sub'])

    # слот для суммирования двух чисел
    @pyqtSlot(int, int)
    def sum(self, arg1, arg2):
        # складываем два аргумента и испускаем сигнал
        self.sumResult.emit(arg1 + arg2)

    # слот для вычитания двух чисел
    @pyqtSlot(int, int)
    def sub(self, arg1, arg2):
        # вычитаем аргументы и испускаем сигнал
        self.subResult.emit(arg1 - arg2)

    def remove_string_special_characters(self, s):

        stripped = re.sub('[^\w\s]', '', s)
        stripped = re.sub('_', '', stripped)

        stripped = re.sub('\s+', ' ', stripped)

        stripped = stripped.strip()

        return stripped


    def get_doc(self, texts):

        doc_info = []
        i = 0
        for text in texts:
            i += 1
            count = self.count_words(text)
            temp = {'doc_id': i, 'doc_length': count}
            doc_info.append(temp)

        return doc_info


    def count_words(self, text):
        count = 0
        words = self.word_tokenize(text)

        for _ in words:
            count += 1

        return count


    def create_freq_dict(self, korpus):
        i = 0
        freq_dict_list = []
        for text in korpus:
            i += 1
            freq_dict = {}
            words = self.word_tokenize(text)
            for word in words:
                word = word.lower()
                self.__word_set.add(word)

                if word in freq_dict:
                    freq_dict[word] += 1
                else:
                    freq_dict[word] = 1

                temp = {'doc_id': i, 'freq_dict': freq_dict}
            freq_dict_list.append(temp)

        return freq_dict_list


    def compute_tf(self, doc_info, freq_dict_list):
        tf_scores = []

        for temp_dict in freq_dict_list:
            id = temp_dict['doc_id']
            for k in temp_dict['freq_dict']:
                temp = {'doc_id': id,
                        'tf_score': temp_dict['freq_dict'][k] / doc_info[id - 1]['doc_length'],
                        'key': k}
                tf_scores.append(temp)

        return tf_scores

    def compute_idf(self, doc_info, freq_dict_list):

        idf_scores = []
        counter = 0

        for d in freq_dict_list:
            counter += 1
            for k in d['freq_dict'].keys():
                count = sum([k in temp_dict['freq_dict'] for temp_dict in freq_dict_list])
                temp = {'doc_id': counter, 'idf_score': math.log(len(doc_info) / count), 'key': k}

                idf_scores.append(temp)

        return idf_scores


    def compute_tfidf(self, tf_scores, idf_scores):
        tfidf_scores = []

        for j in idf_scores:
            for i in tf_scores:
                if j['key'] == i['key'] and j['doc_id'] == i['doc_id']:
                    temp = {'doc_id': j['doc_id'],
                            'tfidf_score': j['idf_score'] * i['tf_score'],
                            'key': i['key']}

            tfidf_scores.append(temp)

        return tfidf_scores


    def read_texts(self):
        files = []

        data_set_folder = os.path.abspath('../DataSet')
        for _, _, filenames in os.walk(data_set_folder):
                files.extend(filenames)

        texts = []
        for _, filename in enumerate(files):
            full_path = f"{data_set_folder}/{filename}"
            if os.path.exists(full_path):
                with open(full_path) as f:
                    texts.append(f.read())

        return texts

    def word_tokenize(self, text):
        words = self.remove_string_special_characters(text).split()
        return list(map(lambda x: x.lower(), words))


    def main(self):
        self.unprepared_texts = self.read_texts()

        texts = [self.remove_string_special_characters(t) for t in self.unprepared_texts]
        doc_info = self.get_doc(texts)

        freq_dict_list = self.create_freq_dict(texts)

        tf_score = self.compute_tf(doc_info, freq_dict_list)
        idf_score = self.compute_idf(doc_info, freq_dict_list)

        tdidf_score = self.compute_tfidf(tf_score, idf_score)

        
        word_range_score = {}
        for _, el in enumerate(tdidf_score):
            word = el['key']
            score = el['tfidf_score']

            if word not in word_range_score:
                word_range_score[word] = 0.0
            word_range_score[word] = word_range_score[word] + score

        for _, word in enumerate(self.__word_set):
            word_range_score[word] /= len(texts)
            self.ranged_word_list.append({'key': word, 'score': word_range_score[word]})
        
        self.ranged_word_list.sort(key=lambda x: x['score'], reverse=True)
        # PLEASE TAKE THIS VALUE

        # for _, el in enumerate(self.ranged_word_list):
        #     print(el)

        # Example
        # for _, el in enumerate(tdidf_score):
        #     print(el)

        # Fields: doc_id - number of file,
        #         tfidf_score - value for view,
        #         key - word

