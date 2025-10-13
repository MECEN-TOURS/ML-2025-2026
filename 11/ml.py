# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "joblib==1.5.2",
#     "numpy==2.3.3",
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
    import polars as pl
    import numpy as np
    return mo, pl


@app.cell
def _(mo):
    mo.md(r"""## Acquisition du dataset""")
    return


@app.cell
def _(pl):
    df = pl.read_parquet("cleaned_data.parquet")
    df
    return (df,)


@app.cell
def _(df):
    X = df.select("appartement", "neuf", "pieces", "surface").to_numpy()
    X
    return (X,)


@app.cell
def _(df):
    y = df.select("prix").to_numpy().reshape((-1,))
    y
    return (y,)


@app.cell
def _(mo):
    mo.md(r"""## Sélection du meilleur modèle""")
    return


@app.cell
def _():
    from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV, cross_val_score
    return GridSearchCV, cross_val_score, train_test_split


@app.cell
def _(X, train_test_split, y):
    Xtr, Xte, ytr, yte = train_test_split(X, y)
    return Xte, Xtr, yte, ytr


@app.cell
def _():
    from sklearn.dummy import DummyRegressor
    from sklearn.linear_model import LinearRegression, Ridge, Lasso
    from sklearn.svm import SVR 
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.neural_network import MLPRegressor
    return (
        DummyRegressor,
        GradientBoostingRegressor,
        LinearRegression,
        MLPRegressor,
        RandomForestRegressor,
    )


@app.cell
def _(DummyRegressor, Xtr, cross_val_score, ytr):
    dr = DummyRegressor()
    dr.fit(Xtr, ytr)
    cross_val_score(dr, Xtr, ytr)
    return


@app.cell
def _(LinearRegression, Xtr, cross_val_score, ytr):
    lr = LinearRegression()
    lr.fit(Xtr, ytr)
    cross_val_score(lr, Xtr, ytr)
    return


@app.cell
def _(RandomForestRegressor, Xtr, cross_val_score, ytr):
    rfr = RandomForestRegressor()
    rfr.fit(Xtr, ytr)
    cross_val_score(rfr, Xtr, ytr)
    return


@app.cell
def _(GradientBoostingRegressor, Xtr, cross_val_score, ytr):
    gbr = GradientBoostingRegressor()
    gbr.fit(Xtr, ytr)
    cross_val_score(gbr, Xtr, ytr)
    return


@app.cell
def _(GridSearchCV, MLPRegressor, Xtr, ytr):
    gsmlp = GridSearchCV(
        MLPRegressor(),
        param_grid=dict(
            max_iter=[10000],
            hidden_layer_sizes=[
                (10, ),
                (30, ), 
                (50, ),
            ]
        )
    )
    gsmlp.fit(Xtr, ytr)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    **CONCLUSION** On constate que le meilleur modèle est le gradient boosting.
    On va l'entrainer et vérifier qu'il n'est pas en surapprentissage.

    **REMARQUE** Il faudrait en fait 

    - évaluer tous les modèles
    - avec plusieurs choix d'hyperparamètre
    - essayer aussi de standardiser les entrées
    - Faire en sorte que les solveurs convergent bien
    """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## Entrainement du modèle final et sérialisation""")
    return


@app.cell
def _(GradientBoostingRegressor, Xte, Xtr, yte, ytr):
    final = GradientBoostingRegressor()
    final.fit(Xtr, ytr)
    print(f"""
    score entrainement {final.score(Xtr, ytr)}
    score test {final.score(Xte, yte)}
          """)
    return (final,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""On constate une déviation nette entre les deux scores mais pas suffisante pour qu'on déclare être en surapprentissage.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**EXERCICE** utiliser la librairie `joblib` pour sérialiser le modèle ci dessus sur le disque.""")
    return


@app.cell
def _():
    import joblib
    return (joblib,)


@app.cell
def _(final, joblib):
    joblib.dump(final, "modele.joblib")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
