import unittest

from fraocme.graph.analysis import (
    count_paths_dag,
    count_paths_with_length,
    enumerate_all_paths,
    find_bottleneck_edges,
    find_critical_nodes,
    get_all_nodes,
    paths_through_node,
)
from fraocme.graph.printer import (
    format_bottleneck_edges,
    format_critical_nodes,
    format_edge,
    format_edge_set,
    format_graph,
    format_graph_as_tree,
    format_node_importance,
    format_node_set,
    format_path,
    format_path_count,
    format_paths,
    format_paths_by_length,
)


class TestFormatPath(unittest.TestCase):
    """Test format_path function."""

    def test_format_path_basic(self):
        path = ["A", "B", "C"]
        result = format_path(path)
        self.assertIsInstance(result, str)
        self.assertIn("A", result)
        self.assertIn("B", result)
        self.assertIn("C", result)

    def test_format_path_with_start_end(self):
        path = ["start", "middle", "end"]
        result = format_path(path, start="start", end="end")
        self.assertIsInstance(result, str)
        self.assertIn("start", result)
        self.assertIn("end", result)

    def test_format_path_empty(self):
        result = format_path([])
        self.assertIsInstance(result, str)

    def test_format_path_single_node(self):
        result = format_path(["A"])
        self.assertIn("A", result)


class TestFormatEdge(unittest.TestCase):
    """Test format_edge function."""

    def test_format_edge_basic(self):
        result = format_edge(("A", "B"))
        self.assertIsInstance(result, str)
        self.assertIn("A", result)
        self.assertIn("B", result)

    def test_format_edge_with_start(self):
        result = format_edge(("start", "B"), start="start")
        self.assertIn("start", result)

    def test_format_edge_with_end(self):
        result = format_edge(("A", "end"), end="end")
        self.assertIn("end", result)


class TestFormatNodeSet(unittest.TestCase):
    """Test format_node_set function."""

    def test_format_node_set_basic(self):
        nodes = {"A", "B", "C"}
        result = format_node_set(nodes)
        self.assertIsInstance(result, str)
        self.assertIn("A", result)
        self.assertIn("B", result)
        self.assertIn("C", result)

    def test_format_node_set_empty(self):
        result = format_node_set(set())
        self.assertIsInstance(result, str)

    def test_format_node_set_with_start_end(self):
        nodes = {"start", "middle", "end"}
        result = format_node_set(nodes, start="start", end="end")
        self.assertIn("start", result)
        self.assertIn("end", result)

    def test_format_node_set_sorted(self):
        nodes = {"C", "A", "B"}
        result = format_node_set(nodes, sort=True)
        # A should appear before B, B before C
        self.assertLess(result.find("A"), result.find("B"))
        self.assertLess(result.find("B"), result.find("C"))


class TestFormatEdgeSet(unittest.TestCase):
    """Test format_edge_set function."""

    def test_format_edge_set_basic(self):
        edges = {("A", "B"), ("B", "C")}
        result = format_edge_set(edges)
        self.assertIsInstance(result, str)
        self.assertIn("A", result)
        self.assertIn("B", result)
        self.assertIn("C", result)

    def test_format_edge_set_empty(self):
        result = format_edge_set(set())
        self.assertIsInstance(result, str)

    def test_format_edge_set_with_start_end(self):
        edges = {("start", "middle"), ("middle", "end")}
        result = format_edge_set(edges, start="start", end="end")
        self.assertIn("start", result)
        self.assertIn("end", result)


class TestFormatPaths(unittest.TestCase):
    """Test format_paths function."""

    def setUp(self):
        self.paths = [
            ["A", "B", "D"],
            ["A", "C", "D"],
            ["A", "B", "C", "D"],
        ]

    def test_format_paths_basic(self):
        result = format_paths(self.paths)
        self.assertIsInstance(result, str)
        self.assertIn("3", result)  # 3 paths

    def test_format_paths_with_start_end(self):
        result = format_paths(self.paths, start="A", end="D")
        self.assertIn("A", result)
        self.assertIn("D", result)

    def test_format_paths_empty(self):
        result = format_paths([])
        self.assertIsInstance(result, str)

    def test_format_paths_max_display(self):
        result = format_paths(self.paths, max_display=2)
        self.assertIsInstance(result, str)

    def test_format_paths_group_by_length(self):
        result = format_paths(self.paths, group_by_length=True)
        self.assertIn("Length", result)


