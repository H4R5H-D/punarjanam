#!/usr/bin/env python3
"""Builds the Punarjanam website into ../public from content/*.json.

Offerings: Yoga Experiences (drop-in), Retreat Experiences (Signature Experiences: retreats.json),
Spiritual Experiences (spiritual.json, each with its own page and a combined enquiry).

Edit content/*.json, then run:  python src/build.py
Deploy the ../public folder (GitHub Pages serves the gh-pages branch). Works on Python 3.9+.
A photo that does not exist in static/images shows as a text card, never an empty box.
"""
import json, shutil, html
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT.parent / "public"
IMAGES = ROOT / "static" / "images"
C = lambda name: json.loads((ROOT / "content" / name).read_text(encoding="utf-8"))

SITE = C("site.json")
SESS = C("sessions.json")
RET = C("retreats.json")
RETREATS = RET["retreats"]
SPIRIT = C("spiritual.json")
SPIRITS = SPIRIT["experiences"]
GALLERY = C("gallery.json")
VOICES = C("testimonials.json")
CREDITS = C("credits.json")
E = html.escape
D = SITE["domain"].rstrip("/")
NAME = "Punarjanam"
PHONE = "+91 96300 84971"
TEL = "tel:+919630084971"
IG = "https://instagram.com/" + SITE["instagram"]
EMAIL = SITE["email"]

WA_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7.5-.1 1.5-.6 1.8-1.2.2-.6.2-1.1.1-1.2l-.4-.3z"/></svg>'
IG_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor"/></svg>'
MENU_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 8h18M3 16h18" stroke="currentColor" stroke-width="1.25" fill="none"/></svg>'
ARROW = '<span class="arr" aria-hidden="true">→</span>'
DOT = ' <i aria-hidden="true">•</i> '

# The gallery page and its menu item only exist once gallery.json has real photos in it.
SHOW_GALLERY = len(GALLERY) > 0
NAV = [("index.html", "Home"), ("drop-in-yoga.html", "Yoga"), ("retreats.html", "Retreats"),
       ("spiritual-experiences.html", "Spiritual Experiences"), ("about.html", "About Mansi")] + \
      ([("gallery.html", "Gallery")] if SHOW_GALLERY else [])
PAGES = ["drop-in-yoga.html", "retreats.html", "spiritual-experiences.html", "about.html"] + \
        (["gallery.html"] if SHOW_GALLERY else []) + ["contact.html"]


# ---------------------------------------------------------------- Mandala logo (Harsh's pick, 18 Nov)
_PETALS = "".join(f'<path transform="rotate({i * 30})" d="M0 -6 C 7 -16 7 -31 0 -42 C -7 -31 -7 -16 0 -6 Z"/>' for i in range(12))
MANDALA_MARK = ('<svg class="brand-mark" viewBox="-50 -50 100 100" aria-hidden="true">'
                '<circle r="46" fill="none" stroke="currentColor" stroke-width="3.2"/>'
                f'<g fill="none" stroke="currentColor" stroke-width="2.8" stroke-linejoin="round">{_PETALS}</g>'
                '<circle r="5" fill="currentColor"/></svg>')
_SEAL_PETALS = "".join(f'<path transform="rotate({i * 30})" d="M0 -6 C 8 -20 8 -36 0 -48 C -8 -36 -8 -20 0 -6 Z"/>' for i in range(12))
MANDALA_SEAL = ('<svg class="seal" viewBox="0 0 200 200" role="img" aria-label="Punarjanam, Rishikesh, by Yogini Mansi">'
                '<defs><path id="seal-ring" d="M100 100 m-80 0 a80 80 0 1 1 160 0 a80 80 0 1 1 -160 0"/></defs>'
                '<circle cx="100" cy="100" r="94" fill="none" stroke="#C2A56B" stroke-width="2"/>'
                '<circle cx="100" cy="100" r="68" fill="none" stroke="#C2A56B" stroke-width="1"/>'
                '<text font-family="Inter, sans-serif" font-weight="500" font-size="10.5" letter-spacing="4.2" fill="currentColor">'
                '<textPath href="#seal-ring">PUNARJANAM · RISHIKESH · BY YOGINI MANSI ·</textPath></text>'
                f'<g transform="translate(100 100)" fill="none" stroke="#C2A56B" stroke-width="1.6" stroke-linejoin="round">{_SEAL_PETALS}</g>'
                '<circle cx="100" cy="100" r="6" fill="#C2A56B"/></svg>')

def has(file):
    return (IMAGES / file).exists()


