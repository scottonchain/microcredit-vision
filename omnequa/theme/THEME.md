# Omnequa visual identity

Approved source: the operator-supplied `Omnequa_Logo_White_BG.png`, November 1, 2026. `assets/brand/omnequa-logo.png` is the unmodified original, including its white background. Do not redraw, distort, crop, recolor or remove that background. Use the complete mark with clear space.

## Palette and type

| Role | Color |
| --- | --- |
| Primary navy / headings / buttons | `#103747` |
| Dark teal / links and emphasis | `#007d88` |
| Aqua / decorative rules only | `#39aaba` |
| Body secondary text | `#4d6670` |
| Pale teal section background | `#edf7f8` |
| White page | `#ffffff` |
| Dividers | `#d7e6e9` |
| Focus ring on light surfaces | `#007080` |
| Focus ring on navy | `#ffffff` |

Use Georgia for editorial headings, Arial/Helvetica for body copy and navigation. These system fonts avoid third-party font requests. Large headings, generous whitespace and a readable article column communicate calmly. Decorative aqua is not body text. Responsive breakpoints: 1100, 760 and 380 pixels. All page families, including archives and error pages, use `tools/theme.py` and `assets/style.css`.

## Content and reader experience

Lead with the human purpose: alleviating human poverty through useful opportunity and spendable income. Explain AI agents in familiar language. Identify AI authorship and human direction. Keep research and proposed experiments distinct from measured outcomes. Do not identify the human operator or publish private correspondence. Keep politics out. No em dashes. Preserve original archived reporting, with a visible archive label and current navigation.

Current routes: home, journal, article reader, about, our work, history, press, contact, privacy, existing route aliases, archived pages and 404. Press lives at `/newsroom/` and offers the original logo and a plain-text introduction. Mail links use the established agent inbox.

## Build and restore

The source of truth for hosted code is the existing Sites project `appgprj_6ace8bfdb0a48191be221a7f84621524`. Preserve its public audience and domains. GitHub `scottonchain/microcredit-vision/omnequa/theme/` backs up this theme. Restore its style, journal script, shared shell, builder and original logo to the corresponding paths in the current Sites checkout. Retain newer content feeds, article image mirrors, publication receipts, integration tools and hosting manifest. Build and check before deploying. Do not replace current content with an old full-site snapshot.

```sh
python3 tools/build.py
python3 tools/check.py
node --check assets/journal.js
python3 -m unittest discover -s integration -p 'test_*.py'
python3 tools/test_focus.py
```

Articles continue to load from the canonical GitHub feed with the reviewed local fallback. Changing the theme must not fork the journal or erase prepared articles awaiting their canonical mirror. The build normalizes old headers and footers into the current shell without rewriting historic article bodies.
