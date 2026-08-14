# MoE, Explained

**A six-chapter book on Mixture-of-Experts — from "what even is an expert" to the load-balancing math that keeps a 671B-parameter model from eating itself.**

Every chapter is a self-contained HTML page with hand-authored SVG diagrams, **step-through
animations** you can pause and scrub, and interactive panels. No build step, no video files —
the content renders from local files alone and works offline. Open a file, read a chapter.

*(The one third-party script in the book is [giscus](https://giscus.app), which powers the
comment thread at the foot of each chapter. Nothing that renders the book depends on it.)*

👉 **[Start reading →](https://noman654.github.io/moe-explained/)**

---

## The promise

Most MoE explainers pick a lane. Either they're a cartoon ("experts are like specialists!")
that leaves you unable to read a paper, or they're a wall of subscripts that assumes you
already know why anyone bothered.

This book refuses to pick. **Every hard idea is climbed in four rungs**, and you stop
at whichever one you need:

| Rung | What it gives you |
|---|---|
| 🟢 **Feel it** | The one-sentence intuition. An analogy, but only where an analogy actually earns its keep. |
| 🟣 **How it works** | The mechanism, with a diagram. What moves, and where. |
| 🟠 **The math** | The real equation from the real paper — with a plain-English "out loud" gloss under *every single one*. |
| ⚪ **Research notes** | What the paper actually found, what's still contested, and where the bodies are buried. |

If you know what a transformer FFN is, you can read chapter 1. If you're building MoE
kernels for a living, chapter 6 still has something for you.

**Ground rules for this book:**
- Every formula is copied from the primary paper, not from memory or another blog.
- Every number is real and cited. No "roughly 10x faster" hand-waving.
- Analogies are labelled as analogies, and every one is followed by where it breaks.

---

## The chapters

### 1 · Every token pays full price — the dense wall and conditional computation
The FFN is where a transformer spends most of its parameters, and every token pays for
all of them. What if it didn't? Total vs. active parameters, and how a 47B model does
13B of work. **You'll derive Mixtral's 47B/13B yourself from a 10-row config table** —
and once you've done that, every MoE spec sheet in the world becomes readable.

*Covers:* dense FFN cost · conditional computation · total vs. active params ·
sparsity ratio · what MoE buys and what it costs.

### 2 · The router — softmax, top-k, and the discrete-choice problem
The router is a single matrix. That's it. But it has to make a *discrete* choice while
staying differentiable, and that tension explains almost every design decision that follows.
Softmax gating → top-k → noisy top-k, plus why the gate value multiplies the output
(and what breaks if it doesn't).

*Covers:* `G(x) = Softmax(TopK(x·W_g))` · why top-k before vs. after softmax matters ·
noisy top-k · the straight-through gradient path · Mixtral's actual routing statistics.

### 3 · Load balancing — the auxiliary loss, and why experts collapse
Left alone, a router picks favourites and the rich get richer: three experts do all the
work, the other five are dead weight you still pay to store. The fix is a loss term that
is deceptively subtle. **This is the chapter with the most misunderstood equation in MoE**
— we'll derive why `f_i · P_i` works when neither factor alone does.

*Covers:* expert collapse · Switch's `α·N·Σ f_i·P_i` · why one factor is
non-differentiable and it doesn't matter · router z-loss · DeepSeek-V3's
auxiliary-loss-free bias trick · sequence-wise vs. batch-wise balance.

### 4 · Capacity factor — the buffer, and the tokens that get thrown away
Experts live in fixed-size buffers because GPUs need static shapes. Overflow past the
buffer and your token is **silently dropped** — it skips the FFN entirely and rides the
residual connection to the next layer. Nobody tells you. The loss just gets slightly worse.

*Covers:* the capacity formula · token dropping via residual passthrough · capacity
factor 1.0 / 1.25 / 2.0 trade-offs · padding waste · expert-choice routing as the
"invert the problem" answer · why inference capacity ≠ training capacity.

### 5 · The lineage — Shazeer → GShard → Switch → Mixtral → DeepSeek-V3
Seven years of the field arguing with itself, as a story. Each paper is a reaction to a
specific thing that hurt about the last one. Ends with DeepSeekMoE's two genuinely new
ideas — fine-grained expert segmentation and shared experts — and why 256 small experts
beat 8 big ones.

*Covers:* the 2017 LSTM-era 137B model · GShard's 600B · Switch's top-1 heresy ·
Mixtral making MoE mainstream · fine-grained + shared experts · the combinatorial
argument for many small experts.

### 6 · The systems reality — expert parallelism, all-to-all, and memory-bound inference
The part the architecture papers skip. Your experts don't fit on one GPU, so routing
becomes a **network operation**: two all-to-all collectives per MoE layer, in the critical
path. And at inference, a sparse model has dense-model memory needs — you pay for all
47B of Mixtral's weights in VRAM to do 13B of arithmetic.

*Covers:* expert parallelism vs. tensor/data parallelism · the two all-to-alls · why
MoE inference is memory-bandwidth-bound · batch size and expert-hit-rate · offloading ·
why MoE is a training-cost win and an inference-*memory* loss.

---

## Repo layout

```
moe-explained/
├── index.html          # book contents page
├── posts/
│   ├── 01-why-moe.html      # ch.1 — shipped
│   ├── 02-the-router.html
│   ├── 03-load-balancing.html
│   ├── 04-capacity-factor.html
│   ├── 05-the-lineage.html
│   └── 06-systems-reality.html
├── assets/
│   ├── moe.css         # the whole design system, one file
│   └── anim.js         # step/scrub animation engine (~4KB, no deps)
└── tools/
    ├── to_artifact.py  # strips a chapter to a shareable fragment
    ├── make_stubs.py   # placeholder pages for unwritten chapters
    └── check.py        # pre-publish QA: JS syntax, links, assets, furniture
```

**To read locally:** `open index.html`. That's the whole toolchain.

**To publish:** push to GitHub, enable Pages on `main` / root. No build.

---

## Status

| # | Chapter | State |
|---|---|---|
| 1 | Every token pays full price | ✅ Shipped — 3 animations, 1 exercise |
| 2 | The router's impossible job | ✅ Shipped — 2 animations, 1 exercise |
| 3 | The loss that watches the router | ✅ Shipped — 2 animations, 1 exercise |
| 4 | The seat that wasn't there | ✅ Shipped — 2 animations, 1 exercise |
| 5 | Seven years of arguing | ✅ Shipped — 1 animation, 1 exercise |
| 6 | When the network becomes the model | ✅ Shipped — 2 animations, 1 exercise |

**The book is complete.** 12 step-through animations, 6 exercises, ~100 minutes of reading.

---

## Primary sources

Every claim in this book traces to one of these. Where a chapter states a formula, it was
copied from the paper — links go to the exact paper, not a summary of it.

1. Shazeer et al. (2017) — [*Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer*](https://arxiv.org/abs/1701.06538)
2. Lepikhin et al. (2020) — [*GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding*](https://arxiv.org/abs/2006.16668)
3. Fedus, Zoph & Shazeer (2021) — [*Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity*](https://arxiv.org/abs/2101.03961)
4. Zoph et al. (2022) — [*ST-MoE: Designing Stable and Transferable Sparse Expert Models*](https://arxiv.org/abs/2202.08906)
5. Zhou et al. (2022) — [*Mixture-of-Experts with Expert Choice Routing*](https://arxiv.org/abs/2202.09368)
6. Jiang et al. (2024) — [*Mixtral of Experts*](https://arxiv.org/abs/2401.04088)
7. Dai et al. (2024) — [*DeepSeekMoE: Towards Ultimate Expert Specialization*](https://arxiv.org/abs/2401.06066)
8. DeepSeek-AI (2024) — [*DeepSeek-V3 Technical Report*](https://arxiv.org/abs/2412.19437)

---

## Feedback & corrections

**Found an error?** That's the most valuable thing you can send. This book's whole
promise is that every formula was copied from the primary paper and every number
verified — so a wrong subscript is a bug, not a nitpick.
[Open an issue](https://github.com/Noman654/moe-explained/issues/new) and it gets
fixed, with the correction noted.

**Questions about the math** belong in the comment thread at the foot of each chapter
(powered by [giscus](https://giscus.app), backed by this repo's
[Discussions](https://github.com/Noman654/moe-explained/discussions)). If a step didn't
land, that's usually the writing's fault — and it tells me what to rewrite.

**Want a topic covered?** The unwritten chapters have comment threads too. Saying what
you want from chapter 3 before it exists is more useful than telling me after.

**PRs welcome** for typos, clearer explanations, and broken links.

---

## Author

Written by **[Mohd Nauman](https://github.com/Noman654)** — [@Noman654](https://github.com/Noman654).

Corrections and questions are welcome in the comments at the foot of any chapter, or
as an [issue](https://github.com/Noman654/moe-explained/issues/new).

---

## License

MIT for the code. Prose is CC BY 4.0 — take it, teach with it, just say where it came from.
