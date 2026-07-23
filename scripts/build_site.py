#!/usr/bin/env python3
"""Génère un site statique « blog » à partir des entrées de veille (fichiers
YYYY-MM-DD*.md à la racine du dépôt).

Usage :
    python3 scripts/build_site.py [--out _site]

Sortie : un dossier autonome (index + une page HTML par entrée + feuille de
style), prêt à être publié par GitHub Pages. Aucun réglage requis côté workflow
quotidien : il suffit d'ajouter un nouveau fichier YYYY-MM-DD.md à la racine, le
site se reconstruit tout seul via l'action GitHub.
"""

from __future__ import annotations

import argparse
import html
import re
from datetime import date
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})")
MOIS = [
    "", "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
]

SITE_TITLE = "Veille techno-scientifique"
SITE_SUBTITLE = (
    "Résumé quotidien des tendances de fond en informatique, systèmes complexes, "
    "IA et sciences — avec les sources."
)


def french_date(y: int, m: int, d: int) -> str:
    return f"{d} {MOIS[m]} {y}"


def strip_markdown(text: str) -> str:
    """Réduit un extrait Markdown à du texte quasi brut pour les cartes."""
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)   # liens -> texte
    text = re.sub(r"[*_`>#]+", "", text)                    # marques
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_meta(md_text: str) -> tuple[str, str]:
    """Retourne (titre, chapô-texte-brut) d'une entrée."""
    lines = md_text.splitlines()
    title = ""
    chapo_lines: list[str] = []
    seen_title = False
    for line in lines:
        if not seen_title:
            if line.startswith("# "):
                title = line[2:].strip()
                seen_title = True
            continue
        stripped = line.strip()
        if stripped.startswith(">"):
            chapo_lines.append(stripped.lstrip("> ").strip())
        elif stripped == "" and not chapo_lines:
            continue          # lignes vides avant le chapô
        elif chapo_lines:
            break             # fin du bloc de citation
        elif stripped and not stripped.startswith(("---", "#")):
            chapo_lines.append(stripped)   # repli : 1er paragraphe
            break
    chapo = strip_markdown(" ".join(chapo_lines))
    # On retire le préfixe « Fil rouge : » s'il existe, pour des cartes plus nettes.
    chapo = re.sub(r"^Fil rouge\s*:\s*", "", chapo)
    return title, chapo


def truncate(text: str, n: int = 300) -> str:
    if len(text) <= n:
        return text
    cut = text[:n].rsplit(" ", 1)[0]
    return cut + "…"


def cap(text: str) -> str:
    return text[0].upper() + text[1:] if text else text


def card_headline(chapo: str) -> tuple[str, str]:
    """Découpe le chapô en (titre de carte, reste-en-résumé).

    Le titre est la première proposition (avant « — », « : » ou «. »)
    car le H1 des entrées est identique (« Veille… — DATE ») et ne distingue rien.
    """
    title = ""
    for sep in (" — ", " : ", ". "):
        idx = chapo.find(sep)
        if 15 <= idx <= 95 and chapo[:idx].count("(") == chapo[:idx].count(")"):
            title = chapo[:idx]
            break
    if not title:
        title = truncate(chapo, 85)
    rest = chapo[len(title):].lstrip(" —:. ")
    return cap(title), cap(rest)


def render_body(md_text: str) -> str:
    md = markdown.Markdown(
        extensions=["extra", "sane_lists", "smarty", "toc"],
        output_format="html5",
    )
    return md.convert(md_text)


PAGE_TMPL = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — {site}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="{root}assets/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🔭</text></svg>">
</head>
<body>
<script>(function(){{var t=localStorage.getItem('theme');if(t)document.documentElement.setAttribute('data-theme',t);}})();</script>
<header class="topbar">
  <a class="brand" href="{root}index.html">🔭 {site}</a>
  <button id="themebtn" class="themebtn" aria-label="Basculer le thème clair/sombre">◐</button>
</header>
<main>
{main}
</main>
<footer class="sitefoot">
  <p>Veille générée automatiquement · <a href="{root}index.html">toutes les entrées</a></p>
