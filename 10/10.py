# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "altair==5.5.0",
#     "openai==2.1.0",
#     "polars==1.34.0",
#     "pydantic==2.11.10",
#     "requests==2.32.5",
# ]
# ///

import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    from requests import get
    return (get,)


@app.cell
def _():
    from pydantic import BaseModel
    return (BaseModel,)


@app.cell
def _():
    import polars as pl
    return (pl,)


@app.cell
def _():
    from io import StringIO
    return (StringIO,)


@app.cell
def _():
    URL = "https://raw.githubusercontent.com/VPerrollaz/immobilier/refs/heads/master/donnees/brute.json"
    return (URL,)


@app.cell
def _(URL, get):
    requete = get(URL)
    requete.ok
    return (requete,)


@app.cell
def _(mo):
    mo.md(
        r"""**EXERCICE** récupérer sous une forme structurée les données du fichier `brute.json`."""
    )
    return


@app.cell
def _(requete):
    type(requete.content)
    return


@app.cell
def _(requete):
    requete.encoding
    return


@app.cell
def _(requete):
    contenu = requete.text
    return (contenu,)


@app.cell
def _(contenu):
    print(contenu[:500])
    return


@app.cell
def _(mo):
    mo.md(
        r"""**REMARQUE** Attention le fichier n'est pas un objet json valide, mais chaque ligne est une entrée json. Le format de fichier s'appelle en fait `jsonl`. Il faut donc le parser en plusieurs étapes."""
    )
    return


@app.cell
def _(BaseModel):
    class Annonce(BaseModel):
        id: str
        genre: str
        prix: str
        pcs: str
        desc: str
        lien: str
    return (Annonce,)


@app.cell
def _(Annonce, contenu):
    annonces = [Annonce.model_validate_json(ligne.strip()) for ligne in contenu.splitlines()]
    return (annonces,)


@app.cell
def _(annonces):
    len(annonces)
    return


@app.cell
def _(mo):
    mo.md(
        r"""**REMARQUE** on veut passer d'un dataset faiblement structuré à un dataset prêt à être utilisé en Machine Learning. Donc en particulier sous forme numérique."""
    )
    return


@app.cell
def _(mo):
    mo.md(r"""**EXERCICE** Basculer du format `list[Annonce]` vers un dataframe polars.""")
    return


@app.cell
def _(StringIO, pl, requete):
    df_brut = pl.read_ndjson(StringIO(requete.text))
    return (df_brut,)


@app.cell
def _(df_brut):
    df_brut
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    **EXERCICE** 

    1. supprimer les doublons.
    2. Exploiter la colonne `genre`
    3. Exploiter la colonne `pcs`
    4. Exploiter la colonne `lien`
    5. Exploiter la colonne `desc`
    6. Extraire les prix comme target
    """
    )
    return


@app.cell(hide_code=True)
def _(pl):
    def elimine_doublons(df: pl.DataFrame) -> pl.DataFrame:
        return df.unique(["id"]).drop("id")
    return (elimine_doublons,)


@app.cell
def _(df_brut, elimine_doublons):
    df_brut.pipe(elimine_doublons)
    return


@app.cell
def _(df_brut):
    df_brut["genre"].value_counts(sort=True)
    return


@app.cell
def _(pl):
    def filtre_genre(df: pl.DataFrame) -> pl.DataFrame:
        return df.filter(
            pl.col("genre").is_in(
                {"Appartement", "Maison / Villa", "Appartement neuf", "Maison / Villa neuve"}
            )
        )
    return (filtre_genre,)


@app.cell
def _(df_brut, elimine_doublons, filtre_genre):
    df_brut.pipe(elimine_doublons).pipe(filtre_genre)
    return


@app.cell
def _(pl):
    def exploite_genre(df: pl.DataFrame) -> pl.DataFrame:
        """Génère les variables explicatives neuf/ancien maison/appartement et supprime la colonne genre"""
        return df.with_columns(
            pl.col("genre").is_in({"Appartement", "Appartement neuf"}).alias("appartement"),
            pl.col("genre").is_in({"Appartement neuf", "Maison / Villa neuve"}).alias("neuf"),
        ).drop("genre")
    return (exploite_genre,)


@app.cell
def _(df_brut, elimine_doublons, exploite_genre, filtre_genre):
    df_brut.pipe(elimine_doublons).pipe(filtre_genre).pipe(exploite_genre)
    return


@app.cell
def _(df_brut, elimine_doublons, exploite_genre, filtre_genre):
    df_brut.pipe(elimine_doublons).pipe(filtre_genre).pipe(exploite_genre)["pcs"].str.contains(
        ".*?p.*?ch.*?m²"
    )
    return


@app.cell
def _(df_brut, elimine_doublons, exploite_genre, filtre_genre, pl):
    df_brut.pipe(elimine_doublons).pipe(filtre_genre).pipe(exploite_genre).filter(
        ~pl.col("pcs").str.contains("([0-9]+)(,[0-9]+)? m²")
    )
    return


@app.cell
def _(pl):
    def selectionne_surface(df: pl.DataFrame) -> pl.DataFrame:
        motif_surface = "([0-9]+)(,[0-9]+)? m²"
        return df.filter(pl.col("pcs").str.contains(motif_surface)).with_columns(
            pl.col("pcs").str.extract(motif_surface, 1).str.to_integer().alias("surface")
        )
    return (selectionne_surface,)


@app.cell
def _(
    df_brut,
    elimine_doublons,
    exploite_genre,
    filtre_genre,
    selectionne_surface,
):
    (
        df_brut.pipe(elimine_doublons)
        .pipe(filtre_genre)
        .pipe(exploite_genre)
        .pipe(selectionne_surface)
    )
    return


@app.cell
def _(pl):
    def gere_pieces(df: pl.DataFrame) -> pl.DataFrame:
        return df.with_columns(
            pl.col("pcs").str.extract("([1-9][0-9]?) p", 1).str.to_integer().alias("pieces")
        )
    return (gere_pieces,)


@app.cell
def _(
    df_brut,
    elimine_doublons,
    exploite_genre,
    filtre_genre,
    gere_pieces,
    pl,
    selectionne_surface,
):
    (
        df_brut.pipe(elimine_doublons)
        .pipe(filtre_genre)
        .pipe(exploite_genre)
        .pipe(selectionne_surface)
        .pipe(gere_pieces)
    ).filter(~pl.col("pcs").str.contains("[0-9] ch"))
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
