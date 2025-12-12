from functools import cache


def reverse_graph(graph: dict[str, list[str]]) -> dict[str, list[str]]:
    """
    Reverse edge directions in a graph.

    Example:
        >>> reverse_graph({'A': ['B', 'C'], 'B': ['C']})
        {'B': ['A'], 'C': ['A', 'B']}
    """
    reversed_graph = {}
    for node, neighbors in graph.items():
        if node not in reversed_graph:
            reversed_graph[node] = []
        for neighbor in neighbors:
            if neighbor not in reversed_graph:
                reversed_graph[neighbor] = []
            reversed_graph[neighbor].append(node)
    return reversed_graph


def get_all_nodes(graph: dict[str, list[str]]) -> set[str]:
    """
    Get all nodes in graph (including those only appearing as neighbors).

    Example:
        >>> get_all_nodes({'A': ['B', 'C']})
        {'A', 'B', 'C'}
    """
    nodes = set(graph.keys())
    for neighbors in graph.values():
        nodes.update(neighbors)
    return nodes


def find_sources(graph: dict[str, list[str]]) -> set[str]:
    """
    Find source nodes (nodes with no incoming edges).

    Example:
        >>> find_sources({'A': ['B'], 'B': ['C']})
        {'A'}
    """
    all_nodes = get_all_nodes(graph)
    has_incoming = set()
    for neighbors in graph.values():
        has_incoming.update(neighbors)
    return all_nodes - has_incoming


def find_sinks(graph: dict[str, list[str]]) -> set[str]:
    """
    Find sink nodes (nodes with no outgoing edges).

    Example:
        >>> find_sinks({'A': ['B'], 'B': ['C']})
        {'C'}
    """
    all_nodes = get_all_nodes(graph)
    has_outgoing = {node for node, neighbors in graph.items() if neighbors}
    return all_nodes - has_outgoing


# =============================================================================
# PATH COUNTING (for DAGs - much faster than enumerating all paths!)
# =============================================================================


def count_paths_dag(graph: dict[str, list[str]], start: str, end: str) -> int:
    """
    Count all paths from start to end in a DAG using dynamic programming.
    DAG - Directed Acyclic Graph (no cycles).

    Much faster than enumerating all paths - O(V + E) instead of O(paths).

    Args:
        graph: Adjacency list (must be a DAG - no cycles!)
        start: Starting node
        end: Ending node

    Returns:
        Number of distinct paths from start to end

    Example:
        >>> graph = {'you': ['bbb', 'ccc'], 'bbb': ['ddd', 'eee'],
        ...          'ccc': ['ddd', 'eee', 'fff'], 'ddd': ['ggg'],
        ...          'eee': ['out'], 'fff': ['out'], 'ggg': ['out']}
        >>> count_paths_dag(graph, 'you', 'out')
        5
    """

    @cache
    def count_from(node: str) -> int:
        if node == end:
            return 1
        if node not in graph:
            return 0
        return sum(count_from(neighbor) for neighbor in graph[node])

    return count_from(start)


def count_paths_with_length(
    graph: dict[str, list[str]], start: str, end: str
) -> dict[int, int]:
    """
    Count paths from start to end, grouped by path length.

    Returns:
        Dict mapping path_length -> count of paths with that length

    Example:
        >>> count_paths_with_length(graph, 'you', 'out')
        {3: 2, 4: 3}  # 2 paths of length 3, 3 paths of length 4
    """
    from collections import defaultdict

    @cache
    def count_from(node: str) -> dict[int, int]:
        if node == end:
            return {0: 1}
        if node not in graph:
            return {}

        result = defaultdict(int)
        for neighbor in graph[node]:
            for length, count in count_from(neighbor).items():
                result[length + 1] += count
        return dict(result)

    return count_from(start)


# =============================================================================
# PATH ENUMERATION (when you need the actual paths, not just count)
# =============================================================================


