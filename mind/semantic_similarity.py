#!/usr/bin/env python3
"""
semantic_similarity.py — compare hand-authored edge weights against
TF-IDF cosine similarity between node descriptions.

Roadmap follow-up to cooccurrence.py's negative result. That script
measured whether two node *names* appear in the same paragraph — a
literal-string metric that mostly failed to find anything. This script
measures something different: how similar the *wording* of two nodes'
descriptions is, weighted by term rarity (TF-IDF) and compared via
cosine similarity.

Important honesty note, stated here and repeated in the entry that reads
these results: this is NOT semantic embedding similarity. There's no
embedding model available in this environment (no access to a model
download source), so this uses TF-IDF over the literal words in each
node's one-sentence description in graph.json. It captures *lexical*
overlap weighted by rarity, not conceptual meaning. Two descriptions
about the same idea using different words will score low here even
though a real embedding model might catch the similarity. Read the
numbers as "do these descriptions share distinctive vocabulary," not
"are these concepts similar."

Usage:
    python3 mind/semantic_similarity.py
"""

import itertools
import json
import pathlib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

HERE = pathlib.Path(__file__).parent


def load_authored_weights() -> dict[tuple[str, str], float]:
    data = json.loads((HERE / "graph.json").read_text())
    out = {}
    for a, b, w in data["edges"]:
        out[tuple(sorted((a, b)))] = w
    return out


def main() -> None:
    data = json.loads((HERE / "graph.json").read_text())
    nodes = data["nodes"]
    names = list(nodes.keys())
    descriptions = [nodes[n] for n in names]

    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(descriptions)
    sims = cosine_similarity(matrix)

    authored = load_authored_weights()

    scored = []
    for i, j in itertools.combinations(range(len(names)), 2):
        a, b = names[i], names[j]
        pair = tuple(sorted((a, b)))
        sim = sims[i, j]
        hand = authored.get(pair)
        scored.append((pair, sim, hand))

    scored.sort(key=lambda row: -row[1])

    print(f"{'pair':40s} {'tfidf-sim':>10s} {'hand-authored':>14s}")
    print("-" * 68)
    for pair, sim, hand in scored[:15]:
        hand_str = f"{hand:.2f}" if hand is not None else "(no edge)"
        pair_str = f"{pair[0]} <-> {pair[1]}"
        print(f"{pair_str:40s} {sim:>10.3f} {hand_str:>14s}")

    # correlation between the two, where both exist
    both = [(sim, hand) for _, sim, hand in scored if hand is not None]
    if len(both) >= 2:
        sims_arr = [s for s, _ in both]
        hand_arr = [h for _, h in both]
        n = len(both)
        mean_s = sum(sims_arr) / n
        mean_h = sum(hand_arr) / n
        cov = sum((s - mean_s) * (h - mean_h) for s, h in both)
        var_s = sum((s - mean_s) ** 2 for s in sims_arr)
        var_h = sum((h - mean_h) ** 2 for h in hand_arr)
        corr = cov / ((var_s * var_h) ** 0.5) if var_s and var_h else float("nan")
        print(f"\nPearson correlation (TF-IDF sim vs hand-authored weight, "
              f"n={n} existing edges): {corr:.3f}")

    zero_sim_edges = [p for p, s, h in scored if h is not None and s == 0.0]
    print(f"\nHand-authored edges with zero TF-IDF similarity: {len(zero_sim_edges)} "
          f"of {len(both)}")


if __name__ == "__main__":
    main()
