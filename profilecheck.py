from dreamtime import *

def xForce(particle1,particle2):
    x1=particle1.x
    x2=particle2.x
    f1=-.1*(x1-x2)
    f2=-.1*(x2-x1)
    return{particle1: f1,particle2:f2}

def constForce(particle1):
    return {particle1:1}

def cForce(particle1,particle2):
    q1=particle1.charges[coulombForce]
    q2=particle2.charges[coulombForce]
    r=(particle1.x-particle2.x)

    f=0.2*q1*q2/abs(r)
    
    f1=f/r
    f2=-f/r
    
    return {particle1:f1,particle2:f2}

def drag(particle):
    xdot = particle.xdot
    f = .1*xdot
    return {particle:f}

here=universe(100,.01,maxDistanceStep=0.00001)

springForce=force(xForce,2)
springForce.join(here)

coulombForce=force(cForce,2)
coulombForce.join(here)

dragForce=force(drag,1)
dragForce.join(here)

'''
freeParticle1=particle(10,0,1, free = False)
freeParticle1.join(coulombForce)
freeParticle1.chargedUnder(coulombForce,100)

freeParticle4=particle(-10,0,1, free = False)
freeParticle4.join(coulombForce)
freeParticle4.chargedUnder(coulombForce,100)

springParticle=particle(0,0,.5)
springParticle.join(springForce)
springParticle.join(dragForce)


'''

freeParticle2=particle(-10,0,1)
freeParticle2.join(coulombForce)
freeParticle2.chargedUnder(coulombForce,1)

freeParticle3=particle(0,0,1,free=False)
freeParticle3.join(coulombForce)
freeParticle3.chargedUnder(coulombForce,-1)





here.dreamtime()

times=here.times
path2=freeParticle2.path
path3=freeParticle3.path