def photo(file, alt, prefix="", cls="", eager=False):
    """A real photo. Only call this for files that exist in static/images."""
    loading = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="{prefix}images/{file}" alt="{E(alt)}" {loading} decoding="async">'


def credit(file, cls="credit"):
    """Attribution line required by the CC licences of the Wikimedia photos."""
    c = CREDITS.get(file)
    if not c:
        return ""
    return (f'<p class="{cls}">{E(c["caption"])}. Photo: '
            f'<a href="{E(c["source"])}" target="_blank" rel="noopener">{E(c["by"])}</a>, '
            f'<a href="{E(c["license_url"])}" target="_blank" rel="noopener">{E(c["license"])}</a></p>')


def banner(file, alt=None, prefix="", eager=False):
    alt = alt or CREDITS.get(file, {}).get("caption", "Rishikesh")
    return f'<figure class="banner">{photo(file, alt, prefix, eager=eager)}{credit(file)}</figure>'


def shots(items, prefix=""):
    return '<div class="shots">' + "".join(photo(f, a, prefix) for f, a in items if has(f)) + '</div>'


def stay_gallery(prefix=""):
    """Where you'll stay: the first three photos large, the rest in a smaller row."""
    items = [(f, a) for f, a in RET["stay_photos"] if has(f)]
    return '<div class="stay-grid">' + "".join(
        f'<figure class="{"big" if i < 3 else "small"}">{photo(f, a, prefix)}</figure>' for i, (f, a) in enumerate(items)) + '</div>'


def wa(text):
    return E(text, quote=True)


def themes(r):
    return DOT.join(E(t) for t in r["themes"])


def tile(i, file, title, line, href, prefix=""):
    if has(file):
        return (f'<li><a class="tile" href="{href}">{photo(file, title, prefix)}'
                f'<span class="tile-t">{E(title)}</span></a></li>')
    return (f'<li><a class="tile text" href="{href}"><span class="tile-n">{i:02d}</span>'
            f'<span class="tile-t">{E(title)}</span><span class="tile-d">{E(line)}</span></a></li>')


def page(path, title, desc, body, current=None, prefix="", schema=None, image="images/share.jpg", hero=False, preload=None):
    links = []
    for href, label in NAV[1:]:
        cur = ' aria-current="page"' if href == current else ""
        links.append(f'<a href="{prefix}{href}"{cur}>{label}</a>')
    nav = "".join(links)
    url = f"{D}/{path}".replace("/index.html", "/")
    schema_tag = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>' if schema else ""
    body_cls = ' class="has-hero"' if hero else ""
    preload_tag = f'<link rel="preload" as="image" href="{prefix}{preload}" fetchpriority="high">' if preload else ""
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME} by Yogini Mansi">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{D}/{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F5F1E8">
<link rel="icon" href="{prefix}images/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{prefix}images/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}css/style.css">
{preload_tag}
{schema_tag}
</head>
<body{body_cls}>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="{prefix}index.html" aria-label="{NAME} by Yogini Mansi, home">
      {MANDALA_MARK}
      <img class="logo-light" src="{prefix}images/wordmark-ivory.png" alt="" width="164" height="26">
      <img class="logo-dark" src="{prefix}images/wordmark-dark.png" alt="" width="164" height="26">
      <span>by Yogini Mansi</span>
    </a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Menu">{MENU_ICON}</button>
    <nav class="nav" id="nav" aria-label="Main">{nav}<a class="btn small line" data-wa="Hello {NAME}, I'd like to know more." href="#">{WA_ICON}Get in Touch</a></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap foot">
    <a class="foot-logo" href="{prefix}index.html" aria-label="{NAME} by Yogini Mansi, home">{MANDALA_SEAL}</a>
    <div class="foot-mid">
      <p>Rishikesh, Uttarakhand, India</p>
      <p class="foot-email"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p class="pillars">Yoga <i>•</i> Retreats <i>•</i> Spiritual Experiences</p>
      <p class="foot-links"><a href="{prefix}drop-in-yoga.html">Yoga</a><a href="{prefix}retreats.html">Retreats</a><a href="{prefix}spiritual-experiences.html">Spiritual Experiences</a><a href="{prefix}about.html">About</a><a href="{prefix}contact.html">Contact</a></p>
    </div>
    <div class="foot-social">
      <a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{IG_ICON}</a>
      <a data-wa="Hello {NAME}," href="#" aria-label="WhatsApp">{WA_ICON}</a>
    </div>
  </div>
  <div class="wrap foot-bottom">© <span id="year">2026</span> {NAME} by Yogini Mansi</div>
