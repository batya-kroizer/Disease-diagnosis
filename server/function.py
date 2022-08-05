import threading

import pandas as pd
# coding=utf8

import numpy as np
from joblib import load
import nltk

nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import math
import csv
import pandas as pd
from search import search_object

import ast


def disease_search(word):
    # read the csv with disease word and the csv with the queries
    df = pd.read_csv("word_classification.csv")
    df_calsses = pd.read_csv("calasses.csv")
    word = word.lower()
    result = []
    # check if the word is disease
    for index, i in enumerate(df_calsses['class']):
        for h in df[i].str.find(" " + word + " "):
            if (h != -1 and not math.isnan(h)):
                # try to find the disease in the csv of the saved old search
                class_csv = pd.read_csv('disease.csv')
                for indexes, z in enumerate(class_csv['disease'].str.find(word)):
                    if (not math.isnan(z) and z != -1):
                        class_csv = class_csv.loc[indexes, :].values.tolist()
                        class_csv.pop(0)
                        for i in range(len(class_csv)):
                            # converting string into dictionary
                            if(not math.isnan(i)):
                                class_csv[i] = ast.literal_eval(class_csv[i])
                                if (class_csv[i]['kind'] == 'defination'):
                                    class_csv[i] = search_object('defination', 'text').search_defination(word).toJSON()
                                else:
                                    class_csv[i]=False;

                        return class_csv

                t = []
                search = []
                # search definition,images and all the queries from the dataset

                search.append(search_object('defination', 'text'))
                t.append(threading.Thread(target=search[0].search_defination, args=(word,)))
                t[0].start()
                search.append(search_object('image', 'image'))

                t.append(threading.Thread(target=search[1].search_image, args=(word,)))
                t[1].start()

                num = 2
                if isinstance(df_calsses.iloc[index]["search_text"], str):
                    for j in df_calsses.iloc[index]["search_text"].split(','):
                        search.append(search_object(j, 'text'))
                        t.append(threading.Thread(target=search[num].search_text, args=(j + word,)))
                        t[num].start()
                        num += 1
                if isinstance(df_calsses.iloc[index]["search_links"], str):
                    for j in df_calsses.iloc[index]["search_links"].split(','):
                        search.append(search_object(j, 'link'))
                        t.append(threading.Thread(target=search[num].search_links, args=(j + word,)))
                        t[num].start()
                        num += 1
                for tr in t:
                    tr.join()
                for s in search:
                    result.append(s.toJSON())
                temp = result
                # add the disease name to the result
                test_keys=['disease']
                for i in temp:
                    test_keys.append(i['kind'])
                # open the file in the write mode to save this search to the future
                temp.insert(0, word)
                res = dict(zip(test_keys, temp))

                with open('disease.csv', 'a', encoding='UTF8') as f:
                    # create the csv writer
                    writer = csv.DictWriter(f, fieldnames=test_keys)
                    # because the definition detail include large text that can't insert to one cell on csv file we will'not save it to the future
                    temp = res['defination']['result'][0]['details']
                    res['defination']['result'][0]['details'] = ""
                    # write a row to the csv file

                    writer.writerow(res)
                # delete the disease name from the result list
                result.pop(0)
                # put the definition detail back on the result
                result[0]['result'][0]['details'] = temp
                return result
    # if not found this disease
    return False


def predict_disease(input):
    # make list from the str that the client send
    input = input.split(',')
    # make dict from all the 132 symptoms
    symtoms_list = pd.read_csv("dataset/training_data.csv").columns[:-2]
    symptoms = dict(zip(symtoms_list, np.zeros(132)))
    # make the symptoms names as a normal sentences
    symtoms_list = [i.replace('_', ' ') for i in symtoms_list]

    # Program to measure the similarity between
    # two sentences using cosine similarity.

    X = input
    # create a list of the symptoms that most close to the symptoms that the client enter
    max_similarity = []
    for x in X:
        if (x != ''):
            x = x.lower()
            max_similarity_acc = 0
            max_similarity_obj = ''
            for y in symtoms_list:
                # tokenization
                X_list = word_tokenize(x)
                Y_list = word_tokenize(y)

                # sw contains the list of stopwords
                sw = stopwords.words('english')
                l1 = [];
                l2 = []

                # remove stop words from the string
                X_set = {w for w in X_list if not w in sw}
                Y_set = {w for w in Y_list if not w in sw}

                # form a set containing keywords of both strings
                rvector = X_set.union(Y_set)
                for w in rvector:
                    if w in X_set:
                        l1.append(1)  # create a vector
                    else:
                        l1.append(0)
                    if w in Y_set:
                        l2.append(1)
                    else:
                        l2.append(0)
                c = 0

                # cosine formula
                for i in range(len(rvector)):
                    c += l1[i] * l2[i]
                cosine = c / float((sum(l1) * sum(l2)) ** 0.5)
                if (cosine > max_similarity_acc):
                    max_similarity_obj = y
                    max_similarity_acc = cosine
            if (max_similarity_acc > 0):
                print(max_similarity_obj)
                max_similarity.append(max_similarity_obj)

    # Set value of 1 corresponding to the symptoms
    for x in max_similarity:
        symptoms[x.replace(' ', '_')] = 1
    # Prepare Test Data
    df_test = pd.DataFrame(columns=list(symptoms.keys()))
    df_test.loc[0] = np.array(list(symptoms.values()))
    clf = ['', '', '', '']
    # Load all pre-trained models
    clf[0] = load(str("./saved_model/random_forest.joblib"))
    clf[1] = load(str("./saved_model/decision_tree.joblib"))
    clf[2] = load(str("./saved_model/gradient_boost.joblib"))
    clf[3] = load(str("./saved_model/mnb.joblib"))
    result = []
    for i in clf:
        result.append(i.predict(df_test))
    # check which disease chose by max models
    chose_disease = pd.Series(result).value_counts().index.tolist()[np.argmax(list(pd.Series(result).value_counts()))]
    print(chose_disease)
    return chose_disease

# print(predict_disease('My head hurts,my vision is blurred'))
