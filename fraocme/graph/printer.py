"""
Graph formatting utilities.

These format pre-computed data - they don't do computation themselves.
User computes data with graph functions, then formats for display.
"""

from fraocme.ui.colors import c

# =============================================================================
# SIMPLE VALUE FORMATTERS
# =============================================================================


def format_path(
    path: list[str],
    start: str | None = None,
    end: str | None = None,
) -> str:
    """
    Format a single path with colors.

    Args:
        path: List of nodes forming the path
        start: Optional start node (colored green)
        end: Optional end node (colored red)

    Example:
        >>> path = ['you', 'bbb', 'eee', 'out']
        >>> print(format_path(path, start='you', end='out'))
        you → bbb → eee → out
    """
    if not path:
        return c.dim("(empty path)")

    parts = []
    for node in path:
        if start and node == start:
            parts.append(c.green(c.bold(node)))
        elif end and node == end:
            parts.append(c.red(c.bold(node)))
        else:
            parts.append(c.cyan(node))

    return c.dim(" → ").join(parts)


def format_edge(
    edge: tuple[str, str],
    start: str | None = None,
    end: str | None = None,
) -> str:
    """
    Format a single edge with colors.

    Example:
        >>> print(format_edge(('you', 'bbb'), start='you'))
        you → bbb
    """
    src, dst = edge

    if start and src == start:
        src_str = c.green(c.bold(src))
    else:
        src_str = c.cyan(src)

    if end and dst == end:
        dst_str = c.red(c.bold(dst))
    else:
        dst_str = c.cyan(dst)

    return f"{src_str} {c.yellow('→')} {dst_str}"


def format_node_set(
    nodes: set[str],
    start: str | None = None,
    end: str | None = None,
    sort: bool = True,
) -> str:
    """
    Format a set of nodes with colors.

    Example:
        >>> critical = {'you', 'out', 'bbb'}
        >>> print(format_node_set(critical, start='you', end='out'))
        {you, bbb, out}
    """
    if not nodes:
        return c.dim("∅")

    node_list = sorted(nodes) if sort else list(nodes)

    parts = []
    for node in node_list:
        if start and node == start:
            parts.append(c.green(c.bold(node)))
        elif end and node == end:
            parts.append(c.red(c.bold(node)))
        else:
            parts.append(c.cyan(node))

    return "{" + ", ".join(parts) + "}"


def format_edge_set(
    edges: set[tuple[str, str]],
    start: str | None = None,
    end: str | None = None,
) -> str:
    """
    Format a set of edges.

    Example:
        >>> bottlenecks = {('you', 'bbb'), ('eee', 'out')}
        >>> print(format_edge_set(bottlenecks))
    """
    if not edges:
        return c.dim("∅")

    parts = [format_edge(e, start, end) for e in sorted(edges)]
    return "{" + ", ".join(parts) + "}"


# =============================================================================
# COLLECTION FORMATTERS (for lists of paths, etc.)
# =============================================================================


def format_paths(
    paths: list[list[str]],
    start: str | None = None,
    end: str | None = None,
    max_display: int = 20,
    group_by_length: bool = True,
) -> str:
    """
    Format multiple paths with colors and grouping.

    Args:
        paths: List of paths (each path is list of nodes)
        start: Start node for coloring
        end: End node for coloring
        max_display: Max paths to show
        group_by_length: Group paths by their length

    Example:
        >>> paths = enumerate_all_paths(graph, 'you', 'out')
        >>> print(format_paths(paths, start='you', end='out'))
    """
    if not paths:
        return c.dim("(no paths)")

    lines = []
    lines.append(c.dim(f"Found {c.cyan(len(paths))} paths:"))

    if group_by_length:
        # Group by length
        by_length: dict[int, list[list[str]]] = {}
        for path in paths:
            length = len(path) - 1  # edges, not nodes
            if length not in by_length:
                by_length[length] = []
            by_length[length].append(path)

        count = 0
        for length in sorted(by_length.keys()):
            if count >= max_display:
                break

            length_paths = by_length[length]
            lines.append(c.dim(f"\n  Length {c.yellow(length)}:"))

            for path in length_paths:
                if count >= max_display:
                    break
                lines.append(f"    {format_path(path, start, end)}")
                count += 1
    else:
        for i, path in enumerate(paths[:max_display]):
            lines.append(f"  {c.dim(f'{i + 1}.')} {format_path(path, start, end)}")

    if len(paths) > max_display:
        lines.append(c.dim(f"\n  ... and {len(paths) - max_display} more"))

    return "\n".join(lines)


