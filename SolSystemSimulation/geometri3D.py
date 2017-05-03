#!/usr/bin/python3

from functools import singledispatch
import math

class punkt3D:
    """Representerer 3D-punkter"""
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        
    def __str__(self,):
        return "Punkt({0}, {1}, {2})".format(self.x,self.y,self.z)

    def __repr__(self):
        return str(self)

    def __add__(self,vektor):
        return punkt3D(self.x+vektor.x, self.y+ vektor.y,self.z+vektor.z)
    
    def __iter__(self):
        return self.generator()

    def generator(self):
        yield self.x
        yield self.y
        yield self.z
    
    def posVektor(self):
        return vektor3D(self.x,self.y,self.z)        

    def tegn(self,fig):
        """ OBS: TEGNER KUN 2D, d.v.s. X- og Y-komponentene"""
        fig.punkt(self.x,self.y)

def forflytning(A,B):
    return B.posVektor()-A.posVektor()

def distanse(A,B):
    forflytning(A,B).lengde()

        
class vektor3D:
    """Representerer 3D-punkter"""
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return "[{0}, {1}, {2}]".format(self.x,self.y,self.z)
   
    def __repr__(self):
        return str(self)

    def __iter__(self):
        return self.generator()

    def generator(self):
        yield self.x
        yield self.y
        yield self.z

    def __add__(self,other):
        """Definerer vektoraddisjon"""
        return vektor3D(self.x+other.x,self.y+other.y,self.z+other.z)
        
    def __rmul__(self,skalar): 
        """Skalering av vektorer"""
        return vektor3D(self.x*skalar,self.y*skalar,self.z*skalar)
    
    def __div__(self,skalar): 
        """Skalering av vektorer"""
        return vektor3D(self.x/skalar,self.y/skalar,self.z/skalar)

    def __sub__(self,other):
        """Vektorsubtraksjon"""
        return self+(-1)*other

    def somPunkt(self):
        return punkt3D(self.x,self.y,self.z)

    def prikk(self,other):
        """Skalarproduktet / (dot-product)"""
        return self.x*other.x+self.y*other.y + self.z*other.z

    def kryss(self,other):
        """ Kryssprodukt"""
        return vektor3D(self.y*other.z- self.z*other.y, self.z*other.x-self.x*other.z, self.x*other.y- self.y*other.x)
    
    def lengde(self):
        """ Lengden til vektoren. Bygger på Pythagoras' teorem"""
        return math.sqrt(self.x**2+self.y**2+self.z**2)
        
    def vinkel(self,other):
        """ Regner ut vinkelen mellom to vektorer, i grader
        u = vektor3D(1,3)
        v = vektor3D(3,1)
        vinkel = u.vinkel(v)
        """
        vinkelIRadianer = math.acos(self.prikk(other)/self.lengde()/other.lengde())
        vinkelIGrader = math.degrees(vinkelIRadianer)
        return vinkelIGrader
    
    def tegn(self,fig):
        """ Tegner vektoren på figuren `fig` med utgangpunkt i origo 
        OBS: Tegner kun X- og Y-komponentene"""
        fig.vektor(0,0,self.x,self.y)
    
    def tegnFra(self,punkt,fig):
        """ Tegner vektoren på figuren `fig` med utgangpunkt i `punkt`
        OBS: Tegner kun X- og Y-komponentene
        """
        fig.vektor(punkt.x, punkt.y, punkt.x + self.x, punkt.y + self.y)



if __name__=='__main__':
    from figur import figur
    #BRUK AV FIGURER
    fig = figur(800,800)
    fig.xmin,fig.xmax,fig.ymin,fig.ymax = -10,10,-10,10

    A = punkt3D(-8,-3,1)
    B = punkt3D(8,4,1)
    C = punkt3D(1,3,1)
    v = vektor3D(1,0,0)
    u= vektor3D(4,5,6)


    A.tegn(fig)
    B.tegn(fig)
    C.tegn(fig)
    (A+v).tegn(fig)
    u.tegn(fig)

    fig.vis()