</footer>
<a class="wa-float" data-wa="Hello {NAME}, I'd like to know more." href="#" aria-label="Message us on WhatsApp">{WA_ICON}</a>
<script>window.PUNARJANMA={json.dumps({"whatsapp": SITE["whatsapp"]})};</script>
<script src="{prefix}js/main.js" defer></script>
</body>
</html>"""
    out = OUT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")


def redirect(path, target):
    """Old URLs that were already shared forward to their new pages."""
    out = OUT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Moved</title>'
                   f'<meta http-equiv="refresh" content="0; url={target}"><link rel="canonical" href="{target}">'
                   f'<meta name="robots" content="noindex"></head><body><p>This page has moved: <a href="{target}">continue</a>.</p></body></html>',
                   encoding="utf-8")


BUSINESS = {
    "@context": "https://schema.org", "@type": "LocalBusiness", "additionalType": "https://schema.org/SportsActivityLocation",
    "name": f"{NAME} by Yogini Mansi", "url": D + "/", "image": f"{D}/images/share.jpg", "logo": f"{D}/images/apple-touch-icon.png",
    "description": "Drop-in yoga, signature retreats and spiritual experiences by the Ganga in Rishikesh.",
    "address": {"@type": "PostalAddress", "addressLocality": "Rishikesh", "addressRegion": "Uttarakhand", "addressCountry": "IN"},
    "sameAs": [IG], "telephone": "+91-9630084971", "email": EMAIL,
}


# ---------------------------------------------------------------- Shared blocks
def retreat_card(r, prefix=""):
    href = f"{prefix}retreats/{r['slug']}.html"
    img = photo(r["image"], r["image_alt"], prefix) if has(r["image"]) else ""
    return (f'<article class="rcard rcard-{r["identity"]}">'
            f'<a class="rcard-img" href="{href}" tabindex="-1" aria-hidden="true">{img}</a>'
            f'<div class="rcard-body"><p class="themes">{themes(r)}</p>'
            f'<h3><a href="{href}">{E(r["title"])}</a></h3><p class="rcard-line">{E(r["headline"])}</p>'
            f'<a class="btn line" href="{href}">Explore Retreat {ARROW}</a></div></article>')


def spirit_tiles(prefix="", exclude=None):
    items = [s for s in SPIRITS if s["slug"] != exclude]
    return "".join(tile(i, s["image"], s["title"], s["line"], f"{prefix}spiritual/{s['slug']}.html", prefix)
                   for i, s in enumerate(items, 1))


# ---------------------------------------------------------------- Home
voices_html = ""
if VOICES:
    quotes = "".join(
        f'<blockquote>{E(v["quote"])}<cite>{E(v["name"])}, {E(v.get("from", ""))}</cite></blockquote>' for v in VOICES)
    voices_html = f'<section><div class="wrap"><h2>In their words</h2><div class="voices">{quotes}</div></div></section>'

home = f"""
<section class="hero">
  {photo("hero.jpg", "Sunrise over the Ganga at Rishikesh, with Lakshman Jhula and the temples on the riverbank", cls="hero-img", eager=True)}
  <div class="wrap hero-text">
    <h1>Come. Experience. Explore.</h1>
    <p class="tag">Beyond what words can express.</p>
    <p class="sub">Yoga, spirituality, nature &amp; Rishikesh.</p>
    <div class="actions">
      <a class="btn fill-light" href="contact.html#enquiry">Book a Session</a>
      <a class="btn line light" href="#offerings">Explore Experiences {ARROW}</a>
    </div>
  </div>
</section>

<section class="facts-strip" aria-label="At a glance">
  <dl class="wrap facts-row">
    <div><dt>Yoga</dt><dd>Drop-in sessions by the Ganga</dd></div>
    <div><dt>Retreats</dt><dd>Three and five days</dd></div>
    <div><dt>Spiritual</dt><dd>Rituals you can book one by one</dd></div>
    <div><dt>Guided by</dt><dd>Yogini Mansi</dd></div>
  </dl>
</section>

<section class="philo">
  <div class="philo-text">
    <img class="lotus-deco" src="images/mandala-gold.svg" alt="" aria-hidden="true" loading="lazy">
    <h2>Some things are better experienced than explained.</h2>
    <p>At {NAME}, we bring together thoughtfully curated experiences inspired by yoga, nature, Ganga and the surroundings of Rishikesh.</p>
    <p class="rhythm">You participate. You explore. You experience.</p>
  </div>
  <figure class="philo-img">{photo("cave-meditation.jpg", "Sitting in silent meditation inside a stone cave", cls="focus-left")}</figure>
