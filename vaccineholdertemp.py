
#!/usr/bin/env python3

# Solve the differential equation for T_v

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# function to compute G air based on first principles
def computeGair(P):
	 T = Tv_init
	 m = 0.8* 4.65283364E-26 + 5.313728639E-26*0.2  # mass of air assume 80% N2 and 20% O2
	 Na= 6.02214 *10**23 #Avogadro's number
	 alpha = 1/(2*Na) *np.sqrt(3*kB/m)
	 Kappa = P*l*alpha/(np.sqrt(T))
	 Gair = Kappa * A/l 
	 print("Pressure = ",P," Gair = ",Gair, " alpha = " , alpha, "Kappa= ", Kappa)
	 return Gair


# function that returns dTv/dt
def model(T_v,t,k):
    #dydt = -k * y
    convection = H*A*(T_b-T_v)
    radiation = emissivity*sigma*A*(T_b**4-T_v**4)

    conductiona1 = Gair[0]*(T_b-T_v)
    conductiona2 = Gair[1]*(T_b-T_v)
    conductiona3 = Gair[2]*(T_b-T_v)

    conductiong10 = Ggten*(T_b -T_v)
    conductionvi = 0
    c0 =0
    c1 = 0
    c2 = 0
    c3 =0
    c4 =0
    c5=0
    if k == 0:
        c0 = 1
    elif k ==1:
    	c1=1
    elif k ==2:
    	c2 = 1
    elif k == 3:
    	c3 = 1
    elif k == 4:
    	c4 = 1
    elif k == 5:
    	c5 = 1
    dTVdt = 1/(mv*cv)*(c0*conductiona1 + c1 *conductiona2 +c2*conductiona3 + c3*conductiong10 + c4*radiation + c5*convection)
    return dTVdt


# define variables
mv = 2.0 #kg
cv = 300.0 #J/kgK
T_b = 300.0 #K
T_i = 200.0 #K
emissivity = 1e-3
sigma = 5.67e-8 #W/(m^2*K^4)
kB = 1.38064852e-23 #m^2kgs^2K-1
l = 0.1 # assume 10 cm sides
A =  6 * 0.1 * 0.1 #m^2
H = 4e-3 # W/(m^2*K)
# initial condition
Tv_init = 200
Ggten = 3 *1e-4 #W/K
Gvi = 0.3 #W/K

# compute G for different P and make graphs based on each Gair
choose_P = np.logspace(0,5,3)  # pressure options in Pa
print(choose_P)
Gair = np.zeros(len(choose_P))
for pp in range(len(choose_P)):
	P = choose_P[pp]
	Gair[pp] = computeGair(P) #0.45*0.001*A/0.1 #W/K

# time points
t = np.linspace(0,2e6, int (1E6))

# solve ODEs for each Gair

klabel = ['conduction air, P='+str(choose_P[0]), 'conduction air, P='+str(choose_P[1]),'conduction air, P='+str(choose_P[2]),'conduction G10', 'radiation', 'convection']
for k in range (0,6):
	y1 = odeint(model,Tv_init,t,args=(k,))
	# plot results
	plt.semilogy(t/3600./24./7.,y1,linewidth=2,label=klabel[k])
plt.xlabel('time [week]')
plt.ylabel('T_v [K]')
plt.legend(title='Heat transfer method',loc='lower right')
plt.grid(True)
plt.show()