from typing import List
from decimal import Decimal
import planeter
from planeter import planet
import numpy
from animasjon import animasjon
from geometri3D import vektor3D as vec

'''
Kickstart code from class
'''
G = 2.959122e-4

Sol = planeter.planet(0, 0, 0, 0, 0, 0, 1, "Sol")
Terra = planeter.planet(-7.3423e-1, -6.8292e-1, -1.1499e-4, 1.1456e-2, -1.2634e-2, -5.7432e-8, 3.0e-6, "Terra")
Luna = planeter.planet(-7.3611e-1, -6.8121e-1, -1.6369e-4, 1.033e-2, -1.3049e-2, -5.0483e-5, 3.7e-8, "Luna")

'''
a_earth = G * 1 / numpy.sqrt(-7.3423e-1 ** 2 + -6.8292e-1**2 + -1.1499e-4**2)**3 
    *[7.3423e-1,
      6.8292e-1,
      1.1499e-4]
'''


def arrayToVec(array) -> vec:
    return vec(array[0], array[1], array[2])


def distance(m1: vec, m2: vec = vec(0, 0, 0)) -> float:
    return (m2 - m1).lengde()


### Oppgave A) ###
def solGravitasjon(posisjon: vec) -> vec:
    # regn ut gravitasjon
    return gravitasjon(posisjon, arrayToVec(Sol.pos), Sol.masse)


### Oppgave B) ###
def gravitasjon(planetA: vec, planetB: vec, masseB: float) -> vec:
    return gravitasjonForce(planetA, planetB, masseB)


def gravitasjonForce(planetA: vec, planetB: vec, masseB: float, masseA: float = 1) -> vec:
    return (planetB - planetA).__mul__(G * masseA * masseB / distance(planetA, planetB) ** 3)


### Oppgave C) ###
def oppgave_C():
    x0jord: vec = arrayToVec(Terra.pos)
    x0Måne: vec = arrayToVec(Luna.pos)

    earthSunAcceleration = solGravitasjon(x0jord)
    moonEarthAcceleration = gravitasjon(x0Måne, x0jord, Terra.masse)
    moonSunAcceleration = solGravitasjon(x0Måne)
    moonEarthSunAcceleration = moonEarthAcceleration + moonSunAcceleration

    printOppgaveC(Terra, [Sol], earthSunAcceleration)
    printOppgaveC(Luna, [Terra], moonEarthAcceleration)
    printOppgaveC(Luna, [Sol], moonSunAcceleration)
    printOppgaveC(Luna, [Terra, Sol], moonEarthSunAcceleration)


def printOppgaveC(planetA: planet, planets: List[planet], acceleration: vec):
    msg = "%s's acceleration according to %s's gravitational pull is of %.2E AU/day^2" % \
          (planetA.navn, [p.navn for p in planets], Decimal(acceleration.lengde()))
    print(msg)


def eulersMethod2(xi1: vec, vi1: vec, h: float, xi2: vec = arrayToVec(Sol.pos), mass2: float = 1) -> [vec,
                                                                                                      vec]:
    a = gravitasjon(xi1, xi2, mass2)
    x_t = xi1 + vi1 * h + 0.5 * (h ** 2) * a * 0.5 * (h ** 2)
    v_t = vi1 + a * h
    return x_t, v_t


def variadicEulersMethod2(xi1: vec, vi1: vec, h: float,
                          otherPlanetsPosMass: []) -> [vec, vec]:
    a: vec = vec(0, 0, 0)
    for planetInfo in otherPlanetsPosMass:
        a += gravitasjon(xi1, planetInfo[0], planetInfo[1])

    x_t = xi1 + vi1 * h + 0.5 * (h ** 2) * a * 0.5 * (h ** 2)
    v_t = vi1 + a * h
    return x_t, v_t


