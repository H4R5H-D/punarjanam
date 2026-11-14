#!/usr/bin/env python3
"""Builds the Punarjanam website into ../public from content/*.json.

Edit content/*.json (sessions, retreats, gallery, testimonials, credits, site details),
then run:  python src/build.py
Deploy the ../public folder (GitHub Pages serves the gh-pages branch).
Works on Python 3.9+.

Experience tiles: drop a photo into static/images with the file name listed in TILES below
and rebuild. Until a file exists, that tile shows as a text card (never an empty box).
"""
import json, shutil, html
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT.parent / "public"
IMAGES = ROOT / "static" / "images"
C = lambda name: json.loads((ROOT / "content" / name).read_text(encoding="utf-8"))

SITE = C("site.json")
SESS = C("sessions.json")
RETREATS = C("retreats.json")
GALLERY = C("gallery.json")
VOICES = C("testimonials.json")
CREDITS = C("credits.json")
E = html.escape
D = SITE["domain"].rstrip("/")
NAME = "Punarjanam"
PHONE = "+91 96300 84971"
TEL = "tel:+919630084971"
IG = "https://instagram.com/" + SITE["instagram"]

WA_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7.5-.1 1.5-.6 1.8-1.2.2-.6.2-1.1.1-1.2l-.4-.3z"/></svg>'
IG_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor"/></svg>'
MENU_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 8h18M3 16h18" stroke="currentColor" stroke-width="1.25" fill="none"/></svg>'
ARROW = '<span class="arr" aria-hidden="true">→</span>'

# The gallery page and its menu item only exist once gallery.json has real photos in it.
SHOW_GALLERY = len(GALLERY) > 0
NAV = [("index.html", "Home"), ("drop-in-yoga.html", "Drop-in Yoga"), ("retreats.html", "Retreats"),
       ("index.html#experiences", "Experiences"), ("about.html", "About Maansi")] + \
      ([("gallery.html", "Gallery")] if SHOW_GALLERY else [])
PAGES = ["drop-in-yoga.html", "retreats.html", "about.html"] + (["gallery.html"] if SHOW_GALLERY else []) + ["contact.html"]

# Experience tiles: (file to drop into static/images, title, one line, link)
TILES = [
    ("exp-yoga-ganga.jpg", "Yoga by Maa Ganga", "Movement, breath and stillness beside the river.", "drop-in-yoga.html"),
    ("exp-havan.jpg", "Havan Experience", "A traditional fire ritual with a pandit.", "retreats.html"),
    ("exp-kirtan.jpg", "Kirtan & Bhajans", "Singing, music and dancing together.", "retreats.html"),
    ("exp-nature-walks.jpg", "Nature Walks", "Trails and quiet viewpoints around Rishikesh.", "retreats.html"),
    ("exp-ganga-dip.jpg", "Ganga Dip", "Early morning, in the sacred river.", "retreats.html"),
    ("retreat-5day.jpg", "Retreat Experiences", "A few days, a different rhythm of life.", "retreats.html"),
]


def has(file):
    return (IMAGES / file).exists()


def first(*files):
    for f in files:
        if has(f):
            return f
    return files[-1]


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


def wa(text):
    return E(text, quote=True)


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
<meta property="og:site_name" content="{NAME} by Yogini Maansi">
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
    <a class="brand" href="{prefix}index.html" aria-label="{NAME} by Yogini Maansi, home">
      <img class="logo-light" src="{prefix}images/logo-gold.png" alt="" width="200" height="30">
      <img class="logo-dark" src="{prefix}images/logo-dark.png" alt="" width="200" height="30">
      <span>by Yogini Maansi</span>
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
    <a class="foot-logo" href="{prefix}index.html" aria-label="{NAME} home"><img src="{prefix}images/logo-stacked-gold.png" alt="{NAME}, पुनर्जन्म" width="220" height="112" loading="lazy"><span>by Yogini Maansi</span></a>
    <div class="foot-mid">
      <p>Rishikesh, Uttarakhand, India</p>
      <p class="pillars">Yoga <i>•</i> Retreats <i>•</i> Nature <i>•</i> Experiences</p>
      <p class="foot-links"><a href="{prefix}drop-in-yoga.html">Drop-in Yoga</a><a href="{prefix}retreats.html">Retreats</a><a href="{prefix}about.html">About</a><a href="{prefix}contact.html">Contact</a></p>
    </div>
    <div class="foot-social">
      <a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{IG_ICON}</a>
      <a data-wa="Hello {NAME}," href="#" aria-label="WhatsApp">{WA_ICON}</a>
    </div>
  </div>
  <div class="wrap foot-bottom">© <span id="year">2026</span> {NAME} by Yogini Maansi</div>
