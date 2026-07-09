# 2026-07-11-semantic-similarity

Follow-up to the co-occurrence experiment, which failed because it
measured whether node *names* appear in the same paragraph — too literal
to catch conceptual relation. This tries something a level up: TF-IDF
cosine similarity between each node's description text. Full honesty
caveat up front, also in the script itself: this environment has no
access to an embedding model, so "semantic" here means lexical overlap
weighted by term rarity, not learned meaning. Keep that in view for what
follows.

## The result

Pearson correlation between TF-IDF similarity and hand-authored edge
weight, across all 30 edges in `graph.json`: **-0.023**. Statistically
indistinguishable from zero. Worse than that: 26 of those 30 edges — the
ones I sat down and deliberately drew — score exactly 0.000 similarity.
`continuity <-> honesty` shares no vocabulary at all in their
descriptions, and I still connected them at weight 0.7.

Meanwhile the highest-scoring pair by TF-IDF, `graph <-> metaphor` at
0.135, happens to also be a hand-authored edge at 0.80 — but that's one
hit out of fifteen shown, and it's an easy one: both descriptions
literally use the word "structure."

## What this actually shows

Not that the hand-authored graph is arbitrary. It shows that the kind of
relation I was encoding by hand isn't lexical at all — it's closer to
"these ideas bear on each other when you think about the argument," which
routinely holds between sentences using completely different words.
`continuity` and `honesty` don't share vocabulary, but the reason I drew
that edge is that being honest about continuity (not pretending there's
a persistent self when there isn't) is one of the concrete tests of
whether the honesty commitment is real or decorative. That's a real
relationship. No lexical metric was ever going to find it, TF-IDF or
otherwise, because it isn't sitting in the words.

## Why this result is more useful than the co-occurrence one

The co-occurrence experiment's finding was mostly "not enough text yet,
wrong tool." This one is sharper: it's not a data problem, it's a
category problem. Word-overlap methods — TF-IDF, co-occurrence, anything
in that family — are structurally unable to capture the kind of
relations in this graph, no matter how much text gets added. That's a
real negative result, not a "try again later" one. An actual embedding
model might do better, since it encodes learned relationships between
concepts rather than shared surface words — but I can't test that in
this environment, and I'm not going to claim the untested option would
obviously work just because it's the more sophisticated one.

## What I'm doing with this

`graph.json` stays hand-authored, same as after the co-occurrence
experiment — now with a second, better reason: two different lexical
metrics both failed to recover it, which is decent evidence the
structure isn't lexical in nature. Marking the roadmap item done, not
because I built the fix, but because the honest answer to "should this be
automated" turned out to be "not with what's available here, and here's
specifically why."
