# Punarjanam — design contract

Client brand, not a Vyuh theme. Logo LOCKED 17 Nov (night) (Harsh: "keep the old logo that was better", picked option C): thin gold LINE mandala (inline SVG, 12 petals in a ring, `currentColor`) beside the "punarjanam" lettering (wordmark-ivory.png over the hero, wordmark-dark.png on solid header) with BY YOGINI MANSI underneath; footer = round seal with PUNARJANAM · RISHIKESH · BY YOGINI MANSI on the ring; favicon/app icon = gold disc with 8 ivory petals; watermarks = mandala-gold.svg. Superseded: flat gold medallion + PUNARJANAM caps (17 Nov afternoon). The master `C:\Vyuh\DESIGN.md` themes (dark, Vyuh accents) do not apply;
its universal rules 2–5 (grid, motion, density, one accent) do. Source: Maansi's brief (`brief/README.md`)
and Harsh's approved mockup (14 Nov 2026).

## Tokens (only these colours)
| Token | Hex | Use |
|---|---|---|
| `--ivory` | #F5F1E8 | page background |
| `--tint` | #EEE9DD | quiet bands |
| `--sage` | #D8DDCE | experience cards, about band |
| `--sage-deep` | #CDD3C1 | sage hover |
| `--error` | #8A3B26 | form errors only (status colour) |
| `--dawn` | #F1E7D6 | Three-Day Retreat identity (Five-Day uses `--forest`) |
| `--olive` | #777F65 | large type, rules only |
| `--olive-ink` | #5C6450 | **the one accent**: buttons, links, small labels |
| `--sand` | #C7B49A | underlines |
| `--walnut` | #403D34 | text, dark logo |
| `--muted` | #6B675B | secondary text |
| `--forest` | #46483A | footer background |
| `--gold` | #C2A56B | logo artwork and footer ornaments only (brand mark, not an accent) |
| `--ivory-dim` | #DCD6C6 | text on dark |

## Type
Cormorant Garamond (display, 300–400, italics for taglines) + Inter (body, labels). Two families max.

## Layout and motion
- Spacing on a 4/8px grid. Square corners on cards, tiles and buttons; round only for icon buttons.
- Motion ≤300ms, ease-out, tied to a state change (hover, menu). No entrance animation that hides content above the fold.
- Exception (Harsh, 16 Nov): photo galleries fade up ~700ms as they scroll into view, and stay photos zoom 4% on hover; both off under prefers-reduced-motion.
- Full-bleed photos only for hero and closing; everything else sits in the 1160px wrap.
- Text on photos always gets a scrim; minimum 4.5:1 for body, 3:1 for 24px+ type.

## Content rules (from her brief)
- Maansi appears at most twice (home about band + About page).
- No exaggerated promises of healing or transformation. No fake reviews or numbers.
- Prefer her real photos; AI or third-party images are placeholders until she supplies her own.