</footer>
<a class="wa-float" data-wa="Hello {NAME}, I'd like to know more." href="#" aria-label="Message us on WhatsApp">{WA_ICON}</a>
<script>window.PUNARJANMA={json.dumps({"whatsapp": SITE["whatsapp"]})};</script>
<script src="{prefix}js/main.js" defer></script>
</body>
</html>"""
    out = OUT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")


BUSINESS = {
    "@context": "https://schema.org", "@type": "LocalBusiness", "additionalType": "https://schema.org/SportsActivityLocation",
    "name": f"{NAME} by Yogini Maansi", "url": D + "/", "image": f"{D}/images/share.jpg", "logo": f"{D}/images/apple-touch-icon.png",
    "description": "Drop-in yoga sessions and small curated retreats in Rishikesh for travellers and beginners.",
    "address": {"@type": "PostalAddress", "addressLocality": "Rishikesh", "addressRegion": "Uttarakhand", "addressCountry": "IN"},
    "sameAs": [IG], "telephone": "+91-9630084971",
}

# ---------------------------------------------------------------- Home
voices_html = ""
if VOICES:
    quotes = "".join(
        f'<blockquote>{E(v["quote"])}<cite>{E(v["name"])}, {E(v.get("from", ""))}</cite></blockquote>' for v in VOICES)
    voices_html = f'<section><div class="wrap"><h2>In their words</h2><div class="voices">{quotes}</div></div></section>'


def tile(i, file, title, line, href):
    if has(file):
        return (f'<li><a class="tile" href="{href}">{photo(file, title)}'
                f'<span class="tile-t">{E(title)}</span></a></li>')
    return (f'<li><a class="tile text" href="{href}"><span class="tile-n">{i:02d}</span>'
            f'<span class="tile-t">{E(title)}</span><span class="tile-d">{E(line)}</span></a></li>')


tiles_html = "".join(tile(i, *t) for i, t in enumerate(TILES, 1))
philo_img = first("philosophy.jpg", "retreat-women.jpg")
about_img = "mansi-portrait.jpg"

home = f"""
<section class="hero">
  {photo("hero.jpg", "Sunrise over the Ganga at Rishikesh, with Lakshman Jhula and the temples on the riverbank", cls="hero-img", eager=True)}
  <div class="wrap hero-text">
    <h1>Come. Experience Rishikesh differently.</h1>
    <p class="tag">An experience, not a lesson.</p>
    <p class="sub">Yoga, nature, Ganga and meaningful experiences.</p>
    <div class="actions">
      <a class="btn fill-light" data-wa="Hello {NAME}, I'd like to book a session." href="#">{WA_ICON}Book a Session</a>
      <a class="btn line light" href="#experiences">Explore Experiences {ARROW}</a>
    </div>
  </div>
</section>

<section class="facts-strip" aria-label="At a glance">
  <dl class="wrap facts-row">
    <div><dt>Format</dt><dd>Drop-in sessions &amp; retreats</dd></div>
    <div><dt>Groups</dt><dd>Small and welcoming</dd></div>
    <div><dt>Where</dt><dd>By the Ganga, Rishikesh</dd></div>
    <div><dt>Guided by</dt><dd>Yogini Maansi</dd></div>
  </dl>
</section>

