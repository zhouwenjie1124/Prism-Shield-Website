# PRISM Shield — project page

Source for <https://zhouwenjie1124.github.io/Prism-Shield-Website/>, the project
website for **PRISM Shield: Certified Body-Frame Point-Cloud Safety Filtering
for Polygonal Robot Footprints**.

The research code lives in a separate repository:
<https://github.com/zhouwenjie1124/PRISM-Shield>.

Built on the
[Academic Project Page Template](https://github.com/eliahuhorwitz/Academic-project-page-template)
(itself adapted from [Nerfies](https://nerfies.github.io)). Pure HTML + Bulma —
no build step, no Jekyll (`.nojekyll` is committed so GitHub Pages serves
`static/` verbatim).

## Publish

Settings → Pages → Source: **Deploy from a branch**, branch `main`, folder
**`/ (root)`**.

## Preview locally

```bash
python3 serve.py
```

Opens <http://localhost:8000> and **reloads the browser automatically** every
time a file in this directory changes, so the edit loop is: save in your
editor, look at the browser. Standard library only, nothing to install.
`python3 serve.py 8080` picks another port, `--no-open` skips launching a
browser. The reload script is injected at serve time and is never part of
`index.html`, so it cannot leak into what GitHub Pages publishes.

## Where the content lives

`index.html` is the whole site. Each section starts with a banner comment, so
`grep -n "=====" index.html` prints a table of contents:

| Section | What you edit there |
|---|---|
| `HERO` | title, authors, affiliation, the four buttons |
| `TEASER` | the top video and its caption |
| `ABSTRACT` | the abstract paragraphs |
| `HEADLINE NUMBERS` | the four stat cards (`stat-num` = the big figure, `stat-lbl` = the caption) |
| `WHY EXACT DISTANCE` | the motivating argument, two columns |
| `METHOD` | the three method columns |
| `CONSERVATISM` | the accuracy figure and table |
| `RESULTS CAROUSEL` | one `<div class="item">` per slide: an `<img>` plus an `<h2 class="subtitle">` caption |
| `REAL TIME` | the latency figure and the speed-up table |
| `ODOMETRY FAULT` | the fault video, figure and text |
| `SAMPLED DATA` | the control-margin figure and table |
| `BIBTEX` | the citation block |

The layout classes come from [Bulma](https://bulma.io/documentation/). The two
that carry most of the structure: `columns` + `column` splits a row (equal
width by default, or `is-half` / `is-four-fifths` to force one), and
`section hero is-light` gives a block the grey background that alternates down
the page.

## Still to fill in

Search `index.html` for `TODO`. As of writing:

| Where | What |
|---|---|
| `<meta name="author">`, hero author block, `citation_author`, JSON-LD | co-authors and their links |
| hero affiliation | `YOUR_LAB, YOUR_UNIVERSITY` |
| Paper button | drop the PDF at `static/pdfs/paper.pdf` |
| arXiv button, `citation_pdf_url`, BibTeX | replace `XXXX.XXXXX` |
| venue | `Preprint, 2026` in the hero, `citation_conference_title` |
| teaser video | see below |

**The teaser is the highest-value fix.** `static/videos/overview.mp4` is an
animated matplotlib trace, not robot footage. An on-board or RViz clip of the
Go2W clearing a narrow gap belongs in that slot, with the trace demoted to a
second panel.

## Assets

Everything under `static/` is a **copy** taken from the research repo — GitHub
Pages only serves what is in this repository, so nothing here can reference the
code repo. Regenerate the originals there, then re-copy.

| `static/` file | Source in `PRISM-Shield` |
|---|---|
| `images/logo.png` | `doc/prism_shield_logo.png`, resized to 1000 px |
| `images/success_vs_gap.png`, `success_vs_don.png` | `experiments/figures/` |
| `images/prism_accuracy_nearfield.png`, `prism_accuracy_signed_compare.png` | `experiments/figures/` |
| `images/benchmark_inference_gpu.png` | `experiments/figures/` |
| `images/odom_xy_t04.png`, `odom_drift_t04.png`, `trial_overview_prism.png` | `experiments/figures/` |
| `images/sampled_data_polygon.png` | `Simulation/results/sampled_data_polygon_cbf/` |
| `images/sampled_data_pointcloud.png`, `sampled_data_certificates.png` | `Simulation/results/sampled_data_pointcloud_cbf/` |
| `videos/overview.mp4` | `experiments/figures/overview_dune.mp4`, re-encoded |
| `videos/odom_fault.mp4` | `experiments/figures/odom_drift_t04.mp4`, re-encoded |
| `images/*_poster.jpg` | first frames of the two videos |
| `images/social_preview.png` | `success_vs_gap.png` padded to 1200×630 for Open Graph |
| `webfonts/` | Font Awesome 5.15.1, added because the template ships the CSS without the fonts |

Re-encoding recipe (keeps the two videos at ~1 MB each instead of ~3.8 MB):

```bash
ffmpeg -i overview_dune.mp4 -c:v libx264 -crf 30 -preset slow -pix_fmt yuv420p -an -movflags +faststart static/videos/overview.mp4
```

## Numbers on the page

Every figure caption and table cites something in the research repo:

- accuracy table → `experiments/data/prism_accuracy_bands.csv` (`nearfield` rows)
- speed table → `test/compare_prism_vs_ecos.csv`
- control-margin table → `Simulation/README.md`
- gap-width claim → `experiments/figures/success_vs_gap.png`

The dense-obstacle-course trials (`experiments/data/dense_scenario_summary.md`)
are **deliberately not** on the page: `min clear.` is negative on all four CBF
trials and that file flags it as possibly self-returns rather than real
contacts. Resolve that before publishing those numbers.
