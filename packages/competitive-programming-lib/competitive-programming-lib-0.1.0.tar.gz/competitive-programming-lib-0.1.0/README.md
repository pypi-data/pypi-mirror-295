# Competitive Programming Library

A comprehensive library of algorithms and data structures commonly used in competitive programming.

## Installation

You can install the package using pip:
```
pip install competitive-programming-lib
```


## Usage

Here's a quick example of how to use some of the algorithms:

```python
from competitive_programming_lib import CompetitiveProgrammingLib as cpl

# Dijkstra's Algorithm
graph = {
    0: {1: 4, 2: 1},
    1: {3: 1},
    2: {1: 2, 3: 5},
    3: {}
}
distances, predecessors = cpl.dijkstra(graph, 0)
print("Shortest distances from node 0:", distances)

# More examples...