def format_path_count(count: int, start: str, end: str) -> str:
    """
    Format path count with context.

    Example:
        >>> count = count_paths_dag(graph, 'you', 'out')
        >>> print(format_path_count(count, 'you', 'out'))
        5 paths from you to out
    """
    start_str = c.green(c.bold(start))
    end_str = c.red(c.bold(end))
    count_str = c.cyan(c.bold(str(count)))

    return f"{count_str} paths from {start_str} to {end_str}"


def format_paths_by_length(
    length_counts: dict[int, int],
    start: str | None = None,
    end: str | None = None,
) -> str:
    """
    Format path counts grouped by length.

    Args:
        length_counts: Dict mapping path_length -> count

    Example:
        >>> counts = count_paths_with_length(graph, 'you', 'out')
        >>> print(format_paths_by_length(counts))
        Paths by length:
          Length 3: 2 paths
          Length 4: 3 paths
    """
    if not length_counts:
        return c.dim("(no paths)")

    total = sum(length_counts.values())
    lines = [f"Paths by length ({c.cyan(total)} total):"]

    for length in sorted(length_counts.keys()):
        count = length_counts[length]
        pct = count / total * 100
        bar_len = int(pct / 5)
        bar = c.cyan("█" * bar_len) + c.dim("░" * (20 - bar_len))

        lines.append(f"  Length {c.yellow(length)}: {bar} {c.cyan(count)} ({pct:.0f}%)")

    return "\n".join(lines)


# =============================================================================
# GRAPH STRUCTURE FORMATTERS
# =============================================================================


def format_graph(
    graph: dict[str, list[str]],
    highlight_nodes: set[str] | None = None,
    highlight_edges: set[tuple[str, str]] | None = None,
    title: str | None = None,
    max_nodes: int = 50,
) -> str:
    """
    Format graph as adjacency list with colors.

    Args:
        graph: Adjacency list {node: [neighbors]}
        highlight_nodes: Nodes to highlight
        highlight_edges: Edges to highlight
        title: Optional title
        max_nodes: Max nodes to display

    Example:
        >>> print(format_graph(graph, highlight_nodes={'you', 'out'}))
    """
    # Calculate sources and sinks
    all_nodes = set(graph.keys())
    for neighbors in graph.values():
        all_nodes.update(neighbors)

    has_incoming = set()
    for neighbors in graph.values():
        has_incoming.update(neighbors)
    sources = all_nodes - has_incoming

    has_outgoing = {node for node, neighbors in graph.items() if neighbors}
    sinks = all_nodes - has_outgoing

    lines = []

    # Title
    if title:
        lines.append(c.bold(f"{'═' * 40}"))
        lines.append(c.bold(f"  {title}"))
        lines.append(c.bold(f"{'═' * 40}"))

    # Stats
    total_edges = sum(len(n) for n in graph.values())
    lines.append(
        c.dim(
            f"Nodes: {c.cyan(len(all_nodes))} │ "
            f"Edges: {c.cyan(total_edges)} │ "
            f"Sources: {c.green(len(sources))} │ "
            f"Sinks: {c.red(len(sinks))}"
        )
    )
    lines.append("")

    # Nodes
    nodes_to_show = sorted(graph.keys())[:max_nodes]

    for node in nodes_to_show:
        neighbors = graph.get(node, [])

        # Format node
        if highlight_nodes and node in highlight_nodes:
            node_str = c.cyan(c.bold(node))
        elif node in sources:
            node_str = c.green(node)
        elif node in sinks:
            node_str = c.red(node)
        else:
            node_str = node

        # Format neighbors
        neighbor_strs = []
        for neighbor in neighbors:
            edge = (node, neighbor)
            if highlight_edges and edge in highlight_edges:
                neighbor_strs.append(c.yellow(c.bold(neighbor)))
            elif highlight_nodes and neighbor in highlight_nodes:
                neighbor_strs.append(c.cyan(neighbor))
            elif neighbor in sinks:
                neighbor_strs.append(c.red(neighbor))
            else:
                neighbor_strs.append(neighbor)

        neighbors_str = ", ".join(neighbor_strs) if neighbor_strs else c.dim("∅")
        lines.append(f"  {node_str} → [{neighbors_str}]")

    if len(graph) > max_nodes:
        lines.append(c.dim(f"\n  ... and {len(graph) - max_nodes} more nodes"))

    return "\n".join(lines)