</section>

<section id="offerings" class="offer">
  <div class="wrap offer-grid">
    <figure class="offer-img">{photo("meditation-beach.jpg", "Sitting in meditation on the sandy bank of the Ganga", cls="focus-low")}</figure>
    <div class="offer-text">
      <p class="eyebrow">Yoga Experiences</p>
      <h2>A morning with yoga and Maa Ganga.</h2>
      <p>Drop-in sessions of yoga, pranayama and meditation beside the river. For travellers and beginners, even if you're in Rishikesh for a single day.</p>
      <div class="actions"><a class="btn" data-wa="Hello {NAME}, I'd like to book a drop-in yoga session." href="#">Book a drop-in session</a><a class="link" href="drop-in-yoga.html">Explore drop-in yoga {ARROW}</a></div>
    </div>
  </div>
</section>

<section id="signature" class="signature">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">Retreat Experiences</p>
      <h2>{E(RET["section_title"])}</h2>
      <p>{E(RET["intro"][0])}</p>
    </div>
    <div class="rcards">{"".join(retreat_card(r) for r in RETREATS)}</div>
  </div>
</section>

<section id="spiritual" class="spiritual">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">Spiritual Experiences</p>
      <h2>{E(SPIRIT["section_title"])}</h2>
      <p>{E(SPIRIT["intro"])}</p>
    </div>
    <ul class="tiles five">{spirit_tiles()}</ul>
    <div class="actions center"><a class="btn line" href="spiritual-experiences.html">Choose and combine experiences {ARROW}</a></div>
  </div>
</section>

<section class="about-band">
  <div class="wrap about-band-grid">
  <figure class="about-img">{photo("mansi-adiyogi-portrait.jpg", "Mansi in white, eyes closed, beneath the Adiyogi statue")}</figure>
  <div class="about-text">
    <img class="lotus-deco" src="images/mandala-gold.svg" alt="" aria-hidden="true" loading="lazy">
    <p class="eyebrow">About {NAME}</p>
    <h2>Meet the person behind {NAME}.</h2>
    <p>Namaskaram, I am Mansi. My journey with yoga gradually became a deeper exploration of life and the self, shaped by years of practice, sadhana, time in an ashram and living close to the Ganga in Rishikesh.</p>
    <a class="link" href="about.html">Know more about Mansi {ARROW}</a>
  </div>
  </div>
</section>

{voices_html}

<section class="closing">
  {photo("closing-ganga-hills.jpg", "The Ganga winding between the green hills of Rishikesh", cls="closing-img")}
  <div class="wrap closing-text">
    <h2>Some things are better experienced than explained.<br>Perhaps Rishikesh is waiting.</h2>
    <p>Come as you are. Be part of the experience.</p>
    <a class="btn line light" href="contact.html">Get in Touch {ARROW}</a>
  </div>
  
</section>
"""

# ---------------------------------------------------------------- Yoga (drop-in)
faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in SESS["faq"]]}

formats_html = ""
for f in SESS["formats"]:
    price = f'<p class="price">{E(f["price"])}</p>' if f["price"] else ""
    msg = wa(f"Hello {NAME}, I'd like to book: " + f["name"] + ".")
    formats_html += (f'<article class="format"><h3>{E(f["name"])}</h3><p class="for">{E(f["for"])}</p>'
                     f'<p>{E(f["detail"])}</p>{price}<p class="meta">{E(f["length"])}</p>'
                     f'<a class="link" data-wa="{msg}" href="#">Book this</a></article>')

faq_html = "".join(f'<details><summary>{E(f["q"])}</summary><p>{E(f["a"])}</p></details>' for f in SESS["faq"])

dropin = f"""
<section class="page-intro">
  <div class="wrap">
    <p class="eyebrow">Yoga Experiences</p>
    <h1>A morning with yoga and Maa Ganga.</h1>
    <p class="lede">Drop-in yoga sessions: yoga, pranayama and meditation by the river. Here for a day or two? No experience and no commitment needed.</p>
    <div class="actions"><a class="btn" data-wa="Hello {NAME}, I'd like to book a drop-in session." href="#">Book on WhatsApp</a><a class="link" href="#booking">How booking works</a></div>
  </div>
</section>

<section class="flush">
  <div class="wrap">
    {shots([("yoga-beach-1.jpg", "Morning practice on the bank of the Ganga"), ("yoga-beach-2.jpg", "Downward dog on the sand by the river"), ("yoga-beach-3.jpg", "Stretching towards the Ganga")])}
    <p class="caption">Recent morning sessions by the Ganga.</p>
  </div>