</footer>
<script>
document.getElementById('themebtn').addEventListener('click',function(){{
  var el=document.documentElement;
  var cur=el.getAttribute('data-theme');
  var next=cur==='dark'?'light':(cur==='light'?'dark':(matchMedia('(prefers-color-scheme: dark)').matches?'light':'dark'));
  el.setAttribute('data-theme',next);localStorage.setItem('theme',next);
}});
</script>
</body>
</html>
"""


def build_index(entries: list[dict], out: Path) -> None:
    cards = []
    for e in entries:
        cards.append(
            f'''<article class="card">
  <a class="card-link" href="{e["slug"]}.html">
    <time datetime="{e["iso"]}">{e["fr_date"]}</time>
    <h2>{html.escape(e["headline"])}</h2>
    <p>{html.escape(e["summary"])}</p>
    <span class="readmore">Lire l'entrée →</span>
  </a>
</article>'''
        )
    count = len(entries)
    main = f'''<section class="hero">
  <h1>{SITE_TITLE}</h1>
  <p class="lede">{SITE_SUBTITLE}</p>
  <p class="meta">{count} entrée{"s" if count > 1 else ""} · la plus récente : {entries[0]["fr_date"] if entries else "—"}</p>
</section>
<section class="cards">
{chr(10).join(cards)}
</section>'''
    page = PAGE_TMPL.format(
        title="Accueil", site=SITE_TITLE, desc=html.escape(SITE_SUBTITLE),
        root="", main=main,
    )
    (out / "index.html").write_text(page, encoding="utf-8")


def build_entry(e: dict, prev_e, next_e, out: Path) -> None:
    nav_prev = (
        f'<a class="pn prev" href="{prev_e["slug"]}.html">← {prev_e["fr_date"]}</a>'
        if prev_e else '<span class="pn disabled"></span>'
    )
    nav_next = (
        f'<a class="pn next" href="{next_e["slug"]}.html">{next_e["fr_date"]} →</a>'
        if next_e else '<span class="pn disabled"></span>'
    )
    main = f'''<article class="entry">
<p class="crumb"><a href="index.html">← Toutes les entrées</a></p>
{e["body"]}
<nav class="entrynav">
  {nav_next}
  {nav_prev}
</nav>
</article>'''
    page = PAGE_TMPL.format(
        title=html.escape(e["title"]), site=SITE_TITLE,
        desc=html.escape(e["summary"]), root="", main=main,
    )
    (out / f'{e["slug"]}.html').write_text(page, encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="_site")
    args = ap.parse_args()
    out = ROOT / args.out
    out.mkdir(parents=True, exist_ok=True)
    (out / "assets").mkdir(exist_ok=True)

    entries = []
    for path in sorted(ROOT.glob("*.md")):
        if path.name in {"journal.md", "README.md"}:
            continue
        m = DATE_RE.match(path.name)
        if not m:
            continue
        y, mo, d = int(m[1]), int(m[2]), int(m[3])
        text = path.read_text(encoding="utf-8")
        title, chapo = extract_meta(text)
        headline, rest = card_headline(chapo) if chapo else ("", "")
        entries.append({
            "slug": path.stem,
            "iso": f"{y:04d}-{mo:02d}-{d:02d}",
            "sortkey": date(y, mo, d),
            "fr_date": french_date(y, mo, d),
            "title": title or path.stem,
            "headline": headline or french_date(y, mo, d),
            "summary": truncate(rest) if rest else "",
            "body": render_body(text),
        })

    entries.sort(key=lambda e: e["sortkey"], reverse=True)  # plus récent d'abord

    build_index(entries, out)
    for i, e in enumerate(entries):
        newer = entries[i - 1] if i > 0 else None            # plus récent
        older = entries[i + 1] if i + 1 < len(entries) else None
        build_entry(e, prev_e=older, next_e=newer, out=out)

    (out / "assets" / "style.css").write_text(CSS, encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Site généré : {out} ({len(entries)} entrées)")


CSS = """:root{
  --bg:#fbfaf7; --fg:#1e1b16; --muted:#6b6459; --card:#ffffff; --border:#e7e1d6;
  --accent:#9a5b2e; --accent-soft:#f0e7dc; --code-bg:#f3efe8; --link:#8a4d24;
  --maxw:760px;
}
:root[data-theme="dark"]{
  --bg:#14130f; --fg:#e9e4da; --muted:#9a9384; --card:#1c1a15; --border:#2c281f;
  --accent:#d79a5b; --accent-soft:#2a2318; --code-bg:#211e18; --link:#e0a86a;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#14130f; --fg:#e9e4da; --muted:#9a9384; --card:#1c1a15;
    --accent:#d79a5b; --accent-soft:#2a2318; --code-bg:#211e18; --link:#e0a86a;
    --border:#2c281f;
  }
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--bg); color:var(--fg);
  font:17px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
}
.topbar{
  position:sticky; top:0; z-index:10; display:flex; align-items:center;
  justify-content:space-between; gap:1rem; padding:.7rem 1.2rem;
  background:color-mix(in srgb,var(--bg) 88%,transparent);
  backdrop-filter:saturate(1.4) blur(8px); border-bottom:1px solid var(--border);
}
.brand{font-weight:700; text-decoration:none; color:var(--fg); font-size:1.02rem}
.themebtn{
  border:1px solid var(--border); background:var(--card); color:var(--fg);
  border-radius:8px; padding:.25rem .55rem; cursor:pointer; font-size:1rem;
}
.themebtn:hover{border-color:var(--accent)}
main{max-width:var(--maxw); margin:0 auto; padding:1.6rem 1.2rem 3rem}
.hero{padding:1.5rem 0 .5rem; border-bottom:1px solid var(--border); margin-bottom:1.5rem}
.hero h1{font-size:2rem; margin:.2rem 0}
.lede{color:var(--muted); font-size:1.05rem; margin:.4rem 0}
.hero .meta{color:var(--muted); font-size:.9rem}
.cards{display:flex; flex-direction:column; gap:1rem}
.card{border:1px solid var(--border); border-radius:14px; background:var(--card); transition:border-color .15s, transform .15s}
.card:hover{border-color:var(--accent); transform:translateY(-2px)}
.card-link{display:block; padding:1.1rem 1.3rem; text-decoration:none; color:inherit}
.card time{color:var(--accent); font-size:.82rem; font-weight:600; letter-spacing:.02em; text-transform:uppercase}
.card h2{margin:.3rem 0 .5rem; font-size:1.25rem; line-height:1.3; color:var(--fg)}
.card p{margin:0 0 .7rem; color:var(--muted); font-size:.96rem}
.readmore{color:var(--link); font-weight:600; font-size:.9rem}
.crumb{margin:0 0 1rem}
.crumb a{color:var(--muted); text-decoration:none; font-size:.9rem}
.crumb a:hover{color:var(--accent)}
.entry{overflow-wrap:break-word}
.entry h1{font-size:1.9rem; line-height:1.2; margin:.2rem 0 1rem}
.entry h2{font-size:1.45rem; margin:2.2rem 0 .8rem; padding-top:.6rem; border-top:1px solid var(--border)}
.entry h3{font-size:1.2rem; margin:1.8rem 0 .2rem; color:var(--accent)}
.entry h3 + p{margin-top:.15rem; color:var(--muted); font-size:.9rem}
.entry h3 + p em{font-style:normal}
.entry p{margin:.8rem 0}
a{color:var(--link)}
a:hover{color:var(--accent)}
.entry blockquote{
  margin:1.2rem 0; padding:.8rem 1.1rem; border-left:3px solid var(--accent);
  background:var(--accent-soft); border-radius:0 8px 8px 0; color:var(--fg);
}
.entry blockquote p{margin:.3rem 0}
hr{border:none; border-top:1px solid var(--border); margin:2rem 0}
code{background:var(--code-bg); padding:.12em .4em; border-radius:5px; font-size:.9em}
pre{background:var(--code-bg); padding:1rem; border-radius:10px; overflow-x:auto}
pre code{background:none; padding:0}
ul,ol{padding-left:1.4rem}
li{margin:.3rem 0}
.tablewrap,.entry{max-width:100%}
table{border-collapse:collapse; width:100%; display:block; overflow-x:auto; font-size:.92rem}
th,td{border:1px solid var(--border); padding:.5rem .7rem; text-align:left; vertical-align:top}
th{background:var(--accent-soft)}
.entrynav{display:flex; justify-content:space-between; gap:1rem; margin-top:2.5rem; padding-top:1.2rem; border-top:1px solid var(--border)}
.pn{text-decoration:none; color:var(--link); font-weight:600; font-size:.92rem}
.pn:hover{color:var(--accent)}
.pn.disabled{visibility:hidden}
.sitefoot{max-width:var(--maxw); margin:0 auto; padding:1.5rem 1.2rem 2.5rem; color:var(--muted); font-size:.85rem; border-top:1px solid var(--border)}
.sitefoot a{color:var(--muted)}
"""


if __name__ == "__main__":
    main()
