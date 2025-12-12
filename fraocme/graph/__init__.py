"""Graph package for node-based network utilities."""

from .analysis import (
    count_paths_dag,
    count_paths_with_length,
    enumerate_all_paths,
    enumerate_paths_generator,
    find_bottleneck_edges,
    find_critical_nodes,
    find_sinks,
    find_sources,
    get_all_nodes,
    node_path_counts,
    paths_through_node,
    reverse_graph,
)
from .parser import (
    parse_adjacency_list,
)
from .printer import (
    format_bottleneck_edges,
    format_critical_nodes,
    format_edge,
    format_edge_set,
    format_graph,
    format_graph_as_tree,
    format_node_importance,
    format_node_set,
    format_path_count,
    format_paths,
    format_paths_by_length,
)

__all__ = [
    # Analysis - graph properties
    "get_all_nodes",
    "find_sources",
    "find_sinks",
    "reverse_graph",
    # Analysis - path counting
    "count_paths_dag",
    "count_paths_with_length",
    "node_path_counts",
    # Analysis - path enumeration
    "enumerate_all_paths",
    "enumerate_paths_generator",
    "paths_through_node",
    # Analysis - critical elements
    "find_critical_nodes",
    "find_bottleneck_edges",
    # Parser
    "parse_adjacency_list",
    # Printer - basic formatting
    "format_edge",
    "format_edge_set",
    "format_node_set",
    "format_graph",
    "format_graph_as_tree",
    # Printer - analysis formatting
    "format_paths",
    "format_paths_by_length",
    "format_path_count",
    "format_critical_nodes",
    "format_bottleneck_edges",
    "format_node_importance",
]
