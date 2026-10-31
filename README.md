# Binôme 08 · Nettoyage du catalogue Netflix

**AMA PIIA cohorte 2** · exercice de nettoyage des données en binômes (sujet donné le 30/10/2026)
**Binôme** : QUENUM Amen et AFOUDA Omotola · **Domaine** : Médias

Nettoyer le catalogue des films et séries de Netflix pour pouvoir analyser les contenus par pays, genre et année.
Données : [Kaggle · shivamb/netflix-shows](https://www.kaggle.com/datasets/shivamb/netflix-shows) (`netflix_titles.csv`, 8 807 lignes, 12 colonnes).

La méthode, la répartition du travail et le planning sont dans **[GUIDE_NETTOYAGE.md](GUIDE_NETTOYAGE.md)**. À lire en premier.

## Contenu du dépôt

| Chemin | Contenu |
|---|---|
| `notebooks/nettoyage_netflix_binome08.ipynb` | Le notebook commun (le livrable) |
| `data/raw/netflix_titles.csv` | Fichier d'origine, **jamais modifié** |
| `data/processed/` | CSV nettoyé(s) produit(s) par le notebook (livrable, versionné) |
| `rapport/` | PDF final exporté depuis le notebook |
| `brouillons/` | Notebooks d'essai personnels (non versionnés) |
| `GUIDE_NETTOYAGE.md` | Méthode, problèmes repérés, répartition, planning |

## Installation (une seule fois)

Prérequis : [Python 3.12](https://www.python.org/downloads/) (cocher « Add python.exe to PATH »), [Git](https://git-scm.com/downloads) et VS Code avec l'extension **Jupyter**.

```powershell
git clone https://github.com/Omotolaaa7/ama-binome08-netflix.git
cd ama-binome08-netflix
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
code .
```

Si PowerShell refuse d'activer l'environnement (« l'exécution de scripts est désactivée ») :

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Ouvrir `notebooks/nettoyage_netflix_binome08.ipynb`, choisir le noyau **`.venv`** en haut à droite, puis **Redémarrer → Exécuter tout**. Si la première cellule plante, le noyau choisi n'est pas le bon.

Sur macOS ou Linux, remplacer `.venv\Scripts\Activate.ps1` par `source .venv/bin/activate`.

## Routine de travail à deux

Les notebooks fusionnent très mal dans Git (c'est du JSON). On évite donc de les modifier en même temps : **un seul d'entre nous a « la main » sur le notebook commun à un instant donné**.

1. Prévenir l'autre : « je prends le notebook ».
2. Récupérer la dernière version : `git pull`
3. Travailler uniquement dans **ses** sections (voir la répartition dans le guide). Pour tester sans gêner l'autre, utiliser un brouillon dans `brouillons/`.
4. Avant de pousser : **Redémarrer → Exécuter tout**, vérifier qu'il n'y a aucune erreur, enregistrer.
5. Envoyer :
   ```powershell
   git add notebooks data/processed
   git commit -m "Partie 2.3 : conversion de date_added"
   git push
   ```
6. Prévenir l'autre : « c'est poussé, à toi ».

En cas de conflit au `git pull` sur le notebook : ne pas éditer le JSON à la main. Garder sa propre version de côté (`copy notebooks\nettoyage_netflix_binome08.ipynb brouillons\ma_version.ipynb`), prendre celle du dépôt (`git checkout --theirs notebooks/nettoyage_netflix_binome08.ipynb`, puis `git add` et `git commit`), et recopier ses cellules dedans.

## Produire le PDF final

À faire à la toute fin, une fois le notebook complet et exécuté sans erreur.

```powershell
jupyter nbconvert --to webpdf --allow-chromium-download --output-dir rapport notebooks/nettoyage_netflix_binome08.ipynb
```

La première fois, la commande télécharge un navigateur Chromium (environ 150 Mo). Si elle échoue, solution de repli sans rien installer :

```powershell
jupyter nbconvert --to html --output-dir rapport notebooks/nettoyage_netflix_binome08.ipynb
```

puis ouvrir le fichier HTML obtenu dans Chrome ou Edge et faire **Ctrl+P → Enregistrer au format PDF**.
