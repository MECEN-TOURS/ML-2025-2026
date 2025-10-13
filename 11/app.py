# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "joblib==1.5.2",
#     "polars==1.34.0",
#     "scikit-learn==1.7.2",
# ]
# ///

import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import joblib
    import polars as pl
    from typing import Literal
    return Literal, joblib, mo, pl


@app.cell
def _(joblib):
    modele = joblib.load("modele.joblib")
    return (modele,)


@app.cell
def _(modele, pl):
    def genere_prix_rationnel(df: pl.DataFrame) -> pl.DataFrame:
        nouveau = df.map_rows(lambda t: modele.predict([[t[0], t[1], t[2], t[3]]])[0])
        return pl.concat([df, nouveau], how="horizontal")


    annonces = genere_prix_rationnel(pl.read_parquet("cleaned_data.parquet"))
    return (annonces,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    **EXERCICE** On veut construire une application prenant en entrée les choix 

    - Appartement/Maison
    - Fourchette de surface
    - Fourchette de nombre de pièces
    - Neuf/Ancien
    - Fourchette de prix

    On devra ensuite filtrer les annonces respectant ces critères.
    Puis utiliser le modèle pour générer le prix rationnel correspondant aux données d'entrée de l'annonce.
    On triera ensuite les annonces filtrées grâce à la différence entre le prix demandé et le prix rationnel.
    """
    )
    return


@app.cell
def _(mo):
    prix = mo.ui.range_slider(
        start=1_000, stop=1_000_000, step=1000, label="Prix", show_value=True
    )
    surface = mo.ui.range_slider(start=10, stop=200, label="Surface", show_value=True)
    pieces = mo.ui.range_slider(start=1, stop=10, label="Nombre de Pièces", show_value=True)
    neuf = mo.ui.dropdown(
        options=["neuf", "ancien", "indifférent"], value="indifférent", label="Neuf/Ancien"
    )
    appartement = mo.ui.dropdown(
        options=["appartement", "maison", "indifférent"],
        value="indifférent",
        label="Appartement/Maison",
    )
    return appartement, neuf, pieces, prix, surface


@app.cell
def _(appartement, mo, neuf, pieces, prix, surface):
    mo.vstack(
        [mo.hstack([appartement, neuf]), mo.hstack([surface, pieces]), prix], align="center"
    )
    return


@app.cell
def _(Literal, pl):
    def filtre_prix(df, critere) -> pl.DataFrame:
        mini, maxi = critere
        return df.filter((mini <= pl.col("prix")) & (pl.col("prix") <= maxi))


    def filtre_surface(df, critere) -> pl.DataFrame:
        mini, maxi = critere
        return df.filter((mini <= pl.col("surface")) & (pl.col("surface") <= maxi))


    def filtre_pieces(df, critere) -> pl.DataFrame:
        mini, maxi = critere
        return df.filter((mini <= pl.col("pieces")) & (pl.col("pieces") <= maxi))


    def filtre_appartement(
        df, critere=Literal["appartement", "maison", "indifférent"]
    ) -> pl.DataFrame:
        if critere == "indifférent":
            return df
        elif critere == "maison":
            return df.filter(~pl.col("appartement"))
        elif critere == "appartement":
            return df.filter(pl.col("appartement"))
        else:
            raise ValueError("Mauvais critère")


    def filtre_neuf(df, critere=Literal["neuf", "ancien", "indifférent"]) -> pl.DataFrame:
        if critere == "indifférent":
            return df
        elif critere == "neuf":
            return df.filter(pl.col("neuf"))
        elif critere == "ancien":
            return df.filter(~pl.col("neuf"))
        else:
            raise ValueError("Mauvais critère")
    return (
        filtre_appartement,
        filtre_neuf,
        filtre_pieces,
        filtre_prix,
        filtre_surface,
    )


@app.cell
def _(pl):
    def reordonne(df):
        return (
            df.with_columns((pl.col("map") - pl.col("prix")).alias("difference"))
            .sort(by=pl.col("difference"), descending=True)
            .select("appartement", "neuf", "pieces", "surface", "prix")
            .head(10)
        )
    return (reordonne,)


@app.cell
def _(
    annonces,
    appartement,
    filtre_appartement,
    filtre_neuf,
    filtre_pieces,
    filtre_prix,
    filtre_surface,
    neuf,
    pieces,
    prix,
    reordonne,
    surface,
):
    (
        annonces.pipe(filtre_neuf, neuf.value)
        .pipe(filtre_appartement, appartement.value)
        .pipe(filtre_pieces, pieces.value)
        .pipe(filtre_prix, prix.value)
        .pipe(filtre_surface, surface.value)
        .pipe(reordonne)
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    **CONCLUSION** pour avoir quelque chose d'utile, il faudrait

    - Reprendre `cleaning.py` pour garder les données complètes de chaque annonce dans le dataset nettoyé
    - On utilise dans `ml.py` les colonnes numériques pour sélectionner et entrainer le modèle
    - On utilise dans `app.py` les colonnes numériques et le modèle pour trier les annonces.
    - On affiche par contre les données au format *humain* de chaque annonce sélectionnée.
    """
    )
    return


if __name__ == "__main__":
    app.run()