class TestFormatPathCount(unittest.TestCase):
    """Test format_path_count function."""

    def test_format_path_count_basic(self):
        result = format_path_count(5, "start", "end")
        self.assertIsInstance(result, str)
        self.assertIn("5", result)
        self.assertIn("start", result)
        self.assertIn("end", result)

    def test_format_path_count_zero(self):
        result = format_path_count(0, "A", "B")
        self.assertIn("0", result)

    def test_format_path_count_large(self):
        result = format_path_count(1000000, "A", "B")
        self.assertIn("1000000", result)


class TestFormatPathsByLength(unittest.TestCase):
    """Test format_paths_by_length function."""

    def test_format_paths_by_length_basic(self):
        length_counts = {2: 3, 3: 5, 4: 2}
        result = format_paths_by_length(length_counts)
        self.assertIsInstance(result, str)
        self.assertIn("2", result)
        self.assertIn("3", result)
        self.assertIn("4", result)

    def test_format_paths_by_length_empty(self):
        result = format_paths_by_length({})
        self.assertIsInstance(result, str)

    def test_format_paths_by_length_single(self):
        result = format_paths_by_length({3: 10})
        self.assertIn("3", result)
        self.assertIn("10", result)


class TestFormatGraph(unittest.TestCase):
    """Test format_graph function."""

    def setUp(self):
        self.graph = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": [],
        }

    def test_format_graph_basic(self):
        result = format_graph(self.graph)
        self.assertIsInstance(result, str)
        self.assertIn("A", result)
        self.assertIn("B", result)
        self.assertIn("C", result)
        self.assertIn("D", result)

    def test_format_graph_with_title(self):
        result = format_graph(self.graph, title="Test Graph")
        self.assertIn("Test Graph", result)

    def test_format_graph_highlight_nodes(self):
        result = format_graph(self.graph, highlight_nodes={"A", "D"})
        self.assertIn("A", result)
        self.assertIn("D", result)

    def test_format_graph_highlight_edges(self):
        result = format_graph(self.graph, highlight_edges={("A", "B")})
        self.assertIn("A", result)
        self.assertIn("B", result)

    def test_format_graph_empty(self):
        result = format_graph({})
        self.assertIsInstance(result, str)

    def test_format_graph_max_nodes(self):
        large_graph = {f"N{i}": [f"N{i + 1}"] for i in range(100)}
        result = format_graph(large_graph, max_nodes=10)
        self.assertIsInstance(result, str)


class TestFormatCriticalNodes(unittest.TestCase):
    """Test format_critical_nodes function."""

    def test_format_critical_nodes_basic(self):
        critical = {"A", "B", "C"}
        result = format_critical_nodes(critical)
        self.assertIsInstance(result, str)
        self.assertIn("A", result)
        self.assertIn("B", result)
        self.assertIn("C", result)
        self.assertIn("Critical", result)

    def test_format_critical_nodes_with_start_end(self):
        critical = {"start", "middle", "end"}
        result = format_critical_nodes(critical, start="start", end="end")
        self.assertIn("start", result)
        self.assertIn("end", result)

    def test_format_critical_nodes_empty(self):
        result = format_critical_nodes(set())
        self.assertIsInstance(result, str)

    def test_format_critical_nodes_with_total_paths(self):
        critical = {"A", "B"}
        result = format_critical_nodes(critical, total_paths=10)
        self.assertIsInstance(result, str)


class TestFormatBottleneckEdges(unittest.TestCase):
    """Test format_bottleneck_edges function."""

    def test_format_bottleneck_edges_basic(self):
        bottlenecks = {("A", "B"), ("B", "C")}
        result = format_bottleneck_edges(bottlenecks)
        self.assertIsInstance(result, str)
        self.assertIn("A", result)
        self.assertIn("B", result)
        self.assertIn("C", result)
        self.assertIn("Bottleneck", result)

    def test_format_bottleneck_edges_with_start_end(self):
        bottlenecks = {("start", "middle")}
        result = format_bottleneck_edges(bottlenecks, start="start", end="end")
        self.assertIn("start", result)

    def test_format_bottleneck_edges_empty(self):
        result = format_bottleneck_edges(set())
        self.assertIsInstance(result, str)


class TestFormatNodeImportance(unittest.TestCase):
    """Test format_node_importance function."""

    def test_format_node_importance_basic(self):
        counts = {"A": 10, "B": 5, "C": 3}
        result = format_node_importance(counts, total_paths=10)
        self.assertIsInstance(result, str)
        self.assertIn("A", result)
        self.assertIn("B", result)
        self.assertIn("C", result)

    def test_format_node_importance_with_start_end(self):
        counts = {"start": 10, "middle": 5, "end": 10}
        result = format_node_importance(
            counts, total_paths=10, start="start", end="end"
        )
        self.assertIn("start", result)
        self.assertIn("end", result)

    def test_format_node_importance_empty(self):
        result = format_node_importance({}, total_paths=0)
        self.assertIsInstance(result, str)

    def test_format_node_importance_max_display(self):
        counts = {f"N{i}": i for i in range(50)}
        result = format_node_importance(counts, total_paths=50, max_display=10)
        self.assertIsInstance(result, str)


