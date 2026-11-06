"""
Module de chargement et de préparation des données pour le Streamlit Dashboard
Nettoyage du catalogue Netflix.
"""

from pathlib import Path
import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
RAW_FILE = DATA_DIR / "raw" / "netflix_titles.csv"
PROPRE_FILE = DATA_DIR / "processed" / "netflix_titles_propre.csv"
PAYS_FILE = DATA_DIR / "processed" / "netflix_pays.csv"
GENRES_FILE = DATA_DIR / "processed" / "netflix_genres.csv"


@st.cache_data
def load_all_data():
    """Charge l'ensemble des jeux de données avec mise en cache Streamlit."""
    raw_df = pd.read_csv(RAW_FILE)
    propre_df = pd.read_csv(PROPRE_FILE)
    pays_df = pd.read_csv(PAYS_FILE)
    genres_df = pd.read_csv(GENRES_FILE)

    # Conversion de date_added en datetime si pas encore fait
    propre_df["date_added_dt"] = pd.to_datetime(propre_df["date_added"], errors="coerce")
    
    # Indicateur ternaire pour anomalie temporelle (règle le biais de la date d'ajout manquante)
    # True = Anomalie avérée (annee_ajout < release_year)
    # False = Vérifié et conforme (annee_ajout >= release_year)
    # 'Indéterminé' = Date d'ajout inconnue (10 lignes)
    propre_df["statut_temporalite"] = "Conforme"
    propre_df.loc[propre_df["date_added"].isna(), "statut_temporalite"] = "Non vérifiable (date inconnue)"
    propre_df.loc[
        propre_df["date_added"].notna() & (propre_df["annee_ajout"] < propre_df["release_year"]),
        "statut_temporalite"
    ] = "Anomalie temporelle"

    return raw_df, propre_df, pays_df, genres_df


def get_summary_metrics(raw_df, propre_df, pays_df, genres_df):
    """Calcule les indicateurs clés globaux pour la vue d'ensemble."""
    nb_lignes_raw = len(raw_df)
    nb_lignes_propre = len(propre_df)
    lignes_supprimees = nb_lignes_raw - nb_lignes_propre
    
    # Calcul des valeurs manquantes initiales brutes vs remplacées
    missing_raw = raw_df.isna().sum().sum()
    
    # Nombre de "Non renseigné"
    non_renseigne_count = 0
    for col in ["director", "cast", "country", "rating"]:
        if col in propre_df.columns:
            non_renseigne_count += (propre_df[col] == "Non renseigné").sum()
            
    dates_manquantes = int(propre_df["date_added"].isna().sum())
    anomalies_temp = int((propre_df["statut_temporalite"] == "Anomalie temporelle").sum())
    nb_pays_uniques = pays_df["pays"].nunique()
    nb_genres_uniques = genres_df["genre"].nunique()
    
    return {
        "nb_lignes_raw": nb_lignes_raw,
        "nb_colonnes_raw": raw_df.shape[1],
        "nb_lignes_propre": nb_lignes_propre,
        "nb_colonnes_propre": propre_df.shape[1],
        "lignes_supprimees": lignes_supprimees,
        "missing_raw": missing_raw,
        "non_renseigne_count": non_renseigne_count,
        "dates_manquantes": dates_manquantes,
        "anomalies_temp": anomalies_temp,
        "nb_assoc_pays": len(pays_df),
        "nb_assoc_genres": len(genres_df),
        "nb_pays_uniques": nb_pays_uniques,
        "nb_genres_uniques": nb_genres_uniques,
        "films_count": int((propre_df["type"] == "Movie").sum()),
        "series_count": int((propre_df["type"] == "TV Show").sum()),
    }