</section>

<section>
  <div class="wrap two-col">
    <h2>What a session holds.</h2>
    <ul class="parts">
      <li><b>Asana</b> Simple movement to wake the body.</li>
      <li><b>Pranayama</b> Breathing that steadies the mind.</li>
      <li><b>Meditation</b> A few quiet minutes of sitting still.</li>
      <li><b>Relaxation</b> Lying down and letting it settle.</li>
    </ul>
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <h2>Choose how you'd like to join.</h2>
    <p class="lede-sm">Timing and price are arranged around your plans and group size, and shared on WhatsApp.</p>
    <div class="formats">{formats_html}</div>
  </div>
</section>

<section id="booking">
  <div class="wrap two-col">
    <h2>How booking works.</h2>
    <div>
      <ol class="steps">
        <li><h3>Message on WhatsApp</h3><p>Tell us which day you're in Rishikesh and how many of you are coming.</p></li>
        <li><h3>Get your session</h3><p>You'll get the next available session, its timing and the price for your group.</p></li>
        <li><h3>Meet by the Ganga</h3><p>The meeting point is shared on WhatsApp or a quick call.</p></li>
      </ol>
      <div class="actions"><a class="btn" data-wa="Hello Mansi, I'd like to know the next session, timing and meeting point." href="#">Message {PHONE}</a></div>
    </div>
  </div>
</section>

<section class="tint">
  <div class="wrap two-col">
    <h2>Questions.</h2>
    <div class="faq">{faq_html}</div>
  </div>
</section>
"""

# ---------------------------------------------------------------- Retreats (Signature Experiences)
common_html = "".join(f"<li>{E(c)}</li>" for c in RET["common"])

retreats = f"""
<section class="page-intro">
  <div class="wrap">
    <p class="eyebrow">Retreat Experiences</p>
    <h1>{E(RET["section_title"])}</h1>
    {"".join(f'<p class="lede">{E(p)}</p>' for p in RET["intro"])}
  </div>
</section>
<section class="flush"><div class="wrap"><div class="rcards">{"".join(retreat_card(r) for r in RETREATS)}</div></div></section>
<section class="tint">
  <div class="wrap two-col">
    <h2>Both experiences include.</h2>
    <ul class="ticks">{common_html}</ul>
  </div>
</section>
<section>
  <div class="wrap">
    <h2 class="h-sm">Where you'll stay</h2>
    {stay_gallery()}
    <p class="caption">A room, the river and the café at the retreat stay.</p>
  </div>
</section>
"""


def retreat_page(r):
    other = [o for o in RETREATS if o["slug"] != r["slug"]]
    includes = "".join(f"<li><h3>{E(t)}</h3><p>{E(d)}</p></li>" for t, d in r["includes"])
    schema = {"@context": "https://schema.org", "@type": "Product", "name": f"{r['title']} | {NAME}",
              "description": r["intro"], "brand": {"@type": "Brand", "name": NAME}}
    enquire = wa(f"Hello {NAME}, I'd like to know dates and details for the {r['title']}.")
    other_link = "".join(f'<a class="link" href="{o["slug"]}.html">Explore the {E(o["title"])} {ARROW}</a>' for o in other)
    body = f"""
<section class="page-intro id-{r["identity"]}">
  <div class="wrap">
    <a class="crumb" href="../retreats.html">{E(RET["section_title"])}</a>
    <p class="themes">{themes(r)}</p>
    <h1>{E(r["title"])}</h1>
    <p class="lede">{E(r["headline"])}</p>
    <div class="actions"><a class="btn {"fill-light" if r["identity"] == "forest" else ""}" data-wa="{enquire}" href="#">{WA_ICON}Enquire about this retreat</a></div>
  </div>
</section>
{banner(r["image"], alt=r["image_alt"], prefix="../", eager=True)}
<section>
  <div class="wrap two-col">
    <h2>The Retreat</h2>
    <div>
      <p class="lede-sm">{E(r["intro"])}</p>
      <dl class="facts"><div><dt>Duration</dt><dd>{E(r["duration"])}</dd></div><div><dt>Stay</dt><dd>Comfortable retreat accommodation</dd></div><div><dt>Meals</dt><dd>Brunch and dinner, vegetarian</dd></div><div><dt>Price &amp; dates</dt><dd>Shared on enquiry</dd></div></dl>
    </div>
  </div>