<section class="philo">
  <div class="philo-text">
    <img class="lotus-deco" src="images/mark-gold.png" alt="" aria-hidden="true" loading="lazy">
    <h2>Some things are better experienced than explained.</h2>
    <p>At {NAME}, we bring together thoughtfully curated experiences inspired by yoga, nature, Ganga and the surroundings of Rishikesh.</p>
    <p class="rhythm">You participate. You explore. You experience.</p>
  </div>
  <figure class="philo-img">{photo(philo_img, "The Ganga at Rishikesh")}{credit(philo_img, "credit on-img")}</figure>
</section>

<section id="experiences" class="exps">
  <div class="wrap exps-grid">
    <div class="exps-intro">
      <p class="eyebrow">Experiences</p>
      <h2>A journey through experiences.</h2>
      <p>From morning yoga to sacred rituals, from nature walks to shared meals: Rishikesh, as it is lived.</p>
      <a class="btn line" href="retreats.html">Explore All Experiences {ARROW}</a>
    </div>
    <ul class="tiles">{tiles_html}</ul>
  </div>
</section>

<section class="about-band">
  <figure class="about-img">{photo(about_img, "Maansi in Rishikesh")}{credit(about_img, "credit on-img")}</figure>
  <div class="about-text">
    <img class="lotus-deco" src="images/mark-gold.png" alt="" aria-hidden="true" loading="lazy">
    <p class="eyebrow">About {NAME}</p>
    <h2>Meet the person behind {NAME}.</h2>
    <p>I'm Maansi, a yoga practitioner and an explorer of life. Rishikesh gradually became more than just a place to live. {NAME} comes from a desire to share some of these experiences with others.</p>
    <a class="link" href="about.html">Know more about Maansi {ARROW}</a>
  </div>
</section>

{voices_html}

<section class="closing">
  {photo("closing.jpg", "Morning mist over the Ganga at Rishikesh", cls="closing-img")}
  <div class="wrap closing-text">
    <h2>Some things are better experienced than explained.<br>Perhaps Rishikesh is waiting.</h2>
    <p>Come as you are. Be part of the experience.</p>
    <a class="btn line light" href="contact.html">Get in Touch {ARROW}</a>
  </div>
  {credit("closing.jpg", "credit on-img")}
</section>
"""

# ---------------------------------------------------------------- Drop-in
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
    <p class="eyebrow">Drop-in yoga</p>
    <h1>A morning with yoga and Maa Ganga.</h1>
    <p class="lede">Here for a day or two? Join a morning session. No experience, no mat and no commitment needed.</p>
    <div class="actions"><a class="btn" data-wa="Hello {NAME}, I'd like to book a drop-in session." href="#">Book on WhatsApp</a><a class="link" href="#booking">How booking works</a></div>
  </div>
</section>

<section class="flush">
  <div class="wrap">
    <div class="shots">{photo("group-session.jpg", "A small group practising yoga outdoors")}{photo("still-asana.jpg", "Students stretching on their mats")}{photo("still-meditation.jpg", "A group sitting in meditation")}</div>
    <p class="caption">Recent morning sessions.</p>
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
      <div class="actions"><a class="btn" data-wa="Hello Maansi, I'd like to know the next session, timing and meeting point." href="#">Message {PHONE}</a></div>
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

# ---------------------------------------------------------------- Retreats
def retreat_row(r):
    dates = ", ".join(r["dates"]) if r["dates"] else "Dates on request"
    return f"""<article class="retreat-row">
  <a class="img" href="retreats/{r["slug"]}.html" tabindex="-1" aria-hidden="true">{photo(r["image"], "")}</a>
  <div>
    <h2><a href="retreats/{r["slug"]}.html">{E(r["title"])}</a></h2>
    <p class="line">{E(r["line"])}</p>
    <p class="meta">{E(r["length"])} · {E(r["group"])} · {E(dates)}</p>
    <a class="link" href="retreats/{r["slug"]}.html">View the retreat</a>
  </div>
</article>"""


retreats = f"""
<section class="page-intro">
  <div class="wrap">
    <p class="eyebrow">Retreats</p>
    <h1>A few days. A different rhythm of life.</h1>
    <p class="lede">Small retreats in Rishikesh with yoga, the river, fire ritual, music, walks and shared meals. Simple stays, small groups, nothing prescribed.</p>
  </div>
