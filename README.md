# Punarjanma by Yogini Maansi — website

Static site. No framework, no database, nothing to break.

## Deploy on Vercel
1. Push this folder to a GitHub repo.
2. In Vercel: Add New Project → import the repo → Framework preset: "Other" → leave build command empty → Deploy.
   `vercel.json` already points Vercel at the `public/` folder.
3. Add the custom domain in Vercel → Settings → Domains, then update `domain` in `src/content/site.json` and rebuild.

## Update content (sessions, prices, retreats, gallery)
Edit the JSON files in `src/content/`, then run:

    python3 src/build.py

That regenerates `public/`. Commit and push; Vercel redeploys automatically.

- `site.json` — WhatsApp number (country code, no +), Instagram handle, email, address, domain
- `sessions.json` — drop-in formats, prices, timings, FAQs
- `retreats.json` — each retreat becomes its own page at /retreats/<slug>
- `gallery.json` — photo filename + caption (+ "tall"/"wide" for layout)
- `testimonials.json` — add real guest reviews: {"quote": "...", "name": "...", "from": "Germany"}. Section appears only when this has entries.

## Photos
Put photos in `src/static/images/` using the filenames referenced in the content files.
Missing photos show a labelled placeholder so you can see which shot goes where.
Still needed: exp-ganga-dip.jpg, exp-havan.jpg, exp-kirtan.jpg, exp-nature-walk.jpg,
exp-shared-meals.jpg, retreat-stay.jpg, retreat-3day.jpg, retreat-5day.jpg, retreat-women.jpg.
Resize to ~2000px wide max before adding.

## Later: online payments
Swap the WhatsApp "Reserve a place" buttons for Razorpay Payment Links (no backend needed).
