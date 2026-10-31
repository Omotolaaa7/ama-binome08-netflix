# Guide du binôme 08 · Comment on nettoie le catalogue Netflix

Ce document dit **qui fait quoi, dans quel ordre, et comment**. Le livrable reste le notebook : ce guide sert à s'organiser, il n'est pas à rendre.

## 1. Ce que l'enseignant attend

D'après la fiche de l'exercice (30/10/2026), chaque binôme rend les mêmes quatre éléments :

| # | Livrable | Dans notre notebook |
|---|---|---|
| 1 | **État des lieux** avant toute correction : dimensions, types, valeurs manquantes, doublons, valeurs aberrantes | Partie 1 |
| 2 | **Corrections justifiées** : ce qui a été fait (suppression, imputation, conversion, harmonisation) et **pourquoi ce choix plutôt qu'un autre** | Partie 2 |
| 3 | **État final** : les mêmes indicateurs recalculés après nettoyage | Partie 3 |
| 4 | **Les fichiers** : notebook pandas commenté **en français** + CSV nettoyé | Partie 4 + `data/processed/` |

Les quatre conseils de la fiche, qui sont aussi les critères de correction probables :

- garder une copie intacte du fichier d'origine (`brut`) et travailler sur une copie (`df`) ;
- **mesurer la perte** avant de supprimer une ligne ou une colonne ;
- une valeur manquante n'est pas forcément une erreur : comprendre **pourquoi** elle manque ;
- le but n'est pas un fichier sans aucun vide, mais un fichier dont **chaque transformation est expliquée**.

En plus, nous avons rendu un **PDF** exporté depuis le notebook (voir le README).

## 2. Répartition

