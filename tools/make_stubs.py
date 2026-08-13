#!/usr/bin/env python3
"""
Generate placeholder pages for chapters that aren't written yet.

Chapter 1 makes ten forward references ("→ chapter 3"), and the sidebar links all
six. Without these stubs every one of those is a 404 on the live site, which reads
as a broken book rather than an unfinished one. A stub says what the chapter will
cover and when — honest, and it keeps the structure navigable.

Writing a real chapter simply overwrites its stub; this script never overwrites a
page that isn't a stub (it checks for the marker).

    python3 tools/make_stubs.py
"""

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MARKER = "<!-- generated-stub -->"

CHAPTERS = [
    ("01-why-moe",         "Every token pays full price",            None),
    ("02-the-router",      "The router",                             dict(
        standfirst="One small matrix has to make a discrete choice while staying "
                   "differentiable enough to train. That tension explains almost "
                   "every design decision in the rest of this book.",
        covers=[
            "Softmax gating: <code>G(x) = Softmax(x · W_g)</code>, straight from Shazeer eq. 3",
            "Top-k, and the thing everyone flattens: <strong>Switch softmaxes over all "
            "N experts then cuts to top-1; Mixtral cuts to top-2 then softmaxes over "
            "just those two</strong> — different denominators, different router gradient",
            "Noisy top-k gating and what the noise is actually for",
            "Why the gate value must multiply the expert output (and what breaks if it doesn't)",
            "Mixtral's real routing statistics — the 63–67% consecutive-token repetition",
        ])),
    ("03-load-balancing",  "Load balancing, and why experts collapse", dict(
        standfirst="Left alone, a router picks favourites and the rich get richer. "
                   "You watched it happen in chapter 1. This is the loss term that "
                   "stops it — the most misunderstood equation in MoE.",
        covers=[
            "Expert collapse, and why it is self-reinforcing",
            "Switch's auxiliary loss <code>α · N · Σ f_i · P_i</code> — and why the "
            "product works when neither factor alone does",
            "Why one factor is non-differentiable and it doesn't matter",
            "Router z-loss: <code>L_z = (1/B) Σ (log Σ e^{x_j})²</code>, and the bfloat16 "
            "roundoff problem it solves",
            "DeepSeek-V3's auxiliary-loss-free bias trick",
        ])),
    ("04-capacity-factor", "Capacity, and the tokens thrown away",   dict(
        standfirst="Experts live in fixed-size buffers because GPUs need static shapes. "
                   "Overflow one and your token is silently dropped — it skips the FFN "
                   "and rides the residual to the next layer. Nothing errors.",
        covers=[
            "The capacity formula: <code>(tokens per batch / experts) × capacity factor</code>",
            "Token dropping via residual passthrough — the failure that doesn't raise",
            "Capacity factor 1.0 / 1.25 / 2.0, and the padding waste each buys",
            "Expert-choice routing: invert the problem and let experts pick tokens",
            "Why inference capacity is a different problem from training capacity",
        ])),
    ("05-the-lineage",     "The lineage: Shazeer → Switch → DeepSeek", dict(
        standfirst="Seven years of the field arguing with itself, as a story. Each "
                   "paper is a reaction to something specific that hurt about the last "
                   "one.",
        covers=[
            "2017: a 137B-parameter model in the LSTM era",
            "GShard's 600B, and sharding as a first-class concern",
            "Switch's top-1 heresy — k=1 was supposed to be impossible",
            "Mixtral making MoE mainstream with open weights",
            "DeepSeekMoE's two real ideas: fine-grained segmentation and shared experts",
            "The combinatorial argument for why 256 small experts beat 8 big ones",
        ])),
    ("06-systems-reality", "The systems reality",                    dict(
        standfirst="The part the architecture papers skip. Your experts don't fit on "
                   "one GPU, so routing becomes a network operation — and a sparse "
                   "model has dense-model memory needs.",
        covers=[
            "Expert parallelism, and how it composes with tensor and data parallelism",
            "The two all-to-all collectives per MoE layer, in the critical path",
            "Why MoE inference is memory-bandwidth-bound, not compute-bound",
            "Batch size and expert hit rate — why MoE loves big batches",
            "Offloading, and why MoE is a training-cost win but an inference-memory loss",
        ])),
]

