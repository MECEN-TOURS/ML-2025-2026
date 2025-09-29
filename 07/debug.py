"""Description.

Utilisation du déboggueur.
Avec
- breakpoint() dans le code
- ou `python -d` pour rentrer dans le code à la première erreur
"""


def fibonacci(n):
    a, b = 0, 1
    breakpoint()
    for _ in range(n):
        a, b = b, a + b
    return a


fibonacci(5)