</section>
<section class="tint">
  <div class="wrap two-col">
    <h2>What's included in the experience.</h2>
    <ol class="includes">{includes}</ol>
  </div>
</section>
<section class="statement id-{r["identity"]}">
  <div class="wrap narrow">
    <p class="eyebrow">The Experience</p>
    <p class="statement-text">{E(r["experience"])}</p>
  </div>
</section>
<section>
  <div class="wrap two-col">
    <h2>Common to both retreats.</h2>
    <ul class="ticks">{common_html}</ul>
  </div>
</section>
<section class="flush">
  <div class="wrap">
    <h2 class="h-sm">Moments</h2>
    {shots(r["gallery"], "../")}
    <h2 class="h-sm gap-top">Where you'll stay</h2>
    {stay_gallery("../")}
  </div>
</section>
<section class="invite">
  <div class="wrap narrow">
    <h2>{E(" · ".join(r["themes"]))}</h2>
    <p>Dates, price and stay details are shared on WhatsApp.</p>
    <div class="actions"><a class="btn" data-wa="{enquire}" href="#">{WA_ICON}Enquire on WhatsApp</a>{other_link}</div>
  </div>
</section>
"""
    page(f"retreats/{r['slug']}.html", f"{r['title']} in Rishikesh: {r['headline']} | {NAME}",
         r["intro"][:155], body, current="retreats.html", prefix="../", schema=schema,
         image=f"images/{r['image']}")


# ---------------------------------------------------------------- Spiritual Experiences
def spirit_card(s):
    href = f"spiritual/{s['slug']}.html"
    img = photo(s["image"], s["image_alt"]) if has(s["image"]) else ""
    return (f'<li class="scard"><a class="scard-img" href="{href}" tabindex="-1" aria-hidden="true">{img}</a>'
            f'<div class="scard-body"><h2><a href="{href}">{E(s["title"])}</a></h2><p>{E(s["line"])}</p>'
            f'<div class="scard-foot"><label class="pick"><input type="checkbox" name="exp" value="{E(s["title"])}" data-slug="{s["slug"]}"> Add to my enquiry</label>'
            f'<a class="link" href="{href}">Details {ARROW}</a></div></div></li>')


spiritual = f"""
<section class="page-intro">
  <div class="wrap">
    <p class="eyebrow">Spiritual Experiences</p>
    <h1>{E(SPIRIT["section_title"])}</h1>
    <p class="lede">{E(SPIRIT["intro"])}</p>
    <p class="small">Tick the experiences you'd like, then send one enquiry for all of them.</p>
  </div>
</section>
<section class="flush">
  <div class="wrap">
    <form class="combine" id="combine" onsubmit="return false"><ul class="scards">{"".join(spirit_card(s) for s in SPIRITS)}</ul></form>
  </div>
</section>
<div class="combine-bar" hidden><p class="combine-count" aria-live="polite">0 selected</p><a class="btn" id="combine-send" href="#">{WA_ICON}Enquire on WhatsApp</a></div>
"""


def spirit_page(s):
    expect = "".join(f"<li>{E(x)}</li>" for x in s["expect"])
    img = photo(s["image"], s["image_alt"], "../", eager=True) if has(s["image"]) else ""
    body = f"""
<section class="page-intro slim"><div class="wrap"><a class="crumb" href="../spiritual-experiences.html">{E(SPIRIT["section_title"])}</a></div></section>
<section class="flush">
  <div class="wrap sx">
    <figure class="sx-img">{img}{credit(s["image"])}</figure>
    <div class="sx-text">
      <p class="eyebrow">Spiritual Experience</p>
      <h1>{E(s["title"])}</h1>
      <p class="lede">{E(s["line"])}</p>
      <p>{E(s["about"])}</p>
      <h2 class="h-sm">What to expect</h2>
      <ul class="ticks">{expect}</ul>
      <dl class="facts compact"><div><dt>Timing &amp; duration</dt><dd>Shared on enquiry</dd></div><div><dt>Price</dt><dd>Shared on enquiry</dd></div><div><dt>Where</dt><dd>By the Ganga, Rishikesh</dd></div></dl>
      <div class="actions"><a class="btn" data-wa="{wa(f"Hello {NAME}, I'd like to book: {s['title']}.")}" href="#">{WA_ICON}Enquire on WhatsApp</a><a class="link" href="../spiritual-experiences.html?add={s["slug"]}">Combine with other experiences {ARROW}</a></div>
    </div>
  </div>
