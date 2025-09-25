# /// script
# requires-python = ">=3.13"
# dependencies = [
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
def _(mo):
    mo.md(
        r"""
    # Initiation au webscraping

    Origines des données:

    1. dataset prêt à l'emploi (csv, xls, parquet) : Kaggle
    2. données peu structurées (json) : requête sur des api distantes (publiques ou privé)
    3. données pour humain sur site web
    """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## Requêtes HTTP""")
    return


@app.cell
def _():
    url = "https://fr.wikipedia.org/wiki/STOXX_Europe_50"
    return (url,)


@app.cell
def _(mo):
    mo.md(r"""**OBJECTIF** récupérer la composition du STOXX 50 à partir de la page wikipédia.""")
    return


@app.cell
def _():
    from requests import get
    return (get,)


@app.cell
def _(get, url):
    page = get(url=url)
    return (page,)


@app.cell
def _(page):
    dir(page)
    return


@app.cell
def _(page):
    page.ok
    return


@app.cell
def _(page):
    print(page.content.decode("utf8"))
    return


@app.cell
def _(mo):
    mo.md(r"""**EXERCICE** déterminer le *user agent* de votre navigateur et l'insérer dans la requête HTTP effectuée avec `get`.""")
    return


@app.cell
def _():
    user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0"
    return (user_agent,)


@app.cell
def _(get, url, user_agent):
    page_v2 = get(url=url, headers={"User-Agent": user_agent})
    return (page_v2,)


@app.cell
def _(page_v2):
    page_v2.ok
    return


@app.cell
def _(page_v2):
    page_v2.text
    return


@app.cell
def _(mo):
    mo.md(r"""## Extraction naïve des donneés""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    **EXERCICE** récupérer la partie du code source dans `page_v2.text` qui correspond à la table des entreprises du STOXX 50.

    **REMARQUE** On rappelle qu'en HTML, une balise ouvrante s'écrit `<type attributs>` et la balise fermante correspondante `</type>`
    Dans notre cas, lorsqu'on inspecte le code source de la page on voit que la balise qui nous intéresse est `<table>`.
    """
    )
    return


@app.cell
def _(page_v2):
    indice_debut = page_v2.text.find("<table")
    return (indice_debut,)


@app.cell
def _(indice_debut, page_v2):
    print(page_v2.text[indice_debut: indice_debut+200])
    return


@app.cell
def _(page_v2):
    indice_fin = page_v2.text.find("</table>") + len("</table>")
    return (indice_fin,)


@app.cell
def _(indice_debut, indice_fin, page_v2):
    code_table = page_v2.text[indice_debut:indice_fin]
    return (code_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
    En examinant le code source on observe les balises

    1. `th` : pour *table header*
    2. `tr` : pour *table row*
    3. `td` : pour *table delimiter*

    **EXERCICE** récupérer la liste des codes sources des lignes de la table.
    """
    )
    return


@app.cell
def _(code_table):
    liste_lignes = list()
    debut = code_table.find("<tr>")
    while debut != -1:
        fin = code_table.find("</tr>", debut)
        liste_lignes.append(code_table[debut+4:fin])
        debut = code_table.find("<tr>", fin)

    len(liste_lignes)
    return (liste_lignes,)


@app.cell
def _(liste_lignes):
    print(liste_lignes[0])
    return


@app.cell
def _(liste_lignes):
    print(liste_lignes[1])
    return


@app.cell
def _(mo):
    mo.md(r"""**EXERCICE** récupérer les éléments de chaque cellule de la table dans une liste de listes de chaine de caractéres.""")
    return


@app.cell
def _(liste_lignes):
    ligne_test = liste_lignes[1]
    indice1 = ligne_test.find("<td>")+4
    indice2 = ligne_test.find("<td>", indice1)
    indice3 = ligne_test.find("<td>", indice2)
    indice4 = ligne_test.find("<td>", indice3)
    print(ligne_test[indice1:indice2 - 6])
    print(ligne_test[indice2+4:indice3 - 14])
    print(ligne_test[indice3+4:indice4 - 6])
    print(ligne_test[indice4+4:- 6])
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    **REMARQUE** la manipulation des indices va vite devenir fatiguante et peu robuste.
        On va utiliser les expressions régulières pour obtenir une extraction plus simple
    """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## Prise en main des regex""")
    return


@app.cell
def _():
    import re
    return (re,)


@app.cell
def _():
    contenu = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper. Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor. Cras vestibulum bibendum augue. Praesent egestas leo in pede. Praesent blandit odio eu enim. Pellentesque sed dui ut augue blandit sodales. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aliquam nibh. Mauris ac mauris sed pede pellentesque fermentum. Maecenas adipiscing ante non diam sodales hendrerit.
    """
    return (contenu,)


@app.cell
def _(mo):
    mo.md(
        r"""
    On aimerait récupérer les phrases. Une phrase correspond au motif 

    1. La première lettre est une majuscule
    2. On a un nombre inconnu de caractères.
    3. On finit par un point.
    """
    )
    return


@app.cell
def _(re):
    phrase = re.compile("[A-Z].*\\.")
    return (phrase,)


@app.cell
def _(mo):
    mo.md(
        r"""
    - `[A-Z]` décrit un caractère entre `A` et `Z` donc une majuscule
    - `.` décrit un caractère quelconque
    - `*` indique une répétition du motif qui précède,
    - `\\.` : point explicite
    """
    )
    return


@app.cell
def _(contenu, phrase):
    phrase.findall(contenu)
    return


@app.cell
def _(mo):
    mo.md(r"""Attention par défaut les répétitions sont gloutonnes, c'est à dire qu'on cherche le plus grand motif possible qui convient. La version non gloutonne de la répétition est `*?`.""")
    return


@app.cell
def _(re):
    phrase_v2 = re.compile("[A-Z].*?\\.")
    return (phrase_v2,)


@app.cell
def _(contenu, phrase_v2):
    phrase_v2.findall(contenu)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    On peut utiliser des parenthèses à l'intérieur du motif pour indiquer des `groupes de capture` c'est à dire des blocs internes au motif qu'on veut isole.

    Par exemple si on veut récupérer le premier mot de chaque phrase.
    """
    )
    return


@app.cell
def _(contenu, re):
    premier_mot = re.compile("([A-Z][a-z]*).*?\\.")
    premier_mot.findall(contenu)
    return


@app.cell
def _(mo):
    mo.md(r"""**EXERCICE** Reprenez l'extraction des données de la page web, en utilisant des regex plutôt que`find`.""")
    return


@app.cell
def _(page_v2, re):
    table = re.compile("<table.*?</table>")
    code_table_v2, = table.findall(page_v2.text.replace("\n", " "))
    code_table_v2
    return (code_table_v2,)


@app.cell
def _(code_table_v2, re):
    ligne = re.compile("<tr>(.*?)</tr>")
    header, *lignes_v2 = ligne.findall(code_table_v2)
    header
    return header, lignes_v2


@app.cell
def _(lignes_v2, re):
    colonne = re.compile("<td>(.*?)</td>")
    table_final = [colonne.findall(ligne_courante) for ligne_courante in lignes_v2]
    return (table_final,)


@app.cell
def _(table_final):
    len(table_final)
    return


@app.cell
def _(table_final):
    table_final[0]
    return


@app.cell
def _(header):
    header
    return


@app.cell
def _():
    from dataclasses import dataclass

    @dataclass
    class Entree:
        Nom: str
        Symbole: str 
        Url: str 
        Secteur: str 
        Pays: str 
    return


@app.cell
def _(mo):
    mo.md(r"""**EXERCICE** Ajuster le code pour obtenir une liste d'`Entree` comme resultat final.""")
    return


@app.cell
def _(re):
    multiples_groupes = re.compile("^([0-9]*?),(.*?),(.*)$")
    multiples_groupes.findall("150,23,1")
    return (multiples_groupes,)


@app.cell
def _(multiples_groupes):
    multiples_groupes.findall("150,2blabla3,1")
    return


@app.cell
def _(multiples_groupes):
    multiples_groupes.findall("1bla50,2blabla3,1")
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
