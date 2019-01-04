# -*- coding: utf-8 -*-

from igraph import *
import numpy as np

def randargmin(b,**kw):
  """ a random tie-breaking argmax"""
  return np.argmin(np.random.random(b.shape) * (b==b.min()), **kw)

def applyTreshold(G, threshold):
    while(G.density() > threshold):
        adj = np.matrix(G.get_adjacency(attribute = "weight")._get_data())
        masked = np.ma.masked_where(adj == 0, adj)
        G.delete_edges([np.unravel_index(randargmin(masked), masked.shape)])
    return G



