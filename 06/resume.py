# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pydantic",
#     "requests",
# ]
# ///
#
from requests import get
from pydantic import BaseModel
from pathlib import Path
import re
import sys


def recupere_page(
    url: str = "https://fr.wikipedia.org/wiki/STOXX_Europe_50",
    user_agent: str = (
        "Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0"
    ),
) -> str:
    """Récupération du code html de la page wikipédia du STOXX 50"""
    requete = get(url=url, headers={"User-Agent": user_agent})
    if requete.ok:
        return requete.text
    else:
        raise ValueError("Problème au téléchargement de la page")


def extraction_table(page: str) -> str:
    """Extraction du code source de la première balise table."""
    motif_table = re.compile("<table.*?</table>")
    resultat, *_ = motif_table.findall(page.replace("\n", " "))
    return resultat


def extraction_lignes(table: str) -> list[str]:
    """Extraction des lignes de la table."""
    motif_ligne = re.compile("<tr>(.*?)</tr>")
    _, *resultat = motif_ligne.findall(
        table
    )  # TODO: vérifier que la première ligne est toujours un header!
    return resultat


class Entree(BaseModel):
    nom: str
    symbole: str
    url: str
    pays: str
    secteur: str


class Resultat(BaseModel):
    contenu: list[Entree]


def extraction_entree(code_ligne: str) -> Entree:
    """Extrait le contenu d'une ligne de la table."""
    motif_ligne = re.compile(
        "<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>"
    )
    symbole, deuxieme, troisieme, secteur = motif_ligne.findall(code_ligne)[0]
    motif_deuxieme = re.compile('href="(.*?)".*>(.*?)</a>')
    url, nom = motif_deuxieme.findall(deuxieme)[0]
    motif_troisieme = re.compile(">(.*?)</a>")
    *_, pays = motif_troisieme.findall(troisieme)
    return Entree(
        nom=nom.strip(),
        symbole=symbole.strip(),
        url=url.strip(),
        pays=pays.strip(),
        secteur=secteur.strip(),
    )


def serialise(nom_fichier: str, resultat: Resultat):
    chemin = Path(".").resolve() / nom_fichier
    if chemin.exists():
        raise ValueError(f"Le fichier {nom_fichier} existe déjà")
    else:
        chemin.write_text(resultat.model_dump_json())


def main():
    """Fonction orchestrant le scraping."""
    code_page = recupere_page()
    code_table = extraction_table(code_page)
    lignes = extraction_lignes(code_table)
    entrees = [extraction_entree(code_ligne) for code_ligne in lignes]
    resultat = Resultat(contenu=entrees)
    # TODO: créer un nom de fichier unique utilisant la date courante
    serialise(nom_fichier="test.json", resultat=resultat)


if __name__ == "__main__":
    main()