def eulersMethod2Generator(thisPlanet: planet, centerOfGravity: planet, h: float = 1):
    x_t: vec = arrayToVec(thisPlanet.pos)
    v_t: vec = arrayToVec(thisPlanet.fart)
    c_o_g_Pos: vec = arrayToVec(centerOfGravity.pos)
    c_o_g_Masse: float = centerOfGravity.masse
    while True:
        yield ((x_t.x, x_t.y), (0, 0))
        x_t, v_t = eulersMethod2(x_t, v_t, h, c_o_g_Pos, c_o_g_Masse)


def oppgave_D(precisionLevel: int = 24):
    """
    Oppgave D:
        initial supposition:
            we expect the result to draw towards 365 days 
            as h tends towards 0 (as precisionLevel tends towards +infinity)
        Observation: 
            it turns out that we reach a total of 365 with steps of precision
            20 < step <= 24 - which would make sense if t is a day with a modification
            of 1/24th, i.e. one set of coordinates per hour.
    """
    h: float = 1.0 / precisionLevel
    amountOfDays: int = 1
    signFlag: int = -1
    sample = []
    halfRevolutionCounter = 3
    for planetCoord in eulersMethod2Generator(Terra, Sol, h):
        if planetCoord[0][0] * signFlag >= 0:
            sample.append(amountOfDays)
            if halfRevolutionCounter == 0:
                break
            amountOfDays = 0
            signFlag *= -1
            halfRevolutionCounter -= 1
        amountOfDays += 1

    halfRevolution = amountOfDays / precisionLevel
    fullRevolution = halfRevolution * 2
    print(f'Oppgave D - days in one revolution of {Terra.navn} '
          f'around {Sol.navn} with step of {str(precisionLevel)}: '
          f'{str(round(fullRevolution))} days')


def oppgave_E_generator(precisionLevel: float = 24):
    TerraPreviousPos, TerraPreviousVel = arrayToVec(Terra.pos), arrayToVec(Terra.fart)
    LunaPreviousPos, LunaPreviousVel = arrayToVec(Luna.pos), arrayToVec(Luna.fart)
    h = 1.0 / precisionLevel
    while True:
        # Calculate Earth's acceleration with Sun
        [TerraNextPos, TerraNextVel] = eulersMethod2(TerraPreviousPos, TerraPreviousVel, h)
        # Calculate Moon's acceleration with Earth
        [LunaNextPos, LunaNextVel] = eulersMethod2(LunaPreviousPos, LunaPreviousVel, h, TerraPreviousPos, Terra.masse)

        yield ((LunaNextPos.x, LunaNextPos.y), (TerraNextPos.x, TerraNextPos.y))
        TerraPreviousPos, TerraPreviousVel, LunaPreviousPos, LunaPreviousVel = \
            TerraNextPos, TerraNextVel, LunaNextPos, LunaNextVel


def oppgave_E(precisionLevel: int = 24):
    """
    According to the animated simulation, the Moon does not
    go around the Earth if affected by the Earth's gravitational 
    pull alone. 
    """
    amountOfDays: int = 1
    signFlag: int = -1
    sample = []
    halfRevolutionCounter = 3
    for planetCoord in oppgave_E_generator(precisionLevel):
        if planetCoord[0][0] * signFlag >= 0:
            sample.append(amountOfDays)
            if halfRevolutionCounter == 0:
                break
            amountOfDays = 0
            signFlag *= -1
            halfRevolutionCounter -= 1
        amountOfDays += 1

    halfRevolution = amountOfDays / precisionLevel
    fullRevolution = halfRevolution * 2
    print(f'Oppgave E - days in one revolution of {Luna.navn} '
          f'around {Sol.navn} with step of {str(precisionLevel)}: '
          f'{str(round(fullRevolution))} days')


