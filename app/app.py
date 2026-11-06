"""
Application Streamlit : Nettoyage du catalogue Netflix.
Binôme 08 : QUENUM Amen et AFOUDA Omotola.
AMA PIIA cohorte 2 (Académie des Mathématiques Appliquées).
Palette sobre :
- Fond principal : blanc cassé #FCFCFB
- Surfaces : gris clair #D5DCDA, gris vert clair #E9F1F0
- Texte : anthracite #252223, texte secondaire gris #6B6664
- Sarcelle foncé #1F6F6E : titres, chiffres clés, accent
- Brique #B23A2E : filets et seconde série
Aucun emoji, aucun caractère U+2014/U+2013, aucune flèche.
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import sys

current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir))

from utils.data_loader import load_all_data, get_summary_metrics
from utils.charts import (
    chart_type_distribution,
    chart_missing_values_comparison,
    chart_top_countries,
    chart_top_genres,
    chart_evolution_annees,
    chart_distribution_duree
)

st.set_page_config(
    page_title="Nettoyage du catalogue Netflix",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        color: #252223;
        background-color: #FCFCFB;
    }
    .stApp {
        background-color: #FCFCFB;
    }
    .main-title {
        color: #1F6F6E;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 4px;
        line-height: 1.2;
    }
    .main-subtitle {
        color: #6B6664;
        font-size: 16px;
        margin-bottom: 20px;
    }
    .kpi-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-color: #FFFFFF;
        border: 1px solid #D5DCDA;
        border-top: 4px solid #1F6F6E;
        border-radius: 6px;
        padding: 14px 10px;
        text-align: center;
        min-height: 125px;
        height: 100%;
    }
    .kpi-number {
        font-size: 56px;
        font-weight: 700;
        color: #1F6F6E;
        line-height: 1.05;
        margin-bottom: 4px;
    }
    .kpi-label {
        font-size: 20px;
        font-weight: 600;
        color: #252223;
        line-height: 1.2;
    }
    .kpi-sub {
        font-size: 15px;
        color: #252223;
        margin-top: 3px;
    }
    .box-accessible {
        background-color: #F2F5F4;
        border-left: 4px solid #1F6F6E;
        padding: 12px 16px;
        border-radius: 4px;
        margin-top: 12px;
        margin-bottom: 12px;
        color: #252223;
        font-size: 15px;
        line-height: 1.5;
    }
    .box-technical {
        background-color: #F2F5F4;
        border-left: 4px solid #B23A2E;
        padding: 12px 16px;
        border-radius: 4px;
        margin-top: 12px;
        margin-bottom: 12px;
        color: #252223;
        font-size: 15px;
        line-height: 1.5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

raw_df, propre_df, pays_df, genres_df = load_all_data()
metrics = get_summary_metrics(raw_df, propre_df, pays_df, genres_df)

with st.sidebar:
    st.markdown("<h3 style='color:#1F6F6E; margin-bottom:2px;'>Catalogue Netflix</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6B6664; font-size:14px; margin-bottom:15px;'>Binôme 08 : QUENUM Amen et AFOUDA Omotola<br>AMA PIIA cohorte 2</p>", unsafe_allow_html=True)

    section = st.radio(
        "Navigation",
        [
            "1. Vue d'ensemble",
            "2. Diagnostic initial",
            "3. Parcours de nettoyage",
            "4. Avant et après",
            "5. Exploration du catalogue",
            "6. Observations sur les données",
            "7. Comprendre la technique"
        ],
        index=0
    )

    st.markdown("<hr style='border:none; border-top:1px solid #D5DCDA; margin:16px 0;'>", unsafe_allow_html=True)
    mode_vue = st.radio(
        "Niveau d'explication",
        [
            "Complet (accessible et technique)",
            "Accessible seul",
            "Technique seul"
        ],
        index=0
    )

show_accessible = mode_vue in ["Complet (accessible et technique)", "Accessible seul"]
show_technical = mode_vue in ["Complet (accessible et technique)", "Technique seul"]

# Colonnes officielles du CSV propre (15 colonnes exactes)
COLS_PROPRE_15 = [
    "show_id", "type", "title", "director", "cast", "country",
    "date_added", "release_year", "rating", "listed_in", "description",
    "annee_ajout", "duree_min", "nb_saisons", "ajout_avant_sortie"
]

# -------------------------------------------------------------
# 1. VUE D'ENSEMBLE
# -------------------------------------------------------------
if section.startswith("1."):
    st.markdown("<div class='main-title'>Nettoyage du catalogue Netflix</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='main-subtitle'>Présentation générale du catalogue et des indicateurs clés après nettoyage.</div>",
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
            <div class='kpi-container'>
                <div class='kpi-number'>8 807</div>
                <div class='kpi-label'>Lignes initiales</div>
                <div class='kpi-sub'>12 colonnes brutes</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class='kpi-container'>
                <div class='kpi-number'>8 800</div>
                <div class='kpi-label'>Lignes finales</div>
                <div class='kpi-sub'>15 colonnes après traitement</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
            <div class='kpi-container'>
                <div class='kpi-number'>7</div>
                <div class='kpi-label'>Lignes supprimées</div>
                <div class='kpi-sub'>0,08 % du volume initial</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
            <div class='kpi-container'>
                <div class='kpi-number'>4 294</div>
                <div class='kpi-label'>Cases marquées</div>
                <div class='kpi-sub'>Texte "Non renseigné"</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("")

    col_g, col_d = st.columns([3, 2])
    with col_g:
        st.plotly_chart(chart_evolution_annees(propre_df), theme=None, width="stretch")
    with col_d:
        st.plotly_chart(chart_type_distribution(propre_df), theme=None, width="stretch")

    if show_accessible:
        st.markdown("""
            <div class='box-accessible'>
                <b>Explication simple :</b><br>
                Le catalogue contient des films et des séries proposés sur Netflix. Au départ, plusieurs informations étaient incomplètes ou mal rangées (durées placées dans la colonne d'âge, espaces invisibles empêchant les recherches, plusieurs pays dans la même case). Nous avons nettoyé l'ensemble sans supprimer de contenu utile, en supprimant uniquement 7 doublons confirmés.
            </div>
        """, unsafe_allow_html=True)

    if show_technical:
        st.markdown("""
            <div class='box-technical'>
                <b>Détails techniques :</b><br>
                Le dataset initial comporte 8 807 lignes et 12 colonnes. Toutes les colonnes de texte étaient stockées en chaînes de caractères (str) et release_year en int64. Le dataset final contient 8 800 lignes et 15 colonnes : nous avons retiré duration (colonne composite) et créé 4 nouvelles colonnes (annee_ajout, duree_min, nb_saisons, ajout_avant_sortie). Les types numériques créés utilisent le type nullable Int64 de pandas.
            </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. DIAGNOSTIC INITIAL
# -------------------------------------------------------------
elif section.startswith("2."):
    st.markdown("<div class='main-title'>Diagnostic de la qualité initiale</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='main-subtitle'>Inventaire des problèmes repérés dans le fichier brut avant toute correction.</div>",
        unsafe_allow_html=True
    )

    t1, t2, t3, t4 = st.tabs([
        "Valeurs manquantes",
        "Espaces et caractères invisibles",
        "Valeurs décalées",
        "Anomalies temporelles et doublons"
    ])

    with t1:
        st.markdown("<b>Valeurs manquantes par colonne (fichier brut) :</b>", unsafe_allow_html=True)
        missing_s = raw_df.isna().sum()
        missing_df = pd.DataFrame({
            "Colonne": missing_s.index,
            "Valeurs manquantes": missing_s.values,
            "Pourcentage": (missing_s.values / len(raw_df) * 100).round(2)
        })
        missing_df["Pourcentage"] = missing_df["Pourcentage"].apply(lambda p: f"{p:.2f} %".replace(".", ","))
        st.dataframe(missing_df[missing_df["Valeurs manquantes"] > 0], width="stretch", hide_index=True)

        if show_accessible:
            st.markdown("""
                <div class='box-accessible'>
                    <b>Explication simple :</b><br>
                    Près de 30 % des réalisateurs sont absents (2 634 cases). Ce n'est pas un oubli : dans une série télévisée, il n'y a généralement pas un réalisateur unique pour toute la série, mais plusieurs selon les épisodes. Supprimer ces lignes aurait supprimé 91 % des séries.
                </div>
            """, unsafe_allow_html=True)

        if show_technical:
            st.markdown("""
                <div class='box-technical'>
                    <b>Détails techniques :</b><br>
                    6 colonnes présentent des valeurs manquantes au départ : director (2 634), country (831), cast (825), date_added (10), rating (4) et duration (3), soit 4 307 cases vides au total. Imputer le mode sur country (les États-Unis) aurait créé un biais majeur sur 831 lignes.
                </div>
            """, unsafe_allow_html=True)

    with t2:
        st.markdown("<b>Espaces superflus et caractères invisibles :</b>", unsafe_allow_html=True)
        st.markdown("""
        - <b>Espaces au début ou à la fin :</b> 89 cases (date_added 88, title 1).<br>
        - <b>Caractères invisibles :</b> 20 cases au total, dont 14 espaces insécables (title 5, description 9) et 6 espaces de largeur nulle (title 5, cast 1).<br>
        - <b>Doubles espaces :</b> 16 cases (title 3, cast 7, description 6).
        """, unsafe_allow_html=True)

        if show_accessible:
            st.markdown("""
                <div class='box-accessible'>
                    <b>Explication simple :</b><br>
                    Un titre comme "Goli Soda 2" commençait par un caractère totalement invisible à l'écran. Si un utilisateur tapait le nom du film dans une barre de recherche, le film n'apparaissait pas car l'ordinateur considérait que les deux textes étaient différents.
                </div>
            """, unsafe_allow_html=True)

        if show_technical:
            st.markdown("""
                <div class='box-technical'>
                    <b>Détails techniques :</b><br>
                    Les fonctions classiques comme str.strip() ne retirent ni l'espace de largeur nulle (\\u200b) ni l'espace insécable (\\xa0) situé au milieu d'une chaîne. Il a fallu combiner str.replace avec regex=False avant de réduire les espaces multiples.
                </div>
            """, unsafe_allow_html=True)

    with t3:
        st.markdown("<b>Les trois spectacles de Louis C.K. (valeurs décalées) :</b>", unsafe_allow_html=True)
        shifted_ids = ["s5542", "s5795", "s5814"]
        st.dataframe(raw_df[raw_df["show_id"].isin(shifted_ids)][["show_id", "title", "rating", "duration"]], width="stretch", hide_index=True)

        if show_accessible:
            st.markdown("""
                <div class='box-accessible'>
                    <b>Explication simple :</b><br>
                    Pour ces trois spectacles, la durée ("74 min", "84 min", "66 min") s'est retrouvée par erreur dans la colonne rating (classification d'âge), et la colonne duration était vide.
                </div>
            """, unsafe_allow_html=True)

        if show_technical:
            st.markdown("""
                <div class='box-technical'>
                    <b>Détails techniques :</b><br>
                    La durée a été déplacée de rating vers duration. rating a été laissé vide puis qualifié en "Non renseigné" en section 2.5 car la classification d'origine est inconnue dans le fichier.
                </div>
            """, unsafe_allow_html=True)

    with t4:
        st.markdown("<b>Anomalies de dates et quasi-doublons :</b>", unsafe_allow_html=True)
        st.markdown("""
        - <b>14 titres ajoutés avant leur année de sortie :</b> 12 séries et 2 films.<br>
        - <b>Quasi-doublons :</b> 6 paires de titres identiques si on ne tient pas compte de la casse.<br>
        - <b>Titres abîmés par Excel :</b> 4 titres transformés en dates par Excel (Feb-09, 22-Jul, 15-Aug, Oct-01).
        """)

        if show_accessible:
            st.markdown("""
                <div class='box-accessible'>
                    <b>Explication simple :</b><br>
                    Parmi les 6 paires de titres qui semblaient identiques, certaines étaient de vrais doublons (comme Love In A Puff présent deux fois avec le même réalisateur), tandis que d'autres correspondaient à deux œuvres distinctes (comme Death Note qui existe à la fois en film et en série d'animation).
                </div>
            """, unsafe_allow_html=True)

        if show_technical:
            st.markdown("""
                <div class='box-technical'>
                    <b>Détails techniques :</b><br>
                    Pour les 14 titres dont l'année d'ajout est inférieure à release_year, l'hypothèse testée est que release_year représente l'année de la dernière saison. Cette hypothèse tient pour 8 séries sur 12 (qui comptent plus d'une saison, comme Arrested Development, BoJack Horseman ou Fuller House). Elle n'explique en revanche ni les 4 séries d'une saison ni les 2 films.
                </div>
            """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 3. PARCOURS DE NETTOYAGE
# -------------------------------------------------------------
elif section.startswith("3."):
    st.markdown("<div class='main-title'>Parcours de nettoyage méthodologique</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='main-subtitle'>Les étapes de nettoyage réalisées, les extraits du notebook et les justifications associées.</div>",
        unsafe_allow_html=True
    )

    st.markdown("### Travail réalisé par Omotola (sections 2.1 à 2.4)")

    with st.expander("Section 2.1 : Espaces superflus et texte à harmoniser"):
        st.markdown("**Extrait du notebook :**")
        st.code(r"""texte = df.select_dtypes(exclude="number").columns
avant = df[texte].copy()

for col in texte:
    df[col] = (
        df[col]
        .str.replace("\u200b", "", regex=False)
        .str.replace("\xa0", " ", regex=False)
        .str.replace(r" {2,}", " ", regex=True)
        .str.strip()
    )""", language="python")
        st.markdown("**Décision et justification :** On nettoie toutes les colonnes texte d'un coup. Remplacer `\\u200b` par rien et `\\xa0` par un espace standard règle les problèmes invisibles.")

    with st.expander("Section 2.2 : Valeurs décalées entre colonnes"):
        st.markdown("**Extrait du notebook :**")
        st.code("""decalees = df["rating"].str.contains("min", na=False)

df.loc[decalees, "duration"] = df.loc[decalees, "rating"]
df.loc[decalees, "rating"] = np.nan""", language="python")
        st.markdown("**Décision et justification :** La durée est sûre pour les 3 spectacles de Louis C.K. On la remet dans duration et on laisse rating vide pour ne pas inventer de classification.")

    with st.expander("Section 2.3 : Date d'ajout (date_added)"):
        st.markdown("**Extrait du notebook :**")
        st.code("""df["date_added"] = pd.to_datetime(df["date_added"], format="%B %d, %Y", errors="coerce")
df["annee_ajout"] = df["date_added"].dt.year.astype("Int64")""", language="python")
        st.markdown("**Décision et justification :** Conversion en datetime pour permettre des analyses temporelles. Les 10 dates vides restent vides. On extrait annee_ajout pour les tris par année.")

    with st.expander("Section 2.4 : Durée (duration)"):
        st.markdown("**Extrait du notebook :**")
        st.code(r"""parties = df["duration"].str.extract(r"^(\d+) (min|Seasons?)$")
nombre = pd.to_numeric(parties[0]).astype("Int64")
unite = parties[1]

df["duree_min"] = nombre.where(unite == "min")
df["nb_saisons"] = nombre.where(unite.isin(["Season", "Seasons"]))
df = df.drop(columns="duration")""", language="python")
        st.markdown("**Décision et justification :** Une colonne ne peut pas porter deux unités. On sépare en duree_min pour les films et nb_saisons pour les séries, toutes deux en Int64 nullable.")

    st.markdown("### Travail réalisé par Amen (sections 2.5 à 2.7)")

    with st.expander("Section 2.5 : Valeurs manquantes"):
        st.markdown("**Extrait du notebook :**")
        st.code("""cols = ["director", "cast", "country"]
df[cols] = df[cols].fillna("Non renseigné")
df["rating"] = df["rating"].fillna("Non renseigné")""", language="python")
        st.markdown("**Décision et justification :** On ne supprime aucune ligne. Imputer par le pays le plus fréquent fausserait l'analyse par pays. On remplace par l'étiquette explicite 'Non renseigné'.")

    with st.expander("Section 2.6 : Colonnes à plusieurs valeurs (tables longues)"):
        st.markdown("**Extrait du notebook :**")
        st.code("""def table_longue(d, colonne, nom):
    t = d[["show_id", colonne]].dropna()
    t = t.assign(**{nom: t[colonne].str.split(", ")}).explode(nom)
    return t[["show_id", nom]].query(f"{nom} != 'Non renseigné'").reset_index(drop=True)

df_pays = table_longue(df, "country", "pays")
df_genres = table_longue(df, "listed_in", "genre")""", language="python")
        st.markdown("**Décision et justification :** Une case avec plusieurs pays empêche un comptage exact. La table longue permet d'avoir une ligne par couple (titre, pays) et (titre, genre).")

    with st.expander("Section 2.7 : Autres problèmes (doublons et harmonisation)"):
        st.markdown("**Extrait du notebook :**")
        st.code(r"""# Harmonisation des classifications
df["rating"] = df["rating"].replace("UR", "NR")

# Suppression des vrais doublons confirmés
df = (df.assign(_titre=df["title"].str.lower())
        .sort_values("date_added", kind="stable", na_position="first")
        .drop_duplicates(["_titre", "type", "release_year"], keep="last")
        .drop(columns="_titre")
        .sort_index())

# Suppression des 3 titres abîmés par Excel ayant un jumeau
abimes = df["title"].str.match(r"^\d{1,2}-[A-Z][a-z]{2}$|^[A-Z][a-z]{2}-\d{2}$")
autres_colonnes = [c for c in df.columns if c not in ["show_id", "title"]]
a_un_jumeau = df.duplicated(autres_colonnes, keep=False)
a_supprimer = df.loc[abimes & a_un_jumeau, "show_id"].tolist()
df = df[~df["show_id"].isin(a_supprimer)]

# Correction du quatrième titre abîmé
df.loc[df["title"] == "Oct-01", "title"] = "October 1"

# Signalement des titres ajoutés avant leur année de sortie
df["ajout_avant_sortie"] = (df["annee_ajout"] < df["release_year"]).fillna(False).astype(bool)""", language="python")
        st.markdown("**Décision et justification :** UR et NR signifient tous deux non classé (3 lignes modifiées). On ne supprime que 7 lignes au total : 4 vrais doublons et 3 titres abîmés par Excel ayant déjà leur jumeau correct.")

    if show_accessible:
        st.markdown("""
            <div class='box-accessible'>
                <b>En résumé :</b><br>
                Chaque décision a été pesée pour éviter toute perte inutile. Au final, 99,92 % des contenus du catalogue ont été conservés.
            </div>
        """, unsafe_allow_html=True)

    if show_technical:
        st.markdown("""
            <div class='box-technical'>
                <b>Rappel méthodologique :</b><br>
                Le notebook applique la règle d'or : mesurer la perte avant toute suppression. Seules les 7 lignes constituant des doublons avérés ont été retirées.
            </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 4. AVANT ET APRÈS
# -------------------------------------------------------------
elif section.startswith("4."):
    st.markdown("<div class='main-title'>Comparatif avant et après nettoyage</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='main-subtitle'>Les indicateurs de la section 3.3 du notebook calculés directement depuis les fichiers CSV.</div>",
        unsafe_allow_html=True
    )

    texte_raw = raw_df.select_dtypes(include="object").columns
    texte_propre = propre_df[COLS_PROPRE_15].select_dtypes(include="object").columns

    def count_raw(motif):
        return int(sum(raw_df[c].str.contains(motif, regex=False, na=False).sum() for c in texte_raw))

    def count_propre(motif):
        return int(sum(propre_df[c].str.contains(motif, regex=False, na=False).sum() for c in texte_propre))

    espaces_bords_raw = int(sum((raw_df[c].notna() & (raw_df[c].str.strip() != raw_df[c])).sum() for c in texte_raw))
    espaces_bords_propre = int(sum((propre_df[c].notna() & (propre_df[c].str.strip() != propre_df[c])).sum() for c in texte_propre))

    ind_data = [
        {"Indicateur": "Dimensions du jeu de données", "Avant nettoyage": f"{raw_df.shape[0]:,} lignes x {raw_df.shape[1]} colonnes".replace(",", " "), "Après nettoyage": f"{propre_df.shape[0]:,} lignes x {len(COLS_PROPRE_15)} colonnes".replace(",", " ")},
        {"Indicateur": "Doublons stricts", "Avant nettoyage": str(int(raw_df.duplicated().sum())), "Après nettoyage": str(int(propre_df[COLS_PROPRE_15].duplicated().sum()))},
        {"Indicateur": "Titres en double (casse et espaces ignorés)", "Avant nettoyage": str(int(raw_df["title"].str.lower().str.strip().duplicated().sum())), "Après nettoyage": str(int(propre_df["title"].str.lower().str.strip().duplicated().sum()))},
        {"Indicateur": "Textes avec un espace au début ou à la fin", "Avant nettoyage": str(espaces_bords_raw), "Après nettoyage": str(espaces_bords_propre)},
        {"Indicateur": "Textes avec un espace insécable", "Avant nettoyage": str(count_raw("\xa0")), "Après nettoyage": str(count_propre("\xa0"))},
        {"Indicateur": "Textes avec un espace de largeur nulle", "Avant nettoyage": str(count_raw("\u200b")), "Après nettoyage": str(count_propre("\u200b"))},
        {"Indicateur": "Textes avec un double espace", "Avant nettoyage": str(count_raw("  ")), "Après nettoyage": str(count_propre("  "))},
        {"Indicateur": "Durées rangées dans rating", "Avant nettoyage": str(int(raw_df["rating"].str.contains("min", na=False).sum())), "Après nettoyage": str(int(propre_df["rating"].str.contains("min", na=False).sum()))},
        {"Indicateur": "Durées manquantes", "Avant nettoyage": str(int(raw_df["duration"].isna().sum())), "Après nettoyage": "0 (duree_min / nb_saisons)"},
        {"Indicateur": "Classifications UR (harmonisées vers NR)", "Avant nettoyage": str(int((raw_df["rating"] == "UR").sum())), "Après nettoyage": str(int((propre_df["rating"] == "UR").sum()))},
        {"Indicateur": "Pays avec une virgule en trop", "Avant nettoyage": str(int(raw_df["country"].str.contains(r"^,|,$", na=False).sum())), "Après nettoyage": str(int(propre_df["country"].str.contains(r"^,|,$", na=False).sum()))},
        {"Indicateur": "Titres abîmés par Excel", "Avant nettoyage": str(int(raw_df["title"].str.match(r"^\d{1,2}-[A-Z][a-z]{2}$|^[A-Z][a-z]{2}-\d{2}$").sum())), "Après nettoyage": str(int(propre_df["title"].str.match(r"^\d{1,2}-[A-Z][a-z]{2}$|^[A-Z][a-z]{2}-\d{2}$").sum()))},
        {"Indicateur": "Titres associés aux États-Unis", "Avant nettoyage": "2 818 (brut sans découpage)", "Après nettoyage": "3 688 (table découpée)"}
    ]

    df_tableau_bilan = pd.DataFrame(ind_data)
    # Hauteur réglée pour voir les 13 lignes d'un seul coup sans défilement
    st.dataframe(df_tableau_bilan, height=510, width="stretch", hide_index=True)

    st.write("")
    st.plotly_chart(chart_missing_values_comparison(raw_df, propre_df), theme=None, width="stretch")

    st.markdown("<b>Aperçu du fichier final (15 colonnes exactes) :</b>", unsafe_allow_html=True)
    st.dataframe(propre_df[COLS_PROPRE_15].head(5), width="stretch", hide_index=True)

    if show_accessible:
        st.markdown("""
            <div class='box-accessible'>
                <b>Lecture des résultats :</b><br>
                Tous les problèmes de formatage et de doublons sont tombés à zéro, sauf un : il reste 2 titres en double (Death Note et Fullmetal Alchemist). C'est normal et souhaité : il s'agit à chaque fois d'un film et d'une série qui portent le même titre.
            </div>
        """, unsafe_allow_html=True)

    if show_technical:
        st.markdown("""
            <div class='box-technical'>
                <b>Bilan des données manquantes :</b><br>
                Le fichier initial comptait 4 307 cases vides. À l'arrivée, 4 294 cases portent l'étiquette 'Non renseigné' et 10 dates sont vides. L'écart s'explique exactement ainsi : 3 cases vides sont parties avec les 7 lignes supprimées, 3 classifications rating ont été vidées (les spectacles de Louis C.K.) et 3 durées manquantes ont été récupérées depuis rating.
            </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 5. EXPLORATION DU CATALOGUE
# -------------------------------------------------------------
elif section.startswith("5."):
    st.markdown("<div class='main-title'>Exploration interactive du catalogue</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='main-subtitle'>Filtrez par type, année et pays : les graphiques et le tableau s'adaptent instantanément.</div>",
        unsafe_allow_html=True
    )

    f1, f2, f3 = st.columns(3)
    with f1:
        type_options = ["Films", "Séries"]
        selected_types = st.multiselect(
            "Type de contenu",
            options=type_options,
            default=type_options,
            placeholder="Choisir un ou plusieurs types"
        )
    with f2:
        y_min = int(propre_df["release_year"].min())
        y_max = int(propre_df["release_year"].max())
        selected_years = st.slider(
            "Années de sortie (par défaut toute la période)",
            min_value=y_min,
            max_value=y_max,
            value=(y_min, y_max)
        )
    with f3:
        liste_top_pays = pays_df["pays"].value_counts().head(25).index.tolist()
        selected_pays = st.multiselect(
            "Filtrer par pays (parmi les 25 premiers)",
            options=liste_top_pays,
            placeholder="Choisir des pays"
        )

    # Application des filtres
    type_map = {"Films": "Movie", "Séries": "TV Show"}
    types_filtres = [type_map[t] for t in selected_types]

    filtered_df = propre_df[
        (propre_df["type"].isin(types_filtres)) &
        (propre_df["release_year"] >= selected_years[0]) &
        (propre_df["release_year"] <= selected_years[1])
    ]

    if selected_pays:
        ids_pays = pays_df[pays_df["pays"].isin(selected_pays)]["show_id"].unique()
        filtered_df = filtered_df[filtered_df["show_id"].isin(ids_pays)]

    # Filtrer pays_df et genres_df sur les show_id de filtered_df pour que les tops suivent les filtres
    valid_ids = set(filtered_df["show_id"])
    filtered_pays_df = pays_df[pays_df["show_id"].isin(valid_ids)]
    filtered_genres_df = genres_df[genres_df["show_id"].isin(valid_ids)]

    st.markdown(
        f"<b>Titres correspondants aux filtres :</b> {len(filtered_df):,} sur {len(propre_df):,}".replace(",", " "),
        unsafe_allow_html=True
    )

    c_g1, c_g2 = st.columns(2)
    with c_g1:
        st.plotly_chart(chart_top_countries(filtered_pays_df, top_n=10), theme=None, width="stretch")
    with c_g2:
        st.plotly_chart(chart_top_genres(filtered_genres_df, top_n=10), theme=None, width="stretch")

    st.plotly_chart(chart_distribution_duree(filtered_df), theme=None, width="stretch")

    with st.expander("Voir le tableau des données filtrées"):
        cols_a_voir = ["show_id", "type", "title", "country", "release_year", "date_added", "duree_min", "nb_saisons", "rating"]
        st.dataframe(filtered_df[cols_a_voir], width="stretch", hide_index=True)

    if show_accessible:
        st.markdown("""
            <div class='box-accessible'>
                <b>Astuce :</b><br>
                Vous pouvez sélectionner la France seule pour observer les genres dominants de la production française, ou isoler les séries pour constater que deux tiers (67,0 %) ne comptent qu'une seule saison.
            </div>
        """, unsafe_allow_html=True)

    if show_technical:
        st.markdown("""
            <div class='box-technical'>
                <b>Fonctionnement du filtre relationnel :</b><br>
                Le filtrage croise la table principale df et les deux tables relationnelles découpées via l'identifiant technique show_id. Les classements Top pays et Top genres sont recalculés dynamiquement à partir des show_id conservés.
            </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 6. OBSERVATIONS SUR LES DONNÉES
# -------------------------------------------------------------
elif section.startswith("6."):
    st.markdown("<div class='main-title'>Observations tirées des données</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='main-subtitle'>Constats chiffrés et analyses tirées du catalogue une fois nettoyé.</div>",
        unsafe_allow_html=True
    )

    o1, o2 = st.columns(2)
    with o1:
        st.markdown("""
        <b>1. Rythme des ajouts sur la plateforme :</b><br>
        - Moins de 100 ajouts par an jusqu'en 2015.<br>
        - 2018 : 1 646 titres ajoutés.<br>
        - 2019 : 2 012 titres ajoutés (seule année à dépasser 2 000 ajouts).<br>
        - 2020 : 1 879 titres ajoutés.<br>
        - Les données de 2021 s'arrêtent au 25 septembre (1 498 ajouts).
        <br><br>
        <b>2. Répartition par type de contenu :</b><br>
        - Films : 6 126 titres (69,6 %).<br>
        - Séries : 2 674 titres (30,4 %).
        """, unsafe_allow_html=True)

    with o2:
        st.markdown("""
        <b>3. Durée et formats :</b><br>
        - Durée médiane des films : 98 minutes.<br>
        - 54,2 % des films durent entre 85 et 115 minutes (3 319 films sur 6 126).<br>
        - Durées extrêmes observées : de 3 minutes à 312 minutes.<br>
        - 67,0 % des séries télévisées n'ont qu'une seule saison (1 792 sur 2 674).
        <br><br>
        <b>4. Les pays les plus représentés :</b><br>
        - États-Unis : 3 688 titres (36,9 % des associations titre-pays).<br>
        - Inde : 1 045 titres (10,4 %).<br>
        - Royaume-Uni : 806 titres (8,1 %).<br>
        - Canada : 445 titres, France : 393 titres.
        """, unsafe_allow_html=True)

    if show_accessible:
        st.markdown("""
            <div class='box-accessible'>
                <b>Ce qu'on retient :</b><br>
                Le catalogue s'est surtout développé à partir de 2016. Deux tiers des séries ne comptent qu'une seule saison, et un peu plus de la moitié des films s'inscrivent dans une durée standard comprise entre 1 h 25 et 1 h 55.
            </div>
        """, unsafe_allow_html=True)

    if show_technical:
        st.markdown("""
            <div class='box-technical'>
                <b>Précision statistique :</b><br>
                L'hypothèse selon laquelle release_year correspond à l'année de la dernière saison tient pour 8 des 12 séries (celles qui comptent plusieurs saisons comme Arrested Development, BoJack Horseman et Fuller House), mais elle n'explique ni les 4 séries d'une saison ni les 2 films.
            </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 7. COMPRENDRE LA TECHNIQUE
# -------------------------------------------------------------
elif section.startswith("7."):
    st.markdown("<div class='main-title'>Comprendre la technique</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='main-subtitle'>Explications pédagogiques des choix techniques et des méthodes Pandas utilisées.</div>",
        unsafe_allow_html=True
    )

    with st.expander("1. Pourquoi avoir séparé pays et genres en tables longues plutôt qu'imputer ?"):
        st.markdown("""
        Imputer les 831 pays manquants par les États-Unis aurait artificiellement gonflé la part américaine. De plus, un titre coproduit comme "United States, India" était considéré comme un seul texte.
        La fonction `table_longue()` utilise `.explode()` pour créer une ligne par association. Cela permet de compter les États-Unis de façon exacte : 3 688 associations au total.
        """)

    with st.expander("2. Pourquoi les comptages des États-Unis indiquent 3 690 en section 2.6 puis 3 688 en section 3.4 ?"):
        st.markdown("""
        En section 2.6, la table longue préliminaire tourne sur le tableau avant suppressions (8 807 lignes).
        En section 2.7, nous supprimons 7 lignes (4 vrais doublons et 3 titres abîmés par Excel).
        Deux des lignes supprimées comprenaient les États-Unis :
        - `s5966` ("22-Jul", doublon du film "22 July", coproduction Norvège, Islande, États-Unis)
        - `s8023` ("Sin Senos sí Hay Paraíso", série coproduite par États-Unis et Colombie)
        Le recalcul donne exactement en section 3.4 : 3 690 - 2 = 3 688. Le chiffre final est parfaitement exact.
        """)

    with st.expander("3. Pourquoi utiliser le type Int64 au lieu de int standard pour duree_min ?"):
        st.markdown("""
        En Python et avec NumPy standard, un type entier ne supporte pas les valeurs manquantes. Si une colonne d'entiers contient un vide, Pandas convertit automatiquement toute la colonne en nombres décimaux (float64), affichant des valeurs comme `90.0`.
        Le type `Int64` (avec un I majuscule) est un type d'extension Pandas qui gère le marqueur `&lt;NA&gt;` tout en conservant des entiers stricts.
        """)

    with st.expander("4. Que penser de l'hypothèse sur les 14 titres ajoutés avant leur sortie ?"):
        st.markdown("""
        L'hypothèse selon laquelle release_year correspond à l'année de la dernière saison est une hypothèse du notebook. Elle tient pour 8 des 12 séries (qui comptent plusieurs saisons comme Arrested Development, BoJack Horseman et Fuller House), mais elle n'explique ni les 4 séries d'une saison ni les 2 films. Le fichier seul ne permet pas de trancher quelle date est exacte.
        De plus, pour les 10 séries sans date d'ajout, l'instruction `fillna(False)` masque l'incertitude : une date inconnue ne signifie pas qu'il n'y a pas d'anomalie, elle rend simplement l'anomalie non vérifiable.
        """)

    if show_accessible:
        st.markdown("""
            <div class='box-accessible'>
                <b>À retenir pour la présentation :</b><br>
                Nous avons privilégié la clarté et la transparence : aucune donnée n'a été inventée, chaque suppression est justifiée, et les limites du fichier sont documentées.
            </div>
        """, unsafe_allow_html=True)

    if show_technical:
        st.markdown("""
            <div class='box-technical'>
                <b>Synthèse d'ingénierie :</b><br>
                Le code final utilise des méthodes robustes : sélection par types de données, normalisation textuelle ordonnée, typage nullable et structuration relationnelle en première forme normale.
            </div>
        """, unsafe_allow_html=True)
