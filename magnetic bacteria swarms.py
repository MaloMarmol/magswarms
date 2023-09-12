import pystokes 
import numpy as np, matplotlib.pyplot as plt
# particle radius, self-propulsion speed, number and fluid viscosity
b, vs, Np, eta = 1.0,1, 10, 0.1

#initialise
r = pystokes.utils.initialCondition(Np)  # initial random distribution of positions
p = np.zeros(3*Np); 
p[2*Np:3*Np] = -0.4 # initial orientation of the colloids


def rhs(rp):
    """
    right hand side of the rigid body motion equation
    rp: is the array of position and orientations of the colloids
    returns the \dot{rp} so that rp can be updated using an integrator
    """
    # assign fresh values at each time step
    r = rp[0:3*Np];   p = rp[3*Np:6*Np]
    norm_p = np.dot(p,p)
    p = p/np.sqrt(norm_p)
    F, v, o,T = np.zeros(3*Np), np.zeros(3*Np), np.zeros(3*Np),np.zeros(3*Np)
    
    force.lennardJonesWall(F, r, lje=0.01, ljr=5, wlje=1.2, wljr=3.4)
    torque.magnetic(T,p,m0=1,Bx=0, By=1, Bz=-0)
    rbm.mobilityTT(v, r, F)  
    rbm.mobilityTR(v,r,T)
    rbm.mobilityRT(o, r, F)  
    rbm.mobilityRR(o,r,T)

   
    l2 = pystokes.utils.irreducibleTensors(2, p,Y0=1)
    v3t = vs*p;
    rbm.propulsionT2s(v,r,l2)
    rbm.propulsionT3t(v, r, v);
    v = v+v3t;
    return np.concatenate( (v,o) )

rbm   = pystokes.wallBounded.Rbm(radius=b, particles=Np, viscosity=eta)
force = pystokes.forceFields.Forces(particles=Np)
torque = pystokes.forceFields.Torques(particles=Np)

# simulate the resulting system
Tf, Npts = 120, 50
pystokes.utils.simulate(np.concatenate((r,p)), Tf,Npts,rhs, filename='swarms')

from scipy.io import loadmat
result=loadmat('swarms')
traj	  = result['X']


for i in range(Npts):
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.quiver(traj[i,0:Np], traj[i,Np:2*Np], traj[i,2*Np:3*Np], traj[i,3*Np:4*Np], traj[i,4*Np:5*Np], traj[i,5*Np:6*Np],length=5)
    ax.set_xlim(-20,20,10)
    ax.set_ylim(-20,20)
    ax.set_zlim(0,10)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()
    
    
"""" 
    
    cpdef magnetic(self, double[:] T, double [:] p, double m0, double Bx, double By, double Bz):
        
        Torque due to magnetotaxis
        
        ...
        Parameters
        ----------
        p: np.array
            An array of Orientations
            An array of size 3*Np,
        T: np.array
            An array of Torques
            An array of size 3*Np,
        m0: float 
            magnetic moment
        Bx,By,Bz : float
            magnetic field components
  
        cdef int Np = self.Np, i, xx = 2*Np
        for i in prange(Np, nogil=True):
            T[i   ] += m0*(p[i+Np]*Bz-p[i+xx]*By)
            T[i+Np] += m0*(p[i+xx]*Bx-p[i]*Bz)
            T[i+xx] += m0*(p[i]*By-p[i+Np]*Bx)
        return 

"""