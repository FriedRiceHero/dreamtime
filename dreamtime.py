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

class vector:
    def __init__(self,components:list[float]):
        self.components=components
        self.dim=len(self.components)
    
    def magnitude(self):
        return magnitude(self.components)
        
    def __repr__(self):
        return 'Vector: {}'.format(str(self.components))

    def __getitem__(self,key:int):
        return self.components[key]
    
    def __setitem__(self,key:int,value):
        self.components[key]=value
    
    def __iter__(self):
        return iter(self.components)
    
    def __add__(self,y):
        return vector([self.components[d]+y[d] for d in range(self.dim)])

    def __radd__(self,y):
        return self.__add__(y)
    
    def __sub__(self,y):
        return vector([self.components[d]-y[d] for d in range(self.dim)])
    
    def __rsub__(self,y):
        return vector([y[d]-self.components[d] for d in range(self.dim)])
    
    def __mul__(self,y):
        return vector([component*y for component in self.components])
    
    def __rmul__(self,y):
        return self.__mul__(y)

    def __truediv__(self,y):
        return vector([component/y for component in self.components])
    
    def __neg__(self):
        return vector([-component for component in self.components])
    
    def __matmul__(self,y):
        return sum([self.components[d]*y[d] for d in range(self.dim)])

    def direction(self):
        return self/self.magnitude()

    



def zeroVector(d):
    return vector([0 for _ in range(d)])
        

class particle:
    def __init__(self,x,xdot,m,free=True):
        self.name=id(self)
        self.x=vector([x]) if isinstance(x,(int,float)) else vector(x)
        self.path=[self.x]
        self.xdot=vector([xdot]) if isinstance(x,(int,float)) else vector(xdot)
        if m==0:
            raise RelativityError('particles must have mass wink wink')
        self.m=m
        if not self.x.dim==self.xdot.dim:
            raise DimensionMismatch('specify the same number of dimensions for position and velocity')
        self.nDim=self.x.dim
        self.force=zeroVector(self.nDim)
        self.nextStep=zeroVector(self.nDim)
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
            self.nextStep=(self.xdot+0.5*(self.force/self.m)*step)*step
            return self.nextStep
        else:
            return zeroVector(self.nDim)
        
    def particleStep(self,step):
        if self.free:
            self.x=self.x+self.nextStep
            self.xdot=self.xdot+(self.force/self.m)*step
        else:
            pass
        

class force:
    def __init__(self,form,nBody):
        
        self.form=form
        self.nBody=nBody
        self.particlesForces={}
        self.subsystems=[]
        self.nDim=0
        
    def join(self,universe):
        universe.acceptForce(self)
        self.universe=universe
        self.nDim=universe.nDim

    def accept(self,particle):
        self.universe.acceptParticle(particle)
        self.particlesForces[particle]=particle.force
    def getSubsystems(self):
        self.subsystems=subsystems(list(self.particlesForces.keys()),self.nBody)
        
    def trialStep(self):
        if len(self.particlesForces)<self.nBody:
            pass
        for subsystem in self.subsystems:
            newForce=self.form(*subsystem)
            for member in subsystem:
                if newForce[member].dim!=member.nDim:
                    raise DimensionMismatch('force {} acts on {} in {} dimensions, wants {}'.format(self,member,len(newForce[member]),member.nDim))
                
    def update(self):
        if len(self.particlesForces)<self.nBody:
            pass
        updatedparticlesForces={member:zeroVector(self.nDim) for member in self.particlesForces}
        for subsystem in self.subsystems:
            newForce=self.form(*subsystem)
            for member in subsystem:
                updatedparticlesForces[member]+=newForce[member]
        self.particlesForces=updatedparticlesForces
        
    def inform(self):
        for member in self.particlesForces:
            self.universe.particlesForces[member]+=self.particlesForces[member]


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
        self.particlesForces={particle:zeroVector(self.nDim) for particle in self.particlesForces}
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
        return numDivs
    
    def dreamtime(self):
        print('this universe dreams...')
        for interaction in self.interactions:
            interaction.getSubsystems()
            interaction.trialStep()
        n=0
        while self.time<self.endOfTheUniverse:
            
            n+=self.evolve(self.timeStep)
            for particle in self.particlesForces:
                particle.path.append(particle.x)
            self.times.append(self.time)
        print(f'took a total of {n} cycles')