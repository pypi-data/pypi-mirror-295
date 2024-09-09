# Librairie Python pour la physique appliquée

## Installation

Dans un terminal :

    pip install physapp

Mise à jour :

```python
pip install --upgrade physapp
```

---

## Dépendances

Cette librairie se base principalement sur les librairies `numpy (>= 1.26.0)` , `matplotlib (>= 3.8.0)` et `scipy (>= 1.11.0)`.

---

## Module `physapp.base`

### > Fonctions disponibles

`derive(y, x)`

`integrale(y, x, xinf, xsup)`

`spectre_amplitude(y, t, T)`

`spectre_RMS(y, t, T)`

`spectre_RMS_dBV(y, t, T)`

### > Exemple

```python
import numpy as np
import matplotlib.pyplot as plt
from physapp import integrale

### IMPORTATION DES DONNEES ###
t, u = np.loadtxt('scope.csv', delimiter=',', skiprows=2, unpack=True)

### CALCULS ###
f = 125
T = 1/f
aire = integrale(u, t, 0, T, plot_ax=plt)
moy = aire/T

### COURBES ###
plt.plot(t, u)
plt.axhline(moy, ls="--", color="C3")
plt.text(0.65*T, moy+0.2, "Moy = {:.2f} V".format(moy), color="C3")
plt.title("Valeur moyenne d'un signal périodique")
plt.xlabel("t (s)")
plt.ylabel("u (V)")
plt.grid()
plt.show()
```

![](https://github.com/david-therincourt/physapp/blob/main/docs/integrale.png?raw=true)

## Module `physapp.modelisation`

Fonctions pour réaliser une modélisation d'une courbe expérimentale.

### > Fonctions classiques

| Fonction                                       | Description               |
| ---------------------------------------------- | ------------------------- |
| `ajustement_lineaire(x, y)`                    | $y=a\cdot x$              |
| `ajustement_affine(x, y)`                      | $y=a\cdot x+b$            |
| `ajustement_parabolique(x, y)`                 | $y=a\cdot x^2+b\cdot x+c$ |
| `ajustement_exponentielle_croissante(x, y)`    | $y=A\cdot(1-e^{-x/\tau})$ |
| `ajustement_exponentielle_decroissante(x, y)`  | $y = A\cdot e^{-x/\tau}$  |
| `ajustement_exponentielle2_croissante(x, y)`   | $y = A\cdot(1-e^{-kx})$   |
| `ajustement_exponentielle2_decroissante(x, y)` | $y = A\cdot e^{-kx}$      |
| `ajustement_puissance(x, y)`                   | $y=A\cdot x^n$            |

### > Réponses fréquentielles

`ajustement_ordre1_passe_bas_transmittance(f, T)`

`ajustement_ordre1_passe_bas_gain(f, G)`

`ajustement_ordre1_passe_bas_dephasage(f, phi)`

`ajustement_ordre1_passe_haut_transmittanc(f, T)`

`ajustement_ordre1_passe_haut_gain(f, G)`

`ajustement_ordre1_passe_haut_dephasage(f, phi)`

`ajustement_ordre2_passe_bas_transmittance(f, T)`

`ajustement_ordre2_passe_haut_transmittance(f, T)`

`ajustement_ordre2_passe_haut_dephasage(f, phi)`

`ajustement_ordre2_passe_bande_transmittance(f, T)`

`ajustement_ordre2_passe_bande_gain(f, G)`

`ajustement_ordre2_passe_bande_dephasage(f, phi)`

### > Exemple

```python
import matplotlib.pyplot as plt
from physapp.modelisation import ajustement_parabolique

x = [0.003,0.141,0.275,0.410,0.554,0.686,0.820,0.958,1.089,1.227,1.359,1.490,1.599,1.705,1.801]
y = [0.746,0.990,1.175,1.336,1.432,1.505,1.528,1.505,1.454,1.355,1.207,1.018,0.797,0.544,0.266]

modele = ajustement_parabolique(x, y)
print(modele)

plt.plot(x, y, '+', label="Mesures")
modele.plot()                        # Trace la courbe du modèle         
#modele.legend()                     # Affiche la légende du modèle
plt.legend()
plt.title("Trajectoire d'un ballon")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.grid()
plt.show()
```

Résultat :

```python
Fonction parabolique
y = a*x^2 + b*x + c
a = (-1.25 ±0.060)
b = (2.04 ±0.11)
c = (0.717 ±0.045)
Intervalle de confiance à 95% sans incertitudes sur x et y.
```

![](https://github.com/david-therincourt/physapp/blob/main/docs/modelisation.png?raw=true)

---

## Module `physapp.csv`

Module d'importation de tableau de données au format CSV à partir des logiciels Aviméca3, Regavi, ...

#### > Fonctions disponibles

`load_txt(fileName)`

`load_avimeca3_txt(fileName)`  

`load_regavi_txt(fileName)`

`load_regressi_txt(fileName)`

`load_regressi_csv(fileName)`

`load_oscillo_csv(filename)`

`load_ltspice_csv(filename)`

`save_txt(data, fileName)`

---
