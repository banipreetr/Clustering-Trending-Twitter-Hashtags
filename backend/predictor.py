from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import nltk
from nltk.corpus import stopwords
import pandas as pd
from gensim.test.utils import get_tmpfile
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from nltk.stem import PorterStemmer

from collections import Counter

model1_file = 'doc2vec1.bin'
model2_file = 'doc2vec2.bin'


def tokenize_text(text, stop_words):
    tokens = []
    for sent in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(sent):
            if len(word) < 2:
                continue
            word = word.lower()
            if word not in stop_words:
                tokens.append(word)
    return tokens


def process():
    porter = PorterStemmer()
    df = pd.read_csv('HashTags.csv')

    stop_words = set(stopwords.words('english'))


    model1 = Doc2Vec.load(model1_file)
    model2 = Doc2Vec.load(model2_file)
    vector_mapping = {}
    group = {}
    group_iter = 1
    groupByID = {}

    tweet_volume = {}
    for _, value in df.iterrows():
        model1_infer = np.array([model1.infer_vector(tokenize_text(porter.stem(value['text']),stop_words))])
        model2_infer = np.array([model2.infer_vector(tokenize_text(porter.stem(value['text']),stop_words))])
        
        vector_mapping[value['tag']] = 0.87*model1_infer + 0.13*model2_infer
        group[value['tag']] = group_iter
        tweet_volume[value['tag']] = value['tweet_volume']
        group_iter += 1


        
    fields = list(vector_mapping.keys())
    for i in range(len(fields)):
        for j in range(i+1, len(fields)):
            similarity = cosine_similarity(vector_mapping[fields[i]], vector_mapping[fields[j]])
            if similarity >= 0.55:
                group[fields[j]] = group[fields[i]]
            
    

    for key, value in group.items():
        if value not in groupByID:
            groupByID[value] = []
        
        groupByID[value].append({"name": key, "tweet_volume": tweet_volume[key]})
    
    result = []
    for _, value in groupByID.items():
        result.append(value)
    
    for grp in result:
        sum = 0
        for tag in grp:
            sum += tag['tweet_volume']
        
        for tag in grp:
            tag['tweet_volume'] /= sum
            tag['tweet_volume'] *= 100 

    return result
    

