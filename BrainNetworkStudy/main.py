# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 23:42:01 2018

@author: Mattia
"""

import pyedflib
import mylib 
import mvar
import mygraph
import numpy as np
import pandas as pd
from igraph import Graph, GraphBase
import matplotlib.pyplot as plt

#%% Load data and store into a dataframe

f = pyedflib.EdfReader('../data/S001R01.edf')
# mylib.print_some_stuff(f)

data = mylib.edfToDataFrame(f)
f._close()

#%%
# 1.1

measures = data.T.values
N, n = measures.shape
p = 3
A_est, sigma = mvar.mvar_fit(measures, p)
sigma = np.diag(sigma)  # DTF + PDC support diagonal noise
# compute DTF
D, freqs = mvar.DTF(A_est, sigma)
# compute PDC
P, freqs = mvar.PDC(A_est, sigma)
# take take a graph relative to a specific frequency
freq = 0.111328 # this has to be chosen better
D = D[np.where(freqs == mylib.find_nearest(freqs, freq)),:,:].reshape(64, 64)
G = Graph.Weighted_Adjacency(D.tolist(), mode = 0) # mode 1 is to say we want an indirected graph
G.vs["names"] = data.columns.values
G = mygraph.applyTreshold(G, 0.2)

#%%

# 2.1

# global clustering coefficient 
# https://igraph.org/python/doc/igraph.Graph-class.html#transitivity_avglocal_undirected
print("global clustering coefficient = ", round(G.transitivity_avglocal_undirected(), 3))

# average path length
# https://igraph.org/python/doc/igraph.GraphBase-class.html#average_path_length
print("global average path lenght = ", round(G.average_path_length(directed = False, unconn=True), 3))

local_ind = pd.DataFrame.from_dict(      { 
                "channel" : G.vs["names"] ,
                "strenght" : G.strength(mode = 3),
                "out-strength" : G.strength(mode = 1), 
                "in-strength" : G.strength(mode = 2)
                }
        )

local_ind.set_index("channel", inplace = True)
#print("\nTop 10 channels by degree\n", local_ind.sort_values(by = "strenght", ascending = False)[1:10])
#print("\nTop 10 channels by OUT degree\n", local_ind.sort_values(by = "out-strength", ascending = False)[1:10])
#print("\nTop 10 channels by IN degree\n", local_ind.sort_values(by = "in-strength", ascending = False)[1:10])



# 2.7
local_ind = pd.DataFrame.from_dict(      { 
                "channel" : G.vs["names"] ,
                "strenght" : G.strength(mode = 3,  weights = "weight"),
                "out-strength" : G.strength(mode = 1,  weights = "weight"), 
                "in-strength" : G.strength(mode = 2,  weights = "weight")
                }
        )

local_ind.set_index("channel", inplace = True)
#print("\nTop 10 channels by generalized degree\n", local_ind.sort_values(by = "strenght", ascending = False)[1:10])
#print("\nTop 10 channels by generalized OUT degree\n", local_ind.sort_values(by = "out-strength", ascending = False)[1:10])
#print("\nTop 10 channels by generalized IN degree\n", local_ind.sort_values(by = "in-strength", ascending = False)[1:10])

#%%
# 2.4 Study the behaviour of global graph indices in function of network density

densities = [i*0.1 for i in range(1,10)] # edit these with the ones provided by the prof
# these two lines take some seconds...
clustering_coeffs = [mygraph.applyTreshold(Graph.Weighted_Adjacency(D.tolist(), mode = 0), i).transitivity_avglocal_undirected() for i in densities]
average_path_lengths = [mygraph.applyTreshold(Graph.Weighted_Adjacency(D.tolist(), mode = 0), i).average_path_length(directed = False, unconn=True) for i in densities]

#%%

# Two subplots, the axes array is 1-d
f, axarr = plt.subplots(2, sharex=True, figsize = (9,9))
axarr[0].plot(densities, clustering_coeffs, color = "green")
axarr[0].set_title('Global Indices vs Graph Density')
axarr[0].set_xlabel("density")
axarr[0].set_ylabel("clustering coefficient")
axarr[0].grid(linestyle = ":")
axarr[1].plot(densities, average_path_lengths, color = "red")
axarr[1].set_xlabel("density")
axarr[1].set_ylabel("average path length")
axarr[1].grid(linestyle = ":")