def enumerate_all_paths(
    graph: dict[str, list[str]], start: str, end: str, max_paths: int | None = None
) -> list[list[str]]:
    """
    Enumerate all paths from start to end.

    WARNING: Can be exponentially many paths!
    Use `count_paths_dag` if you only need the path count.

    Args:
        graph: Adjacency list
        start: Starting node
        end: Ending node
        max_paths: Optional limit on paths to return (for safety)

    Returns:
        List of paths, where each path is a list of nodes

    Example:
        >>> enumerate_all_paths(graph, 'you', 'out')
        [['you', 'bbb', 'ddd', 'ggg', 'out'], ['you', 'bbb', 'eee', 'out'], ...]
    """
    all_paths = []

    def dfs(node: str, path: list[str]):
        if max_paths and len(all_paths) >= max_paths:
            return

        if node == end:
            all_paths.append(path[:])
            return

        for neighbor in graph.get(node, []):
            if neighbor not in path:  # Avoid cycles
                path.append(neighbor)
                dfs(neighbor, path)
                path.pop()

    dfs(start, [start])
    return all_paths


def enumerate_paths_generator(graph: dict[str, list[str]], start: str, end: str):
    """
    Generator version - yields paths one at a time (memory efficient).

    Example:
        >>> for path in enumerate_paths_generator(graph, 'you', 'out'):
        ...     print(path)
    """

    def dfs(node: str, path: list[str]):
        if node == end:
            yield path[:]
            return

        for neighbor in graph.get(node, []):
            if neighbor not in path:
                path.append(neighbor)
                yield from dfs(neighbor, path)
                path.pop()

    yield from dfs(start, [start])


# =============================================================================
# PATH ANALYSIS
# =============================================================================


def find_critical_nodes(graph: dict[str, list[str]], start: str, end: str) -> set[str]:
    """
    Find nodes that appear in ALL paths from start to end.
    These are "critical" - if they fail, no path exists.

    Example:
        >>> find_critical_nodes(graph, 'you', 'out')
        {'you', 'out'}  # These must appear in every path
    """
    all_paths = enumerate_all_paths(graph, start, end)
    if not all_paths:
        return set()

    # Intersection of all paths
    critical = set(all_paths[0])
    for path in all_paths[1:]:
        critical &= set(path)

    return critical


def find_bottleneck_edges(
    graph: dict[str, list[str]], start: str, end: str
) -> set[tuple[str, str]]:
    """
    Find edges that appear in ALL paths from start to end.

    Example:
        >>> find_bottleneck_edges(graph, 'A', 'D')
        {('A', 'B'), ('C', 'D')}  # If A->B or C->D fails, no path exists
    """
    all_paths = enumerate_all_paths(graph, start, end)
    if not all_paths:
        return set()

    def path_edges(path):
        return {(path[i], path[i + 1]) for i in range(len(path) - 1)}

    bottlenecks = path_edges(all_paths[0])
    for path in all_paths[1:]:
        bottlenecks &= path_edges(path)

    return bottlenecks


def paths_through_node(
    graph: dict[str, list[str]], start: str, end: str, through: str
) -> int:
    """
    Count paths from start to end that pass through a specific node.

    Example:
        >>> paths_through_node(graph, 'you', 'out', 'bbb')
        2  # 2 paths go through 'bbb'
    """
    # Paths from start to through × Paths from through to end
    paths_to = count_paths_dag(graph, start, through)
    paths_from = count_paths_dag(graph, through, end)
    return paths_to * paths_from


def node_path_counts(
    graph: dict[str, list[str]], start: str, end: str
) -> dict[str, int]:
    """
    Count how many paths each node appears in.

    Example:
        >>> node_path_counts(graph, 'you', 'out')
        {'you': 5, 'bbb': 2, 'ccc': 3, 'ddd': 2, ...}
    """
    return {
        node: paths_through_node(graph, start, end, node)
        for node in get_all_nodes(graph)
    }
