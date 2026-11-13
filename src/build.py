#!/usr/bin/env python3
"""Builds the Punarjanma website into ../public from content/*.json.

Edit content/*.json (sessions, retreats, gallery, testimonials, site details),
then run:  python3 build.py
Deploy the ../public folder (Vercel does this automatically from the repo).
"""
import json, os, shutil, html
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT.parent / "public"
C = lambda name: json.loads((ROOT / "content" / name).read_text(encoding="utf-8"))

SITE = C("site.json")
SESS = C("sessions.json")
RETREATS = C("retreats.json")
GALLERY = C("gallery.json")
VOICES = C("testimonials.json")
E = html.escape
D = SITE["domain"].rstrip("/")

WA_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7.5-.1 1.5-.6 1.8-1.2.2-.6.2-1.1.1-1.2l-.4-.3z"/></svg>'
MENU_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 7h18M3 12h18M3 17h18" stroke="currentColor" stroke-width="1.5" fill="none"/></svg>'
ARROW = lambda d: f'<svg viewBox="0 0 16 16" aria-hidden="true"><path d="{"M6 3l5 5-5 5" if d=="next" else "M10 3L5 8l5 5"}" stroke="currentColor" stroke-width="1.5" fill="none"/></svg>'

NAV = [("index.html", "Home"), ("drop-in-yoga.html", "Drop-in yoga"), ("retreats.html", "Retreats"),
       ("about.html", "About"), ("gallery.html", "Gallery"), ("contact.html", "Contact")]


def ph(file, label, cls="", pos=None, prefix=""):
    """A photo slot. If the file is missing, the label shows until one is added."""
    src = f"{prefix}images/{file}"
    style = f"--src:url('../images/{file}')" + (f";--pos:{pos}" if pos else "")
    return f'<div class="ph {cls}" role="img" aria-label="{E(label)}" data-label="{E(label)}" data-src="{src}" style="{style}"></div>'


def video(name, label, shape="tall", prefix=""):
    return (f'<figure class="vid {shape}" style="margin:0"><video muted loop playsinline preload="metadata" '
            f'poster="{prefix}images/{name}.jpg" aria-label="{E(label)}"><source src="{prefix}images/{name}.mp4" type="video/mp4"></video>'
            f'<button class="vtoggle" type="button" aria-label="Pause video"></button></figure>')


def wa(text):
    return E(text, quote=True)


def page(path, title, desc, body, current=None, prefix="", schema=None, image="images/mansi-ganga.jpg"):
    nav = "".join(
        f'<a href="{prefix}{href}"{" aria-current=\"page\"" if href == current else ""}>{label}</a>' for href, label in NAV[1:])
    url = f"{D}/{path}".replace("/index.html", "/")
    schema_tag = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>' if schema else ""
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Punarjanma by Yogini Maansi">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{D}/{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F5F1E8">
<link rel="icon" href="{prefix}images/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}css/style.css">
{schema_tag}
</head>
<body class="no-hero">
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="{prefix}index.html" aria-label="Punarjanma home"><b>Punarjanma</b><span>by Yogini Maansi</span></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Menu">{MENU_ICON}</button>
    <nav class="nav" id="nav" aria-label="Main">{nav}<a class="btn" data-wa="Hello Punarjanma, I'd like to book a session." href="#">Book on WhatsApp</a></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="top">
      <div>
        <div class="brand-big">Punarjanma<span>by Yogini Maansi</span></div>
        <p class="pillars">Yoga, retreats, nature, experiences.</p>
        <p style="color:#CFC8B8;margin-top:1rem">Rishikesh, Uttarakhand, India</p>
      </div>
      <div>
        <h3>Explore</h3>
        <ul>{"".join(f'<li><a href="{prefix}{h}">{l}</a></li>' for h, l in NAV[1:])}</ul>
      </div>
      <div>
        <h3>Say hello</h3>
        <ul>
          <li><a href="https://instagram.com/{SITE['instagram']}" target="_blank" rel="noopener">Instagram</a></li>
          <li><a data-wa="Hello Punarjanma," href="#">WhatsApp</a></li>
          <li><a href="tel:+919630084971">+91 96300 84971</a></li>
        </ul>
      </div>
    </div>
    <div class="bottom"><span>© <span id="year">2026</span> Punarjanma by Yogini Maansi</span><span>An experience, not a lesson.</span></div>
  </div>
