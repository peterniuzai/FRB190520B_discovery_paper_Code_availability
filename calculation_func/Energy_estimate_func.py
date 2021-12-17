from astropy import units as u
import numpy as np
#from astropy.cosmology import WMAP9 as cosmo
import astropy.units as u
from astropy.cosmology import FlatLambdaCDM


def Energy_cal(z,fluence):
	'''
	Calculate the Energy based on its redshift
	paras:
		z:		redshift
		fluence: 	(Jy ms)
	return: 
		E:		(erg)
		luminosity distance:	(Gpc)
		comoving distance:	(Gpc)
	'''
	cosmo = FlatLambdaCDM(H0=67.4, Om0=0.315,Neff=2.99,Tcmb0=2.725 * u.K)
	comov_d = cosmo.comoving_distance(z).to('Gpc')
	lumino_d = cosmo.luminosity_distance(z).to('Gpc')
	lu_d = lumino_d.to('cm').value
	
	BW = 1 	#GHz
	Fluence = fluence# (Jy ms)
	E_sun	= 1.0284518344137629e+29 /23 #(erg/s)
	alpha = 0#-1.6
	
#	E = Fluence * BW * 4 * np.pi * lu_d**2 * 1e-29 /(z+1)**(1+alpha)*1e7
	E = 1E39 * fluence * BW * 4 *np.pi *(lu_d/1E28) **2 / (z+1)  #erg
	
	
	return E, lumino_d,comov_d




if __name__ == '__main__':
	z = 0.241
	fluence =  2 #7.8*1e-3 # (Jy ms)
	
	E,lumino_d,comov_d = Energy_cal(z,fluence)
		
	
	
		
	print 'Energy(J)[1J = 10^7 erg]'
	print 'FRB:\t %e J'%(E/1e7)
	print 'FRB:\t %e erg'%E
	print '------------------------------------'
	print 'Luminosity distance:'
	print 'FRB:\t',lumino_d
	print 'Comoviong distance:'
	print 'FRB:\t',comov_d
	print '------------------------------------'

