# MoE, Explained

**A six-chapter book on Mixture-of-Experts — from "what even is an expert" to the
load-balancing math that keeps a 671B-parameter model from eating itself.**

👉 **[Start reading →](https://noman654.github.io/moe-explained/)**

Animated, interactive, self-contained. No build step — open a file, read a chapter.

---

## The chapters

| # | Chapter | In one line |
|---|---------|-------------|
| 1 | [Every token pays full price](https://noman654.github.io/moe-explained/posts/01-why-moe.html) | Why MoE exists — derive Mixtral's 47B/13B yourself from ten config numbers |
| 2 | [The router's impossible job](https://noman654.github.io/moe-explained/posts/02-the-router.html) | A discrete choice that must stay differentiable, and the ordering everyone flattens |
| 3 | [The loss that watches the router](https://noman654.github.io/moe-explained/posts/03-load-balancing.html) | Expert collapse, and why `f·P` works when neither factor alone does |
| 4 | [The seat that wasn't there](https://noman654.github.io/moe-explained/posts/04-capacity-factor.html) | Capacity buffers, silently dropped tokens, and Expert Choice |
| 5 | [Seven years of arguing](https://noman654.github.io/moe-explained/posts/05-the-lineage.html) | Shazeer → GShard → Switch → Mixtral → DeepSeek, as a chain of reactions |
| 6 | [When the network becomes the model](https://noman654.github.io/moe-explained/posts/06-systems-reality.html) | Expert parallelism, the all-to-alls, and why MoE decode is memory-bound |

Every hard idea is climbed in four rungs — *feel it → how it works → the math →
research notes* — so a beginner and a researcher can read the same page and both
leave with something. Each chapter carries step-through animations, a live
calculator, and an exercise with the worked answer folded away.

## The promise

- **Every formula is copied from the primary paper**, not from memory or another blog.
- **Every number is real and cited** — where the book computes or assumes something
  itself, it says so; where a paper is silent, the cell stays blank.
- **Errors get fixed in public.** An adversarial audit against the sources found 18
  in the first draft; the corrections are in the git history.

## Reading & feedback

Read online at the link above, or clone and `open index.html` — that's the whole
toolchain. Comment and react at the foot of any chapter (powered by
[giscus](https://giscus.app)), or [open an issue](https://github.com/Noman654/moe-explained/issues/new)
for a formal correction.

<details>
<summary><strong>Primary sources</strong> — every claim traces to one of these</summary>

1. Shazeer et al. (2017) — [*Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer*](https://arxiv.org/abs/1701.06538)
2. Lepikhin et al. (2020) — [*GShard*](https://arxiv.org/abs/2006.16668)
3. Fedus, Zoph & Shazeer (2021) — [*Switch Transformers*](https://arxiv.org/abs/2101.03961)
4. Zoph et al. (2022) — [*ST-MoE*](https://arxiv.org/abs/2202.08906)
5. Zhou et al. (2022) — [*Mixture-of-Experts with Expert Choice Routing*](https://arxiv.org/abs/2202.09368)
6. Jiang et al. (2024) — [*Mixtral of Experts*](https://arxiv.org/abs/2401.04088)
7. Dai et al. (2024) — [*DeepSeekMoE*](https://arxiv.org/abs/2401.06066)
8. DeepSeek-AI (2024) — [*DeepSeek-V3 Technical Report*](https://arxiv.org/abs/2412.19437)

</details>

<details>
<summary><strong>Repo layout</strong></summary>

```
index.html           # contents page
posts/               # the six chapters, self-contained HTML
assets/              # moe.css (design system) + anim.js (animation engine, ~4KB)
tools/check.py       # pre-publish QA: JS syntax, links, assets, furniture
tools/make_stubs.py  # placeholders for unwritten chapters
tools/to_artifact.py # strips a chapter into a shareable fragment
```

</details>

## Author

Written by **[Mohd Nauman](https://github.com/Noman654)**.

MIT for the code · CC BY 4.0 for the prose — take it, teach with it, say where it came from.