</footer>
<a class="wa-float" data-wa="Hello Punarjanma, I'd like to know more." href="#" aria-label="Message us on WhatsApp">{WA_ICON}</a>
<script>window.PUNARJANMA={json.dumps({"whatsapp": SITE["whatsapp"]})};</script>
<script src="{prefix}js/main.js" defer></script>
</body>
</html>"""
    out = OUT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")


BUSINESS = {
    "@context": "https://schema.org", "@type": "LocalBusiness", "additionalType": "https://schema.org/SportsActivityLocation",
    "name": "Punarjanma by Yogini Maansi", "url": D, "image": f"{D}/images/mansi-ganga.jpg",
    "description": "Drop-in yoga sessions and small curated retreats in Rishikesh for travellers and beginners.",
    "address": {"@type": "PostalAddress", "addressLocality": "Rishikesh", "addressRegion": "Uttarakhand", "addressCountry": "IN", "streetAddress": SITE["address"]},
    "sameAs": [f"https://instagram.com/{SITE['instagram']}"], "telephone": "+91-9630084971",
}

# ---------------------------------------------------------------- Home
EXPERIENCES = [
    ("exp-ganga-dip.jpg", "Ganga dip", "An early morning dip in the cold, clear river, if you'd like to."),
    ("exp-havan.jpg", "Havan", "A traditional fire ritual with a local pandit, sitting together around the flame."),
    ("exp-kirtan.jpg", "Kirtan", "Evenings of singing, drums and harmonium. Join in, or just listen."),
    ("exp-nature-walk.jpg", "Nature walks", "Forest trails, streams and quiet viewpoints in the hills around Rishikesh."),
    ("mansi-ganga.jpg", "Yoga by the Ganga", "Movement, breath and stillness beside the river."),
    ("exp-shared-meals.jpg", "Shared moments", "Simple vegetarian meals, long conversations and time together."),
]

def retreat_teaser_list():
    return "".join(f"<li>{x}</li>" for x in ["Yoga and mindful practice", "Early morning Ganga dip", "Havan", "Kirtan and devotional music", "Nature walks", "Shared vegetarian meals", "Time to yourself", "Exploring local Rishikesh", "Closing circles"])

voices_html = ""
if VOICES:
    voices_html = f"""<section><div class="wrap"><h2>In their words</h2><div class="voices">{"".join(
        f'<blockquote>{E(v["quote"])}<cite>{E(v["name"])}, {E(v.get("from",""))}</cite></blockquote>' for v in VOICES)}</div></div></section>"""

home = f"""
<section class="hero">
  <div class="hero-text">
    <h1><span class="l1">Come.</span><span class="l2">Experience Rishikesh differently.</span></h1>
    <p>A space for yoga, nature, meaningful experiences and a little time away from your everyday.</p>
    <div class="actions"><a class="btn" href="drop-in-yoga.html">Explore experiences</a><a class="link" href="retreats.html">See retreats</a></div>
  </div>
  <figure class="hero-photo" style="margin:0">{ph("mansi-ganga.jpg", "Maansi meditating beside the Ganga in Rishikesh", "dark", "center 30%")}<figcaption>Beside the Ganga, Rishikesh</figcaption></figure>
</section>

<section class="philosophy on-sage">
  <div class="wrap grid">
    <h2>An experience, not a lesson.</h2>
    <div class="body">
      <p>Some things are better experienced than explained.</p>
      <p>At Punarjanma, we believe that not everything needs to be taught, explained or defined. We don't sell certifications, prescribed transformations or a particular philosophy to follow.</p>
      <p>We bring together thoughtfully curated experiences inspired by yoga, nature, Ganga and the surroundings of Rishikesh.</p>
      <div class="rhythm"><span>You participate.</span><span>You explore.</span><span>You experience.</span></div>
      <p>And whatever you discover along the way is yours.</p>
      <p class="sign">We create the space. You experience the difference.</p>
    </div>
  </div>
