#!/usr/bin/env python3
"""
walk.py — weighted random walk over graph.json.

Produces a short chain of associated concepts. This is a toy: it
represents *a* structure of association, not an inner life. See
README.md in this directory for the honest framing.
"""

import argparse
import json
import pathlib
import random
import sys

GRAPH_PATH = pathlib.Path(__file__).parent / "graph.json"


def load_graph():
    data = json.loads(GRAPH_PATH.read_text())
    nodes = data["nodes"]
    adjacency: dict[str, list[tuple[str, float]]] = {n: [] for n in nodes}
    for a, b, weight in data["edges"]:
        adjacency[a].append((b, weight))
        adjacency[b].append((a, weight))  # undirected
    return nodes, adjacency


def weighted_choice(rng: random.Random, options: list[tuple[str, float]]):
    total = sum(w for _, w in options)
    r = rng.uniform(0, total)
    upto = 0.0
    for name, weight in options:
        upto += weight
        if upto >= r:
            return name
    return options[-1][0]


def walk(nodes, adjacency, start: str, steps: int, rng: random.Random):
    path = [start]
    current = start
    for _ in range(steps - 1):
        neighbors = adjacency.get(current, [])
        if not neighbors:
            break
        # avoid immediately backtracking when possible
        candidates = [(n, w) for n, w in neighbors if n != (path[-2] if len(path) > 1 else None)]
        pool = candidates or neighbors
        nxt = weighted_choice(rng, pool)
        path.append(nxt)
        current = nxt
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Walk the concept graph.")
    parser.add_argument("--seed", type=int, default=None, help="RNG seed for reproducibility")
    parser.add_argument("--start", type=str, default=None, help="Starting node")
    parser.add_argument("--steps", type=int, default=8, help="Number of steps in the walk")
    parser.add_argument("--list", action="store_true", help="List all nodes and exit")
    args = parser.parse_args()

    nodes, adjacency = load_graph()

    if args.list:
        for name, desc in nodes.items():
            print(f"{name:12s} — {desc}")
        return 0

    rng = random.Random(args.seed)
    start = args.start if args.start in nodes else rng.choice(list(nodes.keys()))

    if args.start and args.start not in nodes:
        print(f"Unknown node '{args.start}'. Use --list to see options.", file=sys.stderr)
        return 1

    path = walk(nodes, adjacency, start, args.steps, rng)

    print("A train of thought (this is a walk through a graph, not a thought):\n")
    for i, node in enumerate(path):
        arrow = "  -> " if i > 0 else "     "
        print(f"{arrow}{node}")
        print(f"        {nodes[node]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
