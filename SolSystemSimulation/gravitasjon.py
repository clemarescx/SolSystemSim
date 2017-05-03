#!/usr/bin/python3

from geometri2D import punkt2D,vektor2D,forflytning
from figur import figur

# MER ELLER MINDRE TILFELDIG VALGTE VERDIER
STEGLENGDE = 1
T = 100000
G = 0.02
M1 = 1
M2 = 1
O = punkt2D(0,0)

X0 = punkt2D(3,0)
V0 = vektor2D(0,0.1)

# NEWTONS GRAVITASJONSLOV
def sentralGravitasjon(pos):
    d = forflytning(O,pos)
    r = d.lengde()
    return -G*M1*M2/r**3*d

    
# SIMULERINGSSTEG, MED KONSTANT AKSELERASJON
def neste_konstant_akselerasjon(x,v,m = M1,kraft = sentralGravitasjon,h = STEGLENGDE):
    kraft = sentralGravitasjon(x)
    a = 1.0/m*kraft
    nyV = v+h*a
    nyX = x + h*v + 0.5*h**2*a
    return nyX,nyV

# SIMULERINGSSTEG, Euler (Konstant fart)
def neste_euler(x,v,m = M1,kraft = sentralGravitasjon,h = STEGLENGDE):
    kraft = sentralGravitasjon(x)
    a = 1.0/m*kraft
    nyV = v+h*a
    nyX = x + h*v
    return nyX,nyV

# SIMULERINGSSTEG, Forbedret Euler (Konstant fart)
def neste_euler_semiimplisitt(x,v,m = M1,kraft = sentralGravitasjon,h = STEGLENGDE):
    kraft = sentralGravitasjon(x)
    a = 1.0/m*kraft
    nyV = v+h*a
    nyX = x + h*nyV
    return nyX,nyV

# SIMULERINGSSTEG, Leapfrog
def neste_leapfrog(x,v,m = M1, kraft = sentralGravitasjon, h = STEGLENGDE):
    a = 1.0/m*sentralGravitasjon(x)
    nyX = x + h*v + 0.5*h**2*a
    nyA = 1.0/m*sentralGravitasjon(nyX)
    nyV = v+0.5*h*(a+nyA)
    return nyX,nyV


neste = neste_euler_semiimplisitt

# KJØRING AV MANGE STEG MED GENERATOR.
def simulering(n):
    x,v = X0,V0
    yield x
    for i in range(n):
        x,v = neste(x,v)
        yield x


if __name__=='__main__':
    fig = figur(800,800)
    fig.xmin,fig.ymin,fig.xmax,fig.ymax = -10,-10,10,10
    O.tegn(fig)
    fig.kurve(*zip(*((a.x, a.y) for a in simulering(1000))))
    fig.kurve(*zip(*(simulering(int(T/STEGLENGDE)))))
    fig.vis()
