import math
import re

import os

def remove_string_special_characters(s):

    stripped = re.sub('[^\w\s]', '', s)
    stripped = re.sub('_', '', stripped)

    stripped = re.sub('\s+', ' ', stripped)

    stripped = stripped.strip()

    return stripped


def get_doc(texts):

    doc_info = []
    i = 0
    for text in texts:
        i += 1
        count = count_words(text)
        temp = {'doc_id': i, 'doc_length': count}
        doc_info.append(temp)

    return doc_info


def count_words(text):
    count = 0
    words = word_tokenize(text)

    for _ in words:
        count += 1

    return count


def create_freq_dict(korpus):
    i = 0
    freq_dict_list = []
    for text in korpus:
        i += 1
        freq_dict = {}
        words = word_tokenize(text)
        for word in words:
            word = word.lower()
            if word in freq_dict:
                freq_dict[word] += 1
            else:
                freq_dict[word] = 1
            
            temp = {'doc_id': i, 'freq_dict': freq_dict}
        freq_dict_list.append(temp)
    
    return freq_dict_list


def compute_tf(doc_info, freq_dict_list):
    tf_scores = []

    for temp_dict in freq_dict_list:
        id = temp_dict['doc_id']
        for k in temp_dict['freq_dict']:
            temp = {'doc_id': id,
                    'tf_score': temp_dict['freq_dict'][k] / doc_info[id - 1]['doc_length'],
                    'key': k}
            tf_scores.append(temp)

    return tf_scores

def compute_idf(doc_info, freq_dict_list):

    idf_scores = []
    counter = 0

    for d in freq_dict_list:
        counter += 1
        for k in d['freq_dict'].keys():
            count = sum([k in temp_dict['freq_dict'] for temp_dict in freq_dict_list])
            temp = {'doc_id': counter, 'idf_score': math.log(len(doc_info) / count), 'key': k}

            idf_scores.append(temp)

    return idf_scores


def compute_tfidf(tf_scores, idf_scores):
    tfidf_scores = []

    for j in idf_scores:
        for i in tf_scores:
            if j['key'] == i['key'] and j['doc_id'] == i['doc_id']:
                temp = {'doc_id': j['doc_id'],
                        'tfidf_score': j['idf_score'] * i['tf_score'],
                        'key': i['key']}
        
        tfidf_scores.append(temp)
    
    return tfidf_scores
    

def read_texts():
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

def word_tokenize(text):
    words = remove_string_special_characters(text).split()
    return list(map(lambda x: x.lower(), words))


def main():
    unprepared_texts = read_texts()

    texts = [remove_string_special_characters(t) for t in unprepared_texts]
    doc_info = get_doc(texts)

    freq_dict_list = create_freq_dict(texts)

    tf_score = compute_tf(doc_info, freq_dict_list)
    idf_score = compute_idf(doc_info, freq_dict_list)

    tdidf_score = compute_tfidf(tf_score, idf_score)

    # Example
    # for _, el in enumerate(tdidf_score):
    #     print(el)

    # Fields: doc_id - number of file, 
    #         tfidf_score - value for view,
    #         key - word


if __name__ == "__main__":
    main()
