from matplotlib import pyplot as plt
import numpy as np

def iterate(z,dz,c_):
	return (z**2+c_,2*z*dz+1)

def newton(n,c_,w):
	z,dz=c_,1
	for i in range(n-1):
		w=w**2
		z,dz=iterate(z,dz,c_)
	return c_+(w-z)/dz

def approximate(n,k,w):
    c_=w
    cs=[w]
    for i in range(n):
        for j in range(k):
            c_=newton(i,c_,w)
            cs.append(c_)
    return cs


#startpoints=np.exp(1j*2*np.pi*np.linspace(0,1,2001))
#result=np.array([approximate(20,36,w) for w in startpoints])
for i in np.linspace(0,1,50):
    result=approximate(20,36,np.exp(2*np.pi*1j*i))
    X,Y=np.real(result),np.imag(result)
    plt.plot(X,Y)
plt.show()
