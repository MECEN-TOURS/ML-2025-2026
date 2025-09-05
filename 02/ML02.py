import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.optimize import minimize
    from scipy.special import binom 
    return binom, minimize, np, plt


@app.cell
def _(mo):
    mo.md(
        r"""
    # Génération des données

    Fonction $x\mapsto \cos(10 x) e^{-x}$ avec un bruit Gaussien.
    """
    )
    return


@app.cell
def _(np):
    class Echantillon:
        def __init__(self, gauche, droite, bruit, taille_echantillon):
            self.gauche = gauche 
            self.droite = droite
            self.bruit = bruit 
            self.taille_echantillon = taille_echantillon
            self.xs = np.linspace(gauche, droite, taille_echantillon)
            self.ys = self.inconnue(self.xs) + bruit * np.random.randn(taille_echantillon)
    
        def inconnue(self, x):
            return np.cos(10 * x) * np.exp(-x)

        def visualisation(self, rep):
            xs = np.linspace(self.gauche, self.droite, 200)
            ys = self.inconnue(xs)
            rep.plot(xs, ys, color="blue", label="inconnue")
            rep.scatter(self.xs, self.ys, color="red", label="echantillon")
    return (Echantillon,)


@app.cell
def _(Echantillon, plt):
    ech20 = Echantillon(gauche=0., droite=2., bruit=0.1, taille_echantillon=20)
    _, rep = plt.subplots()
    ech20.visualisation(rep)
    rep
    return (ech20,)


@app.cell
def _():
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    # Apprentissage

    On va approcher l'échantillon en

    - minimisant l'erreur quadratique moyenne
    - avec les polynomes de degrés inférieur à $d$
    - en utilisant la base de Bernstein sur l'intervalle $[a,b]$

    $$
    J_2(P) = \frac{1}{N} \sum_{i=1}^N (y_i - P(x_i))^2.
    $$

    $$
    P(X) = \sum_{k=0}^d c_k \binom{d}{k} \left(\frac{X - a}{b-a}\right)^k \left(1 - \frac{X - a}{b-a}\right)^{d-k}
    $$
    """
    )
    return


@app.cell
def _(binom, minimize, np):
    class Bernstein:
        def __init__(self, degres, a, b):
            self.a = a 
            self.b = b
            self.degres = degres
            self.coefficients = np.zeros(degres + 1)

        def predict(self, xs):
            resultat = np.zeros_like(xs)
            variable = (xs - self.a) / (self.b - self.a)
            for (k, c) in enumerate(self.coefficients):
                resultat = (
                    resultat 
                    + c 
                    * binom(self.degres, k) 
                    * np.power(variable, k) 
                    * np.power(1. - variable, self.degres - k)
                )
            return resultat

        def fit(self, xs, ys):
            def a_minimiser(coefficients):
                self.coefficients = coefficients
                return self.erreur(xs, ys)
            
            resultat = minimize(a_minimiser, self.coefficients)
            if not resultat.success:
                print(resultat)
            self.coefficients = resultat.x
    
        def erreur(self, xs, ys):
            return np.mean((self.predict(xs) - ys) ** 2)
    return (Bernstein,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    **EXERCICE** visualiser les polynomes de Bernstein de degrés $2$ de coefficients

    - $(1, 0, 0)$
    - $(0, 1, 0)$
    - $(0, 0, 1)$
    """
    )
    return


@app.cell
def _(Bernstein, np, plt):
    # Vérification de predict
    _P001 = Bernstein(degres=2, a=0, b=2)
    _P001.coefficients = np.array((0, 0, 1))
    _P100 = Bernstein(degres=2, a=0, b=2)
    _P100.coefficients = np.array((1, 0, 0))
    _P010 = Bernstein(degres=2, a=0, b=2)
    _P010.coefficients = np.array((0, 1, 0))

    _xs = np.linspace(0, 2, 200)
    plt.plot(_xs, _P001.predict(_xs))
    plt.plot(_xs, _P010.predict(_xs))
    plt.plot(_xs, _P100.predict(_xs))
    return


