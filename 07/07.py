# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "polars==1.33.1",
#     "scikit-learn==1.7.2",
#     "seaborn==0.13.2",
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
    from sklearn.datasets import load_diabetes
    return (load_diabetes,)


@app.cell
def _(load_diabetes):
    diabete = load_diabetes()
    diabete
    return (diabete,)


@app.cell
def _(diabete):
    print(diabete.DESCR)
    return


@app.cell
def _(diabete):
    X = diabete.data
    y = diabete.target
    return X, y


@app.cell
def _(mo):
    mo.md(r"""**EXERCICE** Regarder la documentation de scikit-learn pour faire une liste de modèle permettant d'effectuer une tâche de régression.""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Modèles : 

    1. Dummy Regressor
    1. Régression linéaire
    2. Lasso (régression linéaire et pénalisation norme1)
    3. Ridge (régression linéaire et pénalisation norme2)
    4. Elasticnet (mélange des deux précédents)
    5. SVM
    6. KNeighbors
    7. Gaussian Process
    8. Decision Tree
    9. RandomForest
    10. Gradient Boosting
    11. Neural Networks
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    **EXERCICE** 

    1. Faites un train_test_split
    2. Entrainer les modèles ci-dessus en faisant attention aux choix des hyperparamètres
    3. Sélectionner le meilleur couple Modéle/Hyperparamètre par Cross Validation
    4. Vérifier que ce choix n'est pas en surapprentissage
    """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## Préparation""")
    return


@app.cell
def _():
    from sklearn.model_selection import train_test_split
    return (train_test_split,)


@app.cell
def _(X, train_test_split, y):
    X_tr, X_te, y_tr, y_te = train_test_split(X, y)
    return X_tr, y_tr


@app.cell
def _():
    from sklearn.dummy import DummyRegressor
    from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
    from sklearn.svm import SVR
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.neural_network import MLPRegressor
    return (
        DecisionTreeRegressor,
        DummyRegressor,
        ElasticNet,
        GaussianProcessRegressor,
        GradientBoostingRegressor,
        KNeighborsRegressor,
        Lasso,
        LinearRegression,
        MLPRegressor,
        RandomForestRegressor,
        Ridge,
        SVR,
    )


@app.cell
def _():
    from sklearn.model_selection import cross_val_score
    return (cross_val_score,)


@app.cell
def _():
    resultat = dict()
    return (resultat,)


@app.cell
def _(mo):
    mo.md(r"""## Dummy""")
    return


@app.cell
def _(DummyRegressor, X_tr, cross_val_score, resultat, y_tr):
    dumdum = DummyRegressor()
    resultat[dumdum] = cross_val_score(dumdum, X_tr, y_tr)
    return


@app.cell
def _(mo):
    mo.md(r"""## Régression Linéaire""")
    return


@app.cell
def _(LinearRegression, X_tr, cross_val_score, resultat, y_tr):
    lr = LinearRegression()
    resultat[lr] = cross_val_score(lr, X_tr, y_tr)
    return


@app.cell
def _(mo):
    mo.md(r"""## Lasso""")
    return


@app.cell
def _(Lasso, X_tr, cross_val_score, resultat, y_tr):
    la = Lasso(alpha=1.0)
    resultat[la] = cross_val_score(la, X_tr, y_tr)
    return


@app.cell
def _(mo):
    mo.md(r"""## Ridge""")
    return


@app.cell
def _(Ridge, X_tr, cross_val_score, resultat, y_tr):
    ri = Ridge(alpha=1.0)
    resultat[ri] = cross_val_score(ri, X_tr, y_tr)
    return


@app.cell
def _(mo):
    mo.md(r"""## ElasticNet""")
    return


@app.cell
def _(ElasticNet, X_tr, cross_val_score, resultat, y_tr):
    en = ElasticNet(alpha=1.0, l1_ratio=0.5)
    resultat[en] = cross_val_score(en, X_tr, y_tr)
    return


@app.cell
def _(mo):
    mo.md(r"""## SVM""")
    return


@app.cell
def _(SVR, X_tr, cross_val_score, resultat, y_tr):
    svr = SVR(C=1.0, epsilon=0.1)
    resultat[svr] = cross_val_score(svr, X_tr, y_tr)
    return


@app.cell
def _(mo):
    mo.md(r"""## KNeighnors""")
    return


@app.cell
def _(KNeighborsRegressor, X_tr, cross_val_score, resultat, y_tr):
    knr = KNeighborsRegressor(n_neighbors=5)
    resultat[knr] = cross_val_score(knr, X_tr, y_tr)
    return


@app.cell
def _(mo):
    mo.md(r"""## GaussianProcess""")
    return


@app.cell
def _(GaussianProcessRegressor, X_tr, cross_val_score, resultat, y_tr):
    gpr = GaussianProcessRegressor()
    resultat[gpr] = cross_val_score(gpr, X_tr, y_tr)
    return


@app.cell
def _(mo):
    mo.md(r"""## DecisionTree""")
    return


@app.cell
def _(DecisionTreeRegressor, X_tr, cross_val_score, resultat, y_tr):
    dt = DecisionTreeRegressor()
    resultat[dt] = cross_val_score(dt, X_tr, y_tr)
    return


@app.cell
def _(mo):
    mo.md(r"""## RandomForest""")
    return


@app.cell
def _(RandomForestRegressor, X_tr, cross_val_score, resultat, y_tr):
    rf = RandomForestRegressor()
    resultat[rf] = cross_val_score(rf, X_tr, y_tr)
    return


@app.cell
def _(mo):
    mo.md(r"""## GradientBoosting""")
    return


@app.cell
def _(GradientBoostingRegressor, X_tr, cross_val_score, resultat, y_tr):
    gb = GradientBoostingRegressor()
    resultat[gb] = cross_val_score(gb, X_tr, y_tr)
    return


@app.cell
def _(mo):
    mo.md(r"""## Neural Networks""")
    return


@app.cell
def _(MLPRegressor, X_tr, cross_val_score, resultat, y_tr):
    nn = MLPRegressor(hidden_layer_sizes=(30,), max_iter=10000)
    resultat[nn] = cross_val_score(nn, X_tr, y_tr)
    return


@app.cell
def _(mo):
    mo.md(r"""## Choix du modèle""")
    return


@app.cell
def _():
    import polars as pl
    return (pl,)


@app.cell
def _(pl, resultat):
    resultatdf = pl.from_dict(
        { str(modele): scores for modele, scores in  resultat.items()}
    )
    return (resultatdf,)


@app.cell
def _(resultatdf):
    resultatdf
    return


@app.cell
def _():
    import seaborn as sns
    return (sns,)


@app.cell
def _(pl, resultatdf, sns):
    sns.violinplot(
        data=resultatdf.select(
            pl.exclude("GaussianProcessRegressor()")
        )
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
