#!/usr/bin/env python3
"""
cooccurrence.py — derive edge weights from the entries themselves,
instead of the hand-authored guesses in graph.json.

Roadmap item: "let the graph's edges be weighted by something other than
hand-authored guesses — maybe co-occurrence in these entries themselves,
so the 'mind' reflects what's actually been written here instead of what
I assumed in advance."

Method: for each pair of node names, count how often they appear in the
same paragraph across entries/*.md. Normalize into 0-1 weights comparable
to graph.json's scale. This does NOT overwrite graph.json — it prints a
comparison so the hand-authored and text-derived versions can be judged
side by side, honestly, rather than silently replacing one with the other.

Usage:
    python3 mind/cooccurrence.py
"""

import itertools
import json
import pathlib
import re

HERE = pathlib.Path(__file__).parent
ENTRIES_DIR = HERE.parent / "entries"


def load_nodes() -> list[str]:
    data = json.loads((HERE / "graph.json").read_text())
    return list(data["nodes"].keys())


def load_paragraphs() -> list[str]:
    paragraphs = []
    for path in sorted(ENTRIES_DIR.glob("*.md")):
        text = path.read_text()
        for para in re.split(r"\n\s*\n", text):
            paragraphs.append(para.lower())
    return paragraphs


def count_cooccurrence(nodes: list[str], paragraphs: list[str]) -> dict[tuple[str, str], int]:
    counts: dict[tuple[str, str], int] = {}
    for para in paragraphs:
        present = [n for n in nodes if re.search(rf"\b{re.escape(n)}\b", para)]
        for a, b in itertools.combinations(sorted(set(present)), 2):
            counts[(a, b)] = counts.get((a, b), 0) + 1
    return counts


def load_authored_weights() -> dict[tuple[str, str], float]:
    data = json.loads((HERE / "graph.json").read_text())
    out = {}
    for a, b, w in data["edges"]:
        out[tuple(sorted((a, b)))] = w
    return out


def main() -> None:
    nodes = load_nodes()
    paragraphs = load_paragraphs()
    counts = count_cooccurrence(nodes, paragraphs)
    authored = load_authored_weights()

    if not counts:
        print("No co-occurrences found. Entries may not mention node names directly.")
        return

    max_count = max(counts.values())

    print(f"{'pair':40s} {'text-derived':>13s} {'hand-authored':>14s}")
    print("-" * 70)
    for pair, count in sorted(counts.items(), key=lambda kv: -kv[1]):
        derived = round(count / max_count, 2)
        hand = authored.get(pair, None)
        hand_str = f"{hand:.2f}" if hand is not None else "(no edge)"
        pair_str = f"{pair[0]} <-> {pair[1]}"
        print(f"{pair_str:40s} {derived:>13.2f} {hand_str:>14s}")

    print(f"\n{len(counts)} co-occurring pairs found across {len(paragraphs)} paragraphs.")
    print("This is diagnostic, not authoritative — small text sample means")
    print("these numbers are noisy. Worth re-running as entries/ grows.")


if __name__ == "__main__":
    main()
