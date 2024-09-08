micodag is a Python package for learning Bayesian network using mixed integer convex programming. 

- Related paper:
  1. Integer Programming for Learning Directed Acyclic Graphs from Non-identifiable Gaussian Models
  2. An Asymptotically Optimal Coordinate Descent Algorithm for Learning Bayesian Networks from Gaussian Models
- Authors: Tong Xu, Armeen Taeb, Simge Kucukyavuz, Ali Shojaie
- Code for reproducing experiments in the paper is available on [Github](https://github.com/AtomXT/MICP-NID)
- Source code: https://github.com/AtomXT/micodag

# Install

```angular2html
$ pip install micodag
```

# Simple example

Please download the following test files:
    [data](https://github.com/AtomXT/MICP-NID/blob/b600b9ecbe51cc3d633ca17c6d1a760658acff9d/Data/RealWorldDatasetsTXu/3bowling/data_3bowling_n_500_iter_1.csv),
    [true graph](https://github.com/AtomXT/MICP-NID/blob/b600b9ecbe51cc3d633ca17c6d1a760658acff9d/Data/RealWorldDatasetsTXu/3bowling/Sparse_Original_edges_9_500_3.txt),
and
    [moral graph](https://github.com/AtomXT/MICP-NID/blob/b600b9ecbe51cc3d633ca17c6d1a760658acff9d/Data/RealWorldDatasetsTXu/3bowling/Sparse_Moral_edges_9_500_3.txt).


```
import micodag as mic
import pandas as pd
import numpy as np

data = pd.read_csv("data_3bowling_n_500_iter_1.csv", header=None)
moral = pd.read_table('Sparse_Moral_edges_9_500_3.txt', delimiter=",", header=None)
true_B = pd.read_table('Sparse_Original_edges_9_500_3.txt', delimiter=",", header=None)
n, p = data.shape
lam = 12*np.log(p)/n

true_moral_ = [[0] * data.shape[1] for i in range(data.shape[1])]
for i in range(len(moral)):
    true_moral_[moral.iloc[i, 0] - 1][moral.iloc[i, 1] - 1] = 1
true_moral_ = np.array(true_moral_)

RGAP, B, _, obj, _ = mic.optimize(data, moral, lam)
est, min_obj = mic.CD(data, true_moral_, MAX_cycles=400,
                  lam=np.sqrt(12 * np.log(p) / n))
B_arcs = pd.DataFrame([[i+1, j+1] for i in range(p) for j in range(p) if B[i, j] != 0])
B_arcs_cd = pd.DataFrame([[i+1, j+1] for i in range(p) for j in range(p) if est[i, j] != 0])
print(B_arcs)
print(B_arcs_cd)
print(true_B)

```