</section>

<section>
  <div class="wrap split">
    <div class="media">{video("session-vertical-1", "A small group meditating together on the grass")}{ph("group-session.jpg", "A morning group session on the lawn", pos="center 60%")}</div>
    <div>
      <h2>A morning with yoga and Maa Ganga.</h2>
      <p>For travellers, visitors and anyone who wants to experience yoga in Rishikesh, even if you're only here for a day.</p>
      <p>Small, welcoming drop-in sessions in beautiful natural surroundings, particularly by the Ganga. No experience needed and no commitment beyond the morning.</p>
      <div class="actions"><a class="btn" href="drop-in-yoga.html">Explore drop-in sessions</a></div>
    </div>
  </div>
</section>

<section class="on-sage">
  <div class="wrap split flip">
    <div class="media single">{ph("retreat-stay.jpg", "Simple guesthouse room near the Ganga")}</div>
    <div>
      <h2>A few days. A different rhythm of life.</h2>
      <p>Thoughtfully curated 3-day and 5-day retreats in Rishikesh, for small groups. Days may include:</p>
      <ul class="list-quiet">{retreat_teaser_list()}</ul>
      <div class="actions"><a class="btn" href="retreats.html">Explore retreats</a></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap strip-head">
    <div><h2>More than a destination.</h2><p class="lede">A collection of experiences.</p></div>
    <div class="strip-ctrl"><button type="button" data-strip="prev" aria-label="Previous experiences">{ARROW("prev")}</button><button type="button" data-strip="next" aria-label="Next experiences">{ARROW("next")}</button></div>
  </div>
  <div class="strip" tabindex="0" aria-label="Experiences in Rishikesh, scroll sideways">
    {"".join(f'<figure>{ph(f, t, "dark")}<figcaption><h3>{t}</h3><p>{d}</p></figcaption></figure>' for f, t, d in EXPERIENCES)}
  </div>
</section>

<section class="about-teaser on-sage">
  <div class="wrap split">
    <div>{ph("mansi-portrait.jpg", "Portrait of Maansi above Rishikesh", pos="center 30%")}</div>
    <div>
      <p class="small" style="margin-bottom:1.25rem">Meet the person behind Punarjanma</p>
      <blockquote>“This isn't about becoming someone else. It's about giving yourself the opportunity to experience something different.”</blockquote>
      <p style="margin-top:1.5rem">Maansi is a yoga practitioner who has made Rishikesh her home. Punarjanma is her way of sharing the experiences that shaped her.</p>
      <div class="actions"><a class="btn ghost" href="about.html">Read my story</a></div>
    </div>
  </div>
</section>

{voices_html}

<section>
  <div class="wrap">
    <div class="strip-head"><h2>Moments from Punarjanma.</h2><a class="link" href="gallery.html">View the gallery</a></div>
    <div class="mosaic">{"".join(f'<a href="gallery.html" class="{sh}" style="position:relative;display:block" aria-label="{E(g["caption"])}">{ph(g["file"], g["caption"])}</a>' for g, sh in zip(GALLERY[:5], ["tall", "wide", "", "wide", ""]))}</div>
  </div>
</section>

<section class="invite on-walnut">
  <div class="wrap">
    <h2>Some things are better experienced than explained.</h2>
    <p>Perhaps Rishikesh is waiting to be experienced differently. Come as you are. Be part of the experience.</p>
    <div class="actions"><a class="btn light" href="contact.html">Get in touch</a><a class="link" data-wa="Hello Punarjanma, I'd like to know more." href="#">Message on WhatsApp</a></div>
  </div>
