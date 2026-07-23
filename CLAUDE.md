# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Kai Golan Hashiloni's personal academic website, built with Jekyll using the remote theme `daviddarnes/alembic` (see `_config.yml`). It's a static site deployed via GitHub Pages (repo name `golankai.github.io`) — there is no build pipeline or CI config in this repo beyond Jekyll itself.

## Commands

```
bundle install              # install Ruby/Jekyll dependencies
bundle exec jekyll serve    # run local dev server at http://localhost:4000
```

There are no tests, linters, or JS/CSS build steps — content changes are just Markdown/HTML edits rendered by Jekyll on push.

## Structure

- Top-level `*.md` files (`index.md`, `publications.md`, `news.md`, `activity.md`, `cv.md`, `contact.md`, `dharmabench.md`, `id10m-jam.md`, `404.md`) are Jekyll pages, each with YAML front matter (`title`, `permalink`, and sometimes `sitemap: false` / `indexing: false` for hidden pages) followed by inline HTML/Markdown content.
- `_config.yml` defines site-wide settings and the header/footer navigation (`navigation_header` / `navigation_footer`). Adding a page to the main nav means adding an entry here.
- `_includes/custom_style.html` holds a site-wide `<style>` override (link colors, buttons, `<hr>`) and is pulled into pages via `{% include custom_style.html %}` — nearly every page includes this at the top.
- `_posts/` holds blog posts (Jekyll date-prefixed filenames); `blog/index.html` is the blog listing page.
- `assets/` holds images and the CV PDF (`assets/cv.pdf`), referenced directly by pages (e.g. `/assets/kai.jpg`).
- `_site/` and `.jekyll-cache/` are Jekyll build output/cache — gitignored, never edit by hand.

## Page conventions

- Pages style themselves with inline `<style>` blocks scoped to a page-specific class (e.g. `.jam-page`, `.pub-list`, `.news-row`) rather than shared stylesheets — follow this pattern for new pages instead of adding to `_includes/custom_style.html`, which is reserved for global overrides.
- The accent color `#1a4b8c` (hover: `#6a9bd0`) is used consistently across pages for headings, links, and buttons — match it in any new styled sections.
- Research project landing pages (`dharmabench.md`, `id10m-jam.md`) are minimal single-purpose pages linking out to the paper/code/dataset, with `sitemap: false` and `indexing: false` to keep them out of search indexing while still being directly linkable. Follow this pattern for future paper landing pages.
- `news.md`, `publications.md`, and `activity.md` group entries by year using a repeated heading + list-row structure — check the existing markup in these files before adding entries so new items match the existing format.
