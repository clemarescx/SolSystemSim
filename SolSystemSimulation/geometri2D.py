#!/usr/bin/python3

from functools import singledispatch
import math

class punkt2D:
    """Representerer 2D-punkter"""
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    def __str__(self,):
        return "Punkt({0}, {1})".format(self.x,self.y)

    def __repr__(self):
        return str(self)

    def __add__(self,vektor):
        return punkt2D(self.x+vektor.x, self.y+ vektor.y)
    
    def __iter__(self):
        return self.generator()

    def generator(self):
        yield self.x
        yield self.y
    
    def posVektor(self):
        return vektor2D(self.x,self.y)        

    def tegn(self,fig):
        fig.punkt(self.x,self.y)

def forflytning(A,B):
    return B.posVektor()-A.posVektor()

def distanse(A,B):
    forflytning(A,B).lengde()

        
class vektor2D:
    """Representerer 2D-punkter"""
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return "[{0}, {1}]".format(self.x,self.y)
   
    def __repr__(self):
        return str(self)

    def __iter__(self):
        return self.generator()

    def generator(self):
        yield self.x
        yield self.y

    def __add__(self,other):
        """Definerer vektoraddisjon"""
        return vektor2D(self.x+other.x,self.y+other.y)
        
    def __rmul__(self,skalar): 
        """Skalering av vektorer"""
        return vektor2D(self.x*skalar,self.y*skalar)
    
    def __div__(self,skalar): 
        """Skalering av vektorer"""
        return vektor2D(self.x/skalar,self.y/skalar)

    def __sub__(self,other):
        """Vektorsubtraksjon"""
        return self+(-1)*other

    def roter90(self):
        return vektor2D(-self.y,self.x)

    def somPunkt(self):
        return punkt2D(self.x,self.y)

    def prikk(self,other):
        """Skalarproduktet / (dot-product)"""
        return self.x*other.x+self.y*other.y
    
    def lengde(self):
        """ Lengden til vektoren. Bygger på Pythagoras' teorem"""
        return math.sqrt(self.x*self.x+self.y*self.y)
        
    def vinkel(self,other):
        """ Regner ut vinkelen mellom to vektorer, i grader
        u = vektor2D(1,3)
        v = vektor2D(3,1)
        vinkel = u.vinkel(v)
        """
        vinkelIRadianer = math.acos(self.prikk(other)/self.lengde()/other.lengde())
        vinkelIGrader = math.degrees(vinkelIRadianer)
        return vinkelIGrader
    
    def tegn(self,fig):
        """ Tegner vektoren på figuren `fig` med utgangpunkt i origo """
        fig.vektor(0,0,self.x,self.y)
    
    def tegnFra(self,punkt,fig):
        """ Tegner vektoren på figuren `fig` med utgangpunkt i `punkt`"""
        fig.vektor(punkt.x, punkt.y, punkt.x + self.x, punkt.y + self.y)


class linje2D:
    
    def __init__(self,punkt,normal):
        self.normal = (1.0/normal.lengde())*normal # Normalisering
        self.c = self.normal.prikk(punkt.posVektor())

    @staticmethod
    def gjennomPunkter(A,B):
        v = B.posVektor() - A.posVektor()
        return linje2D.gjennomPunktLangsVektor(A,v)

    @staticmethod
    def gjennomPunktLangsVektor(A,v):
        return linje2D(A,v.roter90())

    def dist(self,punkt):
        """Måler vinkelrett avstand mellom linjen og punktet 'punkt' 
        positiv avstand betyr at 'punkt' ligger i halvplanet som 
        normalvektoren peker mot."""
        return self.normal.prikk(punkt.posVektor()) - self.c

    def tegn(self,fig):
        if self.normal.y*(fig.xmax-fig.xmin) > self.normal.x*(fig.ymax-fig.ymin):
            x0 = fig.xmin;
            y0 = (self.c - self.normal.x*x0)/self.normal.y
            x1 = fig.xmax;
            y1 = (self.c - self.normal.x*x1)/self.normal.y
        else:
            y0 = fig.ymin;
            x0 = (self.c-self.normal.y*y0)/self.normal.x
            y1 = fig.ymax;
            x1 = (self.c-self.normal.y*y1)/self.normal.x

        fig.linje(x0,y0,x1,y1)



class sirkel2D:
    def __init__(self,sentrum,radius):
        self.sentrum = sentrum
        self.radius = radius
    
    def dist(self,punkt):
        """Måler avstand mellom punkt og sirkel. Avstanden er positiv når punktet ligger utenfor sirkelen"""
        return (self.sentrum.posVektor()-punkt.posVektor()).lengde() - self.radius

    def skjæring(self,other):
        if (isinstance(other,linje2D)):
            return self._linjeSkjæring(other)
        else:
            raise NotImplementedError("Unsupported operation")

    def _linjeSkjæring(self,linje):
        d = linje.dist(self.sentrum)
        if (d**2 > self.radius**2):
            return ()
        midtpunkt = self.sentrum.posVektor() - d*linje.normal 
        if (d**2 == self.radius**2):
            return (midpunkt.somPunkt(),)
        else:
            korrigering = math.sqrt(self.radius**2-d**2)*linje.normal.roter90()
            a = midtpunkt+korrigering
            b = midtpunkt-korrigering
            return (a.somPunkt(),b.somPunkt())

    def tegn(self,fig):
        fig.sirkel(self.sentrum.x,self.sentrum.y,self.radius)
        self.sentrum.tegn(fig)

            
        



if __name__=='__main__':
    from figur import figur
    #BRUK AV FIGURER
    fig = figur(800,800)
    fig.xmin,fig.xmax,fig.ymin,fig.ymax = -10,10,-10,10

    A = punkt2D(-8,-3)
    B = punkt2D(8,4)
    C = punkt2D(1,3)

    a = linje2D.gjennomPunkter(A,B)
    s = sirkel2D(C,4)
    p1,p2 = s.skjæring(a)


    print(a.dist(p1))
    print(a.dist(p2))
    print(s.dist(p1))
    print(s.dist(p2))

    A.tegn(fig)
    B.tegn(fig)
    s.tegn(fig)
    a.tegn(fig)
    p1.tegn(fig)
    p2.tegn(fig)

    fig.vis()

