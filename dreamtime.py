class DimensionMismatch(Exception):
    pass

class RelativityError(Exception):
    pass

def magnitude(vector):
    return sum([a**2 for a in vector])**(1/2)

def subsystems(s,n):
    if n==0:
        return [[]]
    return [[s[a]]+b for a in range(len(s)) for b in subsystems(s[a+1:],n-1)]

class unitVector:
    def __init__(self,components):
        self.components=components
        self.magnitude=1
        
    
class vector:
    def __init__(self,components):
        self.components=components
        self.magnitude=magnitude(components)
        self.direction=unitVector(components/self.magnitude)

def vectorFrom(point1,point2):
    return vector([point2[d]-point1[d] for d in range(len(point1))])
        

class particle:
    def __init__(self,x,xdot,m,free=True):
        self.name=id(self)
        self.x=[x] if isinstance(x,(int,float)) else x
        self.path=[x]
        self.xdot=[xdot] if isinstance(x,(int,float)) else xdot
        if m==0:
            raise RelativityError('particles must have mass wink wink')
        self.m=m
        if not len(x)==len(xdot):
            raise DimensionMismatch('specify the same number of dimensions for position and velocity')
        self.nDim=len(x)
        self.force=[0 for _ in range(self.nDim)]
        self.nextStep=[0 for _ in range(self.nDIm)]
        self.feels=[]
        self.free=free
        self.charges={}
        
    
    def chargedUnder(self,force,charge):
        self.charges[force]=charge

    def join(self,force):
        force.accept(self)
        self.feels.append(force)
            
    def nextParticleStep(self,step):
        if self.free:
            self.nextStep=[(self.xdot[d]+0.5*(self.force[d]/self.m)*step)*step for d in range(self.nDim)]
            return self.nextStep
        else:
            return 0
        
    def particleStep(self,step):
        if self.free:
            self.x=[self.x[d]+self.nextStep[d] for d in range(self.nDim)]
            self.xdot=[self.xdot[d]+(self.force[d]/self.m)*step for d in range (self.nDim)]
            self.path.append(self.x)
        else:
            self.path.append(self.x)
        

class force:
    def __init__(self,form,nBody):
        
        self.form=form
        self.nBody=nBody
        self.existsIn=[]
        self.particlesForces={}
        self.subsystems=[]
        self.nDim=0
        
    def join(self,universe):
        universe.acceptForce(self)
        self.existsIn.append(universe)
        self.nDim=universe.nDim

    def accept(self,particle):
        for universe in self.existsIn:
            universe.acceptParticle(particle)
        self.particlesForces[particle]=0
    def getSubsystems(self):
        self.subsystems=subsystems(list(self.particlesForces.keys()),self.nBody)
        
    def trialStep(self):
        if len(self.particlesForces)<self.nBody:
            pass
        for subsystem in self.subsystems:
            newForce=self.form(*subsystem)
            for member in subsystem:
                if len(newForce[member])!=member.nDim:
                    raise DimensionMismatch('force {} acts on {} in {} dimensions, wants {}'.format(self,member,len(newForce[member]),member.nDim))
                
    def update(self):
        updatedparticlesForces={member: 0 for member in self.particlesForces}
        if len(self.particlesForces)<self.nBody:
            pass
        for subsystem in self.subsystems:
            newForce=self.form(*subsystem)
            for member in subsystem:
                updatedparticlesForces[member]+=newForce[member]
        self.particlesForces=updatedparticlesForces
        
    def inform(self):
        for member in self.forces:
            for universe in self.existsIn:
                universe.particles[member]+=self.forces[member]


class universe:
    def __init__(self,nDim,whenToStop,timeStep,maxDistanceStep=0.0001):
        self.time=0
        self.times=[0]
        self.endOfTheUniverse=whenToStop
        self.timeStep=timeStep
        self.maxDistanceStep=maxDistanceStep
        self.interactions=[]
        self.particlesForces={}
        self.nDim=nDim

    def acceptForce(self,force):
        self.interactions.append(force)
        
    def acceptParticle(self,particle):
        if particle.nDim!=self.nDim:
            raise DimensionMismatch('trying to join a particle with {} dimensions to a universe with {} dimensions'.format(particle.nDim,self.nDim))
        self.particlesForces[particle]=particle.force
        
    def evolve(self,timeStep):
        numDivs=1
        self.particlesForces={particle:0 for particle in self.particlesForces}
        for interaction in self.interactions:
            interaction.update()
            interaction.inform()
        for particle in self.particlesForces:
            particle.force=self.particlesForces[particle]
        if max([magnitude(particle.nextParticleStep(timeStep)) for particle in self.particlesForces])>self.maxDistanceStep:
            numDivs-=1
            numDivs+=self.evolve(timeStep/2)
            numDivs+=self.evolve(timeStep/2)
        else:
            for particle in self.particlesForces:
                particle.particleStep(timeStep)
            self.time+=timeStep
            self.times.append(self.time)
        return numDivs
    
    def dreamtime(self):
        print('this universe dreams...')
        for interaction in self.interactions:
            interaction.getSubsystems()
            interaction.trialStep()
        while self.time<self.endOfTheUniverse:
            n=self.evolve(self.timeStep)
            if n>=1024:
                print('time {} took {} segments to calculate               '.format(self.time,n),end='\r')