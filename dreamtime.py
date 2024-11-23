class particle:
    def __init__(self,x,xdot,m,free=True):
        self.name=id(self)
        self.x=x
        self.path=[x]
        self.xdot=xdot
        if m==0:
            raise ValueError('particles must have mass wink wink')
        self.m=m
        self.force=0
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
            return (self.xdot+0.5*(self.force/self.m)*step)*step
        else:
            return 0
        
    def particleStep(self,step):
        if self.free:
            self.x=self.x+(self.xdot+0.5*(self.force/self.m)*step)*step
            self.xdot=self.xdot+(self.force/self.m)*step
            self.path.append(self.x)
        else:
            self.path.append(self.x)
        
def subsystems(s,n):
    if n==0:
        return [[]]
    return [[s[a]]+b for a in range(len(s)) for b in subsystems(s[a+1:],n-1)]

class force:
    def __init__(self,form,nBody):
        
        self.form=form
        self.nBody=nBody
        self.existsIn=[]
        self.forces={}
        
    def join(self,universe):
        universe.acceptForce(self)
        self.existsIn.append(universe)

    def accept(self,particle):
        for universe in self.existsIn:
            universe.acceptParticle(particle)
        self.forces[particle]=0
        
    def update(self):
        updatedForces={member: 0 for member in self.forces}
        if len(self.forces)<self.nBody:
            pass
        for subsystem in subsystems(list(self.forces.keys()),self.nBody):
            newForce=self.form(*subsystem)
            for member in subsystem:
                updatedForces[member]+=newForce[member]
        self.forces=updatedForces
        
    def inform(self):
        for member in self.forces:
            for universe in self.existsIn:
                universe.particles[member]+=self.forces[member]
            

class universe:
    def __init__(self,whenToStop,timeStep,maxDistanceStep=0.0001):
        self.time=0
        self.times=[0]
        self.endOfTheUniverse=whenToStop
        self.timeStep=timeStep
        self.maxDistanceStep=maxDistanceStep
        self.forces=[]
        self.particles={}
        
    def acceptForce(self,force):
        self.forces.append(force)
        
    def acceptParticle(self,particle):
        self.particles[particle]=particle.force
        
    def evolve(self,timeStep):
        numDivs=1
        self.particles={particle:0 for particle in self.particles}
        for force in self.forces:
            force.update()
            force.inform()
        for particle in self.particles:
            particle.force=self.particles[particle]
        if max([particle.nextParticleStep(timeStep) for particle in self.particles])>self.maxDistanceStep:
            numDivs-=1
            numDivs+=self.evolve(timeStep/2)
            numDivs+=self.evolve(timeStep/2)
        else:
            for particle in self.particles:
                particle.particleStep(timeStep)
            self.time+=timeStep
            self.times.append(self.time)
        return numDivs
    
    def dreamtime(self):
        print('this universe dreams...')
        while self.time<self.endOfTheUniverse:
            n=self.evolve(self.timeStep)
            if n>=1024:
                print('time {} took {} segments to calculate               '.format(self.time,n),end='\r')