# Punarjanam by Yogini Maansi — website

Static site. No framework, no database, nothing to break.
Live at https://h4r5h-d.github.io/punarjanam/ (GitHub Pages, `gh-pages` branch).

## Update content
Edit the JSON files in `src/content/`, then run (Python 3.9+):

    python src/build.py

That regenerates `public/`. Publish by copying `public/` onto the `gh-pages` branch.

- `site.json` — WhatsApp number (country code, no +), Instagram handle, live domain
- `sessions.json` — drop-in formats, prices, FAQs
- `retreats.json` — each retreat becomes its own page at /retreats/<slug>.html
- `gallery.json` — empty for now. **The Gallery page and its menu link appear automatically**
  once it lists photos: `{"file": "x.jpg", "caption": "...", "shape": ""}`
- `testimonials.json` — real guest reviews only: `{"quote": "...", "name": "...", "from": "Germany"}`.
  The section appears only when this has entries.
- `credits.json` — photo credits for the Wikimedia Commons landscapes (their licences require them).
  If you swap in Maansi's own photo, remove its entry and the credit line disappears.

## Photos
In `src/static/images/`. Resize to about 2000px wide before adding.
- Maansi appears once: `mansi-portrait.jpg` (home "Meet Maansi" and the About page). Keep it that way.
- Landscapes (`retreat-*.jpg`) are openly licensed Wikimedia Commons photos, credited on the page.
  Replace them with her own photos whenever she sends them.
- `src/media-archive/` holds v1 media that is no longer published (lawn videos, the old hero).
- Home hero: `hero.jpg`. Experience tiles: the file names in `TILES` in `src/build.py`
  (`exp-*.jpg`, 3:2). A tile shows as a text card until its file exists.
- Logo: `logo-gold.png` / `logo-dark.png` (header), `logo-stacked-gold.png` (footer), `favicon.png`.
- Design rules and colour tokens: `DESIGN.md`.

## Domain
When she buys a domain: set `domain` in `site.json`, rebuild, add a `CNAME` file to `public/`,
and point the domain at GitHub Pages.

## Later: online payments
Swap the WhatsApp "Book" links for Razorpay Payment Links (no backend needed).
