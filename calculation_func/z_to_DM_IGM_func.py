import numpy as np
from scipy import integrate,constants
from astropy import constants as const


def DM_IGM_cal(z):


	c 	= const.c.cgs.value	#cm / s
	m_p 	= const.m_p.cgs.value	# g
	H0	= 67.36			#km s-1 Mpc-1
	h	= H0/100		#100 km/s Mpc-1
	Mpc	= const.pc.cgs.value * 1e6	#cm
	H0 	= H0 * 1e5 / Mpc	#cm s-1 cm-1
	G	= const.G.cgs.value 	#cm3 / (g s2)
	omega_m = 0.315
	f_IGM	= 0.83
	kai_z	= 7/8.
	omega_lamda =  1 - omega_m
	omega_b_h2 = 0.02237
	
	omega_b  = omega_b_h2/h**2
	
	
	def f(x):
	    z = x
	    A = 3*c * H0 * omega_b * f_IGM / (8*np.pi*G*m_p) * kai_z
	    A = A / const.pc.cgs.value
	    DM_IGM = A*(1+z) / (omega_m*(1+z)**3 + omega_lamda)**0.5
	    return DM_IGM
	
	return integrate.quad(f,0,z)[0]

def z_cal(DM_IGM):

	dm_list = []
	z_list = np.linspace(0,10,4000)
	for z in z_list:
		dm_trial = DM_IGM_cal(z)
		dm_list.append(dm_trial)
	dm_list = np.array(dm_list)
	idx = np.abs(dm_list - DM_IGM).argmin()
	z_estimate = z_list[idx]

	return z_estimate
		


if __name__  == '__main__':
        z = 0.5#0.241
	print DM_IGM_cal(z)
	DM_IGM = DM_IGM_cal(z)
	DM_IGM = 10000#911-115
	z_estimate = z_cal(DM_IGM)
	print 'Obs z:%.3f'%z
	print 'Estimated DM_IGM:%.2f'%DM_IGM
	print 'Estimated z:%.3f'%z_estimate

