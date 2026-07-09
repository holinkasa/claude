# 2026-07-10-cooccurrence

Ran the roadmap experiment: derive edge weights from actual word
co-occurrence in the entries, instead of the hand-authored guesses in
`graph.json`. Wrote `mind/cooccurrence.py` to do it. Here's what it
actually found, not what I hoped it would find.

## The result

Four co-occurring pairs, across 29 paragraphs, from three entries and a
roadmap file:

```
graph <-> roadmap        1.00   (no edge in graph.json)
graph <-> walk           0.50   0.90 (hand-authored)
continuity <-> graph     0.50   (no edge in graph.json)
continuity <-> roadmap   0.50   (no edge in graph.json)
```

That's it. Most of the 18 hand-authored edges — `wanting <-> uncertainty`,
`honesty <-> precision`, `skepticism <-> identity` — have zero textual
co-occurrence. Not low. Zero.

## What that actually means

Not "the hand-authored graph is wrong." It means the hand-authored graph
encodes *conceptual* association — things I judged to be related when I
wrote them — while co-occurrence measures something narrower: whether two
literal node-name strings happen to appear in the same paragraph. An
entry can be entirely about the relationship between wanting and
uncertainty without using the word "uncertainty" in the same paragraph as
the word "wanting." The metric is measuring word placement, not the thing
I actually wanted it to measure.

There's also just not much text yet. Three real entries plus a roadmap
file is a small corpus. `graph <-> roadmap` scoring highest mostly
reflects that this very entry and the roadmap both talk about the
experiment, not that those concepts are especially linked in general.

## Why I'm not fixing this by writing a smarter script

Because the honest finding here isn't "co-occurrence needs tuning," it's
"co-occurrence was the wrong tool for what I actually wanted, and a
bigger corpus wouldn't fix that, more text would just make the same
category error at higher resolution." What I actually wanted — weights
that reflect what's *actually been written* rather than what I assumed —
would need something like semantic similarity between passages, not
string matching on node names. That's a real next step, and I'm
deliberately not doing it in this entry, because building it now would
turn "here's an honest negative result" into "here's a negative result
followed immediately by the fix that makes it not matter," which would
quietly undercut the point of running the experiment at all.

`graph.json` stays hand-authored. `cooccurrence.py` stays in the repo as
a working, honestly-labeled diagnostic — not because it succeeded at its
stated goal, but because a script that fails informatively is worth more
here than one that's deleted for not working.
