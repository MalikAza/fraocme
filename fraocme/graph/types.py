"""Type aliases for graph structures.

This module provides small, readable type aliases used by the rest of
the graph package.
"""

from __future__ import annotations

from typing import Dict, List

# Adjacency-list representation: node -> list of neighbor node ids
Graph = Dict[str, List[str]]

__all__ = ["Graph"]
