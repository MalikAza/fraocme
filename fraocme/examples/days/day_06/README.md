# Day 06 — Graph utilities example

This example demonstrates several `fraocme.graph` utilities for working with
node-based directed graphs.

Files
- `solution.py`: Solver showing how to parse a simple adjacency-list graph and
  use `count_paths_dag`, `enumerate_all_paths`, and `find_critical_nodes`.

Input format
- A simple adjacency list, one edge per line, e.g.:
```
you -> a
A -> b
b -> out
A -> b
```

How it works
- `parse()` uses `parse_adjacency_list()` to build a `dict[str, list[str]]`.
- `part1()` counts all DAG paths from node `you` to node `out`, prints a small
  debug summary of the count, shows up to 10 example paths, and prints critical
  nodes (nodes that every path passes through).

Run
- Example run:

```powershell
fraocme run 6 --debug
```

This will print debug output demonstrating the graph functions in action.