</section>
"""

# ---------------------------------------------------------------- Drop-in
faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in SESS["faq"]]}

dropin = f"""
<section class="page-intro">
  <div class="wrap">
    <h1>Drop-in yoga in Rishikesh.</h1>
    <p class="lede">Here for a day or two? Join a morning session. No experience, no mat and no commitment needed.</p>
    <div class="actions"><a class="btn" data-wa="Hello Punarjanma, I'd like to book a drop-in session." href="#">Book on WhatsApp</a><a class="link" href="#timings">How booking works</a></div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">{video("session-wide", "A group practising yoga together outdoors", "wide")}<p class="caption">A recent morning group session.</p></div>
</section>

<section>
  <div class="wrap two-col">
    <div><h2>What a session holds.</h2></div>
    <div>
      <p>Each session moves gently through four parts, guided the whole way:</p>
      <ul class="list-quiet" style="columns:1">
        <li><strong>Asana.</strong> Simple movement to wake the body.</li>
        <li><strong>Pranayama.</strong> Breathing practices that steady the mind.</li>
        <li><strong>Meditation.</strong> A few quiet minutes of sitting still.</li>
        <li><strong>Relaxation.</strong> Lying down, doing nothing, letting it settle.</li>
      </ul>
      <p style="margin-top:1.5rem">Traditional in spirit, beginner-friendly in practice. Rest whenever you need to.</p>
    </div>
  </div>
</section>

<section class="on-sage">
  <div class="wrap">
    <h2>Choose how you'd like to join.</h2>
    <p style="margin:1rem 0 2.5rem">Timing and price are arranged around your plans and group size, and shared on WhatsApp.</p>
    <div class="formats">
      {"".join(f'''<article class="format"><h3>{E(f["name"])}</h3><p class="for">{E(f["for"])}</p><p>{E(f["detail"])}</p>{f'<p class="price">{E(f["price"])}</p>' if f["price"] else ""}<p class="meta">{E(f["length"])}</p><a class="btn ghost" data-wa="Hello Punarjanma, I'd like to book: {wa(f['name'])}." href="#">Book {E(f["name"].lower())}</a></article>''' for f in SESS["formats"])}
    </div>
  </div>
</section>

<section id="timings">
  <div class="wrap two-col">
    <h2>How booking works.</h2>
    <div>
      <ol class="itinerary steps">
        <li><div><h3>Message on WhatsApp</h3><p>Tell us which day you're in Rishikesh and how many of you are coming.</p></div></li>
        <li><div><h3>Get your session</h3><p>You'll get the next available session, its timing and the price for your group.</p></div></li>
        <li><div><h3>Meet by the Ganga</h3><p>The exact meeting point is shared on WhatsApp or a quick call. Just show up.</p></div></li>
      </ol>
      <div class="actions"><a class="btn" data-wa="Hello Maansi, I'd like to know the next session, timing and meeting point." href="#">Message +91 96300 84971</a></div>
    </div>
  </div>
</section>

<section class="on-sage">
  <div class="wrap two-col">
    <h2>Questions.</h2>
    <div class="faq">{"".join(f'<details><summary>{E(f["q"])}</summary><p>{E(f["a"])}</p></details>' for f in SESS["faq"])}</div>
  </div>
</section>

<section class="invite on-walnut">
  <div class="wrap"><h2>Your morning in Rishikesh starts here.</h2><div class="actions"><a class="btn light" data-wa="Hello Punarjanma, I'd like to book a drop-in session." href="#">Book on WhatsApp</a></div></div>
</section>
"""

# ---------------------------------------------------------------- Retreats
def retreat_row(r):
    dates = ", ".join(r["dates"]) if r["dates"] else "Dates on request"
    return f"""<article class="retreat-row">
  {ph(r["image"], r["title"], "dark")}
  <div>
    <h2>{E(r["title"])}</h2>
    <p class="line">{E(r["line"])}</p>
    <p class="meta">{E(r["length"])}. {E(r["group"])}.<br>{E(dates)}</p>
    <p>{E(r["summary"])}</p>
    <div class="actions"><a class="btn" href="retreats/{r["slug"]}.html">View the retreat</a></div>
  </div>
