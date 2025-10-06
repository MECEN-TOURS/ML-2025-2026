# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "beautifulsoup4==4.14.2",
#     "lxml==6.0.2",
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Scraping 2.0

    1. On va récupérer les données de [List of S&P 500 companies](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies)
    2. On va utiliser un parser html, en l'occurence [lxml](https://pypi.org/project/lxml/)
    3. On va utiliser également la librairie [beautiful soup](https://pypi.org/project/beautifulsoup4/)
    """
    )
    return


@app.cell
def _():
    from bs4 import BeautifulSoup as BS
    return (BS,)


@app.cell
def _():
    import lxml
    return


@app.cell
def _():
    URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companie"
    return


@app.cell
def _():
    from pydantic import BaseModel
    return (BaseModel,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""**EXERCICE** Récupérer le code html correspondant à l'url ci-dessus. En faisant une requête http."""
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    **REMARQUE** on a ici juste sauvegarder la page web depuis le navigateur.
    On charge ensuite le contenu du fichier.
    Cela contourne les problèmes de type captcha, javascript...
    """
    )
    return


@app.cell
def _():
    from pathlib import Path
    return (Path,)


@app.cell
def _(Path):
    repertoire = Path(".").resolve()
    return (repertoire,)


@app.cell
def _(repertoire):
    repertoire
    return


@app.cell
def _(repertoire):
    list(repertoire.glob("*"))
    return


@app.cell
def _(repertoire):
    fichier = list(repertoire.glob("*"))[0]
    return (fichier,)


@app.cell
def _(fichier):
    fichier
    return


@app.cell
def _(fichier):
    code_html = fichier.read_text()
    return (code_html,)


@app.cell
def _(code_html):
    len(code_html)
    return


@app.cell
def _(code_html):
    print(code_html[:200])
    return


@app.cell
def _(mo):
    mo.md(
        r"""**REMARQUE** On va maintenant passer d'une chaine de caractère à un objet `BeautifulSoup` et utiliser ce dernier."""
    )
    return


@app.cell
def _(BS, code_html):
    soupe = BS(code_html, features="html.parser")
    return (soupe,)


@app.cell
def _(soupe):
    type(soupe)
    return


@app.cell
def _():
    return


@app.cell
def _(mo):
    mo.md(
        r"""**REMARQUE** On peut directement explorer l'arborescence html à partir de cet objet."""
    )
    return


@app.cell
def _(soupe):
    for enfant in soupe.children:
        print(enfant.name)
    return


@app.cell
def _(mo):
    mo.md(r"""**REMARQUE** on peut en fait faire des recherches dans l'arborescence.""")
    return


@app.cell
def _(soupe):
    soupe.find_all("table")
    return


@app.cell
def _(soupe):
    soupe.find_all("table", attrs={"id": "constituents"})
    return


@app.cell
def _(soupe):
    ma_table = soupe.find("table", attrs={"id": "constituents"})
    return (ma_table,)


@app.cell
def _(ma_table):
    type(ma_table)
    return


@app.cell
def _(ma_table):
    ma_table
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    **EXERCICE** utiliser les méthodes précédentes pour extraire les informations souhaitées.
        On utilisera aussi pydantic pour sérialiser le résultat final.
    """
    )
    return


@app.cell
def _(ma_table):
    corps = ma_table.find("tbody")
    return (corps,)


@app.cell
def _(corps):
    type(corps)
    return


@app.cell
def _(corps):
    _, *lignes = corps.find_all("tr")
    assert len(lignes) == 503
    return (lignes,)


@app.cell
def _(lignes):
    ligne_test = lignes[234]
    print(ligne_test)
    return (ligne_test,)


@app.cell
def _(ligne_test):
    print(ligne_test.prettify())
    return


@app.cell
def _(BaseModel):
    # On pourrait utiliser des datatypes URL et Date pour les champs commençant lien_ et date_


    class EntreeSP500(BaseModel):
        symbole: str
        lien_nyse: str
        nom: str
        lien_wiki: str
        domaine: str
        sous_domaine: str
        siege: str
        date_entree: str
        cik: str
        date_fondation: str
    return (EntreeSP500,)


@app.cell
def _(BaseModel, EntreeSP500):
    class ParseResult(BaseModel):
        contenu: list[EntreeSP500]
        url: str
        description: str
    return (ParseResult,)


@app.cell
def _(mo):
    mo.md(
        r"""**EXERCICE** Construiser un objet `ParseResult` pertinent et sérialiser le sur disque."""
    )
    return


@app.cell
def _(EntreeSP500, ligne_test):
    def parse_ligne(ligne: "bs4.element.Tag") -> EntreeSP500:
        tds = ligne.find_all("td")
        assert len(tds) == 8
        return EntreeSP500(
            symbole=tds[0].a.text.strip(),
            lien_nyse=tds[0].a.get("href"),
            nom=tds[1].a.text.strip(),
            lien_wiki=tds[1].a.get("href"),
            domaine=tds[2].text.strip(),
            sous_domaine=tds[3].text.strip(),
            siege=tds[4].text.strip(),
            date_entree=tds[5].text.strip(),
            cik=tds[6].text.strip(),
            date_fondation=tds[7].text.strip(),
        )


    parse_ligne(ligne_test)
    return (parse_ligne,)


@app.cell
def _(ParseResult, lignes, parse_ligne):
    resultat = ParseResult(
        contenu=[parse_ligne(ligne) for ligne in lignes],
        url="https://en.wikipedia.org/wiki/List_of_S%26P_500_companie",
        description="Récupération de la liste des entreprises du SP500",
    )
    return (resultat,)


@app.cell
def _(Path, resultat):
    sauvegarde = Path(".") / "sp500.json"
    if not sauvegarde.exists():
        sauvegarde.write_text(resultat.model_dump_json())
    return (sauvegarde,)


@app.cell
def _(mo):
    mo.md(r"""**EXERCICE** Récupérer un objet `ParseResult` depuis le fichier de sauvegarde.""")
    return


@app.cell
def _(ParseResult, sauvegarde):
    ParseResult.model_validate_json(sauvegarde.read_text())
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
