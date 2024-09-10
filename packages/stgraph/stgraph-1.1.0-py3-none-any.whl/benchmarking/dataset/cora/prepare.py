import json

import numpy as np
from rich import inspect
from rich.pretty import pprint
from dgl.data import CoraGraphDataset

# edges = 10556
# num_nodes = 2708
# features per node = 1433

dataset = CoraGraphDataset()
g = dataset[0]

cora_data = {}

# getting the edge list
edges = []
src_list = g.edges()[0].tolist()
dst_list = g.edges()[1].tolist()

for i in range(len(src_list)):
    src = src_list[i]
    dst = dst_list[i]
    edges.append([src, dst])

cora_data['edges'] = edges
cora_data['features'] = g.ndata['feat'].tolist()
cora_data['labels'] = g.ndata['label'].tolist()

# inspect(g.ndata['label'])

inspect(cora_data)

with open("cora.json", "w") as fp:
    json.dump(cora_data, fp)