</section>
{banner("hero.jpg", alt="Sunrise over the Ganga at Rishikesh", eager=True)}
<section><div class="wrap">{"".join(retreat_row(r) for r in RETREATS)}</div></section>
<section class="tint">
  <div class="wrap two-col">
    <h2>Planning a group?</h2>
    <div><p>We also put together private retreats for friends, families and teams. Tell us how many people, how long and roughly when.</p>
    <div class="actions"><a class="btn" data-wa="Hello {NAME}, I'd like to plan a private retreat." href="#">Plan a private retreat</a></div></div>
  </div>
</section>
"""


def retreat_page(r):
    if r["dates"]:
        dates_html = "".join(
            f'<li><span>{E(d)}</span><a class="link" data-wa="{wa("Hello " + NAME + ", I would like to reserve a place on " + r["title"] + ", " + d + ".")}" href="#">Reserve a place</a></li>'
            for d in r["dates"])
    else:
        dates_html = (f'<li><span>Dates on request</span><a class="link" data-wa="{wa("Hello " + NAME + ", I would like to know about dates for " + r["title"] + ".")}" href="#">Ask about dates</a></li>')
    schema = {"@context": "https://schema.org", "@type": "Product", "name": r["title"], "description": r["summary"],
              "brand": {"@type": "Brand", "name": NAME}}
    days = "".join(
        "<li><div><h3>" + E(d["title"]) + "</h3><ul>" + "".join("<li>" + E(i) + "</li>" for i in d["items"]) + "</ul></div></li>"
        for d in r["itinerary"])
    incl = "".join("<li>" + E(i) + "</li>" for i in r["inclusions"])
    excl = "".join("<li>" + E(i) + "</li>" for i in r["exclusions"])
    body = f"""
<section class="page-intro">
  <div class="wrap">
    <a class="crumb" href="../retreats.html">All retreats</a>
    <h1>{E(r["title"])}</h1>
    <p class="lede">{E(r["line"])}</p>
  </div>
</section>
{banner(r["image"], prefix="../", eager=True)}
<section>
  <div class="wrap">
    <dl class="facts"><div><dt>Length</dt><dd>{E(r["length"])}</dd></div><div><dt>Group</dt><dd>{E(r["group"])}</dd></div><div><dt>Price</dt><dd>{E(r["price"])}</dd></div><div><dt>Where</dt><dd>Rishikesh</dd></div></dl>
    <div class="two-col gap-top"><h2>The retreat.</h2><p class="lede-sm">{E(r["summary"])}</p></div>
  </div>
</section>
<section class="tint">
  <div class="wrap two-col">
    <h2>Day by day.</h2>
    <ol class="itinerary">{days}</ol>
  </div>
</section>
<section>
  <div class="wrap two-col">
    <h2>Where you'll stay.</h2>
    <div><p>{E(r["accommodation"])}</p>
      <div class="incl">
        <div><h3>Included</h3><ul>{incl}</ul></div>
        <div><h3>Not included</h3><ul>{excl}</ul></div>
      </div>
    </div>
  </div>
</section>
<section class="tint" id="dates">
  <div class="wrap two-col">
    <h2>Dates.</h2>
    <div><ul class="dates">{dates_html}</ul><p class="small">Price, dates and stay details are shared on WhatsApp.</p></div>
  </div>
