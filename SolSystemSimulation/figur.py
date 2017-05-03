#!/usr/bin/python3

# AVHENGER AV AT MODULEN tkinter er installert.

import tkinter as tk
import math

class figur:
    """Klasse for å lage enkle figurer

    Eksempel på bruk:

        fig = figur(1200,800) # vindu med størrelse 1200 x 800

        fig.settRekkevidde(-1.5,1.5,-1.5,1.5)
        fig.inverterYretning()

        fig.rektangel(0.5,0.5,0.9,0.7)
        fig.punkt(.4,.5)

        fig.linje(-1,0,1,0)

        xs = ( math.sin(0.01*i) for i in range(629) )
        ys = ( math.cos(0.01*i) for i in range(629) )

        fig.polygon(xs,ys)

        fig.sirkel(0.5,0.5,0.5)

        fig.punkt(0,0)

        fig.vis()

    """

    def __init__(self,bredde=1000,høyde=600):
        self._bredde = bredde
        self._høyde = høyde
        self._rot = tk.Tk()

        self.lerret = tk.Canvas(self._rot, width = self._bredde, height = self._høyde)
        self.lerret.pack()
        
        self.xmin, self.xmax = 0,bredde
        self.ymin, self.ymax = 0,høyde
        


    def _remap(t,a,b,A,B):
        """private helper function. Maps the interval [a,b] onto the interval [A,B]"""
        return A + (t-a)/(b-a)*(B-A)  

    def _transform(self,x,y):
        """Transformerer gitte xy-verdier til vinduskoordinater"""
        return figur._remap(x,self.xmin,self.xmax,0,self._bredde), figur._remap(y,self.ymin,self.ymax,self._høyde,0)



    #
    # Geometriske former
    #########################3
    def linje(self,x0,y0,x1,y1,**kwargs):
        """ Tegner en linje fra (x0,y0) til (x1,y1)"""

        x0,y0 = self._transform(x0,y0)
        x1,y1 = self._transform(x1,y1)
        self.lerret.create_line(x0,y0,x1,y1,**kwargs)

    def vektor(self,x0,y0,x1,y1):
        """ Tegner en linje fra (x0,y0) til (x1,y1)"""
        x0,y0 = self._transform(x0,y0)
        x1,y1 = self._transform(x1,y1)

        self.lerret.create_line(x0,y0,x1,y1,arrow=tk.LAST,arrowshape=(12,15,5))

    def dot(self,x,y):
        """Tegner en prikk i punktet (x,y)"""
        x,y = self._transform(x,y)
        self.lerret.create_oval(x-1,y-1,x+1,y+1,fill="black")

    def punkt(self,x,y):
        """Tegner en prikk i punktet (x,y)"""
        x,y = self._transform(x,y)
        self.lerret.create_oval(x-2,y-2,x+2,y+2,fill="black")

    def punkter(self,xs,ys):
        """Tegner prikker i punktene (xs[0],ys[0]), (xs[1],ys[1]) ,...."""
        for x,y in zip(xs,ys):
            self.punkt(x,y);


    # AVHENGER AV linje og punkt
    def polygon(self,xs,ys):
        """Tegner polygonet gjennom gjennom punktene (xs[0],ys[0]), (xs[1],ys[1]) ,...."""
        xs,ys = iter(xs),iter(ys)
        xp,yp= next(xs),next(ys)
        x0,y0 = xp,yp

        for x,y in zip(xs,ys):
            self.linje(xp,yp,x,y)
            xp,yp = x,y
        self.linje(xp,yp,x0,y0)

    def kurve(self,xs,ys):
        xs,ys = iter(xs),iter(ys)
        xp,yp = next(xs),next(ys)
        for x,y in zip(xs,ys):
            self.linje(xp,yp,x,y)
            xp,yp = x,y
            

    # AVHENGER AV polygon
    def rektangel(self,x0,y0,x1,y1):
        """Tegner rektangel der (x0,y0) og (x1,y1) er diagonalt motsatte hjørner"""
        self.polygon((x for x in (x0,x0,x1,x1,x0)),(y for y in (y0,y1,y1,y0,y0)))

    # Avhenger av polygon
    def sirkel(self, x0,y0, r):
        """Tegner sirkel med sentrum i x0,y0 og radius r"""
        self.polygon(( x0+r*math.cos(0.01*i) for i in range(629)),(y0+r*math.sin(0.01*i) for i in range(629)))
    
    #
    # DIREKTE TILGANG TIL PIKSLENE
    #################################
    def settPiksel(self,x,y,farge):
        """setter fargen `farge` på pikselen med vinduskoordinater `x` `y`"""
        self.lerret.create_rectangle(x,y,x+1,y+1,fill=farge,width=0)

    def piksler(self):
        for x in range(self._bredde):
            for y in range(self._høyde):
                yield x,y

    #
    # Må kalles for at figuren skal vises
    ###########################################
    def vis(self):
        self._rot.mainloop();



#
# Uformell enhetstesting
#
if __name__=="__main__":
    import math
    fig = figur()

    fig.xmin = -1.5
    fig.xmax = 1.5
    fig.ymin = -1.5
    fig.ymax = 1.5

    
    fig.rektangel(0.5,0.5,0.9,0.7)
    fig.punkt(.4,.5)
    fig.vektor(-1,0,1,1)
    fig.punkt(0,0)
    fig.vektor(0,0,.5,.5)
    fig.vektor(0,0,.5,-.5)
    fig.sirkel(0.5,0.5,0.5)

    # MER KOMPLISERT KURVE
    xs = ( 0.5*math.sin(0.05*i)*math.cos(0.06*i)-.6 for i in range(629) ) # GENERATOR COMPREHENSION SYNTAKS
    ys = ( math.cos(0.04*i) for i in range(629) ) # GENERATOR COMPREHENSION SYNTAKS
    fig.polygon(xs,ys)

    # AD HOC-løsning for fargebehandling.
    # Tkinter ser ut til å kreve
    # at fargene representeres som hex-strenger.
    # I utgangspunktet vikrer det idiotisk å 
    # gå via et string-objekt.
    # TODO: Eliminer denne workarounden ved å sende
    # rgb-verdiene rett til create_rectangle. (Det er 
    # dog tilsynelatende ikke mulig.)
    def rgb2hex(r,g,b):
        number =r*(1<<16) + g*(1<<8) + b
        string = "#"+hex((1<<24) + int(number))[3:]
        return string 

    def colorFunction(x,y):
        return rgb2hex(x+y,abs(y-x),0.3*x)

    for x,y in fig.piksler():
        if (x-300)**2 + (y-100)**2 < 1300:
            fig.settPiksel(x,y,colorFunction(x,y))

    for x,y in fig.piksler():
        if (x-100)**2 + (y-500)**2 < 1300:
            fig.settPiksel(x,y,"blue")

    fig.vis()
