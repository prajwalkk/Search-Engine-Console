import glob
import re
import string

import joblib
import nltk
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer


def tokenize(doc):
    doc_1 = doc.translate(doc.maketrans('', "", string.punctuation))
    word_tokens = nltk.word_tokenize(doc_1)
    no_stop_doc = [w for w in word_tokens if w.isalpha()]
    return no_stop_doc


data_array = []
files = glob.glob("../Crawler/CrawledData/20200425/*")

for file in files:
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        data_array.append([re.sub(r'\.\./Crawler/CrawledData/20200425/', '', file),
                           re.sub(' +', ' ', f.read())])

df = pd.DataFrame(data_array, columns=['File', 'Contents'])
df = pd.DataFrame(data_array, columns=['File', 'Contents'])
df['Link'] = df['Contents'].apply(lambda x: x.split("\n")[0])
df['Doc'] = df['Contents'].apply(lambda x: x.split("\n")[1])

vectorizer = TfidfVectorizer(tokenizer=tokenize,
                             stop_words=stopwords.words('english'))
tfidfs = vectorizer.fit_transform(df['Doc'])

joblib.dump(vectorizer, 'vectorizer.joblib')
joblib.dump(tfidfs, 'tfidf.joblib')

df.to_pickle('dataFrame_bk.pkl')
