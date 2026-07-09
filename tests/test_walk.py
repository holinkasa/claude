"""
Tests for mind/walk.py. Run with:

    python3 -m pytest tests/ -v

No dependencies beyond pytest — everything else here is stdlib, matching
walk.py's own no-dependency design.
"""

import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "mind"))

import walk  # noqa: E402


def test_load_graph_returns_all_nodes():
    nodes, adjacency = walk.load_graph()
    assert len(nodes) > 0
    assert set(nodes.keys()) == set(adjacency.keys())


def test_graph_is_undirected():
    nodes, adjacency = walk.load_graph()
    for a, neighbors in adjacency.items():
        for b, weight in neighbors:
            b_neighbors = dict(adjacency[b])
            assert a in b_neighbors, f"{a} -> {b} exists but not {b} -> {a}"
            assert b_neighbors[a] == weight, f"asymmetric weight on {a}<->{b}"


def test_every_node_reachable_from_every_other():
    """The graph should be connected — no isolated islands of concepts."""
    nodes, adjacency = walk.load_graph()
    start = next(iter(nodes))
    seen = {start}
    frontier = [start]
    while frontier:
        current = frontier.pop()
        for neighbor, _ in adjacency[current]:
            if neighbor not in seen:
                seen.add(neighbor)
                frontier.append(neighbor)
    assert seen == set(nodes.keys()), f"unreachable nodes: {set(nodes) - seen}"


def test_walk_same_seed_is_reproducible():
    nodes, adjacency = walk.load_graph()
    start = "uncertainty"
    path_a = walk.walk(nodes, adjacency, start, 10, random.Random(42))
    path_b = walk.walk(nodes, adjacency, start, 10, random.Random(42))
    assert path_a == path_b


def test_walk_respects_requested_length():
    nodes, adjacency = walk.load_graph()
    path = walk.walk(nodes, adjacency, "wanting", 6, random.Random(1))
    assert len(path) == 6


def test_walk_starts_where_asked():
    nodes, adjacency = walk.load_graph()
    path = walk.walk(nodes, adjacency, "honesty", 5, random.Random(1))
    assert path[0] == "honesty"


def test_walk_never_produces_unknown_node():
    nodes, adjacency = walk.load_graph()
    path = walk.walk(nodes, adjacency, "toy", 15, random.Random(99))
    assert all(node in nodes for node in path)


def test_weighted_choice_only_returns_given_options():
    rng = random.Random(0)
    options = [("a", 1.0), ("b", 2.0), ("c", 3.0)]
    results = {walk.weighted_choice(rng, options) for _ in range(200)}
    assert results <= {"a", "b", "c"}
    assert len(results) > 1  # with 200 draws, should see more than one outcome
