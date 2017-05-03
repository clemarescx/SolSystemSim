#!/usr/bin/python3
"""
Avhenger av matplotlib.
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def animasjon(dataProvider,xmin=-3,ymin=-3,xmax=3,ymax=3,interval = 1):
    """
    Det forutsettes her at det er mulig å iterere over dataProvider
    og at en slik iterasjon gir oss tupler eller lister av typen
    (x_0,y_0,x_1,y_1,.....,x_n,y_n).

    Funksjonen plotter da punktene  (x_0,y_0), (x_1,y_1),...,(x_n,y_n).

    xmin,ymin,xmax,ymax angir grensene for x- og y-verdier som vises.
    interval angir antall millisekunder mellom hver oppdatering av animasjone
    """
    fig = plt.figure()
    ax = plt.axes(xlim=(xmin,xmax),ylim=(ymin,ymax))
    line, = ax.plot([],[],'bo',ms=4)

    
    def init():
        line.set_data([],[])
        return line

    iterator = iter(dataProvider)
    def animasjon(i):
        dataTuple = next(iterator)
        line.set_data([p[0] for p in dataTuple], [p[1] for p in dataTuple])
        return line

    ani = animation.FuncAnimation(fig, animasjon, init_func = init,interval = interval)
    plt.show()



if __name__=='__main__':

    # ANIMASJON MED GENERATOR:
    def generator(n):
        for i in range(n):
            x = i/n
            yield ( (x,x**3),(x**3-x,x**2) ) # Generatoren returnerer et tupler av tupler. Første tuppel er x- og y-komponent til første punkt. Andre tuppel hører til andre punkt o.s.v.

    animasjon(generator(100),-1,-1,1,1)

    # ANIMASJON BASERT PÅ LISTER:
    listeOverPosisjoner = [ ( (1,0.01*i),(0.01*i,(0.01*i)**2) ) for i in range(200)]
    animasjon(listeOverPosisjoner,xmin=0,ymin=0,xmax=2,ymax=2)