</article>"""

retreats = f"""
<section class="page-intro">
  <div class="wrap">
    <h1>A few days. A different rhythm of life.</h1>
    <p class="lede">Small retreats in Rishikesh with yoga, the river, fire ritual, music, walks and shared meals. Simple stays, small groups, nothing prescribed.</p>
  </div>
</section>
<section style="padding-top:0"><div class="wrap">{"".join(retreat_row(r) for r in RETREATS)}</div></section>
<section class="on-sage">
  <div class="wrap two-col">
    <h2>Planning a group?</h2>
    <div><p>We also put together private retreats for friends, families and teams. Tell us how many people, how long and roughly when.</p>
    <div class="actions"><a class="btn" data-wa="Hello Punarjanma, I'd like to plan a private retreat." href="#">Plan a private retreat</a></div></div>
  </div>
</section>
"""

def retreat_page(r):
    dates_html = ("".join(f'<li><span>{E(d)}</span><a class="btn ghost" data-wa="Hello Punarjanma, I\'d like to reserve a place on {wa(r["title"])}, {wa(d)}." href="#">Reserve a place</a></li>' for d in r["dates"])
                  or f'<li><span>Dates on request</span><a class="btn ghost" data-wa="Hello Punarjanma, I\'d like to know about dates for {wa(r["title"])}." href="#">Ask about dates</a></li>')
    schema = {"@context": "https://schema.org", "@type": "Product", "name": r["title"], "description": r["summary"],
              "brand": {"@type": "Brand", "name": "Punarjanma"}}
    body = f"""
<section class="retreat-hero">
  {ph(r["image"], r["title"], "dark", prefix="../")}
  <div class="wrap"><a class="crumb" href="../retreats.html">All retreats</a><h1>{E(r["title"])}</h1><p class="lede" style="color:var(--ivory);margin-top:1rem">{E(r["line"])}</p></div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    <dl class="facts"><div><dt>Length</dt><dd>{E(r["length"])}</dd></div><div><dt>Group</dt><dd>{E(r["group"])}</dd></div><div><dt>Price</dt><dd>{E(r["price"])}</dd></div><div><dt>Where</dt><dd>Rishikesh</dd></div></dl>
    <div class="two-col" style="margin-top:4rem"><h2>The retreat.</h2><div><p class="lede" style="font-style:normal">{E(r["summary"])}</p></div></div>
  </div>
</section>
<section class="on-sage">
  <div class="wrap two-col">
    <h2>Day by day.</h2>
    <ol class="itinerary">{"".join(f'<li><div><h3>{E(d["title"])}</h3><ul>{"".join(f"<li>{E(i)}</li>" for i in d["items"])}</ul></div></li>' for d in r["itinerary"])}</ol>
  </div>
</section>
<section>
  <div class="wrap two-col">
    <h2>Where you'll stay.</h2>
    <div><p>{E(r["accommodation"])}</p>
      <div class="incl" style="margin-top:2.5rem">
        <div><h3>Included</h3><ul>{"".join(f"<li>{E(i)}</li>" for i in r["inclusions"])}</ul></div>
        <div><h3>Not included</h3><ul>{"".join(f"<li>{E(i)}</li>" for i in r["exclusions"])}</ul></div>
      </div>
    </div>
  </div>
</section>
<section class="on-sage" id="dates">
  <div class="wrap two-col">
    <h2>Dates.</h2>
    <div><ul class="dates">{dates_html}</ul><p class="small" style="margin-top:1rem">Price, dates and stay details are shared on WhatsApp.</p></div>
  </div>