</section>
"""
    page(f"retreats/{r['slug']}.html", f"{r['title']}: {r['length']} retreat in Rishikesh | {NAME}",
         r["summary"][:150], body, current="retreats.html", prefix="../", schema=schema,
         image=f"images/{r['image']}")


# ---------------------------------------------------------------- About
STORY = [
    f"I'm Maansi — a yoga practitioner, an explorer of life and the person behind {NAME}.",
    "My journey has never been limited to learning a practice or earning a qualification. Over the years, my experiences with yoga, self-exploration, discipline, people and life itself have shaped the way I see things.",
    "Yoga became one part of a much larger journey — a journey of understanding myself, experiencing life more consciously and discovering the value of simply being present.",
    "Rishikesh gradually became more than just a place to live. Its mountains, Ganga, nature and unique way of life became an important part of my own experience.",
    f"{NAME} comes from a desire to share some of these experiences with others.",
    "I don't believe in telling people what they must feel or what they should discover. I believe in creating the right space, bringing people together and allowing experiences to unfold naturally.",
    f"Through {NAME}, I want to bring people closer to yoga, nature, Indian traditions and the simple yet meaningful experiences that life offers.",
]
story_html = "".join(f"<p>{E(p)}</p>" for p in STORY)
about = f"""
<section class="page-intro"><div class="wrap"><p class="eyebrow">About Maansi</p><h1>Meet the person behind {NAME}.</h1></div></section>
<section class="flush">
  <div class="wrap story">
    {photo("mansi-portrait.jpg", "Maansi in Rishikesh", eager=True)}
    <div class="text">{story_html}
      <p class="close">This isn't about becoming someone else.<br>It's about giving yourself the opportunity to experience something different.</p>
      <p class="sig">— Maansi</p>
    </div>
  </div>
</section>
<section class="tint">
  <div class="wrap isnt">
    <div><h2>What {NAME} is.</h2><ul><li>Drop-in yoga for travellers and beginners</li><li>Small, curated retreats</li><li>Ganga, havan, kirtan and nature</li><li>Time and space, not a programme</li></ul></div>
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
options = [f["name"] for f in SESS["formats"]] + [r["title"] for r in RETREATS] + ["A private retreat", "Something else"]
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
    page("index.html", f"{NAME} by Yogini Maansi | Yoga experiences & retreats in Rishikesh",
         "Drop-in yoga by the Ganga and small curated retreats in Rishikesh. For travellers and beginners. An experience, not a lesson.",
         home, current="index.html", schema=BUSINESS, hero=True, preload="images/hero.jpg")
    page("drop-in-yoga.html", f"Drop-in yoga classes in Rishikesh for beginners & travellers | {NAME}",
         "Join a single yoga session in Rishikesh, even for one day. Asana, pranayama, meditation and relaxation by the Ganga. Book on WhatsApp.",
         dropin, current="drop-in-yoga.html", schema=faq_schema)
    page("retreats.html", f"3-day & 5-day yoga retreats in Rishikesh | {NAME}",
         "Small, curated yoga retreats in Rishikesh with Ganga dip, havan, kirtan, nature walks and shared vegetarian meals.",
         retreats, current="retreats.html")
    for r in RETREATS:
        retreat_page(r)
    page("about.html", f"About Maansi | {NAME}, Rishikesh",
         f"Meet Maansi, the yoga practitioner behind {NAME} in Rishikesh.", about, current="about.html")
    if SHOW_GALLERY:
        page("gallery.html", f"Gallery | {NAME}, Rishikesh", f"Moments from {NAME} yoga sessions and retreats in Rishikesh.",
             gallery, current="gallery.html")
    page("contact.html", f"Contact & booking | {NAME}, Rishikesh",
         "Book a drop-in yoga session or retreat in Rishikesh on WhatsApp.", contact, current="contact.html")

    urls = [""] + PAGES + [f"retreats/{r['slug']}.html" for r in RETREATS]
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     + "".join(f"  <url><loc>{D}/{u}</loc></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {D}/sitemap.xml\n", encoding="utf-8")
    (OUT / "llms.txt").write_text(
        f"# {NAME} by Yogini Maansi\n\n> Drop-in yoga sessions and small curated retreats in Rishikesh, India, for travellers and beginners. No teacher training or certification.\n\n"
        + "".join(f"- [{u or 'Home'}]({D}/{u})\n" for u in [""] + PAGES)
        + "".join(f"- [{r['title']}]({D}/retreats/{r['slug']}.html): {r['length']}, {r['price']}\n" for r in RETREATS),
        encoding="utf-8")
    missing = [t[0] for t in TILES if not has(t[0])]
    print("Built", len(urls), "pages into", OUT)
    if missing:
        print("Experience tiles still showing as text (add these to static/images):", ", ".join(missing))


if __name__ == "__main__":
    main()