def oppgave_F_generator(precisionLevel: int = 24):
    TerraPreviousPos, TerraPreviousVel = arrayToVec(Terra.pos), arrayToVec(Terra.fart)
    LunaPreviousPos, LunaPreviousVel = arrayToVec(Luna.pos), arrayToVec(Luna.fart)
    h = 1.0 / precisionLevel
    while True:
        # Calculate Earth's acceleration with Sun
        [TerraNextPos, TerraNextVel] = eulersMethod2(TerraPreviousPos, TerraPreviousVel, h)
        # Calculate Moon's acceleration with Earth AND Sun
        [LunaNextPos, LunaNextVel] = variadicEulersMethod2(LunaPreviousPos, LunaPreviousVel, h,
                                                           [(TerraPreviousPos, Terra.masse),
                                                            (arrayToVec(Sol.pos), Sol.masse)])

        ## We make the earth the origin of the simulation,
        # and adjust the Moon's position accordingly
        # LunaNextPos_adj = LunaNextPos - TerraNextPos
        # TerraNextPos_adj = TerraNextPos - TerraNextPos
        # yield ((LunaNextPos_adj.x, LunaNextPos_adj.y), (TerraNextPos_adj.x, TerraNextPos_adj.y))

        # Normal simulation with Sun at the origin
        yield ((LunaNextPos.x, LunaNextPos.y), (TerraNextPos.x, TerraNextPos.y), (0, 0))

        TerraPreviousPos, TerraPreviousVel, LunaPreviousPos, LunaPreviousVel = \
            TerraNextPos, TerraNextVel, LunaNextPos, LunaNextVel


def oppgave_F(precisionLevel=24):
    amountOfDays: int = 1
    signFlag: int = -1
    sample = []
    halfRevolutionCounter = 3
    for planetCoord in oppgave_F_generator(precisionLevel):
        if planetCoord[0][0] * signFlag >= 0:
            sample.append(amountOfDays)
            if halfRevolutionCounter == 0:
                break
            amountOfDays = 0
            signFlag *= -1
            halfRevolutionCounter -= 1
        amountOfDays += 1

    halfRevolution = amountOfDays / precisionLevel
    fullRevolution = halfRevolution * 2
    print(f'Oppgave F - days in one revolution of {Luna.navn} '
          f'around {Sol.navn} with step of {str(precisionLevel)}: '
          f'{str(round(fullRevolution))} days (incl Earth\'s gravitational pull)')


