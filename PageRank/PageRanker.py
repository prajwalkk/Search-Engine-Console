import glob
import pickle
from collections import Counter

import networkx as nx

from Crawler.GenerateGraph import remove_nodes

G = nx.read_gpickle(r'D:\UIC_Projects_Assignments\IR\SearchEngine\Crawler\Links\20200425\final_graph.gpickle')

files = glob.glob(r"D:\UIC_Projects_Assignments\IR\SearchEngine\Crawler\CrawledData\20200425\*")
links = []
for i in files:
    with open(i, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        link = content.split('\n')[0]
        links.append(link)

# Remove nodes that are not a part of the corpus
remove_nodes(links, G)
pageRank = Counter(nx.pagerank(G, alpha=0.85, weight='weight'))
print(len(pageRank))
with open('page_rank.pkl', 'wb') as f:
    pickle.dump(pageRank, f)