class TestFormatGraphAsTree(unittest.TestCase):
    """Test format_graph_as_tree function."""

    def setUp(self):
        self.graph = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": [],
        }

    def test_format_graph_as_tree_basic(self):
        result = format_graph_as_tree(self.graph, root="A")
        self.assertIsInstance(result, str)
        self.assertIn("A", result)
        self.assertIn("B", result)
        self.assertIn("C", result)

    def test_format_graph_as_tree_with_end(self):
        result = format_graph_as_tree(self.graph, root="A", end="D")
        self.assertIn("A", result)
        self.assertIn("D", result)

    def test_format_graph_as_tree_with_path_counts(self):
        path_counts = {"A": 2, "B": 1, "C": 1, "D": 2}
        result = format_graph_as_tree(self.graph, root="A", path_counts=path_counts)
        self.assertIsInstance(result, str)

    def test_format_graph_as_tree_max_depth(self):
        deep_graph = {f"N{i}": [f"N{i + 1}"] for i in range(20)}
        deep_graph["N20"] = []
        result = format_graph_as_tree(deep_graph, root="N0", max_depth=5)
        self.assertIsInstance(result, str)

    def test_format_graph_as_tree_max_branches(self):
        wide_graph = {"root": [f"child{i}" for i in range(20)]}
        for i in range(20):
            wide_graph[f"child{i}"] = []
        result = format_graph_as_tree(wide_graph, root="root", max_branches=3)
        self.assertIsInstance(result, str)


class TestPrinterIntegration(unittest.TestCase):
    """Integration tests using real graph analysis results."""

    def setUp(self):
        # Day 11 example graph
        self.graph = {
            "you": ["bbb", "ccc"],
            "bbb": ["ddd", "eee"],
            "ccc": ["ddd", "eee", "fff"],
            "ddd": ["ggg"],
            "eee": ["out"],
            "fff": ["out"],
            "ggg": ["out"],
            "out": [],
        }
        self.start = "you"
        self.end = "out"

    def test_integration_format_path_count(self):
        count = count_paths_dag(self.graph, self.start, self.end)
        result = format_path_count(count, self.start, self.end)
        self.assertIn("5", result)
        self.assertIn("you", result)
        self.assertIn("out", result)

    def test_integration_format_paths(self):
        paths = enumerate_all_paths(self.graph, self.start, self.end)
        result = format_paths(paths, start=self.start, end=self.end)
        self.assertIn("5", result)

    def test_integration_format_paths_by_length(self):
        lengths = count_paths_with_length(self.graph, self.start, self.end)
        result = format_paths_by_length(lengths)
        self.assertIn("3", result)  # Length 3 paths
        self.assertIn("4", result)  # Length 4 paths

    def test_integration_format_critical_nodes(self):
        critical = find_critical_nodes(self.graph, self.start, self.end)
        result = format_critical_nodes(critical, start=self.start, end=self.end)
        self.assertIn("you", result)
        self.assertIn("out", result)

    def test_integration_format_bottleneck_edges(self):
        bottlenecks = find_bottleneck_edges(self.graph, self.start, self.end)
        result = format_bottleneck_edges(bottlenecks, start=self.start, end=self.end)
        self.assertIsInstance(result, str)

    def test_integration_format_node_importance(self):
        total = count_paths_dag(self.graph, self.start, self.end)
        counts = {
            node: paths_through_node(self.graph, self.start, self.end, node)
            for node in get_all_nodes(self.graph)
        }
        result = format_node_importance(counts, total, start=self.start, end=self.end)
        self.assertIn("you", result)
        self.assertIn("out", result)

    def test_integration_format_graph(self):
        critical = find_critical_nodes(self.graph, self.start, self.end)
        bottlenecks = find_bottleneck_edges(self.graph, self.start, self.end)
        result = format_graph(
            self.graph,
            title="Day 11 Graph",
            highlight_nodes=critical,
            highlight_edges=bottlenecks,
        )
        self.assertIn("Day 11 Graph", result)

    def test_integration_format_graph_as_tree(self):
        path_counts = {
            node: paths_through_node(self.graph, self.start, self.end, node)
            for node in get_all_nodes(self.graph)
        }
        result = format_graph_as_tree(
            self.graph,
            root=self.start,
            end=self.end,
            path_counts=path_counts,
        )
        self.assertIn("you", result)


if __name__ == "__main__":
    unittest.main()