| Partie | Qui | Contenu |
|---|---|---|
| 1. État des lieux | **à deux** (appel + partage d'écran) | Les deux doivent connaître le jeu de données par cœur pour la présentation |
| 2.1 Texte et espaces | **Omotola** | |
| 2.2 Valeurs décalées | **Omotola** | |
| 2.3 `date_added` | **Omotola** | |
| 2.4 `duration` | **Omotola** | |
| 2.5 Manquants (`director`, `cast`, `country`, `rating`, `date_added`) | **Amen** | |
| 2.6 Colonnes à plusieurs valeurs | **Amen** | |
| 2.7 Autres problèmes | **Amen** | |
| 3. État final | **à deux** | |
| 4. Export + PDF | **à deux** | |

Omotola a plutôt des conversions (beaucoup de code, décisions simples). Amen a plutôt des décisions (moins de code, plus d'argumentation). Les sections d'Amen s'exécutent **après** celles d'Omotola : en attendant, Amen peut préparer son code dans `brouillons/` sur `brut.copy()`, puis le recopier dans le notebook commun quand c'est son tour.

## 3. Planning (présentation prévue jeudi 5/11)

| Jour | À faire | Qui |
|---|---|---|
| **Sam 31/10** | Dépôt GitHub créé, Amen invité, installation chez Amen (README), chacun lance le notebook sans erreur | à deux |
| **Dim 1/11** | Partie 1 complète + tableau bilan 1.5 rempli | à deux |
| **Lun 2/11** | Sections 2.1 à 2.4 poussées · Amen prépare 2.5 à 2.7 en brouillon | Omotola · Amen |
| **Mar 3/11** | Sections 2.5 à 2.7 intégrées dans le notebook commun · Omotola relit | Amen · Omotola |
| **Mer 4/11** | Parties 3 et 4, relecture complète, **Redémarrer → Exécuter tout**, PDF, répétition de l'oral | à deux |
| **Jeu 5/11** | Présentation. On ne touche plus au dépôt ce jour-là | |

## 4. Ce qu'on sait déjà du fichier

Premier diagnostic fait sur `netflix_titles.csv` pour savoir où chercher. **Ces chiffres doivent être retrouvés par le code de la partie 1** : on ne les recopie pas à la main.

- **8 807 lignes, 12 colonnes**. Toutes les colonnes sont du texte sauf `release_year` (entier).
- **Aucun doublon strict**, aucun `show_id` en double.

### Valeurs manquantes

| Colonne | Manquants | % | Remarque |
|---|---|---|---|
| `director` | 2 634 | 29,9 % | **91 % des séries** n'ont pas de réalisateur, contre 3 % des films : souvent une information inexistante plutôt qu'un oubli |
| `cast` | 825 | 9,4 % | Documentaires, dessins animés… |
| `country` | 831 | 9,4 % | |
| `date_added` | 10 | 0,1 % | Que des séries (Friends, Frasier…) |
| `rating` | 4 | < 0,1 % | Plus 3 valeurs décalées, voir ci-dessous |
| `duration` | 3 | < 0,1 % | Ce sont les 3 valeurs décalées |

### Problèmes repérés

| Problème | Colonne(s) | Lignes | Section |
|---|---|---|---|
| Espaces au début de la date (`" August 4, 2017"`) | `date_added` | 88 | 2.1 / 2.3 |
| **Espaces insécables** invisibles (`\xa0`), ex. `"Consequences\xa0"` | `title`, `description` | 5 + 9 | 2.1 |
| **Espaces de largeur nulle** (`​`), totalement invisibles, ex. `"​Goli Soda 2"` | `title`, `cast` | 5 + 1 | 2.1 |
| Doubles espaces, ex. `"Tremors 5:  Bloodline"` | `title`, `cast`, `description` | 3 + 7 + 6 | 2.1 |
| **Durée rangée dans `rating`** (`"74 min"`) et `duration` vide : les 3 spectacles de Louis C.K. (s5542, s5795, s5814) | `rating`, `duration` | 3 | 2.2 |
| Date d'ajout en texte (`"September 25, 2021"`) | `date_added` | 8 797 | 2.3 |
| Une colonne, deux unités : `"90 min"` (films) et `"2 Seasons"` / `"1 Season"` (séries) | `duration` | 8 804 | 2.4 |
| Plusieurs valeurs par case séparées par des virgules | `country` (1 320), `listed_in` (6 787), `cast` (7 101), `director` (614) | | 2.6 |
| Pays commençant par une virgule (`", South Korea"`) ou finissant par une virgule (`"Poland,"`) | `country` | 2 + 5 | 2.6 |
| `NR` (*Not Rated*) et `UR` (*Unrated*) veulent dire la même chose | `rating` | 80 + 3 | 2.7 |
| **Quasi-doublons** : même titre à la casse près (`Love in a Puff` / `Love In A Puff`, `Consequences` / `Consequences\xa0`…) | `title` | 6 paires | 2.7 |
| Même description pour des versions linguistiques (`Petta` / `Petta (Telugu Version)`) | `description` | 59 | 2.7 |
| Ajouté sur Netflix **avant** l'année de sortie (12 séries, 2 films) | `date_added`, `release_year` | 14 | 2.7 |
| Pays historiques (`West Germany`, `Soviet Union`, `East Germany`) | `country` | quelques-unes | 2.6 / 2.7 |

## 5. Pistes par section

Ce sont des **pistes**, pas des réponses : la décision et sa justification sont à vous, et c'est ce qui est noté.

### 2.1 Texte et espaces · Omotola
- Repérer les colonnes concernées en cherchant explicitement `"  "` (double espace), `"\xa0"` et `"​"` avec `str.contains(..., regex=False)`.
- Piège 1 : avec pandas 3, le texte est stocké par pyarrow, et `\s` dans une expression régulière ne reconnaît **pas** l'espace insécable : une recherche `r"\s$"` passe à côté de `"Consequences\xa0"`. `str.strip()` l'enlève bien en début et fin de texte, mais pas au milieu (`"Legend\xa0of\xa0Exorcism"`) : remplacer `"\xa0"` par `" "`.
- Piège 2 : `str.strip()` n'enlève **pas** l'espace de largeur nulle `"​"`, ni au début ni à la fin. Il faut le supprimer (remplacer par `""`, pas par une espace), sinon `"​Goli Soda 2"` reste un titre différent de `"Goli Soda 2"` et se trie mal.
- Ordre conseillé : remplacer `​` puis `\xa0`, réduire les doubles espaces, puis `strip()`. Vérifier ensuite qu'il ne reste aucun des trois.
- Compter les lignes modifiées : comparer la colonne avant et après (`(avant != apres).sum()`).

### 2.2 Valeurs décalées · Omotola
- Les 3 lignes où `rating` vaut `"xx min"` : la durée est **sûre** (elle a le bon format), on peut la déplacer dans `duration` sans rien inventer.
- Que devient alors `rating` pour ces 3 lignes ? On ne connaît pas la vraie classification : la laisser vide et le dire.
- À faire **avant** 2.4, sinon ces 3 films n'auront pas de durée.

### 2.3 `date_added` · Omotola
- `pd.to_datetime(..., format="%B %d, %Y", errors="coerce")` après `str.strip()`. Préciser le format évite que pandas devine.
- Vérifier que le nombre de dates vides après conversion = nombre de vides avant (10). Si c'est plus, des dates ont échoué : les afficher et comprendre pourquoi.
- Pour l'analyse « par année », ajouter une colonne `annee_ajout` (et éventuellement `mois_ajout`).

### 2.4 `duration` · Omotola
- Une colonne ne peut pas porter deux unités : la découper en `duree_min` (films) et `nb_saisons` (séries), toutes deux de type entier **nullable** `Int64` (qui accepte les vides).
- Vérifier la cohérence avec `type` : aucun film ne doit avoir de saisons, aucune série de minutes (`pd.crosstab`).
- Regarder les extrêmes de `duree_min` (min 3 min, max 312 min) : aberrant ou réel ? Afficher les titres avant de décider.
- Garder ou supprimer l'ancienne colonne `duration` ? À justifier.

### 2.5 Valeurs manquantes · Amen
Trois options pour chaque colonne : **supprimer** la ligne, **imputer** (remplir), **marquer** (laisser vide ou mettre une étiquette explicite). Pour chacune, mesurer combien de lignes seraient perdues.
- `director` : comparer le taux de vides entre films et séries (`pd.crosstab(df["type"], df["director"].isna())`). Imputer un réalisateur inventerait de l'information. Supprimer ferait perdre 30 % du catalogue.
- `country` : imputer avec le pays le plus fréquent (États-Unis) **fausserait** directement l'analyse par pays, qui est le sujet. Expliquer pourquoi on ne le fait pas.
- `cast` : même raisonnement.
- `date_added` (10) et `rating` (4 + 3 de la section 2.2) : très peu de lignes. Supprimer ou garder vide ? Les deux se défendent, il faut juste le dire.
- Si on choisit d'écrire une étiquette (`"Non renseigné"`) plutôt que de laisser vide, expliquer pourquoi, et savoir qu'elle apparaîtra comme un « pays » dans les comptages.

### 2.6 Colonnes à plusieurs valeurs · Amen
- Le problème : `"United States, India"` compte comme **un** pays dans un `value_counts()`. Impossible d'analyser « par pays » ou « par genre » tel quel.
- Outil : `str.split(",")` puis `explode()` puis `str.strip()` donne une ligne par (titre, pays).
- Attention aux 7 pays mal formés (`", South Korea"`, `"United States,"`…) : après `split` + `explode`, ils donnent des pays vides `""` à retirer.
- Proposition : garder dans le CSV principal les listes nettoyées (séparateur `", "` homogène, sans virgule en tête ou en fin ni case vide), et exporter **deux tables longues** à part : `netflix_pays.csv` (`show_id`, `pays`) et `netflix_genres.csv` (`show_id`, `genre`). On justifie : une table par relation, pas de colonnes `pays_1`, `pays_2`… à moitié vides.
- `cast` (36 000 acteurs différents) et `director` : le sujet ne demande pas d'analyse par acteur, on peut les laisser en liste. À dire.
- `listed_in` : 42 genres. Les genres de séries et de films sont distincts (`Dramas` / `TV Dramas`) : les fusionner ou non ? Et les genres génériques `Movies` / `TV Shows` ?

### 2.7 Autres problèmes · Amen
C'est la partie qui montre qu'on a cherché au-delà de la fiche : elle compte.
- `NR` / `UR` : harmoniser en une seule valeur. `TV-Y7-FV` (6 lignes) est une variante de `TV-Y7` : fusionner ou garder ?
- **Quasi-doublons** : comparer les titres en minuscules et sans espaces (`str.lower().str.strip()`). Pour chaque paire, regarder `type`, `director`, `release_year` : `Death Note` (film 2017) et `DEATH NOTE` (série anime) sont deux contenus différents, `Love in a Puff` en double avec le même réalisateur ressemble à un vrai doublon. Décider au cas par cas et l'écrire.
- **Descriptions identiques** : ce sont des versions doublées (Telugu, Tamil…), pas des doublons. Le constater suffit.
- **Ajouté avant la sortie** : 12 des 14 lignes sont des séries. Hypothèse : pour une série, `release_year` est l'année de la **dernière saison**. Garder et documenter, plutôt que corriger.

### 3. État final · à deux
- Recalculer **exactement** les mêmes indicateurs qu'en partie 1, côte à côte avec `brut` : un tableau avant / après (dimensions, types, manquants par colonne).
- Le plus simple est d'écrire en partie 1 une petite fonction (`def etat(d): ...`) qui renvoie le tableau, et de l'appeler sur `brut` puis sur `df` en partie 3.
- Un graphique avant / après des manquants (barres) fait bien dans le PDF et à l'oral.

### 4. Export · à deux
- `df.to_csv(PROPRE, index=False)` + les tables longues si on les fait.
- Relire le fichier avec `pd.read_csv(PROPRE, parse_dates=["date_added"])` et vérifier les types : un CSV ne garde pas les types, il faut le dire.

## 6. Règles d'écriture du notebook

- Chaque correction = **une cellule de code + une cellule « Décision »** avec les trois lignes déjà prévues : ce qui a été fait, pourquoi ce choix plutôt qu'un autre, combien de lignes sont touchées. Le nombre de lignes doit venir d'un `print` du code, pas être tapé à la main.
- Commentaires et textes **en français**. Les noms de colonnes d'origine restent en anglais, les colonnes qu'on crée sont en français (`duree_min`, `annee_ajout`).
- On ne modifie **jamais** `brut`. Tout se fait sur `df`.
- Pas de cellule qui ne marche que si on l'exécute deux fois ou dans le désordre : avant chaque `git push`, **Redémarrer → Exécuter tout**.

## 7. Vérifications avant de rendre

- [ ] Le notebook s'exécute de haut en bas sans erreur, sur les **deux** PC.
- [ ] Aucun `# TODO` ni `…` ne reste dans le notebook.
- [ ] Chaque section 2.x a sa cellule « Décision » remplie, avec un nombre de lignes touchées.
- [ ] Le tableau 1.5 (bilan) est rempli et chaque ligne renvoie à une section 2.x.
- [ ] La partie 3 compare avant / après avec les mêmes indicateurs que la partie 1.
- [ ] `data/processed/netflix_titles_propre.csv` existe et se relit correctement.
- [ ] Le PDF est dans `rapport/` et se lit correctement (tableaux pas coupés, graphiques visibles).
- [ ] Tout est poussé sur GitHub : `git status` ne montre rien en attente.

## 8. Pour l'oral

Une trame de 5 minutes, chacun présente ce qu'il a codé :

1. Le jeu de données et le but de l'analyse (pays, genre, année) · 30 s
2. L'état des lieux : les 3 ou 4 problèmes les plus marquants, chiffres à l'appui · 1 min
3. Les corrections d'Omotola · 1 min 30
4. Les corrections d'Amen, en insistant sur les **choix** (pourquoi on n'impute pas le pays) · 1 min 30
5. Avant / après et ce qu'on ferait avec plus de temps · 30 s

Questions probables : « Pourquoi ne pas avoir supprimé les lignes sans réalisateur ? », « Pourquoi ne pas avoir rempli les pays manquants ? », « Comment avez-vous trouvé les valeurs décalées ? ». Chacun doit pouvoir répondre sur **toutes** les sections, pas seulement les siennes.
