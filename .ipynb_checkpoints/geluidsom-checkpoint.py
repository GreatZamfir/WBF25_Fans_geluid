# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 16:51:31 2020

@author: A642983
"""

import numpy as np
import pandas as pd
from numpy import array as a


# formulas -------
def dB_to_value(in_dB): 
    return (10.0**(in_dB/10.0 ))
            
def value_to_dB(value): 
    return 10.0*np.log10(value)

def dB_sum(levels, axis = None):
    #logaritmische som over een matrix 'levels' in decibel,  in richting 'axis'
    non_dB = dB_to_value(levels)
    non_dB_total = np.sum(non_dB, axis =axis)
    return  value_to_dB(non_dB_total)

def dB_add(levels_list):
    # logaritmische som van levels in decibel
    #  levels_list = list van waarden of matrices "levels". matrices moeten gelijkvormig zijn

    non_dB = [ 10.0**(levels/10.0 ) for levels in levels_list]
    non_dB_total = sum(non_dB)
    return 10.0*np.log10( non_dB_total)
    
def dB_multiply(levels, factor):
    #logaritmische vermenigvuldiging van een matrix 'levels' in decibel,  in richting 'axis'
    return levels + 10.0*np.log10(factor)

def area_of_box(l, b=None,h=None):
    try: #l is iterable
        h = l[2]
        b = l[1]
        l = l[0]
    except TypeError:
        pass #not an iterable
    # totaal oppervlakte van alle wanden van een rechthoekige doos
    return 2*(l*b + b*h + l*h)

def area_of_sphere(r):
    return 4*np.pi*r**2

def Lp_direct_point(Lw, r, Q):
    # Lp waarde op basis van Lw, afstand r en direction factor Q. Q =2 voor vlakke vloer, 4 voor vloer+muur, 8 voor kamer-hoek
    return dB_multiply(Lw, Q/area_of_sphere(r))

def room_coefficient(oppervlaktes, absorpties):
    #berekent room_coefficient voor sabine vergelijking
    # r is frequentie-afhankelijk
    # R[f] = sum(S_i * alpha_i[f])/ 1 - (alpha_gemiddeld[f])
    
    #input: oppervlaktes: [N] array 
    #       absorpties:   [NxM] array, absorptie per oppervlk en per frequentie-band
    #  output:  [M] array, per frequentie-band
    S_keer_alpha = absorpties.dot(oppervlaktes)
    S_tot = np.sum(oppervlaktes)
    alpha_gem = S_keer_alpha/S_tot
    
    return S_keer_alpha/(1-alpha_gem)
    
    
    
    
# program----------------------------------------------
if __name__=="__main__":
    pass

    
    