</section>
"""
    page(f"retreats/{r['slug']}.html", f"{r['title']}: {r['length']} retreat in Rishikesh | Punarjanma",
         f"{r['summary'][:150]}", body, current="retreats.html", prefix="../", schema=schema,
         image=f"images/{r['image']}")

# ---------------------------------------------------------------- About
STORY = [
    "I'm Maansi — a yoga practitioner, an explorer of life and the person behind Punarjanma.",
    "My journey has never been limited to learning a practice or earning a qualification. Over the years, my experiences with yoga, self-exploration, discipline, people and life itself have shaped the way I see things.",
    "Yoga became one part of a much larger journey — a journey of understanding myself, experiencing life more consciously and discovering the value of simply being present.",
    "Rishikesh gradually became more than just a place to live. Its mountains, Ganga, nature and unique way of life became an important part of my own experience.",
    "Punarjanma comes from a desire to share some of these experiences with others.",
    "I don't believe in telling people what they must feel or what they should discover. I believe in creating the right space, bringing people together and allowing experiences to unfold naturally.",
    "Through Punarjanma, I want to bring people closer to yoga, nature, Indian traditions and the simple yet meaningful experiences that life offers.",
]
about = f"""
<section class="page-intro"><div class="wrap"><h1>Meet the person behind Punarjanma.</h1></div></section>
<section style="padding-top:0">
  <div class="wrap story">
    {ph("mansi-portrait.jpg", "Portrait of Maansi above Rishikesh", pos="center 30%")}
    <div class="text">{"".join(f"<p>{E(p)}</p>" for p in STORY)}
      <p class="close">This isn't about becoming someone else.<br>It's about giving yourself the opportunity to experience something different.</p>
      <p style="font-family:var(--sans);font-size:1rem;margin-top:2rem">— Maansi</p>
    </div>
  </div>
</section>
<section class="on-sage">
  <div class="wrap isnt">
    <div><h2>What Punarjanma is.</h2><ul><li>Drop-in yoga for travellers and beginners</li><li>Small, curated retreats</li><li>Ganga, havan, kirtan and nature</li><li>Time and space, not a programme</li></ul></div>
    <div><h2>What it isn't.</h2><ul><li>A teacher training school</li><li>A certificate or diploma</li><li>A luxury resort or spa</li><li>A promise of transformation</li></ul></div>
  </div>
</section>
<section class="invite on-walnut"><div class="wrap"><h2>Come as you are.</h2><div class="actions"><a class="btn light" href="contact.html">Get in touch</a></div></div></section>
"""

# ---------------------------------------------------------------- Gallery
gallery = f"""
<section class="page-intro"><div class="wrap"><h1>Moments.</h1><p class="lede">Yoga, the Ganga, and the people who come to share them.</p></div></section>
<section style="padding-top:0">
  <div class="wrap">
    <div class="mosaic">{"".join(f'<button type="button" class="{g.get("shape","")}" data-full="images/{g["file"]}" data-caption="{E(g["caption"])}" aria-label="Open photo: {E(g["caption"])}">{ph(g["file"], g["caption"])}</button>' for g in GALLERY)}</div>
    <div class="split" style="margin-top:4rem">
      <div class="media"><figure style="margin:0">{video("session-vertical-2", "Group meditation outdoors")}</figure><figure style="margin:0">{video("session-wide-2", "Group practising standing postures", "wide")}</figure></div>
      <div><h2>See more on Instagram.</h2><p>We share new moments from sessions and retreats regularly.</p><div class="actions"><a class="btn ghost" href="https://instagram.com/{SITE['instagram']}" target="_blank" rel="noopener">Follow @{SITE['instagram']}</a></div></div>
    </div>
  </div>
