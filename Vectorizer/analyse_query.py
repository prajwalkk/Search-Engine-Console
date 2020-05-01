import joblib
import pickle

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

RESULT_LIMIT = 10
QUERY_EXPN_LIMIT = 20
vectorizer = joblib.load('vectorizer.joblib')
tfidfs = joblib.load('tfidf.joblib')
df = pd.read_pickle('dataFrame_bk.pkl')
page_rank = pickle.load(open('D:\\UIC_Projects_Assignments\\IR\\SearchEngine\\PageRank\\page_rank.pkl', 'rb'))

print(type(page_rank))

query = str(input('Enter Query: '))
print(query)
q_tfidf = vectorizer.transform([query])
print(q_tfidf.shape, tfidfs.shape)

dict_cossim = {}
for i in range(len(df)):
    int_dict = {}
    int_dict = {'Link': df.loc[i]['Link'],
                'Content': df.loc[i]['Doc'],
                'CosSim': cosine_similarity(tfidfs[i], q_tfidf),
                'PageRank': page_rank[df.loc[i]['Link']]
                }
    dict_cossim[i] = int_dict
cosine_similarity(tfidfs[0], q_tfidf)

top_n = sorted(dict_cossim.keys(),
               key=lambda x: dict_cossim[x]['CosSim'][0],
               reverse=True)[:RESULT_LIMIT]

top_n_page_rank = sorted(dict_cossim.keys(),
                         key=lambda x: (dict_cossim[x]['CosSim'][0] + dict_cossim[x]['PageRank']),
                         reverse=True)[:RESULT_LIMIT]

print("Cosssim")
for i in top_n:
    print(dict_cossim[i]['Link'], dict_cossim[i]['CosSim'][0])

print("Cosssim + PageRanks")
for i in top_n_page_rank:
    print(dict_cossim[i]['Link'], dict_cossim[i]['CosSim'][0] + dict_cossim[i]['PageRank'])

# Calculating the Query terms to expand
relevant_docs_sum = np.sum(tfidfs[top_n], axis=0)
irrelevant = np.subtract(np.sum(tfidfs, axis=0),
                         relevant_docs_sum)
alpha, beta, gamma = 1, 0.75, 0.15
nr, d_nr = (10, tfidfs.shape[0] - 10)
query_m = q_tfidf + (beta * relevant_docs_sum / nr) - (gamma * irrelevant / d_nr)
yy = np.asarray(query_m).flatten()
indices = np.argpartition(yy, -QUERY_EXPN_LIMIT)[-QUERY_EXPN_LIMIT:]

features = vectorizer.get_feature_names()
queries_terms = [features[i] for i in indices]

print(queries_terms)
