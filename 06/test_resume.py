"""Test du module resume.py"""

from resume import extraction_entree, Entree


def test_extraction_entree():
    input = """ <td>ABBN VX</td> <td><a href="/wiki/Groupe_ABB" class="mw-redirect" title="Groupe ABB">Groupe ABB</a></td> <td><span class="datasortkey" data-sort-value="Suisse"><span class="flagicon"><span class="mw-image-border noviewer" typeof="mw:File"><a href="/wiki/Fichier:Flag_of_Switzerland.svg" class="mw-file-description" title="Drapeau de la Suisse"><img alt="Drapeau de la Suisse" src="//upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Flag_of_Switzerland.svg/20px-Flag_of_Switzerland.svg.png" decoding="async" width="15" height="15" class="mw-file-element" srcset="//upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Flag_of_Switzerland.svg/40px-Flag_of_Switzerland.svg.png 1.5x" data-file-width="512" data-file-height="512" /></a></span> </span><a href="/wiki/Suisse" title="Suisse">Suisse</a></span></td> <td>Industrie </td>"""
    resultat = extraction_entree(input)
    assert resultat == Entree(
        nom="Groupe ABB",
        symbole="ABBN VX",
        url="/wiki/Groupe_ABB",
        pays="Suisse",
        secteur="Industrie",
    )