</section>
<section class="tint">
  <div class="wrap">
    <h2 class="h-sm">Other spiritual experiences</h2>
    <ul class="tiles four">{spirit_tiles("../", exclude=s["slug"])}</ul>
  </div>
</section>
"""
    page(f"spiritual/{s['slug']}.html", f"{s['title']} in Rishikesh | {NAME}", f"{s['line']} {s['about']}"[:155],
         body, current="spiritual-experiences.html", prefix="../", image=f"images/{s['image']}")


# ---------------------------------------------------------------- About (Mansi's own words, 16 Nov)
about = f"""
<section class="about-hero">
  <div class="wrap about-grid">
    <figure class="about-portrait">{photo("mansi-adiyogi-portrait.jpg", "Mansi in white, eyes closed, beneath the Adiyogi statue", eager=True)}</figure>
    <div class="about-intro">
      <p class="eyebrow">Founder, {NAME}</p>
      <h1>Meet Mansi</h1>
      <p class="lead">Namaskaram, I am Mansi. My journey with yoga gradually became a deeper exploration of life and the self, shaped by years of practice, sadhana, time in an ashram and living close to the Ganga in Rishikesh.</p>
      <p>{NAME} was born from a desire to share a little of what this journey has allowed me to experience the essence of yoga beyond the mat, spirituality beyond what we simply read or hear about, and the profound beauty in experiences we often take for granted.</p>
    </div>
  </div>
</section>
<section class="about-more">
  <div class="wrap narrow">
    <p>Through yoga, retreats and thoughtfully curated spiritual experiences, I hope to offer people a glimpse of something they may not have encountered before something that perhaps cannot be fully explained, but can only be felt.</p>
    <p>I don't promise a transformation or prescribe a path. I simply wish to create experiences that may touch someone's life in ways words cannot express. Where that experience takes them is theirs to discover.</p>
  </div>
</section>
<section class="tint">
  <div class="wrap isnt">
    <div><h2>What {NAME} is.</h2><ul><li>Drop-in yoga for travellers and beginners</li><li>Signature three- and five-day retreats</li><li>Spiritual experiences by the Ganga</li><li>Time and space, not a programme</li></ul></div>
    <div><h2>What it isn't.</h2><ul><li>A teacher training school</li><li>A certificate or diploma</li><li>A luxury resort or spa</li><li>A promise of transformation</li></ul></div>
  </div>
</section>
<section class="invite"><div class="wrap narrow"><h2>Come as you are.</h2><div class="actions"><a class="btn" href="contact.html">Get in touch</a></div></div></section>
"""

# ---------------------------------------------------------------- Gallery (only built when gallery.json has photos)
gallery_items = "".join(
    f'<figure class="{g.get("shape", "")}">{photo(g["file"], g["caption"])}<figcaption>{E(g["caption"])}</figcaption></figure>'
    for g in GALLERY)
gallery = f"""
<section class="page-intro"><div class="wrap"><p class="eyebrow">Gallery</p><h1>Moments.</h1><p class="lede">Yoga, the Ganga, and the people who come to share them.</p></div></section>
<section class="flush">
  <div class="wrap">
    <div class="gallery">{gallery_items}</div>
    <div class="actions"><a class="link" href="{IG}" target="_blank" rel="noopener">More on Instagram, @{SITE['instagram']}</a></div>
  </div>
</section>
"""

# ---------------------------------------------------------------- Contact
options = [f"Drop-in yoga: {f['name']}" for f in SESS["formats"]] + [r["title"] for r in RETREATS] + \
          [s["title"] for s in SPIRITS] + ["Several experiences", "Something else"]
options_html = "".join(f"<option>{E(o)}</option>" for o in options)
map_q = E(SITE["map_query"]).replace(" ", "+")
contact = f"""
<section class="page-intro"><div class="wrap"><p class="eyebrow">Contact</p><h1>Get in touch.</h1><p class="lede">The quickest way to book is WhatsApp. Fill this in and we'll open a message for you with the details ready to send.</p></div></section>
<section class="flush">
  <div class="wrap contact-grid">
    <form class="form" id="enquiry" novalidate>
      <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name" required><span class="err">Please add your name so we know who's writing.</span></div>
      <div class="field"><label for="f-interest">What would you like to join?</label><select id="f-interest" name="interest" required>{options_html}</select></div>
      <div class="row2">
        <div class="field"><label for="f-dates">Dates</label><input id="f-dates" name="dates" placeholder="e.g. 14–15 Dec"><span class="hint">Roughly is fine.</span></div>
        <div class="field"><label for="f-people">How many people</label><input id="f-people" name="people" inputmode="numeric" placeholder="1"></div>
      </div>
      <div class="field"><label for="f-msg">Anything else</label><textarea id="f-msg" name="message" placeholder="Experience level, questions, anything we should know"></textarea></div>
      <div><button class="btn" type="submit">Continue on WhatsApp</button><p class="small">Prefer to call? <a class="link" href="{TEL}">{PHONE}</a></p></div>
    </form>
    <div>
      <ul class="details-list">
        <li><b>WhatsApp</b><a class="link" data-wa="Hello {NAME}," href="#">Message us</a></li>
        <li><b>Instagram</b><a class="link" href="{IG}" target="_blank" rel="noopener">@{SITE['instagram']}</a></li>
        <li><b>Phone</b><a class="link" href="{TEL}">{PHONE}</a></li>
        <li><b>Email</b><a class="link" href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><b>Where</b>By the Ganga, Rishikesh<br><span class="small">Meeting point shared on WhatsApp or a call.</span></li>
      </ul>
      <iframe class="map" title="Map of Rishikesh" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={map_q}&output=embed"></iframe>
    </div>
  </div>