# =============================================================================
# ANALYSIS FORMATTERS
# =============================================================================


def format_critical_nodes(
    critical_nodes: set[str],
    total_paths: int | None = None,
    start: str | None = None,
    end: str | None = None,
) -> str:
    """
    Format critical nodes analysis.

    Args:
        critical_nodes: Set of critical nodes
        total_paths: Optional total path count for context
        start: Start node
        end: End node

    Example:
        >>> critical = find_critical_nodes(graph, 'you', 'out')
        >>> print(format_critical_nodes(critical, start='you', end='out'))
    """
    lines = []

    header = f"Critical Nodes ({c.cyan(len(critical_nodes))})"
    lines.append(c.bold(header))
    lines.append(c.dim("Nodes that appear in ALL paths (removal breaks connectivity)"))
    lines.append("")

    if not critical_nodes:
        lines.append(c.dim("  (none - all nodes have alternates)"))
        return "\n".join(lines)

    for node in sorted(critical_nodes):
        if start and node == start:
            marker = c.green("▶")
            node_str = c.green(c.bold(node))
            label = c.dim(" (start)")
        elif end and node == end:
            marker = c.red("◀")
            node_str = c.red(c.bold(node))
            label = c.dim(" (end)")
        else:
            marker = c.yellow("★")
            node_str = c.yellow(c.bold(node))
            label = c.dim(" (critical)")

        lines.append(f"  {marker} {node_str}{label}")

    return "\n".join(lines)


def format_bottleneck_edges(
    bottleneck_edges: set[tuple[str, str]],
    start: str | None = None,
    end: str | None = None,
) -> str:
    """
    Format bottleneck edges analysis.

    Args:
        bottleneck_edges: Set of bottleneck edges
        start: Start node for coloring
        end: End node for coloring

    Example:
        >>> bottlenecks = find_bottleneck_edges(graph, 'you', 'out')
        >>> print(format_bottleneck_edges(bottlenecks))
    """
    lines = []

    header = f"Bottleneck Edges ({c.cyan(len(bottleneck_edges))})"
    lines.append(c.bold(header))
    lines.append(c.dim("Edges that appear in ALL paths (removal breaks connectivity)"))
    lines.append("")

    if not bottleneck_edges:
        lines.append(c.dim("  (none - all edges have alternates)"))
        return "\n".join(lines)

    for edge in sorted(bottleneck_edges):
        lines.append(f"  {c.yellow('⚡')} {format_edge(edge, start, end)}")

    return "\n".join(lines)


def format_node_importance(
    node_path_counts: dict[str, int],
    total_paths: int,
    start: str | None = None,
    end: str | None = None,
    max_display: int = 20,
) -> str:
    """
    Format node importance as heatmap/bar chart.

    Args:
        node_path_counts: Dict mapping node -> paths through it
        total_paths: Total number of paths
        start: Start node
        end: End node
        max_display: Max nodes to show

    Example:
        >>> # First compute the data
        >>> total = count_paths_dag(graph, 'you', 'out')
        >>> counts = {node: paths_through_node(graph, 'you', 'out', node)
        ...           for node in get_all_nodes(graph)}
        >>> print(format_node_importance(counts, total, start='you', end='out'))
    """
    if not node_path_counts:
        return c.dim("(no nodes)")

    lines = []
    lines.append(c.bold(f"Node Importance ({c.cyan(total_paths)} total paths)"))
    lines.append(c.dim("How many paths pass through each node"))
    lines.append("")

    # Sort by count descending
    sorted_nodes = sorted(node_path_counts.items(), key=lambda x: -x[1])

    # Find max name length for alignment
    max_name = max(len(n) for n, _ in sorted_nodes[:max_display])

    for node, count in sorted_nodes[:max_display]:
        if count == 0:
            continue

        pct = count / total_paths * 100
        bar_len = int(pct / 5)  # 20 chars = 100%

        # Color based on percentage
        if pct >= 100:
            bar_color = c.green
        elif pct >= 50:
            bar_color = c.yellow
        else:
            bar_color = c.red

        bar = bar_color("█" * bar_len) + c.dim("░" * (20 - bar_len))

        # Node formatting
        if start and node == start:
            node_str = c.green(c.bold(f"{node:<{max_name}}"))
            marker = c.green("▶")
        elif end and node == end:
            node_str = c.red(c.bold(f"{node:<{max_name}}"))
            marker = c.red("◀")
        elif pct >= 100:
            node_str = c.yellow(c.bold(f"{node:<{max_name}}"))
            marker = c.yellow("★")
        else:
            node_str = f"{node:<{max_name}}"
            marker = " "

        lines.append(
            f"  {marker} {node_str} {bar} {c.dim(f'{count:>4}')} ({pct:>5.1f}%)"
        )

    if len(sorted_nodes) > max_display:
        lines.append(c.dim(f"\n  ... and {len(sorted_nodes) - max_display} more"))

    return "\n".join(lines)


