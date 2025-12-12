"""
Day 06: Graph Path Analysis

Demonstrates graph utilities:
- Parsing adjacency lists
- Counting paths (DAG)
- Enumerating paths
- Finding critical nodes and bottleneck edges
- Node importance analysis
"""

from fraocme import Solver
from fraocme.graph import (
    count_paths_dag,
    count_paths_with_length,
    enumerate_all_paths,
    find_bottleneck_edges,
    find_critical_nodes,
    find_sinks,
    find_sources,
    get_all_nodes,
    paths_through_node,
)
from fraocme.graph.parser import parse_adjacency_list
from fraocme.graph.printer import (
    format_bottleneck_edges,
    format_critical_nodes,
    format_graph,
    format_graph_as_tree,
    format_node_importance,
    format_path_count,
    format_paths,
    format_paths_by_length,
)
from fraocme.ui.colors import c


class Day6(Solver):
    def parse(self, raw: str) -> dict[str, list[str]]:
        """
        Parse adjacency list graph.

        Expected format:
            you: bbb ccc
            bbb: ddd eee
            ccc: ddd eee fff
        """
        graph = parse_adjacency_list(raw, separator=": ")

        # Debug: Show parsed graph structure
        sources = find_sources(graph)
        sinks = find_sinks(graph)
        all_nodes = get_all_nodes(graph)

        self.debug(c.bold("═" * 50))
        self.debug(c.bold("  Parsed Graph"))
        self.debug(c.bold("═" * 50))
        self.debug(f"Nodes: {c.cyan(len(all_nodes))}")
        self.debug(f"Sources: {c.green(sources)}")
        self.debug(f"Sinks: {c.red(sinks)}")
        self.debug("")
        self.debug(format_graph(graph, highlight_nodes=sources | sinks))

        return graph

    def part1(self, graph: dict[str, list[str]]) -> int:
        """
        Part 1: Count all paths from 'you' to 'out'.

        Find every possible path through the device network.
        """
        start, end = "you", "out"

        self.debug(c.bold("\n" + "═" * 50))
        self.debug(c.bold("  Part 1: Count All Paths"))
        self.debug(c.bold("═" * 50))

        # Count paths efficiently (DP)
        count = count_paths_dag(graph, start, end)
        self.debug(format_path_count(count, start, end))
        self.debug("")

        # Show paths grouped by length
        length_counts = count_paths_with_length(graph, start, end)
        self.debug(format_paths_by_length(length_counts))
        self.debug("")

        # Enumerate and display paths (limited)
        paths = enumerate_all_paths(graph, start, end, max_paths=10)
        self.debug(format_paths(paths, start=start, end=end, max_display=10))
        self.debug("")

        # Show as tree
        path_counts = {
            node: paths_through_node(graph, start, end, node)
            for node in get_all_nodes(graph)
        }
        self.debug(c.bold("Path Tree:"))
        self.debug(
            format_graph_as_tree(graph, root=start, end=end, path_counts=path_counts)
        )

        return count

    def part2(self, graph: dict[str, list[str]]) -> int:
        """
        Part 2: Find the most important non-critical node.

        Critical nodes appear in ALL paths (removing them breaks connectivity).
        We want to find the non-critical node that appears in the MOST paths.
        This is the "most important optional node" - a good candidate to monitor.

        Returns the number of paths through that node.
        """
        start, end = "you", "out"

        self.debug(c.bold("\n" + "═" * 50))
        self.debug(c.bold("  Part 2: Critical Analysis"))
        self.debug(c.bold("═" * 50))

        # Find critical nodes (appear in ALL paths)
        critical = find_critical_nodes(graph, start, end)
        self.debug(format_critical_nodes(critical, start=start, end=end))
        self.debug("")

        # Find bottleneck edges (appear in ALL paths)
        bottlenecks = find_bottleneck_edges(graph, start, end)
        self.debug(format_bottleneck_edges(bottlenecks, start=start, end=end))
        self.debug("")

        # Calculate importance for all nodes
        total_paths = count_paths_dag(graph, start, end)
        all_nodes = get_all_nodes(graph)

        importance = {
            node: paths_through_node(graph, start, end, node) for node in all_nodes
        }

        self.debug(
            format_node_importance(importance, total_paths, start=start, end=end)
        )
        self.debug("")

        # Find most important NON-critical node
        non_critical = all_nodes - critical

        if not non_critical:
            self.debug(c.yellow("All nodes are critical - no optional nodes exist!"))
            return 0

        most_important = max(non_critical, key=lambda n: importance[n])
        most_important_count = importance[most_important]

        # Show result
        self.debug(c.bold("─" * 40))
        self.debug(c.bold("Result:"))
        self.debug(
            f"  Most important non-critical node: {c.cyan(c.bold(most_important))}"
        )
        self.debug(
            f"  Appears in {c.green(most_important_count)}/{c.cyan(total_paths)} paths "
            f"({c.yellow(f'{most_important_count / total_paths * 100:.1f}%')})"
        )
        self.debug("")

        # Show graph with highlights
        self.debug(c.bold("Graph with analysis:"))
        self.debug(
            format_graph(
                graph,
                title="Critical Analysis",
                highlight_nodes=critical | {most_important},
                highlight_edges=bottlenecks,
            )
        )

        return most_important_count