### Experiment
def eulerSpringForce(thisPlanet: planet):
    ##
    #   Supposition:
    #   We think of the gravitational force of a celestial body towards another as
    #   an invisible spring. Since we are dealing with objects in space (and we are
    #   only modelling a simplified version of graviation), we can use Hooke's law
    #   and leave out the dampening factor - we want the simulation to go on perpetually.
    #
    #   Spring forces:
    #   x(t) = restPosition + (startVelocity / omega) * sin(omega * t) + (currentPosition - restPosition) * cos(omega * t)
    #   Where omega is the square root of the angular frequency: omega = sqrt(k/m)
    #
    #   Hooke's law:
    #   f = -k(currentPosition - restPosition)
    #   or
    #   f = k(restPosition - currentPosition)
    #   ==>
    #   f = ma , so:
    #   ma  = k(restPosition - currentPosition)
    #   a   = k(restPosition - currentPosition) / m
    #   k   = am / (restPosition - currentPosition)
    #
    #   Angular frequency = omega^2 = k / m
    #        = am / (restPosition - currentPosition) / m
    #        = a / (restPosition - currentPosition)
    #
    #   We search for a:
    #       Newton's law of gravitation:
    #       f   = G * mass1 * mass2 / length(position2 - position1)^3 * (position2 - position1)
    #       acceleration of object1:
    #       f   = a * mass1
    #       so:
    #       a   = f / mass1
    #           = G * mass1 * mass2 / length(position2 - position1)^3 * (position2 - position1) / mass1
    #           = G * mass2 / length(position2 - position1)^3 * (position2 - position1)
    #
    #   omega^2 = G * restMass2 / length(restPosition - currentPosition)^3 * (restPosition - currentPosition) / (restPosition - currentPosition)
    #           = G * restMass2 / length(restPosition - currentPosition)^3
    #   omega   = sqrt( G * restMass2 / length(restPosition - currentPosition)^3 )
    #

    ##########################
    ## Helper methods START ##
    ##########################

    def angularFrequency(movingPlanetCurrentPos: vec, restMass: float, restPlanetPos: vec = vec(0, 0, 0)):
        return numpy.sqrt(G * restMass / (distance(movingPlanetCurrentPos, restPlanetPos) ** 3))

    def spring_x(_currentPos: vec, _currentVel: vec, restMass: float, t: float, _restPos: vec = vec(0, 0, 0)):
        angFreq: float = angularFrequency(_currentPos, restMass, _restPos)
        return _restPos + _currentVel / angFreq * numpy.sin(angFreq * t) + (_currentPos - _restPos) * numpy.cos(
            angFreq * t)

    def spring_v(_currentPos: vec, _currentVel: vec, restMass: float, t: float, _restPos: vec = vec(0, 0, 0)):
        angFreq: float = angularFrequency(_currentPos, restMass, _restPos)
        return _currentVel * numpy.cos(angFreq * t) - angFreq * (_currentPos - _restPos) * numpy.sin(angFreq * t)

    def spring_a(_currentPos: vec, _currentVel: vec, _restMass: float, t: float, _restPos: vec = vec(0, 0, 0)):
        return -1 * (angularFrequency(_currentPos, _restMass, _restPos) ** 2) * spring_x(_currentPos, _currentVel,
                                                                                         _restMass, t, _restPos)

    ##########################
    ## Helper methods START ##
    ##########################

    x0: vec = arrayToVec(thisPlanet.pos)
    v0: vec = arrayToVec(thisPlanet.fart)
    h: float = 1.0 / 24
    t: int = 0

    x_t: vec = spring_x(x0, v0, 1, t * h)
    v_t: vec = spring_v(x0, v0, 1, t * h)
    '''
    #alternative A:
    at = spring_a(x0, v0, 1, step)
    v_t = spring_v(x0, v0, 1, step)
    x_t = spring_x(x0, v0, 1, step)
    euler_xt = x_t + v_t * step + 0.5 * at * step **2
    '''
    '''
    #alternative B: 
    at = spring_a(x0, v0, 1, step)
    v_t = spring_v(x0, v0, 1, step) + at * step
    x_t = spring_x(x0, v0, 1, step) + v_t * step
    '''

    while True:
        yield ((x_t.x, x_t.y), (0, 0))
        x_t: vec = spring_x(x_t, v_t, 1, t * h)
        v_t: vec = spring_v(x_t, v_t, 1, t * h)

        '''
        #alternative A: 
        yield ((euler_xt.x, euler_xt.y), (0,0))
        at = spring_a(x_t, v_t, 1, step)
        v_t = spring_v(x_t, v_t, 1, step)
        x_t = spring_x(x_t, v_t, 1, step)
        euler_xt = x_t + v_t * step + 0.5 * at * step **2
        '''
        '''
        #alternative B: 
        yield ((x_t.x, x_t.y), (0,0))
        at = spring_a(x_t, v_t, 1, step)
        v_t = spring_v(x_t, v_t, 1, step) + at * step
        x_t = spring_x(x_t, v_t, 1, step) + v_t * step   
        '''

        t += 1


if __name__ == '__main__':
    pass
    ##
    oppgave_C()
    ##
    oppgave_D()
    ##
    # oppgave_E()
    ## animasjon(oppgave_E_generator(1))
    ##
    # oppgave_F()
    animasjon(oppgave_F_generator(1))

    # animasjon(eulersMethod2Generator(Terra, Sol, 1))
    # animasjon(eulersMethod2Generator(Luna, Terra, 1))
    # animasjon(eulerSpringForce(Terra))
