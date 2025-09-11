# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "matplotlib==3.10.6",
#     "numpy==2.3.3",
#     "openai==1.107.1",
#     "scikit-learn==1.7.2",
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
    mo.md("""# Exploration des datasets de scikit-learn""")
    return


@app.cell
def _():
    from sklearn.datasets import fetch_20newsgroups
    return (fetch_20newsgroups,)


@app.cell
def _(fetch_20newsgroups):
    ds = fetch_20newsgroups()
    return (ds,)


@app.cell
def _(ds):
    type(ds)
    return


@app.cell
def _(ds):
    dir(ds)
    return


@app.cell
def _(ds):
    type(ds.data)
    return


@app.cell
def _(ds):
    type(ds.target)
    return


@app.cell
def _(ds):
    ds.data[0]
    return


@app.cell
def _(ds):
    len(ds.data)
    return


@app.cell
def _(ds):
    len(ds.target)
    return


@app.cell
def _(ds):
    ds.target_names
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    Le dataset précédent a comme donnée 

    - en entrée le contenu de fichiers
    - en sortie une catégorie correspondant à la thématique du sous forum où a été posté le texte

    On va commencer par un dataset de classification moins ambitieux.
    """
    )
    return


@app.cell
def _():
    from sklearn.datasets import load_iris
    return (load_iris,)


@app.cell
def _(load_iris):
    iris = load_iris()
    iris
    return (iris,)


@app.cell
def _(iris):
    print(iris.DESCR)
    return


@app.cell
def _(iris):
    X = iris.data
    y = iris.target
    return X, y


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    # Classification

    **EXERCICE**

    1. Séparer le dataset entre données d'entrainement et données de test
    2. Faite tourner le modèle de régression logistique
    1. Evaluer le résultat du modèle
    """
    )
    return


@app.cell
def _():
    from sklearn.linear_model import LogisticRegression
    return (LogisticRegression,)


@app.cell
def _():
    from sklearn.model_selection import train_test_split
    return (train_test_split,)


@app.cell
def _(X, train_test_split, y):
    X_tr, X_te, y_tr, y_te = train_test_split(X, y)
    return X_te, X_tr, y_te, y_tr


@app.cell
def _(LogisticRegression):
    lr = LogisticRegression()
    return (lr,)


@app.cell
def _(X_tr, lr, y_tr):
    lr.fit(X_tr, y_tr)
    return


@app.cell
def _():
    from sklearn.metrics import confusion_matrix
    return (confusion_matrix,)


@app.cell
def _(X_tr, confusion_matrix, lr, y_tr):
    confusion_matrix(y_tr, lr.predict(X_tr))
    return


@app.cell
def _(X_te, confusion_matrix, lr, y_te):
    confusion_matrix(y_te, lr.predict(X_te))
    return


@app.cell
def _(mo):
    mo.md(
        """
    **REMARQUE**
    Les scores servent à comparer des modèles pas à évaluer un modèle dans le vide.

    On va comparer au dummy classifier pour évaluer l'apport du modèle.
    """
    )
    return


@app.cell
def _():
    from sklearn.dummy import DummyClassifier
    return (DummyClassifier,)


@app.cell
def _(DummyClassifier):
    dc = DummyClassifier()
    return (dc,)


@app.cell
def _(X_tr, dc, y_tr):
    dc.fit(X_tr, y_tr)
    return


@app.cell
def _(X_tr, confusion_matrix, dc, y_tr):
    confusion_matrix(y_tr, dc.predict(X_tr))
    return


@app.cell
def _(X_te, confusion_matrix, dc, y_te):
    confusion_matrix(y_te, dc.predict(X_te))
    return


@app.cell
def _():
    from sklearn.metrics import classification_report
    return (classification_report,)


@app.cell
def _(X, classification_report, lr, y):
    print(classification_report(y_true = y, y_pred = lr.predict(X)))
    return


@app.cell
def _(X, classification_report, dc, y):
    print(classification_report(y_true = y, y_pred = dc.predict(X)))
    return


@app.cell
def _(mo):
    mo.md("""**CONCLUSION** On voit que la tâche n'était pas complètement évidente vu les scores du DummmyClassifier. La régression logistique fait donc un travail très raisonnable.""")
    return


@app.cell
def _(mo):
    mo.md("""# Nouveau dataset""")
    return


@app.cell
def _():
    from sklearn.datasets import load_digits
    return (load_digits,)


@app.cell
def _(load_digits):
    digits = load_digits()
    return (digits,)


@app.cell
def _(digits):
    print(digits.DESCR)
    return


@app.cell
def _(mo):
    mo.md("""**EXERCICE** Visualiser les images correspondantes aux 10 premières entrées du dataset""")
    return


@app.cell
def _(digits):
    Xd, yd = digits.data, digits.target
    return Xd, yd


@app.cell
def _(Xd):
    Xd[0]
    return


@app.cell
def _():
    import matplotlib.pyplot as plt
    return (plt,)


@app.cell
def _(Xd, plt):
    plt.spy(Xd[0].reshape(8, 8))
    return


