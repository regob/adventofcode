import re
import time
import random
from itertools import product
from collections import namedtuple
from multiprocessing import Pool
import networkx as nx
import matplotlib.pyplot as plt

INPUT_FILE = 'input/2023_25.txt'

with open(INPUT_FILE) as fp:
    txt = fp.read().strip()

e = {}

for line in txt.split('\n'):
    nd, neighs = line.split(':')
    neighs = neighs.strip().split()
    s = e.setdefault(nd, set())
    s |= set(neighs)
    for neigh in neighs:
        e.setdefault(neigh, set()).add(nd)

nodes = list(e.keys())
n = len(nodes)

g = nx.Graph()

for nd, neighs in e.items():
    for neigh in neighs:
        g.add_edge(nd, neigh, name=f"{nd}-{neigh}")

nx.write_graphml(g, 'day25.graphml')
# run Yifan Hu layout in Gephi, then delete the 3 edges in the middle
# run connected components stat and export from data lab to csv to check component sizes