NAV = "\n".join(
    '        <li><a{cur} href="{slug}.html">{title}</a></li>'.format(
        slug=slug, title=title,
        cur=' aria-current="page"' if slug == cur else (' class="soon"' if meta else ''))
    for cur in ["{cur}"] for slug, title, meta in CHAPTERS)


def page(idx, slug, title, meta):
    n = idx + 1
    nav = "\n".join(
        '        <li><a{a} href="{s}.html">{t}</a></li>'.format(
            s=s, t=t,
            a=' aria-current="page"' if s == slug else ('' if m is None else ' class="soon"'))
        for s, t, m in CHAPTERS)
    covers = "\n".join("      <li>%s</li>" % c for c in meta["covers"])
    prev_link = ""
    if idx > 0:
        ps, pt, _ = CHAPTERS[idx - 1]
        prev_link = ('<a href="%s.html"><span class="k">Previous chapter</span>'
                     '<span class="t"><strong>%d &middot; %s</strong></span></a>'
                     % (ps, idx, pt))
    return f"""<!doctype html>
<html lang="en">
{MARKER}
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — MoE, Explained ch.{n}</title>
<meta name="description" content="Chapter {n} of MoE, Explained. Being written.">
<link rel="stylesheet" href="../assets/moe.css">
</head>
<body>

<header class="masthead">
  <div class="wrap">
    <a class="brand" href="../index.html">MoE<em>,</em> Explained</a>
    <nav><a href="../index.html">Contents</a></nav>
  </div>
</header>

<div class="book">
  <nav class="booknav" aria-label="Table of contents">
    <details open>
      <summary>Contents</summary>
      <p class="navtitle">Chapters</p>
      <ol>
{nav}
      </ol>
      <p class="navfoot">Every formula copied from the primary paper. Every number
      cited. Blank cells where a paper doesn't report a figure.</p>
    </details>
  </nav>

  <article>
    <div class="chapmark"><span class="n">{n}</span><span class="l">Chapter {n}<br>Not written yet</span></div>
    <h1>{title}</h1>
    <p class="standfirst">{meta["standfirst"]}</p>

    <div class="rung mech">
      <span class="tag">Being written</span>
      <p>This chapter isn't finished. The book is written one chapter at a time and
      reviewed before the next one starts, so what ships is checked rather than
      merely drafted &mdash; every formula copied from the primary paper, every
      number verified.</p>
      <p><a href="01-why-moe.html">Chapter 1 is complete and readable now.</a></p>
    </div>

    <h2>What this chapter will cover</h2>
    <ul>
{covers}
    </ul>

    <p>Want to be told when it lands? <a href="https://github.com/Noman654/moe-explained">Watch
    the repo on GitHub</a> &mdash; releases and commits show up there first. Spotted an
    error in a chapter that <em>is</em> published, or want something covered here?
    <a href="https://github.com/Noman654/moe-explained/issues/new">Open an issue</a>.</p>

    <nav class="seriesnav">
      {prev_link}
      <a href="../index.html"><span class="k">All chapters</span>
      <span class="t"><strong>Contents</strong></span></a>
    </nav>
  </article>
</div>

<footer class="site"><div class="wrap">
  MoE, Explained &middot; Chapter {n} of 6 &middot; Prose CC BY 4.0, code MIT
</div></footer>

</body>
</html>
"""


def main():
    wrote, skipped = [], []
    for i, (slug, title, meta) in enumerate(CHAPTERS):
        if meta is None:
            continue                       # a real chapter lives here
        path = REPO / "posts" / f"{slug}.html"
        if path.exists() and MARKER not in path.read_text(encoding="utf-8"):
            skipped.append(slug)           # never clobber real writing
            continue
        path.write_text(page(i, slug, title, meta), encoding="utf-8")
        wrote.append(slug)
    print("wrote stubs:  " + (", ".join(wrote) or "none"))
    if skipped:
        print("left alone (real chapters): " + ", ".join(skipped))


if __name__ == "__main__":
    main()