@app.cell
def _(Xd, plt):
    plt.imshow(16 - Xd[0].reshape(8, 8), cmap="grey")
    return


@app.cell
def _(yd):
    yd[0]
    return


@app.cell
def _(Xd, plt):
    plt.imshow(16 - Xd[1].reshape(8, 8), cmap="grey")
    return


@app.cell
def _(yd):
    yd[1]
    return


@app.cell
def _(mo):
    mo.md("""**EXERCICE** Entrainer un modèle de classification sur ce dataset.""")
    return


@app.cell
def _(Xd, train_test_split, yd):
    Xd_tr, Xd_te, yd_tr, yd_te = train_test_split(Xd, yd)
    return Xd_te, Xd_tr, yd_te, yd_tr


@app.cell
def _(DummyClassifier):
    dcd = DummyClassifier(strategy="uniform")
    return (dcd,)


@app.cell
def _(Xd_tr, dcd, yd_tr):
    dcd.fit(Xd_tr, yd_tr)
    return


@app.cell
def _(Xd, classification_report, dcd, yd):
    print(classification_report(yd, dcd.predict(Xd)))
    return


@app.cell
def _(LogisticRegression):
    lrd = LogisticRegression(max_iter=1000)
    return (lrd,)


@app.cell
def _(Xd_tr, lrd, yd_tr):
    lrd.fit(Xd_tr, yd_tr)
    return


@app.cell
def _(Xd, classification_report, lrd, yd):
    print(classification_report(yd, lrd.predict(Xd)))
    return


@app.cell
def _(mo):
    mo.md("""**EXERCICE** identifier et visualiser les images mal classifiées.""")
    return


@app.cell
def _():
    from sklearn.metrics import f1_score
    return (f1_score,)


@app.cell
def _(Xd_tr, f1_score, lrd, yd_tr):
    f1_score(yd_tr, lrd.predict(Xd_tr), average=None)
    return


@app.cell
def _(Xd_te, f1_score, lrd, yd_te):
    f1_score(yd_te, lrd.predict(Xd_te), average=None)
    return


@app.cell
def _(Xd_te, lrd, yd_te):
    masque = (yd_te != lrd.predict(Xd_te))
    return (masque,)


@app.cell
def _(masque):
    masque
    return


@app.cell
def _(Xd_te, lrd, masque, yd_te):
    pbx = Xd_te[masque]
    nombrepb = yd_te[masque]
    predpb = lrd.predict(Xd_te)[masque]
    return nombrepb, pbx, predpb


@app.cell
def _(nombrepb, pbx, plt, predpb):
    def visualisation(indice):
        _, rep = plt.subplots()
        rep.imshow(16 - pbx[indice].reshape(8, 8), cmap="grey")
        rep.set_title(f"prédit: {predpb[indice]}, réalité {nombrepb[indice]}")
        return rep
    return (visualisation,)


@app.cell
def _(visualisation):
    visualisation(1)
    return


@app.cell
def _(mo, nombrepb):
    indice = mo.ui.slider(start=0, stop=len(nombrepb) - 1, label="indice", show_value=True)
    indice
    return (indice,)


@app.cell
def _(indice, visualisation):
    visualisation(indice=indice.value)
    return


@app.cell
def _(mo):
    mo.md("""
    # Nouveau dataset plus ambitieux""")
    return


@app.cell
def _():
    from sklearn.datasets import fetch_kddcup99
    return (fetch_kddcup99,)


@app.cell
def _(fetch_kddcup99):
    kdd = fetch_kddcup99()
    return (kdd,)


@app.cell
def _(kdd):
    print(kdd.DESCR)
    return


@app.cell
def _(mo):
    mo.md("""
    **EXERCICE** Répéter la démarche précédente.""")
    return


@app.cell
def _(kdd):
    X1, y1 = kdd.data, kdd.target
    return X1, y1


@app.cell
def _(X1):
    type(X1)
    return


@app.cell
def _(X1):
    X1.shape
    return


@app.cell
def _(y1):
    type(y1)
    return


@app.cell
def _(y1):
    y1.shape
    return


@app.cell
def _(y1):
    y1[0]
    return


@app.cell
def _(X1):
    X1[0]
    return


@app.cell
def _(mo):
    mo.md("""
    **PROBLEME** on voit que certains champs ne sont pas numériques, mais des chaines de caractéres encodées en bytes.""")
    return


@app.cell
def _():
    import numpy as np
    return (np,)


@app.cell
def _(np, y1):
    np.unique(y1, return_counts=True)
    return


@app.cell
def _():
    from sklearn.preprocessing import OrdinalEncoder
    return (OrdinalEncoder,)


@app.cell
def _(OrdinalEncoder):
    oe = OrdinalEncoder()
    return (oe,)


@app.cell
def _(oe, y1):
    y2 = oe.fit_transform(y1.reshape(-1, 1))
    return (y2,)


@app.cell
def _(np, y2):
    np.unique(y2, return_counts=True)
    return


@app.cell
def _(OrdinalEncoder, X1):
    oex = OrdinalEncoder()
    X2 = oex.fit_transform(X1)
    return (X2,)


@app.cell
def _(X2):
    X2.dtype
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