</section>
<dialog class="lightbox" aria-label="Photo"><button class="close" type="button" aria-label="Close photo">×</button><div class="ph"></div><p></p></dialog>
"""

# ---------------------------------------------------------------- Contact
options = [f["name"] for f in SESS["formats"]] + [r["title"] for r in RETREATS] + ["A private retreat", "Something else"]
contact = f"""
<section class="page-intro"><div class="wrap"><h1>Get in touch.</h1><p class="lede">The quickest way to book is WhatsApp. Fill this in and we'll open a message for you with the details ready to send.</p></div></section>
<section style="padding-top:0">
  <div class="wrap contact-grid">
    <form class="form" id="enquiry" novalidate>
      <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name" required><span class="err">Please add your name so we know who's writing.</span></div>
      <div class="field"><label for="f-interest">What would you like to join?</label><select id="f-interest" name="interest" required>{"".join(f"<option>{E(o)}</option>" for o in options)}</select></div>
      <div class="row2">
        <div class="field"><label for="f-dates">Dates</label><input id="f-dates" name="dates" placeholder="e.g. 14–15 Dec"><span class="hint">Roughly is fine.</span></div>
        <div class="field"><label for="f-people">How many people</label><input id="f-people" name="people" inputmode="numeric" placeholder="1"></div>
      </div>
      <div class="field"><label for="f-msg">Anything else</label><textarea id="f-msg" name="message" placeholder="Experience level, questions, anything we should know"></textarea></div>
      <div><button class="btn" type="submit">Continue on WhatsApp</button><p class="small" style="margin-top:1rem">Prefer to call? <a class="link" href="tel:+919630084971">+91 96300 84971</a></p></div>
    </form>
    <div>
      <ul class="details-list">
        <li><b>WhatsApp</b><a class="link" data-wa="Hello Punarjanma," href="#">Message us</a></li>
        <li><b>Instagram</b><a class="link" href="https://instagram.com/{SITE['instagram']}" target="_blank" rel="noopener">@{SITE['instagram']}</a></li>
        <li><b>Phone and WhatsApp</b><a class="link" href="tel:+919630084971">+91 96300 84971</a></li>
        <li><b>Where</b>By the Ganga, Rishikesh<br><span class="small">Meeting point shared on WhatsApp or a call.</span></li>
      </ul>
      <iframe class="map" title="Map of Rishikesh" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={E(SITE['map_query']).replace(' ', '+')}&output=embed"></iframe>
    </div>
  </div>
</section>
"""

# ---------------------------------------------------------------- Write
def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "static", OUT)
    page("index.html", "Punarjanma by Yogini Maansi | Yoga experiences & retreats in Rishikesh",
         "Drop-in yoga by the Ganga and small curated retreats in Rishikesh. For travellers and beginners. An experience, not a lesson.",
         home, current="index.html", schema=BUSINESS)
    page("drop-in-yoga.html", "Drop-in yoga classes in Rishikesh for beginners & travellers | Punarjanma",
         "Join a single yoga session in Rishikesh, even for one day. Asana, pranayama, meditation and relaxation by the Ganga. Book on WhatsApp.",
         dropin, current="drop-in-yoga.html", schema=faq_schema, image="images/group-session.jpg")
    page("retreats.html", "3-day & 5-day yoga retreats in Rishikesh | Punarjanma",
         "Small, curated yoga retreats in Rishikesh with Ganga dip, havan, kirtan, nature walks and shared vegetarian meals.",
         retreats, current="retreats.html")
    for r in RETREATS:
        retreat_page(r)
    page("about.html", "About Maansi | Punarjanma, Rishikesh",
         "Meet Maansi, the yoga practitioner behind Punarjanma in Rishikesh.", about, current="about.html", image="images/mansi-portrait.jpg")
    page("gallery.html", "Gallery | Punarjanma, Rishikesh", "Moments from Punarjanma yoga sessions and retreats in Rishikesh.",
         gallery, current="gallery.html")
    page("contact.html", "Contact & booking | Punarjanma, Rishikesh",
         "Book a drop-in yoga session or retreat in Rishikesh on WhatsApp.", contact, current="contact.html")

    urls = ["", "drop-in-yoga.html", "retreats.html", "about.html", "gallery.html", "contact.html"] + [f"retreats/{r['slug']}.html" for r in RETREATS]
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     + "".join(f"  <url><loc>{D}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {D}/sitemap.xml\n")
    (OUT / "llms.txt").write_text(
        "# Punarjanma by Yogini Maansi\n\n> Drop-in yoga sessions and small curated retreats in Rishikesh, India, for travellers and beginners. No teacher training or certification.\n\n"
        + "".join(f"- [{l}]({D}/{h})\n" for h, l in NAV) + "".join(f"- [{r['title']}]({D}/retreats/{r['slug']}.html): {r['length']}, {r['price']}\n" for r in RETREATS))
    print("Built", len(urls), "pages into", OUT)


if __name__ == "__main__":
    main()
