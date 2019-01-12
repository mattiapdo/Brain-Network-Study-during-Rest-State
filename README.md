# README

### Usage

`python main.py`



freq = 10 Hz roughly corresponds to Alpha (mu) ERD

freq = 28 Hz roughly corresponds to Beta ERS



### Small World Networks

Duncan Watts and Steven Strogatz found that

[1]: https://en.wikipedia.org/wiki/Small-world_network#cite_note-3	"Watts, Duncan J.; Strogatz, Steven H. (June 1998). &quot;Collective dynamics of &#39;small-world&#39; networks&quot;. Nature. 393 (6684): 440–442"

graphs can be classified according to two important global indexes:

1. clustering coefficient
2. average shortest path

We say a network to be a **small world network** when

- for any given node, neighbors of that node are likely to be neighbors of each other (read: high clustering coefficient)

- the average distance L between two nodes (average shortest path) scales as the logarithm of the number of nodes in the network 
  $$
  L \sim \log N
  $$



#### Small World Network Index

https://en.wikipedia.org/wiki/Small-world_network

https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3604768/

https://arxiv.org/pdf/cond-mat/9903108.pdf

The `bctpy` is the `Python` translation of the Brain Connectivity Toolbox (natively in `MATLAB`) https://github.com/aestrivex/bctpy

- download the repository
- run  `python setup.py install` 

We make use of two methods:

`bct.randmio_dir(R, iter)`:  this function randomizes a directed network, while preserving the in- and out-degree distributions. In weighted networks, the function preserves the out-strength but not the in-strength distributions.

`bct.latmio_dir(R, iter, D=None)`: this function “latticizes” a directed network, while preserving the in- and out-degree distributions. In weighted networks, the function preserves the out-strength but not the in-strength distributions.



### Motif Analysis

Roughly speaking, motifs in a given network are induced subgraphs which are recurrent and statistically significant: it appears with a higher frequency that it would be expected in 'similar' random networks.

So let $G$ be a network, and $G_k$ one of its own subnetworks composed by $k$ nodes. If we count how many times $G_k$ appears in $G$ for some $k$, we obtain something really analogous to a frequency spectrum, that can give a description about the basic building blocks of the net.

We can immediately guess that the action of counting how many times a given $G_k$ occurs in $G$ is really computationally expensive (note also that the cardinality of the set $\{ G_k \text{ for k} \in \mathbb{N\} }$ grows exponentially with $k$). That's why one usually concentrate just on subgraphs of size $k = 3, 4$.

To be more formal, we say an induced subgraph $G_k$ of $G$ to be a **motif** (an over represented subgraph) if, for some set of parameters {p, U, D, N} these three requirements are satisfied:

1. $\mathbb{P}(f_{rand}(G_k) > f_{original}(G_k)) < p$
2. $f_{original}(G_k) > U$
3. $f_{original}(G_k)- f_{rand}(G_k)>D f_{rand}(G_k)$

Then a $Z$ score is assigned to each induced subgraph
$$
Z = \frac{f_{original}(G_k) - <f_{rand}(G_k)>}{s(f_{rand}(G_k))}
$$
   where $s(\cdot)$ is the sample standard deviation. 

Important because of their interpretations in many case studies are **anti-motifs** also: they are induced subgraphs that satisfy the following requirements:

1. $\mathbb{P}(f_{rand}(G_k) < f_{original}(G_k)) < p$
2. $f_{original}(G_k)- f_{rand}(G_k) < D f_{rand}(G_k)$

To perform motif analysis (i.e. to find motifs and anti-motifs in our network), we make use of the software `mfinder` version 1.2.

It is available at http://www.weizmann.ac.il/mcb/UriAlon/research/network-motifs.

It has not a graphical interface, and we must use the propt, running a command like:

`mfinder1.2 ./data/inputForMA.txt -s 3 -r 1000 `

Where..

- `-s` is the desired subgraph size

- `-r` is the number of random networks to be generated

