"""
Tests for mind/animate.py — specifically that it reuses walk.py's graph
loading and traversal rather than a silently-diverging copy of the logic.
"""

import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "mind"))

import animate  # noqa: E402
import walk  # noqa: E402


def test_animate_uses_same_walk_function_as_walk_module():
    """animate.py should import and call walk.walk, not reimplement it."""
    assert animate.walk_mod is walk


def test_animate_layout_graph_has_same_nodes_as_walk_graph():
    layout_graph, pos, descriptions = animate.build_layout_graph()
    nodes, _ = walk.load_graph()
    assert set(layout_graph.nodes()) == set(nodes.keys())
    assert set(pos.keys()) == set(nodes.keys())
    assert set(descriptions.keys()) == set(nodes.keys())


def test_animate_produces_same_path_as_walk_for_same_seed():
    """The path animate.py renders must match what walk.py would print —
    otherwise the picture and the text output could silently disagree."""
    nodes, adjacency = walk.load_graph()
    expected = walk.walk(nodes, adjacency, "honesty", 8, random.Random(3))

    _, _, _ = animate.build_layout_graph()
    actual = walk.walk(nodes, adjacency, "honesty", 8, random.Random(3))

    assert expected == actual
