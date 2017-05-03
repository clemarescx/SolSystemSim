#!/usr/bin/python3

# DATA SOM BESKRIVER TILSTANDEN 19.4.2017 00:00:00 (ASTRONOMISK TID, omtrent 69 sekunder foran UTC)
# Hentet fra JPL Horizons https://ssd.jpl.nasa.gov/horizons.cgi
import sys
import numpy

# Måleenhet for TID: døgn: 1 d = 86400 s (Middelsoldøgn, altså 24 timer)
# Måleenhet for AVSTAND: AU (astronomiske enheter) 1 au = 149597870699 m
# Måleenhet for HASTIGHET: Astronomiske enheter pr. døgn.
# Måleenhet for AKSELERASJON: au/d^2

ANTALL_METER_I_EN_AU = 149597870699.0
ANTALL_SEKUNDER_I_ET_DØGN = 86400.0

#NEWTONS KONSTANT, i ulike måleenhetssystemer:
NEWTONS_KONSTANT_STD = 6.67408e-11 # m^3/(kg*s^2)
NEWTONS_KONSTANT_AU = NEWTONS_KONSTANT_STD / ANTALL_METER_I_EN_AU**3 * ANTALL_SEKUNDER_I_ET_DØGN**2 # au**3/(kg*d^2)


class planet:
    def __init__(self,x,y,z,vx,vy,vz,masse,navn = "UKJENT"):
        self.pos = numpy.array([x,y,z])
        self.fart = numpy.array([vx,vy,vz])
        self.masse = masse
        self.navn = navn
        self.others = list() # TOM LISTE
    
    def __str__(self):
        return "({0}, {1}, {2}) ({3})".format(*self.pos,**self.navn)

    
    def legg_til_nabo(self, other):
        self.others.append(other)

    def gravitasjon(self,pos):
        """ regner ut akselerasjonen til et legeme i posisjon 'pos'
        som følge av gravitasjonskraften fra denne planeten,
        utifra Newtons gravitasjonslov"""
        forflytning = self.pos-pos # Peker mot 'self'
        avstand = numpy.sqrt(forflytning.dot(forflytning))
        return forflytning * NEWTONS_KONSTANT_AU * self.masse / avstand**3

    def akselerasjon(self):
        a = numpy.array([0.0,0.0,0.0])
        for o in self.others:
            a += o.gravitasjon(self.pos)
        return a


    def euler(self,steglengde):
        akselerasjon = self.akselerasjon()
        self.pos += self.fart*steglengde 
        self.fart += akselerasjon*steglengde

    def semiimplisitt_euler_A(self,steglengde):
        self.fart += self.akselerasjon()*steglengde
        self.pos += self.fart*steglengde

    def semiimplisitt_euler_B(self,steglengde):
        self.pos += self.fart*steglengde
        self.fart += self.akselerasjon()*steglengde





# LEGEME             x                       y                       z                       vx                      vy                              vz                 mn       navn
SOL     =   planet( 3.043214707062220e-03,  4.653316939537629e-03, -1.487620752755869e-04, -3.766740500322170e-06,  6.471546046067104e-06,  8.456284103527783e-08, 1.988544e30, "Sola"  )
JORD    =   planet(-8.762736739504592E-01, -4.806132137534411E-01, -1.262360996138753E-04,  8.023506896593865E-03, -1.512365998243756E-02,  1.172844898850050E-06, 5.97219e24,  "Jorda" )
LUNA   =    planet(-8.751828476689488E-01, -4.830382477575933E-01,  1.698414685680612E-05,  8.528548281530733E-03, -1.486940505004675E-02, -4.044722740074771E-05, 7.349e22,    "Månen" )
MARS =      planet( 3.573307903995526E-01,  1.499668239413485E+00,  2.248516938651534E-02, -1.309021310215260E-02,  4.424052391590009E-03,  4.138239373671828E-04,  6.4185e23)
JUPITER =   planet(-5.158650533447512E+00, -1.757624959474611E+00,  1.226686713441053E-01,  2.345064553996783E-03, -6.785148245133824E-03, -2.429251889171018E-05, 1898.13e24,  "Jupiter")


PLANETER = [SOL,JORD,LUNA,MARS,JUPITER]

for a in PLANETER:
    for b in PLANETER:
        if a==b:
            continue
        a.legg_til_nabo(b)

def print_data_line(sep=" ",fil=sys.stdout):
    print(*( a for p in PLANETER for  a in (p.pos[0],p.pos[1])),sep=sep,file=fil)
    





if __name__=='__main__':
    
    print(SOL.gravitasjon(JORD.pos))

    print(JORD.akselerasjon())
    print(LUNA.akselerasjon())
    print(*JORD.others,sep='\n')

    print_data_line()
