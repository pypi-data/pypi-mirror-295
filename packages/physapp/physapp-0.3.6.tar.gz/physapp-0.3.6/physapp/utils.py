# David THERINCOURT - 2022
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
Module utils

Fonctions :
-----------

    pround(x, n)

        | Arrondir à N chiffres significatif avec zéro après.
        
    markdownTable(data)
    
        | Présente les valeurs de plusieurs listes (données) dans un tableau au format Markdown.

@author: David Thérincourt - 2023  
"""
import numpy as np
from math import log10




#######################################################
#  Arrondir à N chiffres significatif avec zéro après #
#######################################################
def pround(x, n):
    """ Convertit un flottant en une chaîne de caractères avec n chiffres significatifs.
    
    Paramètres :
        x (float) : valeur à arrondir.
        n (int)   : nombre de chiffres significatifs.

    Retourne :
        (str) : Valeur arrondie.
    """
    x = float(x)
    x0 = abs(x)
    
    if x0<0.01:
        ch = "{:." + str(n-1) + "e}"
        x_str = ch.format(x)
        
    if 0.01<=x0<1:
        ch = "{:." + str(n) + "g}"
        x_str = ch.format(x)
        if x_str=='1':
            if n>1:
                x_str += "."
                x_str += "0"*(n-1)
            return x_str
        else:
            m = x_str.split('.')[-1]
            nx = len(m.split('0')[-1])
            if nx<n:
                x_str += "0"*(n-nx)
                return x_str
            
    if 1<=x0<10000:
        p = int(log10(x0))
        x_str = str(round(x, n-1-p))
        t = x_str.split(".")
        if len(t[0])>=n:
            x_str = x_str[:-2]
        nx = len(t[0]+t[1])
        if nx<n:
            x_str += "0"*(n-nx)
            
    elif 10000<=x0:
        ch = "{:." + str(n-1)+"e}"
        x_str = ch.format(x)
        
    return x_str




#########################################################
#     Sélectionner des valeurs dans un tableau Numpy    #
######################################################### 
def _find_indice_up(x0, x):
    if type(x) == list:
        x = np.array(x)
    if (x[0] <= x0 <= x[-1]):
        return np.where(x>=x0)[0][0]
    else:
        messag = "{} not in x array !".format(x0)
        raise ValueError(messag)
    
def _find_indice_down(x0, x):
    if type(x) == list:
        x = np.array(x)
    if (x[0] <= x0 <= x[-1]):
        return np.where(x<=x0)[0][-1]
    else:
        messag = "{} not in x array !".format(x0)
        raise ValueError(messag)

        
def shape(x, y, xlim_inf, xlim_sup):

    # Trans forme les listes en tableau Numpy
    if type(x) == list:
        x = np.array(x)
    if type(y) == list:
        y = np.array(y)

    # Supprime les valeur à Nan (not a number)
    mask = ~(np.isnan(x) | np.isnan(y)) # masque de suppression des NAN
    x, y = x[mask], y[mask]             # sélectionne les valeur sans NAN   
    
    if xlim_inf==None and xlim_sup==None:
        return x, y, (x[0], x[-1])
    
    if xlim_inf==None:
        xlim_inf=x[0]
    
    if xlim_sup==None:
        xlim_sup=x[-1]
    
    i_inf = _find_indice_up(xlim_inf,  x)
    i_sup = _find_indice_down(xlim_sup,  x)
    
    return x[i_inf:i_sup+1], y[i_inf:i_sup+1], (xlim_inf, xlim_sup)