@app.cell
def _(Bernstein, np, plt):
    def experience(degres, echantillon):
        P2 = Bernstein(degres, a=0, b=2)
        P2.fit(echantillon.xs, echantillon.ys)
    
        _, rep = plt.subplots()
        rep.set_title(f"d={degres}")
        echantillon.visualisation(rep)
        xs = np.linspace(echantillon.gauche, echantillon.droite, 200)
        rep.plot(xs, P2.predict(xs), color="cyan", label="prédicteur")
        rep.legend()
        return rep
    return (experience,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**EXERCICE** Expérimenter avec des degrés plus élevés.""")
    return


@app.cell
def _(ech20, experience):
    experience(degres=2, echantillon=ech20)
    return


@app.cell
def _(ech20, experience):
    experience(degres=5, echantillon=ech20)
    return


@app.cell
def _(ech20, experience):
    experience(degres=7, echantillon=ech20)
    return


@app.cell
def _(ech20, experience):
    experience(degres=10, echantillon=ech20)
    return


@app.cell
def _(ech20, experience):
    experience(degres=15, echantillon=ech20)
    return


@app.cell
def _(ech20, experience):
    experience(degres=20, echantillon=ech20)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Méthodologie

    Dans la situation présente on connait l'échantillon (points rouges) et la fonction inconnue.
    On peut donc juger de l'adéquation à l'échantillon mais aussi de la capacité du modèle à généraliser.

    Dans la pratique, on aura que l'échantillon.
    Comment peut-on juger de la capacité du modèle à généraliser?
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    **EXERCICE** Ajouter une possibilité dans la classe échantillon de générer les abcisses en utilisant la loi uniforme plutot qu'en découpant régulièrement l'intervalle.
    Reprendre alors l'expérience ci-dessus.
    """
    )
    return


@app.cell
def _(np, plt):
    class EchantillonV2:
        def __init__(self, gauche, droite, bruit, taille_echantillon, aleatoire=False):
            self.gauche = gauche 
            self.droite = droite
            self.bruit = bruit 
            self.taille_echantillon = taille_echantillon
            if aleatoire:
                self.xs = np.random.uniform(low=self.gauche, high=self.droite, size=(self.taille_echantillon,))
            else:
                self.xs = np.linspace(gauche, droite, taille_echantillon)
            self.ys = self.inconnue(self.xs) + bruit * np.random.randn(taille_echantillon)
    
        def inconnue(self, x):
            return np.cos(10 * x) * np.exp(-x)

        def visualisation(self, rep=None, couleur=None):
            if couleur is None:
                couleur="red"
            if rep is None:
                _, rep = plt.subplots()
            xs = np.linspace(self.gauche, self.droite, 200)
            ys = self.inconnue(xs)
            rep.plot(xs, ys, color="blue", label="inconnue")
            rep.scatter(self.xs, self.ys, color=couleur, label="echantillon")
            return rep
    return (EchantillonV2,)


@app.cell
def _(EchantillonV2):
    ech30 = EchantillonV2(gauche=0., droite=2., bruit=0.1, taille_echantillon=30, aleatoire=True)
    ech30.visualisation()
    return (ech30,)


