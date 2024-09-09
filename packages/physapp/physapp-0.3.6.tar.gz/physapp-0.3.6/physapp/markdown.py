# David THERINCOURT - 2023
#
# The MIT License (MIT)
#
# Copyright (c) 2014-2019 Damien P. George
# Copyright (c) 2017 Paul Sokolovsky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Module pour l'exportation des données vers un tableau Markdown

Fonctions
---------

    markdown_table(*args, header = [], col_witdh = 12, nb_round = 4)
    
        | Retourne un tableau au format Markdown à partir de plusieurs listes ou tableaux Numpy.
    
    
Example
-------

    >>> x = [1,2,3,4,5]
    >>> y = [45,23,58,69,56]
    >>> z = [8,9,10,23,78]
    >>> table = markdown_table(x, y, z)
    >>> print(table)

    |     var_1    |     var_2    |     var_3    |
    | ------------ | ------------ | ------------ |
    | 1            | 45           | 8            |
    | 2            | 23           | 9            |
    | 3            | 58           | 10           |
    | 4            | 69           | 23           |
    | 5            | 56           | 78           |

    >>> table = markdown_table(x, y, z, header=['x', 'y', 'z'])
    >>> print(table)

    |       x      |       y      |       z      |
    | ------------ | ------------ | ------------ |
    | 1            | 45           | 8            |
    | 2            | 23           | 9            |
    | 3            | 58           | 10           |
    | 4            | 69           | 23           |
    | 5            | 56           | 78           |

        
@author: David Thérincourt - 2023
"""

import numpy as np


def _celluleText(text: str, width: int) -> str:
    space_before = (width - len(text))//2
    space_after = width - len(text) - space_before
    return "| " + " "*space_before + text + " "*space_after

def _celluleValue(x: float, width: int, nb_round:int) -> int:
    formater = "{:." + str(nb_round) + "g}"
    val = formater.format(x)
    return "| " + val + " "*(width - len(val)) 
    

def markdown_table(*args, header: list = [], col_witdh: int = 12, nb_round: int = 4) -> str:
    """ Retourne un tableau au format Markdown à partir des plusieurs listes ou tableaux Numpy.

    Paramètres :
        *args       (list)     : tableaux des données à afficher dans le tableau Markdown

    Paramètres optionnels :    
        header      (1D array) : liste des étiquettes de l'entête.
        col_witdh   (int)      : largeur en caractères d'une colonne.
        nb_round    (int)      : nombre de chiffres significatifs pour les arrondis.

    Retourne :
        (str) : chaîne de caractères au format Markdown
    """

    data = list(zip(*args)) # Transposition des listes
 
    nb_row = len(data)
    nb_col = len(data[0])
    witdh = col_witdh + 1
    md_table = ""

    ### Ajoute noms des entêtes par défaut
    if header==[]:
        for i in range(nb_col):
            header.append("var_{}".format(i+1))
    
    if len(header) != nb_col:
        raise Exception("Taille de la liste de l'argument header non conforme au nombre de colonnes à afficher !")

    ### Ligne d'entête        
    for i in range(nb_col):
        md_table += _celluleText(header[i], witdh)
    md_table += "|\n"
    
    ### Ligne de sépration
    for i in range(nb_col):
        md_table += "| " + "-"*(witdh-1) + " "
    md_table += "|\n"
    
    ### Ligne de données
    for i in range(nb_row):
        for j in range(nb_col):
            md_table += _celluleValue(data[i][j], witdh, nb_round)
        md_table += "|\n"
    
    return md_table


if __name__ == "__main__":
    x = [1,2,3,4,5]
    y = [45,23,58,69,56]
    z = [8,9,10,23,78]
    table = markdown_table(x, y, z, header=['x', 'y', 'z'])
    print(table)