# =============================================================================
# TREE FORMATTER
# =============================================================================


def format_graph_as_tree(
    graph: dict[str, list[str]],
    root: str,
    end: str | None = None,
    max_depth: int = 10,
    max_branches: int = 5,
    path_counts: dict[str, int] | None = None,
) -> str:
    """
    Format graph paths as ASCII tree starting from root.

    Args:
        graph: Adjacency list
        root: Root node to start from
        end: Optional end node (shown with checkmark)
        max_depth: Maximum tree depth
        max_branches: Max children per node
        path_counts: Optional pre-computed path counts per node

    Example:
        >>> print(format_graph_as_tree(graph, 'you', end='out'))
        you (5 paths)
        ├── bbb (2 paths)
        │   ├── ddd (1 path)
        │   │   └── ggg → out ✓
        │   └── eee → out ✓
        └── ccc (3 paths)
            ├── ddd (1 path)
            │   └── ggg → out ✓
            ├── eee → out ✓
            └── fff → out ✓
    """
    lines = []
    visited_in_path = set()

    def format_subtree(node: str, prefix: str, is_last: bool, depth: int):
        if depth > max_depth:
            lines.append(f"{prefix}{'└' if is_last else '├'}── {c.dim('...')}")
            return

        connector = "└── " if is_last else "├── "

        # Node formatting
        if node == root:
            node_str = c.green(c.bold(node))
        elif end and node == end:
            node_str = c.red(c.bold(node))
            lines.append(f"{prefix}{connector}{node_str} {c.green('✓')}")
            return
        elif node in visited_in_path:
            lines.append(f"{prefix}{connector}{c.dim(f'{node} (cycle)')}")
            return
        else:
            node_str = c.cyan(node)

        # Path count annotation
        if path_counts and node in path_counts:
            count = path_counts[node]
            count_str = c.dim(f" ({count} path{'s' if count != 1 else ''})")
        else:
            count_str = ""

        lines.append(f"{prefix}{connector}{node_str}{count_str}")

        # Children
        children = graph.get(node, [])
        if not children:
            return

        visited_in_path.add(node)

        if len(children) > max_branches:
            children_to_show = children[:max_branches]
            truncated = len(children) - max_branches
        else:
            children_to_show = children
            truncated = 0

        new_prefix = prefix + ("    " if is_last else "│   ")

        for i, child in enumerate(children_to_show):
            is_child_last = (i == len(children_to_show) - 1) and truncated == 0
            format_subtree(child, new_prefix, is_child_last, depth + 1)

        if truncated > 0:
            lines.append(f"{new_prefix}└── {c.dim(f'... +{truncated} more')}")

        visited_in_path.remove(node)

    # Root node
    if path_counts and root in path_counts:
        count_str = c.dim(f" ({path_counts[root]} total paths)")
    else:
        count_str = ""

    lines.append(f"{c.green(c.bold(root))}{count_str}")

    # Children of root
    children = graph.get(root, [])
    for i, child in enumerate(children):
        is_last = i == len(children) - 1
        format_subtree(child, "", is_last, 1)

    return "\n".join(lines)
