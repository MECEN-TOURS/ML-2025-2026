# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "matplotlib==3.10.6",
#     "numpy==2.3.2",
#     "scikit-learn==1.7.2",
# ]
# ///

import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    return mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    # Première partie de  séance

    Suite à un bogue en salle de TP, pas d'ordinateur utilisable.
    Première partie théorique.

    1. Rappels sur les deux premières séances.
    2. Souligner le rôle arbitraire de l'erreur quadratique moyenne.
    3. Modélisation par inférence puis décision.
    1. Inférence en modélisant par un champs de lois normales plutôt que par une fonction.
    1. Le principe de maximum de vraisemblance ramène alors à l'erreur quadratique moyenne pour l'espérance
    1. Approche similaire pour un problème de classification
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
    # Deuxième partie de séance

    Prise en main de scikit-learn:

    1. Installation avec uv
    1. Exploration de la documentation pour reproduire le contenu des deux premières séances
    """
    )
    return


@app.cell
def _(mo):
    mo.md("""## Génération du dataset""")
    return


@app.cell
def _(np):
    def inconnue(xs):
        return np.cos(10. * xs) * np.exp(-xs)
    return (inconnue,)


@app.cell
def _(inconnue, np, plt):
    xs = np.linspace(0., 2., 20)
    ys = inconnue(xs) + 0.1 * np.random.randn(20)

    plt.scatter(xs, ys, label="échantillon", color="red")

    _x = np.linspace(0, 2., 200)
    plt.plot(_x, inconnue(_x), label="fonction cachée", color="blue")
    plt.legend()
    return xs, ys


@app.cell
def _(mo):
    mo.md("""## Régression linéaire""")
    return


@app.cell
def _():
    from sklearn.linear_model import LinearRegression
    return (LinearRegression,)


@app.cell
def _(LinearRegression, xs, ys):
    X = xs.reshape(20, 1)
    lr = LinearRegression(fit_intercept=True)
    lr.fit(X, ys)
    return X, lr


@app.cell
def _(inconnue, lr, np, plt, xs, ys):
    plt.scatter(xs, ys, label="échantillon", color="red")

    _x = np.linspace(0, 2., 200)
    plt.plot(_x, inconnue(_x), label="fonction cachée", color="blue")
    plt.plot(_x, lr.predict(_x.reshape(-1, 1)), color="cyan", label="prédiction")
    plt.legend()
    return


@app.cell
def _(mo):
    mo.md("""## Modèle Polynômial""")
    return


@app.cell
def _():
    from sklearn.preprocessing import PolynomialFeatures
    return (PolynomialFeatures,)


@app.cell
def _(PolynomialFeatures, X):
    pf = PolynomialFeatures(degree=5)
    Xp = pf.fit_transform(X)
    Xp.shape
    return Xp, pf


@app.cell
def _(LinearRegression, Xp, ys):
    modele = LinearRegression(fit_intercept=False)
    modele.fit(Xp, ys)
    return (modele,)


@app.cell
def _(inconnue, modele, np, pf, plt, xs, ys):
    plt.scatter(xs, ys, label="échantillon", color="red")

    _x = np.linspace(0, 2., 200)
    plt.plot(_x, inconnue(_x), label="fonction cachée", color="blue")

    _X = pf.fit_transform(_x.reshape(-1, 1))
    plt.plot(_x, modele.predict(_X), color="cyan", label="prédiction")
    plt.legend()
    return


@app.cell
def _(mo):
    mo.md(
        """
    ## Exploration interactive avec Marimo

    On suggère de passer en **app view** pour expérimenter avec la suite et observer l'impact du degré sur la fidélité du modèle.
    """
    )
    return


@app.cell
def _(mo):
    degres = mo.ui.slider(label="degré du modèle", start=1, stop=20, show_value=True)
    degres
    return (degres,)


@app.cell
def _(
    LinearRegression,
    PolynomialFeatures,
    X,
    degres,
    inconnue,
    np,
    plt,
    xs,
    ys,
):
    _pf = PolynomialFeatures(degree=degres.value)
    _Xp = _pf.fit_transform(X)
    _modele = LinearRegression(fit_intercept=False)
    _modele.fit(_Xp, ys)

    plt.scatter(xs, ys, label="échantillon", color="red")
    _x = np.linspace(0, 2., 200)
    plt.plot(_x, inconnue(_x), label="fonction cachée", color="blue")
    _X = _pf.fit_transform(_x.reshape(-1, 1))
    plt.plot(_x, _modele.predict(_X), color="cyan", label="prédiction")
    plt.legend()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
