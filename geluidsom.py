# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 16:51:31 2020

@author: A642983
"""

import numpy as np
import pandas as pd
import numpy.array as a


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

# program----------------------------------------------
if __name__=="__main__":
# data input 
    #geluidsvermogens vanuit Reitz
    LwA = pd.DataFrame(
        data = {
           'octaves'       :[63,     125,   250,   500, 1000, 2000, 4000, 8000],
            'voor_demper':[88.6,   93,  90.9,  78.3, 67.9, 71.1, 77.2, 73.9],
            'huis'       :[85.2, 93.6, 100.5, 100.9, 99.3, 95.2, 88.7, 79.5]
        }
    )
    LwA = LwA.set_index('octaves')
    
    # ruwe dimensies van 1 fan
    box_fan = a([4,3,3])  #l, b, h
    #ruwe dimensies van ruimte
    box_ruimte = a([16.8, 8, 5]) 
    
#afgeleide waarden LwA
    LwA['tot_1_fan'] = dB_add( [ 
            LwA['voor_demper'], 
            LwA['huis']
        ])
    LwA['tot_2_fans'] = dB_multiply(LwA['tot_1_fan'], 2)
    

# LpA waarden, voor verscillende lokaties

    # Reitz defineert "1 meter afstand van fan" als een rechthoekige doos rondom de fan

    sound_box_fan = box_fan + a([2., 2.,1.])  # 1 meter afstand rondom de box en naar boven
    sound_box_area = area_of_box(sound_box_fan) - sound_box_fan[1]* sound_box_fan[2] #oppervlak van sound_box, geen vloer
    
    LpA = pd.DataFrame()
    # LpA op 1 meter afstand van fan, aanname dat vermogen gelijk verdeelt is over rechthoekige doos
    LpA['huis_1meter'] = dB_multiply(
                LwA['huis'], 
                1./sound_box_area
            )
    # LpA op 1 meter voor demper, aanname dat geluid over halve  bol verdeeld is
    LpA['voor_demper_1m'] = Lp_direct_point(
            Lw=LwA['voor_demper'],
            r=1.,
            Q= 2.  #halve bol voor demper
        )
    # LpA 2 meter naast midden van demper, aanname dat geluid over halve bol verdeeld is. 
    LpA['voor_demper_2m'] = Lp_direct_point(   
            Lw=LwA['voor_demper'],
            r=1.,
            Q= 2.  #halve bol voor demper
        )
    # LpA 1 meter naast fan (ongeveer 2m naast midden van demper), dus gezamenlijk effect van huis en demper
    LpA['naast_fan_1m'] = dB_add([
            LpA['huis_1meter'],
            LpA['voor_demper_2m']
        ])
    # 2 fans. 1 meter afstand fan 1 van is ook ongeveer 1 meter afstand van fan ernaast, dus piek is beide bij elkaar
    LpA['naast_2fans_1m'] = dB_multiply( LpA['naast_fan_1m'] , 2)  # hoogste geluid is tussen twee fans in
    
# diffuus veld

    
    
