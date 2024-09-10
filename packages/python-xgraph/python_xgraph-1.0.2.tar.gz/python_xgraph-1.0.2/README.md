# python-xgraph

`python-xgraph` is a simple Python library for working with graphs. It provides basic functionalities like adding vertices and edges, performing DFS and BFS, detecting cycles, and more.

## Installation

You can install the package via pip:

```bash
pip install python-xgraph
```

## Usage

```
from python_xgraph import Graph

g = Graph(directed=True)
g.add_vertex("A")
g.add_edge("A", "B")
print(g.dfs("A"))
```

Initialize using a dictionary
```
from python_xgraph import Graph

g = Graph({"A":["B","C"], "B":["D","E"], "C":["X","Y"]}, directed=True)

print(g.has_cycle())
print(g.topological_sort(reverse=True))

```