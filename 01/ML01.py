import marimo

__generated_with = "0.14.17"
app = marimo.App()


@app.cell
def _():
    import numpy as np
    return (np,)


@app.cell
def _():
    import matplotlib.pyplot as plt
    return (plt,)


@app.cell
def _():
    from scipy.optimize import minimize
    return (minimize,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Méthodologie ML""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Génération des données""")
    return


@app.cell
def _(np):
    def inconnue(x):
        return np.cos(10. * x) * np.exp(- x / 2)
    return (inconnue,)


@app.cell
def _(inconnue, np):
    xs = np.linspace(0, 2, 200)
    ys = inconnue(xs)
    return xs, ys


@app.cell
def _(plt, xs, ys):
    plt.plot(xs, ys)
    return


@app.cell
def _(inconnue, np, plt, xs, ys):
    nb_points = 20
    xl, xr = 0, 2

    eps = 0.1

    XS = np.linspace(xl, xr, nb_points)
    YS = inconnue(XS) + eps * np.random.rand(nb_points)

    plt.plot(xs, ys)
    plt.scatter(XS, YS, color='red')
    return XS, YS


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## ML

    La problèmatique est la suivante : connaissant les points rouges $(x_1, y_1)\ldots, (x_N, y_N)$, on veut reconstruire la courbe bleue.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Régression linéaire

    On cherche la courbe bleue parmis les fonctions 

    $$
    x \mapsto a x + b
    $$

    celle qui "colle" le mieux au nuage de points rouges.

    Pour ça on a besoin d'une fonction d'erreur.

    $$
    J_2(a,b) = \sum_{i=1}^N (y_i - (a x_i + b))^2.
    $$

    On cherche $(a,b)$ minimisant $J_2$.

    A ce stade, l'erreur quadratique paraît arbitraire, on pourrait imaginer minimiser

    $$
    J_1(a,b) = \sum_{i=1}^N | y_i - (a x_i + b)|.
    $$
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**REMARQUE** l'avantage de l'erreur quadratique est qu'en annulant le gradient on se retrouve à résoudre un système linéaire en $(a,b)$. On peut donc trouver des formules explicites.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    **EXERCICE** :

    1. Coder la fonction $J_2$ en python
    2. Utiliser `minimize` pour trouver $(a,b)$.
    """
    )
    return


@app.cell
def _(XS, YS, np):
    def J2(ps):
        a, b = ps
        return np.sum((YS - a * XS - b) ** 2)
    return (J2,)


@app.cell
def _(J2, minimize):
    resultat = minimize(J2, [0, 0])
    resultat
    return (resultat,)


@app.cell
def _(resultat):
    a ,b = resultat.x
    return a, b


@app.cell
def _(XS, YS, a, b, plt, xs, ys):
    plt.plot(xs, ys, color="blue", label="fonction cachée")
    plt.scatter(XS, YS, color='red', label="échantillon")
    plt.plot(xs, a * xs + b, color="cyan", label="prédiction")
    plt.legend()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    **CONCLUSION** On voit que le modèle n'est pas satisfaisant.
    Mais surtout on voit même à partir des points rouge que le modèle n'est pas satisfaisant il reste loin de l'échantillon.

    Fondamentalement, le modèle n'est pas assez complexe pour reproduire l'échantillon, on voit que le minimum de $J_2$ est resté à 4.6.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Nouveau modèle""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    On va chercher le prédicteur parmi les polynômes de degrés inférieur à un certain entier $d$.

    $$
    x\mapsto \sum_{k=0}^d a_k x^k
    $$

    Les $(a_0,...,a_d)$ sont les paramètres qu'on obtiendra automatiquement par minimisation de l'erreur.

    Par contre, $d$ est un hyperparamètre, qui est choisi par le modélisateur.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    **EXERCICE**
    Effectuer l'entrainement pour $d=5$.
    """
    )
    return


@app.cell
def _(XS, YS, np):
    d = 5

    def erreur(ps):
        residus = np.zeros_like(XS)
        puissances = np.ones_like(XS)
        for p in ps:
            residus = residus + p * puissances
            puissances = puissances * XS
        return np.sum((residus - YS) ** 2)
    return d, erreur


@app.cell
def _(d, erreur, minimize, np):
    resultat_1 = minimize(erreur, np.zeros(d + 1))
    resultat_1
    return (resultat_1,)


@app.cell
def _(XS, YS, np, plt, resultat_1, xs, ys):
    ps = resultat_1.x
    residus = np.zeros_like(xs)
    puissances = np.ones_like(xs)
    for p in ps:
        residus = residus + p * puissances
        puissances = puissances * xs
    plt.plot(xs, ys, color='blue', label='fonction cachée')
    plt.scatter(XS, YS, color='red', label='échantillon')
    plt.plot(xs, residus, color='cyan', label='prédiction')
    plt.legend()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**CONCLUSION** il y a du mieux mais on reste loin d'avoir une erreur négligeable.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Refactor du code""")
    return


@app.cell
def _(np):
    class Polynome:
        def __init__(self, coefficients: list[float]):
            self.coefficients = coefficients

        def degres(self) -> int:
            return len(self.coefficients) - 1

        def __call__(self, xs):
            residus = np.zeros_like(xs)
            puissances = np.ones_like(xs)
            for p in self.coefficients:
                residus = residus + p * puissances
                puissances = puissances * xs
            return residus
    return (Polynome,)


@app.cell
def _(Polynome, plt, xs):
    identite = Polynome([0, 1])
    plt.plot(xs, identite(xs))
    return