@app.cell
def _(ech30, experience):
    experience(degres=10, echantillon=ech30)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    **REMARQUE** On voit que la capacité du modèle à généraliser dans les zones où il y a peu de points rouges est limité.
    On va donc séparer l'échantillon en deux

    1. Une partie servira encore à l'entrainement
    2. Une autre partie sera laissée de coté pendant l'entrainement et permettra de tester la capacité à généraliser

    On appelle cette méthode un `train_test_split`.

    **EXERCICE** Coder une fonction `train_test_split` prenant en entrée un échantillon et le découpant en deux de manière aléatoire suivant une certaine proportion.
    """
    )
    return


@app.cell
def _(EchantillonV2, np):
    def train_test_split(
        echantillon: EchantillonV2, 
        proportion: float = 0.7
    ) -> tuple[EchantillonV2, EchantillonV2]:
        if proportion < 0 or proportion > 1:
            raise ValueError("Proportion doit etre entre 0 et 1")
        x_tr, y_tr, x_te, y_te = [], [], [], []
        for x, y in zip(echantillon.xs, echantillon.ys):
            if np.random.rand() < proportion:
                x_tr.append(x)
                y_tr.append(y)
            else:
                x_te.append(x)
                y_te.append(y)

        ech_tr = EchantillonV2(
            gauche=echantillon.gauche,
            droite=echantillon.droite, 
            bruit=echantillon.bruit, 
            taille_echantillon=len(x_tr),
        )
        ech_tr.xs = np.array(x_tr)
        ech_tr.ys = np.array(y_tr)
        ech_te = EchantillonV2(
            gauche=echantillon.gauche,
            droite=echantillon.droite, 
            bruit=echantillon.bruit, 
            taille_echantillon=len(x_te),
        )
        ech_te.xs = np.array(x_te)
        ech_te.ys = np.array(y_te)
        return ech_tr, ech_te
    return (train_test_split,)


@app.cell
def _(ech30, train_test_split):
    ech30_tr, ech30_te = train_test_split(echantillon=ech30, proportion=0.7)
    return ech30_te, ech30_tr


@app.cell
def _(ech30_te, ech30_tr):
    _rep = ech30_tr.visualisation(couleur="red")
    ech30_te.visualisation(rep=_rep, couleur="green")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**EXERCICE** Afficher les courbes d'erreur de la partie training et de la partie test en fonction du degrés du modèle utilisé.""")
    return


@app.cell
def _(Bernstein, plt):
    def courbes_erreurs(ech_tr, ech_te, dmax):
        erreurs_tr, erreurs_te = [], []
        for d in range(2, dmax+1):
            bern = Bernstein(a=ech_tr.gauche, b=ech_tr.droite, degres=d)
            bern.fit(ech_tr.xs, ech_tr.ys)
            erreurs_tr.append(bern.erreur(ech_tr.xs, ech_tr.ys))
            erreurs_te.append(bern.erreur(ech_te.xs, ech_te.ys))

        _, rep = plt.subplots()
        rep.set_title(f"N={ech_tr.taille_echantillon}")
        rep.set_xlabel("degre du polynome")
        rep.semilogy(range(2, dmax+1), erreurs_tr, label="entrainement")
        rep.semilogy(range(2, dmax+1), erreurs_te, label="test")
        rep.legend()
        return rep
    return (courbes_erreurs,)


@app.cell
def _(courbes_erreurs, ech30_te, ech30_tr):
    courbes_erreurs(ech_te=ech30_te, ech_tr=ech30_tr, dmax=20)
    return


@app.cell
def _(EchantillonV2, train_test_split):
    ech60 = EchantillonV2(gauche=0., droite=2., bruit=0.1, taille_echantillon=60, aleatoire=True)
    ech60_tr, ech60_te = train_test_split(echantillon=ech60, proportion=0.7)
    _rep = ech60_tr.visualisation(couleur="red")
    ech60_te.visualisation(rep=_rep, couleur="green")
    return ech60_te, ech60_tr


@app.cell
def _(courbes_erreurs, ech60_te, ech60_tr):
    courbes_erreurs(ech_te=ech60_te, ech_tr=ech60_tr, dmax=30)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
     **CONCLUSION** On voit qu'au début les deux erreurs diminuent lorsque la complexité du modèle augmente.
     Par contre, il finit par se passer un décrochage entre l'erreur d'entrainement qui continue à diminuer et celle de test qui augmente.
    """
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
