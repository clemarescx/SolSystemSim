#!/usr/bin/python3

from geometri2D import punkt2D,vektor2D,forflytning
from figur import figur
from planeter import PLANETER,print_data_line

import numpy

#MÅLEENHETER FOR TID
DØGN = 1.0
ÅR = 365.25*DØGN
TIME = DØGN/24
MINUTT = TIME/60


# BETINGELSER FOR SIMULERINGEN
STEGLENGDE = TIME
T = 3*ÅR
N = int(T/STEGLENGDE)


def solsystemGenerator(n=N):
    for i in range(n):
        for planet in PLANETER:
            planet.semiimplisitt_euler_B(STEGLENGDE/2)
        for planet in PLANETER:
            planet.semiimplisitt_euler_A(STEGLENGDE/2)

        yield tuple((planet.pos[0],planet.pos[1]) for planet in PLANETER)

def testMedAnimasjon():
    from animasjon import animasjon
    animasjon(solsystemGenerator())


def testMedStatiskFigur():

    fig = figur(1000,1000)

#   fig.xmin,fig.ymin,fig.xmax,fig.ymax = -.9,-1.2,0,-.4 # INNZOOMING PÅ START
#   fig.xmin,fig.ymin,fig.xmax,fig.ymax = -1.1,-1.1,1.1,1.1 # OVERBLIKK
    fig.xmin,fig.ymin,fig.xmax,fig.ymax = -6,-6,6,6 # OVERBLIKK MED JUPITER
#   fig.xmin,fig.ymin,fig.xmax,fig.ymax = -.01,-.01,.01,.01 # FOR Å SE PÅ MÅNEN SETT FRA JORDA.
    
    for state in solsystemGenerator():
        for planet in state:
            fig.dot(planet[0],planet[1])
    fig.vis()



if __name__=='__main__':
    testMedStatiskFigur()
    testMedAnimasjon()
