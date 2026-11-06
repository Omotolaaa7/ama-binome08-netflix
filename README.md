# Binôme 08 : Nettoyage et restructuration du catalogue Netflix

AMA PIIA cohorte 2 (Académie des Mathématiques Appliquées)  
Exercice de nettoyage des données en binôme  
Binôme : QUENUM Amen et AFOUDA Omotola  
Domaine : Médias  

Nettoyer le catalogue des films et séries de Netflix pour pouvoir analyser les contenus par pays, genre et année.  
Données : Kaggle shivamb/netflix-shows (netflix_titles.csv, 8 807 lignes, 12 colonnes brutes).  

La méthode, les problèmes repérés et la répartition initiale du travail sont décrits dans GUIDE_NETTOYAGE.md.  

---

## Contenu du dépôt

```text
ama-binome08-netflix/
│
├── data/
│   ├── raw/
│   │   └── netflix_titles.csv               # Fichier d'origine intact (8 807 lignes x 12 colonnes)
│   └── processed/
│       ├── netflix_titles_propre.csv        # Fichier nettoyé (8 800 lignes x 15 colonnes)
│       ├── netflix_pays.csv                 # Table longue des pays (10 003 associations)
│       └── netflix_genres.csv               # Table longue des genres (19 304 associations)
│
├── app/
│   ├── app.py                              # Application Streamlit
│   └── utils/
│       ├── data_loader.py                  # Chargement et calcul des métriques avec cache
│       └── charts.py                       # Graphiques interactifs
│
├── reports/
│   ├── rapport_netflix.docx                # Rapport d'analyse détaillé
│   ├── presentation_netflix.pptx           # Présentation orale (notes incluses)
│   └── img/                                # Figures insérées dans le rapport et les diapos
│
├── rapport/
│   └── nettoyage_netflix_binome08.pdf      # Export PDF original du notebook
│
├── notebooks/
│   └── nettoyage_netflix_binome08.ipynb    # Le notebook d'origine commenté
│
├── docs/
│   └── explication_du_code_binome08.docx   # Document d'explication interne
│
├── GUIDE_NETTOYAGE.md                      # Guide méthodologique initial
├── requirements.txt                        # Liste des dépendances figées
└── README.md
```

---

## Lancement rapide

### 1. Activer l'environnement virtuel

```powershell
.venv\Scripts\Activate.ps1
```

*(Sur macOS ou Linux : `source .venv/bin/activate`)*

### 2. Lancer le dashboard Streamlit

```powershell
streamlit run app/app.py
```

L'application s'ouvre sur `http://localhost:8501`.  
Elle propose 7 pages d'exploration avec deux niveaux de lecture (accessible et technique).

### 3. Consulter les documents

- Rapport Word : `reports/rapport_netflix.docx`
- Support de présentation : `reports/presentation_netflix.pptx` (déroulé de 9 min 15 s avec notes orales et diapositives de réserve)
- Notebook : `notebooks/nettoyage_netflix_binome08.ipynb`

---

## Chiffres clés vérifiés

| Indicateur | Valeur brute | Valeur nettoyée |
|---|---|---|
| Lignes | 8 807 | 8 800 (7 doublons supprimés) |
| Colonnes | 12 | 15 (4 colonnes ajoutées, 1 retirée) |
| Données manquantes | 4 307 cases vides | 4 294 marquées "Non renseigné", 10 dates vides |
| Associations Titre-Pays | Listes groupées | 10 003 lignes (table découpée) |
| Associations Titre-Genre | Listes groupées | 19 304 lignes (table découpée) |
| Titres liés aux États-Unis | 2 818 (brut) | 3 688 (table découpée) |
