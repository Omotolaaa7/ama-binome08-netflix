"""
Module de génération des graphiques interactifs Plotly.
Nouvelle palette :
- Fond principal : blanc cassé #FCFCFB
- Texte : anthracite #252223, texte secondaire gris #6B6664
- Sarcelle foncé #1F6F6E : titres, chiffres clés, série principale
- Brique #B23A2E : seconde série et filets
- Gris #6B6664 : troisième série
- gris clair #D5DCDA et gris vert clair #E9F1F0 : touches de fond seulement
Police : Segoe UI. Aucun emoji, aucun U+2014/U+2013, aucune flèche.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

COLOR_BG = "#FCFCFB"
COLOR_TEXT = "#252223"
COLOR_MUTED = "#6B6664"
COLOR_ACCENT = "#1F6F6E"
COLOR_SECOND = "#B23A2E"
COLOR_THIRD = "#6B6664"
COLOR_GRID = "rgba(107, 102, 100, 0.15)"

THEME_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=COLOR_TEXT, family="Segoe UI, sans-serif", size=16),
    title_font=dict(size=18, color=COLOR_ACCENT, family="Segoe UI, sans-serif"),
    legend=dict(
        bgcolor="rgba(252, 252, 251, 0.95)",
        borderwidth=0,
        font=dict(color=COLOR_TEXT, size=15)
    ),
    # automargin évite que les noms de pays et de genres soient coupés à gauche
    template=go.layout.Template(layout=dict(
        xaxis=dict(automargin=True, title_standoff=14),
        yaxis=dict(automargin=True, title_standoff=14),
    )),
    margin=dict(l=40, r=40, t=50, b=40),
)


def chart_type_distribution(propre_df):
    """Diagramme circulaire de la répartition Films et Séries."""
    if propre_df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="Aucune donnée à afficher.",
            showarrow=False,
            font=dict(size=16, color=COLOR_MUTED)
        )
        fig.update_layout(**THEME_LAYOUT, title="Répartition films et séries")
        return fig

    n_films = int((propre_df["type"] == "Movie").sum())
    n_series = int((propre_df["type"] == "TV Show").sum())
    total = n_films + n_series

    pct_films = (n_films / total * 100) if total > 0 else 0
    pct_series = (n_series / total * 100) if total > 0 else 0

    labels = [
        f"Films ({str(round(pct_films, 1)).replace('.', ',')} %)",
        f"Séries ({str(round(pct_series, 1)).replace('.', ',')} %)"
    ]
    values = [n_films, n_series]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.55,
                marker=dict(
                    colors=[COLOR_ACCENT, COLOR_SECOND],
                    line=dict(color=COLOR_BG, width=2)
                ),
                textinfo="none",
                hoverinfo="label+value",
            )
        ]
    )
    fig.update_layout(
        **THEME_LAYOUT,
        title="Répartition films et séries",
        showlegend=True,
    )
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig


def chart_missing_values_comparison(raw_df, propre_df):
    """Comparatif des valeurs manquantes entre brut et nettoyé."""
    cols_vides = ["director", "country", "cast", "date_added", "rating", "duration"]
    raw_missing = raw_df.isna().sum()

    data = []
    for col in cols_vides:
        nb_raw = int(raw_missing.get(col, 0))
        if col in propre_df.columns:
            nb_propre_nan = int(propre_df[col].isna().sum())
            nb_propre_marques = int((propre_df[col] == "Non renseigné").sum())
        else:
            nb_propre_nan = 0
            nb_propre_marques = 0

        data.append({
            "Colonne": col,
            "Brut (cases vides)": nb_raw,
            "Nettoyé (Non renseigné)": nb_propre_marques,
            "Nettoyé (dates vides)": nb_propre_nan
        })

    df_plot = pd.DataFrame(data)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_plot["Colonne"],
        y=df_plot["Brut (cases vides)"],
        name="Brut (cases vides)",
        marker_color=COLOR_MUTED,
        text=df_plot["Brut (cases vides)"],
        textposition="outside",
        textfont=dict(size=14, color=COLOR_TEXT)
    ))
    fig.add_trace(go.Bar(
        x=df_plot["Colonne"],
        y=df_plot["Nettoyé (Non renseigné)"],
        name="Nettoyé (Non renseigné)",
        marker_color=COLOR_ACCENT,
        text=df_plot["Nettoyé (Non renseigné)"],
        textposition="outside",
        textfont=dict(size=14, color=COLOR_TEXT)
    ))
    fig.add_trace(go.Bar(
        x=df_plot["Colonne"],
        y=df_plot["Nettoyé (dates vides)"],
        name="Nettoyé (dates vides)",
        marker_color=COLOR_SECOND,
        text=df_plot["Nettoyé (dates vides)"],
        textposition="outside",
        textfont=dict(size=14, color=COLOR_TEXT)
    ))

    fig.update_layout(
        **THEME_LAYOUT,
        barmode="group",
        title="Données manquantes : brut vs nettoyé",
        xaxis=dict(title="Colonne", gridcolor=COLOR_GRID, linecolor=COLOR_MUTED),
        yaxis=dict(title="Nombre de valeurs", gridcolor=COLOR_GRID, linecolor=COLOR_MUTED),
    )
    return fig


def chart_top_countries(pays_df, top_n=10):
    """Top pays producteurs sur la table filtrée."""
    if pays_df.empty or "pays" not in pays_df.columns:
        fig = go.Figure()
        fig.add_annotation(
            text="Aucun pays pour la sélection en cours.",
            showarrow=False,
            font=dict(size=16, color=COLOR_MUTED)
        )
        fig.update_layout(**THEME_LAYOUT, title=f"Top {top_n} des pays producteurs", xaxis_visible=False, yaxis_visible=False)
        return fig

    top_p = pays_df["pays"].value_counts().head(top_n).reset_index()
    top_p.columns = ["Pays", "Titres"]
    top_p = top_p.sort_values("Titres", ascending=True)

    fig = go.Figure(
        go.Bar(
            x=top_p["Titres"],
            y=top_p["Pays"],
            orientation="h",
            marker=dict(color=COLOR_ACCENT),
            text=top_p["Titres"].apply(lambda v: f"{v:,}".replace(",", " ")),
            textposition="outside",
            textfont=dict(size=15, color=COLOR_TEXT)
        )
    )
    max_val = max(top_p["Titres"]) if not top_p.empty else 100
    fig.update_layout(
        **THEME_LAYOUT,
        title=f"Top {top_n} des pays producteurs",
        xaxis=dict(
            title="Nombre de titres associés",
            range=[0, max_val * 1.18],
            gridcolor=COLOR_GRID,
            linecolor=COLOR_MUTED
        ),
        yaxis=dict(title="Pays", gridcolor=COLOR_GRID, linecolor=COLOR_MUTED),
    )
    return fig


def chart_top_genres(genres_df, top_n=10):
    """Top genres sur la table filtrée."""
    if genres_df.empty or "genre" not in genres_df.columns:
        fig = go.Figure()
        fig.add_annotation(
            text="Aucun genre pour la sélection en cours.",
            showarrow=False,
            font=dict(size=16, color=COLOR_MUTED)
        )
        fig.update_layout(**THEME_LAYOUT, title=f"Top {top_n} des genres", xaxis_visible=False, yaxis_visible=False)
        return fig

    top_g = genres_df["genre"].value_counts().head(top_n).reset_index()
    top_g.columns = ["Genre", "Titres"]
    top_g = top_g.sort_values("Titres", ascending=True)

    fig = go.Figure(
        go.Bar(
            x=top_g["Titres"],
            y=top_g["Genre"],
            orientation="h",
            marker=dict(color=COLOR_SECOND),
            text=top_g["Titres"].apply(lambda v: f"{v:,}".replace(",", " ")),
            textposition="outside",
            textfont=dict(size=15, color=COLOR_TEXT)
        )
    )
    max_val = max(top_g["Titres"]) if not top_g.empty else 100
    fig.update_layout(
        **THEME_LAYOUT,
        title=f"Top {top_n} des genres",
        xaxis=dict(
            title="Nombre de titres associés",
            range=[0, max_val * 1.18],
            gridcolor=COLOR_GRID,
            linecolor=COLOR_MUTED
        ),
        yaxis=dict(title="Genre", gridcolor=COLOR_GRID, linecolor=COLOR_MUTED),
    )
    return fig


def chart_evolution_annees(propre_df):
    """Ajouts par année sur Netflix (2008 à 2021)."""
    if propre_df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="Aucune donnée à afficher.",
            showarrow=False,
            font=dict(size=16, color=COLOR_MUTED)
        )
        fig.update_layout(**THEME_LAYOUT, title="Ajouts par année")
        return fig

    ajouts = propre_df["annee_ajout"].dropna().astype(int).value_counts().sort_index()
    df_plot = pd.DataFrame({"Année": ajouts.index, "Ajouts": ajouts.values})
    df_plot = df_plot[(df_plot["Année"] >= 2008) & (df_plot["Année"] <= 2021)]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_plot["Année"],
        y=df_plot["Ajouts"],
        marker_color=COLOR_ACCENT,
        text=df_plot["Ajouts"].apply(lambda v: f"{v:,}".replace(",", " ")),
        textposition="outside",
        textfont=dict(size=14, color=COLOR_TEXT)
    ))

    max_val = max(df_plot["Ajouts"]) if not df_plot.empty else 100
    fig.update_layout(
        **THEME_LAYOUT,
        title="Ajouts par année (2021 : jusqu'au 25 septembre)",
        xaxis=dict(title="Année d'ajout", dtick=1, gridcolor=COLOR_GRID, linecolor=COLOR_MUTED),
        yaxis=dict(
            title="Nombre de titres ajoutés",
            range=[0, max_val * 1.12],
            gridcolor=COLOR_GRID,
            linecolor=COLOR_MUTED
        ),
    )
    return fig


def chart_distribution_duree(propre_df):
    """Distribution de la durée des films (en minutes) ou des séries (en saisons)."""
    if propre_df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="Aucun contenu ne correspond aux critères sélectionnés.",
            showarrow=False,
            font=dict(size=16, color=COLOR_MUTED)
        )
        fig.update_layout(**THEME_LAYOUT, title="Distribution des formats", xaxis_visible=False, yaxis_visible=False)
        return fig

    films = propre_df[propre_df["type"] == "Movie"]["duree_min"].dropna()
    series = propre_df[propre_df["type"] == "TV Show"]["nb_saisons"].dropna()

    # Si seules les séries sont sélectionnées (pas de films mais des séries)
    if films.empty and not series.empty:
        counts = series.value_counts().sort_index().reset_index()
        counts.columns = ["Saisons", "Nombre"]
        counts["Label"] = counts["Saisons"].apply(lambda s: f"{int(s)} saison" if s == 1 else f"{int(s)} saisons")

        fig = go.Figure(
            go.Bar(
                x=counts["Label"],
                y=counts["Nombre"],
                marker_color=COLOR_SECOND,
                text=counts["Nombre"].apply(lambda v: f"{v:,}".replace(",", " ")),
                textposition="outside",
                textfont=dict(size=14, color=COLOR_TEXT)
            )
        )
        max_v = max(counts["Nombre"]) if not counts.empty else 100
        fig.update_layout(
            **THEME_LAYOUT,
            title="Répartition des séries par nombre de saisons",
            xaxis=dict(title="Nombre de saisons", gridcolor=COLOR_GRID, linecolor=COLOR_MUTED),
            yaxis=dict(title="Nombre de séries", range=[0, max_v * 1.12], gridcolor=COLOR_GRID, linecolor=COLOR_MUTED),
        )
        return fig

    # Si aucun film ni aucune série
    if films.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="Aucun film ne correspond aux critères sélectionnés.",
            showarrow=False,
            font=dict(size=16, color=COLOR_MUTED)
        )
        fig.update_layout(**THEME_LAYOUT, title="Durée des films (en minutes)", xaxis_visible=False, yaxis_visible=False)
        return fig

    # Cas standard : affichage des films en minutes
    med = films.median()
    fig = px.histogram(
        films,
        x="duree_min",
        nbins=40,
        color_discrete_sequence=[COLOR_ACCENT],
        title="Durée des films (en minutes)"
    )
    fig.add_vline(
        x=med,
        line_dash="dash",
        line_color=COLOR_TEXT,
        annotation_text=f"Médiane : {int(med)} min",
        annotation_position="top right",
        annotation_font=dict(size=16, color=COLOR_TEXT)
    )
    fig.update_layout(
        **THEME_LAYOUT,
        xaxis=dict(title="Durée en minutes", gridcolor=COLOR_GRID, linecolor=COLOR_MUTED),
        yaxis=dict(title="Nombre de films", gridcolor=COLOR_GRID, linecolor=COLOR_MUTED),
    )
    return fig
