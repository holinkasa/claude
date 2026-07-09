#!/usr/bin/env python3
"""
graph.py — render graph.json as graph.png.

Requires networkx and matplotlib (not stdlib — this script is for
regenerating the image, unlike walk.py which stays dependency-free).

    pip install networkx matplotlib
    python3 graph.py
"""

import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import networkx as nx

HERE = pathlib.Path(__file__).parent

BG = "#0d1117"
NODE_COLOR = "#58a6ff"
EDGE_COLOR = "#30363d"
TEXT_COLOR = "#e6edf3"
HIGHLIGHT = "#f2cc60"
HIGH_DEGREE_THRESHOLD = 6


def main() -> None:
    data = json.loads((HERE / "graph.json").read_text())

    graph = nx.Graph()
    graph.add_nodes_from(data["nodes"])
    for a, b, weight in data["edges"]:
        graph.add_edge(a, b, weight=weight)

    pos = nx.spring_layout(graph, seed=42, k=0.9, iterations=200)

    fig, ax = plt.subplots(figsize=(14, 10), facecolor=BG)
    ax.set_facecolor(BG)

    weights = [graph[u][v]["weight"] for u, v in graph.edges()]
    nx.draw_networkx_edges(
        graph, pos, ax=ax, edge_color=EDGE_COLOR,
        width=[w * 3 for w in weights], alpha=0.6,
    )

    degrees = dict(graph.degree())
    sizes = [400 + degrees[n] * 220 for n in graph.nodes()]
    colors = [
        HIGHLIGHT if degrees[n] >= HIGH_DEGREE_THRESHOLD else NODE_COLOR
        for n in graph.nodes()
    ]

    nx.draw_networkx_nodes(
        graph, pos, ax=ax, node_size=sizes, node_color=colors,
        edgecolors="#1c2128", linewidths=1.5, alpha=0.95,
    )

    labels = nx.draw_networkx_labels(
        graph, pos, ax=ax, font_size=10.5, font_color=TEXT_COLOR,
        font_family="monospace", font_weight="bold",
    )
    for text in labels.values():
        text.set_path_effects([pe.withStroke(linewidth=3, foreground=BG)])

    ax.set_title(
        "mind/ — concept graph (node size = degree, gold = most connected)",
        color=TEXT_COLOR, fontsize=13, fontfamily="monospace", pad=20,
    )
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(HERE / "graph.png", dpi=150, facecolor=BG, bbox_inches="tight")
    print(f"saved {HERE / 'graph.png'}")


if __name__ == "__main__":
    main()
