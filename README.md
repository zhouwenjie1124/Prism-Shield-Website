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
| `NARROW GAP` | experiment 1: the three-up video comparison, the argument, the success figure |
| `METHOD` | the three method columns |
| `CONSERVATISM` | the accuracy figure and table |
| `ODOMETRY FAULT` | experiment 2: the two-up video pair and the drift figure |
| `MOTION CONSTRAINTS` | experiment 3: the actuation-model table and its video |
| `NOMINAL POLICIES` | experiment 4: Falco / NavRL integration |
| `NONCONVEX BAR` | experiment 5: the attached-bar videos |
| `RESULTS CAROUSEL` | one `<div class="item">` per slide: an `<img>` plus an `<h2 class="subtitle">` caption |
| `INSIDE ONE TRIAL` | the annotated command/clearance trace |
| `REAL TIME` | the latency figure and the speed-up table |
| `SAMPLED DATA` | the control-margin figure and table |
| `BIBTEX` | the citation block |

Video blocks use two helper classes defined in the `<style>` block at the top of
`index.html`: `video-grid cols-2` / `cols-3` lays clips side by side and
collapses to one column under 768 px, and `video-cap` styles the label beneath
(`is-ours` = blue, `is-base` = red, matching the colours in the plots).

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
| `images/*_poster.jpg` | a mid frame of each video, generated with ffmpeg |
| `images/social_preview.png` | `success_vs_gap.png` padded to 1200×630 for Open Graph |
| `webfonts/` | Font Awesome 5.15.1, added because the template ships the CSS without the fonts |

Re-encoding recipe (keeps the two videos at ~1 MB each instead of ~3.8 MB):

```bash
ffmpeg -i overview_dune.mp4 -c:v libx264 -crf 30 -preset slow -pix_fmt yuv420p -an -movflags +faststart static/videos/overview.mp4
```

### Videos from the talk deck

The nine hardware clips come from `DUNE Shield.pptx` (kept out of git by
`.gitignore` — it is ~600 MB). A `.pptx` is a zip: `unzip` it and the raw
recordings are `ppt/media/mediaN.mp4`, all 4K/30. Mapping:

| `static/videos/` | pptx | slide | label on the slide |
|---|---|---|---|
| `narrow_ours.mp4` | media3 | 8 | DUNE-CBF (Ours), 60 cm |
| `narrow_ellipse.mp4` | media2 | 8 | Composite CBF (Ellipse) [5], 90 cm |
| `narrow_circle.mp4` | media1 | 8 | Composite CBF (Circle) [3], 100 cm |
| `odom_nofilter.mp4` | media5 | 9 | Without Safety Filter |
| `odom_ours.mp4` | media4 | 9 | DUNE-CBF (Ours) — cropped, the source is a small inset on a black 4K canvas |
| `motion_constraints.mp4` | media6 | 11 | unsafe command v = 0.5 m/s, ω = 0.8 sin(1.25 t) rad/s |
| `nominal_policies.mp4` | media7 | 12 | Falco [6] / NavRL [7], shown at 2× |
| `bar_doorway.mp4` | media8 | 13 | Nonconvex footprint with an attached bar |
| `bar_outdoor.mp4` | media10 | 14 | same experiment, outdoors |

`media9` (slide 14, second outdoor angle) is unused — add it if the section
needs a third panel. Re-encode recipe, 4K → 1280 wide, ~0.3–2.6 MB per clip:

```bash
ffmpeg -i ppt/media/media3.mp4 -vf scale=1280:-2 -c:v libx264 -crf 30 -preset medium \
       -pix_fmt yuv420p -an -movflags +faststart static/videos/narrow_ours.mp4
```

`media4` additionally needs `-vf "crop=1680:996:2034:82,scale=1280:-2"`.

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
