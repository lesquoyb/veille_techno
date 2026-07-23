# Veille techno-scientifique

Résumés quotidiens des tendances de fond en informatique, systèmes complexes, IA
et sciences — chaque entrée est un fichier Markdown `AAAA-MM-JJ.md` à la racine.

## Site de lecture (GitHub Pages)

Un site « blog » est généré automatiquement à partir des entrées : une page
d'accueil listant les numéros du plus récent au plus ancien, et une page par
entrée. Le workflow [`.github/workflows/pages.yml`](.github/workflows/pages.yml)
reconstruit et publie le site **à chaque push sur `main`** — il n'y a donc rien
à faire de plus au quotidien : ajouter un nouveau `AAAA-MM-JJ.md` suffit.

### Activation (une seule fois)

Dans le dépôt : **Settings → Pages → Build and deployment → Source = « GitHub
Actions »**. Le prochain push (ou un lancement manuel du workflow via l'onglet
Actions) publiera le site ; l'URL apparaît dans le résumé du job `deploy`.

> ⚠️ Ce dépôt est **privé**. GitHub Pages sur un dépôt privé nécessite un plan
> **GitHub Pro/Team/Enterprise** ; sans Enterprise, **le site publié est public**
> (URL peu devinable mais non protégée). À garder en tête avant d'activer.

## Aperçu local

```bash
pip install markdown
python3 scripts/build_site.py --out _site
# puis ouvrir _site/index.html dans un navigateur
```

## Structure

- `AAAA-MM-JJ.md` — les entrées de veille (source de vérité).
- `journal.md` — mémoire inter-sessions : préférences du lecteur, sujets déjà
  couverts, pistes de suivi. **Non publié** sur le site.
- `scripts/build_site.py` — générateur du site statique.
- `.github/workflows/pages.yml` — build + déploiement automatiques.