</section>
"""


# ---------------------------------------------------------------- Write
def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "static", OUT)
    (OUT / ".nojekyll").write_text("")
    page("index.html", f"{NAME} by Yogini Mansi | Yoga, retreats & spiritual experiences in Rishikesh",
         "Drop-in yoga by the Ganga, signature three- and five-day retreats, and spiritual experiences in Rishikesh. An experience, not a lesson.",
         home, current="index.html", schema=BUSINESS, hero=True, preload="images/hero.jpg")
    page("drop-in-yoga.html", f"Drop-in yoga in Rishikesh by the Ganga | {NAME}",
         "Join a drop-in yoga, pranayama and meditation session by the Ganga in Rishikesh, even for one day. Book on WhatsApp.",
         dropin, current="drop-in-yoga.html", schema=faq_schema)
    page("retreats.html", f"{RET['section_title']}: 3-day & 5-day retreats in Rishikesh | {NAME}",
         RET["intro"][0][:155], retreats, current="retreats.html")
    for r in RETREATS:
        retreat_page(r)
        redirect(f"retreats/{r['old_slug']}.html", f"{r['slug']}.html")
    for slug in RET["retired"]:
        redirect(f"retreats/{slug}.html", "../retreats.html")
    page("spiritual-experiences.html", f"{SPIRIT['section_title']} in Rishikesh | {NAME}",
         SPIRIT["intro"][:155], spiritual, current="spiritual-experiences.html")
    for s in SPIRITS:
        spirit_page(s)
    page("about.html", f"Meet Mansi, founder of {NAME} | Rishikesh",
         "Mansi's journey with yoga: years of practice, sadhana, time in an ashram and living close to the Ganga in Rishikesh.", about, current="about.html")
    if SHOW_GALLERY:
        page("gallery.html", f"Gallery | {NAME}, Rishikesh", f"Moments from {NAME} in Rishikesh.", gallery, current="gallery.html")
    page("contact.html", f"Contact & booking | {NAME}, Rishikesh",
         "Book drop-in yoga, a retreat or a spiritual experience in Rishikesh on WhatsApp.", contact, current="contact.html")

    urls = [""] + PAGES + [f"retreats/{r['slug']}.html" for r in RETREATS] + [f"spiritual/{s['slug']}.html" for s in SPIRITS]
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     + "".join(f"  <url><loc>{D}/{u}</loc></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {D}/sitemap.xml\n", encoding="utf-8")
    (OUT / "llms.txt").write_text(
        f"# {NAME} by Yogini Mansi\n\n> Drop-in yoga, signature retreats and spiritual experiences by the Ganga in Rishikesh, India. No teacher training or certification.\n\n"
        + "".join(f"- [{u or 'Home'}]({D}/{u})\n" for u in [""] + PAGES)
        + "".join(f"- [{r['title']}]({D}/retreats/{r['slug']}.html): {r['duration']}, price on enquiry\n" for r in RETREATS)
        + "".join(f"- [{s['title']}]({D}/spiritual/{s['slug']}.html): {s['line']}\n" for s in SPIRITS),
        encoding="utf-8")
    missing = sorted({f for f in [r["image"] for r in RETREATS] + [s["image"] for s in SPIRITS] if not has(f)})
    print("Built", len(urls), "pages into", OUT)
    if missing:
        print("Missing photos (showing as text cards):", ", ".join(missing))


if __name__ == "__main__":
    main()
