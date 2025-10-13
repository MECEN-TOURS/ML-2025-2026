# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "polars",
#     "requests",
# ]
# ///

"""Description.

Utilités et script de nettoyage des données.
"""

from io import StringIO
from requests import get
import polars as pl


def recupere_donnees_brutes() -> pl.DataFrame:
    url = "https://raw.githubusercontent.com/VPerrollaz/immobilier/refs/heads/master/donnees/brute.json"
    texte = get(url).text
    return pl.read_ndjson(StringIO(texte))


def elimine_doublons(df: pl.DataFrame) -> pl.DataFrame:
    return df.unique(["id"]).drop("id")


def filtre_genre(df: pl.DataFrame) -> pl.DataFrame:
    return df.filter(
        pl.col("genre").is_in(
            {
                "Appartement",
                "Maison / Villa",
                "Appartement neuf",
                "Maison / Villa neuve",
            }
        )
    )


def exploite_genre(df: pl.DataFrame) -> pl.DataFrame:
    """Génère les variables explicatives neuf/ancien maison/appartement et supprime la colonne genre"""
    return df.with_columns(
        pl.col("genre").is_in({"Appartement", "Appartement neuf"}).alias("appartement"),
        pl.col("genre")
        .is_in({"Appartement neuf", "Maison / Villa neuve"})
        .alias("neuf"),
    ).drop("genre")


def selectionne_surface(df: pl.DataFrame) -> pl.DataFrame:
    motif_surface = "([0-9]+)(,[0-9]+)? m²"
    return df.filter(pl.col("pcs").str.contains(motif_surface)).with_columns(
        pl.col("pcs").str.extract(motif_surface, 1).str.to_integer().alias("surface")
    )


def gere_pieces(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pl.col("pcs").str.extract("([1-9][0-9]?) p", 1).str.to_integer().alias("pieces")
    )


def gere_prix(df: pl.DataFrame) -> pl.DataFrame:
    motif_prix = "([0-9]* [0-9]*) €"
    return df.with_columns(
        pl.col("prix").str.extract(motif_prix).str.replace(" ", "").str.to_integer()
    )


def main():
    df_brut = recupere_donnees_brutes()
    intermediaire = (
        df_brut.pipe(elimine_doublons)
        .pipe(filtre_genre)
        .pipe(exploite_genre)
        .pipe(selectionne_surface)
        .pipe(gere_pieces)
        .pipe(gere_prix)
        .select(["appartement", "neuf", "pieces", "surface", "prix"])
    )
    intermediaire.write_parquet("cleaned_data.parquet")


if __name__ == "__main__":
    main()
