# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "scikit-learn==1.7.2",
#     "scipy==1.16.2",
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
    X = diabete.data
    y = diabete.target
    return X, y


@app.cell
def _():
    from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, RandomizedSearchCV
    return GridSearchCV, RandomizedSearchCV, cross_val_score, train_test_split


@app.cell
def _(X, train_test_split, y):
    Xtr, Xte, ytr, yte = train_test_split(X, y)
    return Xtr, ytr


@app.cell
def _():
    from sklearn.linear_model import LinearRegression, Lasso 
    from sklearn.neural_network import MLPRegressor
    return Lasso, LinearRegression, MLPRegressor


@app.cell
def _(LinearRegression, Xtr, cross_val_score, ytr):
    lr = LinearRegression()
    lrscore = cross_val_score(lr, Xtr, ytr)
    lrscore
    return


@app.cell
def _(mo):
    mo.md(r"""## Ajustement Lasso""")
    return


@app.cell
def _(mo):
    mo.md(r"""**EXERCICE** Regarder l'impact de l'ajustement du paramètre $\alpha$ dans le modèle Lasso sur le score de cross validation.""")
    return


@app.cell
def _(Lasso):
    la = Lasso()
    return


@app.cell
def _(GridSearchCV, Lasso):
    gcv = GridSearchCV(
        Lasso(), 
        param_grid={
            "alpha": [10**p for p in range(-5, 3)]
    }
    )
    return (gcv,)


@app.cell
def _(Xtr, gcv, ytr):
    gcv.fit(Xtr, ytr)
    gcv.best_params_, gcv.best_score_
    return


@app.cell
def _(gcv):
    gcv.cv_results_
    return


@app.cell
def _(mo):
    mo.md(r"""**REMARQUE** Le meilleur hyperparamètre pour le Lasso semble être $\alpha=0.01$""")
    return


@app.cell
def _(LinearRegression, Xtr, cross_val_score, ytr):
    cross_val_score(LinearRegression(), Xtr, ytr)
    return


@app.cell
def _(Lasso, Xtr, cross_val_score, ytr):
    cross_val_score(Lasso(alpha=0.01), Xtr, ytr)
    return


@app.cell
def _(mo):
    mo.md(r"""**EXERCICE** Regarder comment fonctionne `RandomizedSearchCV`.""")
    return


@app.cell
def _():
    import scipy.stats as stats
    return (stats,)


@app.cell
def _(stats):
    normale = stats.norm()
    normale
    return (normale,)


@app.cell
def _(normale):
    for _ in range(10):
        print(normale.rvs())
    return


@app.cell
def _(Lasso, RandomizedSearchCV, stats):
    rcv = RandomizedSearchCV(Lasso(), dict(alpha=stats.expon()), n_iter=50)
    return (rcv,)


@app.cell
def _(Xtr, rcv, ytr):
    rcv.fit(Xtr, ytr)
    rcv.best_params_, rcv.best_score_
    return


@app.cell
def _(mo):
    mo.md(r"""## Ajustement du réseau de neurones""")
    return


@app.cell
def _(GridSearchCV, MLPRegressor):
    nng = GridSearchCV(
        MLPRegressor(), 
        param_grid=dict(
           hidden_layer_sizes=[
               (3,), (9,), (15,)
           ],
            max_iter=[100000],
        )
    )
    return (nng,)


@app.cell
def _(Xtr, nng, ytr):
    nng.fit(Xtr, ytr)
    nng.best_params_, nng.best_score_
    return


@app.cell
def _():
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    **EXERCICE** déterminer le nombre de paramètres pour chacun des choix d'hyperparamètres.

    Correction au tableau: $12 n +1* paramètres pour une couche cachée de $n$ neurones.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Preprocessing

    [la documentation de MLP](https://scikit-learn.org/stable/modules/neural_networks_supervised.html#tips-on-practical-use)
    suggère que la normalisation des données est critique pour les réseaux de neurones.

    On va assembler un pipeline normalisation suivant du réseau de neurones.
    """
    )
    return


@app.cell
def _():
    from sklearn.preprocessing import MinMaxScaler, StandardScaler
    return MinMaxScaler, StandardScaler


@app.cell
def _():
    from sklearn.pipeline import Pipeline
    return (Pipeline,)


@app.cell
def _(MLPRegressor, Pipeline, StandardScaler):
    assemblage = Pipeline(
        steps=[
            ("normalisation", StandardScaler()),
            ("prediction", MLPRegressor())
        ]
    )
    return (assemblage,)


@app.cell
def _(assemblage):
    assemblage.get_params()
    return


@app.cell
def _(GridSearchCV, assemblage):
    gca = GridSearchCV( 
        assemblage, 
        param_grid=dict(
            prediction__hidden_layer_sizes=[
                (5,), (10,), (15,),
            ], 
            prediction__max_iter=[100000],
        )
    )
    return (gca,)


@app.cell
def _(Xtr, gca, ytr):
    gca.fit(Xtr, ytr)
    gca.best_params_, gca.best_score_
    return


@app.cell
def _(GridSearchCV, MLPRegressor, MinMaxScaler, Pipeline):
    gcm = GridSearchCV(
        Pipeline(
            steps=[
                ("normalisation", MinMaxScaler()),
                ("prediction", MLPRegressor()),
            ],
        ),
        param_grid=dict(
            prediction__hidden_layer_sizes=[
                (5,), (10,), (15,),
            ], 
            prediction__max_iter=[100000],
        )
    )
    return (gcm,)


@app.cell
def _(Xtr, gca, gcm, ytr):
    gcm.fit(Xtr, ytr)
    gcm.best_params_, gca.best_score_
    return


@app.cell
def _(mo):
    mo.md(r"""**EXERCICE** Faite la même chose pour les modèles `KNeighborsRegressor` et `GaussianProcessRegressor`.""")
    return


@app.cell
def _():
    from sklearn.neighbors import KNeighborsRegressor
    return (KNeighborsRegressor,)


@app.cell
def _(GridSearchCV, KNeighborsRegressor):
    gknr = GridSearchCV(
        KNeighborsRegressor(),
        param_grid=dict(
            n_neighbors=range(2, 15),
            weights=["uniform", "distance"],
        )
    )
    return (gknr,)


@app.cell
def _(Xtr, gknr, ytr):
    gknr.fit(Xtr, ytr)
    gknr.best_params_, gknr.best_score_
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