@app.cell
def _(Polynome, XS, YS, np):
    def erreur_1(ps):
        modele = Polynome(ps)
        return np.sum((modele(XS) - YS) ** 2)
    return (erreur_1,)


@app.cell
def _(erreur_1, minimize, np):
    d_1 = 8
    resultat_2 = minimize(erreur_1, x0=np.zeros(d_1 + 1))
    resultat_2
    return (resultat_2,)


@app.cell
def _(Polynome, XS, YS, plt, resultat_2, xs, ys):
    _predicteur = Polynome(resultat_2.x)
    plt.plot(xs, ys, color='blue', label='fonction cachée')
    plt.scatter(XS, YS, color='red', label='échantillon')
    plt.plot(xs, _predicteur(xs), color='cyan', label='prédiction')
    plt.legend()
    return


@app.cell
def _(Polynome, XS, YS, erreur_1, minimize, np, plt, xs, ys):
    d_2 = 10
    resultat_3 = minimize(erreur_1, x0=np.zeros(d_2 + 1))
    print(resultat_3)
    _predicteur = Polynome(resultat_3.x)
    plt.plot(xs, ys, color='blue', label='fonction cachée')
    plt.scatter(XS, YS, color='red', label='échantillon')
    plt.plot(xs, _predicteur(xs), color='cyan', label='prédiction')
    plt.legend()
    return (d_2,)


@app.cell
def _(d_2, plt, xs):
    plt.plot(xs, xs)
    plt.plot(xs, xs ** (d_2 // 2))
    plt.plot(xs, xs ** d_2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**CONCLUSION** le solveur n'arrive pas à converger. Le problème n'est pas tant d'avoir choisi un modèle polynomial, mais de le paramétrer avec la base des puissances de $x$.""")
    return


@app.cell
def _(XS, YS, np):
    def erreur_2(ps):
        modele = np.polynomial.Chebyshev(ps)
        return np.sum((modele(XS) - YS) ** 2)
    return (erreur_2,)


@app.cell
def _(erreur_2, minimize, np):
    d_3 = 10
    resultat_4 = minimize(erreur_2, x0=np.zeros(d_3 + 1))
    print(resultat_4)
    return (resultat_4,)


@app.cell
def _(XS, YS, np, plt, resultat_4, xs, ys):
    _predicteur = np.polynomial.Chebyshev(resultat_4.x)
    plt.plot(xs, ys, color='blue', label='fonction cachée')
    plt.scatter(XS, YS, color='red', label='échantillon')
    plt.plot(xs, _predicteur(xs), color='cyan', label='prédiction')
    plt.legend()
    return


@app.cell
def _(XS, YS, minimize, np, plt, xs, ys):
    def erreur_3(ps):
        modele = np.polynomial.Legendre(ps)
        return np.sum((modele(XS) - YS) ** 2)
    d_4 = 10
    resultat_5 = minimize(erreur_3, x0=np.zeros(d_4 + 1))
    print(resultat_5)
    _predicteur = np.polynomial.Legendre(resultat_5.x)
    plt.plot(xs, ys, color='blue', label='fonction cachée')
    plt.scatter(XS, YS, color='red', label='échantillon')
    plt.plot(xs, _predicteur(xs), color='cyan', label='prédiction')
    plt.legend()
    return


@app.cell
def _(XS, YS, minimize, np, plt, xs, ys):
    def erreur_4(ps):
        modele = np.polynomial.Laguerre(ps)
        return np.sum((modele(XS) - YS) ** 2)
    d_5 = 10
    resultat_6 = minimize(erreur_4, x0=np.zeros(d_5 + 1))
    print(resultat_6)
    _predicteur = np.polynomial.Laguerre(resultat_6.x)
    plt.plot(xs, ys, color='blue', label='fonction cachée')
    plt.scatter(XS, YS, color='red', label='échantillon')
    plt.plot(xs, _predicteur(xs), color='cyan', label='prédiction')
    plt.legend()
    return


@app.cell
def _(XS, YS, minimize, np, plt, xs, ys):
    def erreur_5(ps):
        modele = np.polynomial.Hermite(ps)
        return np.sum((modele(XS) - YS) ** 2)
    d_6 = 10
    resultat_7 = minimize(erreur_5, x0=np.zeros(d_6 + 1))
    print(resultat_7)
    _predicteur = np.polynomial.Hermite(resultat_7.x)
    plt.plot(xs, ys, color='blue', label='fonction cachée')
    plt.scatter(XS, YS, color='red', label='échantillon')
    plt.plot(xs, _predicteur(xs), color='cyan', label='prédiction')
    plt.legend()
    return (d_6,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    **EXERCICE** : On pourrait implémenter la base de Bernstein sur $[a, b]$ qui aux cofficients $(c_0, ..., c_d)$ associe

    $$
    \sum_{k=0}^d c_k \binom{d}{k} \left(\frac{x-a}{b-a}\right)^k \left(\frac{b-x}{b-a}\right)^{d-k}
    $$
    """
    )
    return


@app.cell
def _():
    from scipy.special import binom
    return (binom,)


@app.cell
def _(a, b, binom, coefficients, d_6):
    class Bernstein:

        def __init__(self, a, b, coefficients):
            self.a = a
            self.b = b
            self.coefficients = coefficients

        def __call__(self, xs):
            y = (xs - a) / (b - a)
            somme = 0
            for k, c in enumerate(coefficients):
                somme = somme + c * y ** k * binom(len(self.coefficients), k) * (1 - y) ** (d_6 - k)
            return somme
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    **EXERCICE** 
    1. Visualiser la base de Bernstein pour des petites valeurs.
    2. Faire l'entrainement dans cette base.
    """
    )
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
