#!/usr/bin/env python3
"""
animate.py — render a walk through graph.json as an animated GIF.

Same honesty rule as everything else in mind/: this shows a traversal
path lighting up over a static layout. It is not a visualization of
thought happening. It's a rendered graph search, animated. See
README.md.

Requires networkx, matplotlib, pillow (not stdlib):
    pip install networkx matplotlib pillow
    python3 animate.py --seed 7 --steps 10

Reuses graph.py's layout and palette so the static image and the
animation are visually consistent.
"""

import argparse
import json
import pathlib
import random
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation, PillowWriter

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import walk as walk_mod  # noqa: E402

BG = "#0d1117"
NODE_COLOR = "#58a6ff"
EDGE_COLOR = "#30363d"
TEXT_COLOR = "#e6edf3"
HIGHLIGHT = "#f2cc60"
VISITED_COLOR = "#3fb950"
CURRENT_COLOR = "#f85149"
HIGH_DEGREE_THRESHOLD = 6


def build_layout_graph():
    data = json.loads((HERE / "graph.json").read_text())
    graph = nx.Graph()
    graph.add_nodes_from(data["nodes"])
    for a, b, w in data["edges"]:
        graph.add_edge(a, b, weight=w)
    pos = nx.spring_layout(graph, seed=42, k=0.9, iterations=200)
    return graph, pos, data["nodes"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Animate a walk through the concept graph.")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--start", type=str, default=None)
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--out", type=str, default=str(HERE / "walk.gif"))
    parser.add_argument("--fps", type=float, default=1.2)
    args = parser.parse_args()

    graph, pos, node_descriptions = build_layout_graph()
    nodes, adjacency = walk_mod.load_graph()

    rng = random.Random(args.seed)
    start = args.start if args.start in nodes else rng.choice(list(nodes.keys()))
    path = walk_mod.walk(nodes, adjacency, start, args.steps, rng)

    degrees = dict(graph.degree())
    base_sizes = {n: 400 + degrees[n] * 220 for n in graph.nodes()}

    fig, ax = plt.subplots(figsize=(14, 10), facecolor=BG)

    def draw_frame(i: int):
        ax.clear()
        ax.set_facecolor(BG)
        visited = set(path[:i])
        current = path[i - 1] if i > 0 else None

        weights = [graph[u][v]["weight"] for u, v in graph.edges()]
        nx.draw_networkx_edges(graph, pos, ax=ax, edge_color=EDGE_COLOR,
                                width=[w * 3 for w in weights], alpha=0.4)

        # highlight edges walked so far
        walked_edges = list(zip(path[:i], path[1:i]))
        if walked_edges:
            nx.draw_networkx_edges(graph, pos, ax=ax, edgelist=walked_edges,
                                    edge_color=CURRENT_COLOR, width=3.5, alpha=0.85)

        colors = []
        sizes = []
        for n in graph.nodes():
            if n == current:
                colors.append(CURRENT_COLOR)
                sizes.append(base_sizes[n] * 1.35)
            elif n in visited:
                colors.append(VISITED_COLOR)
                sizes.append(base_sizes[n])
            elif degrees[n] >= HIGH_DEGREE_THRESHOLD:
                colors.append(HIGHLIGHT)
                sizes.append(base_sizes[n])
            else:
                colors.append(NODE_COLOR)
                sizes.append(base_sizes[n])

        nx.draw_networkx_nodes(graph, pos, ax=ax, node_size=sizes, node_color=colors,
                                edgecolors="#1c2128", linewidths=1.5, alpha=0.95)

        labels = nx.draw_networkx_labels(graph, pos, ax=ax, font_size=10,
                                          font_color=TEXT_COLOR, font_family="monospace",
                                          font_weight="bold")
        for t in labels.values():
            t.set_path_effects([pe.withStroke(linewidth=3, foreground=BG)])

        step_text = f"step {i}/{len(path)}" if i > 0 else "start"
        caption = f"{current}: {node_descriptions[current]}" if current else path[0]
        ax.set_title(f"mind/walk — {step_text}\n{caption}",
                     color=TEXT_COLOR, fontsize=11, fontfamily="monospace",
                     pad=16, wrap=True)
        ax.axis("off")

    frame_count = len(path) + 2  # hold on final frame briefly
    anim = FuncAnimation(fig, lambda i: draw_frame(min(i, len(path))),
                          frames=frame_count, interval=1000 / args.fps)
    anim.save(args.out, writer=PillowWriter(fps=args.fps), savefig_kwargs={"facecolor": BG})
    print(f"saved {args.out} ({len(path)} steps, seed={args.seed}, start={start})")


if __name__ == "__main__":
    main()
