import numpy as np
from astropy.coordinates import SkyCoord
from z_to_DM_IGM_func import DM_IGM_cal
import astropy.units as u
import pyne2001


def DM_cal(FRB_name,z,Ra,Dec,DM_obs):
        c = SkyCoord(Ra, Dec, unit=(u.hourangle, u.deg))

        gl =  c.galactic.l.degree
        gb =  c.galactic.b.degree

        DM_MK   = pyne2001.get_galactic_dm(gl,gb) #cm^-3*pc
        DM_halo = 30 #cm^-3*pc
        #if DM_halo + DM_MK < 120:
        #       DM_halo = 120-DM_MK
        DM_obs  = DM_obs#1200#2450#1228 #cm^-3*pc
        #Z = (DM_obs - DM_MK)/855.
        DM_IGM  = DM_IGM_cal(z) #Z*855 #+-6% error bar
        DM_host_obs = DM_obs - DM_halo - DM_MK - DM_IGM
        #DM_host_obs = 200
        #DM_IGM = DM_obs - DM_halo - DM_MK - DM_host_obs

        #
        print '--------------------------------------------'
        print 'FRB:',FRB_name
        print 'Ra:%s,Dec:%s'%(Ra,Dec)
        print 'Gl:%.2f,Gb:%.2f'%(gl,gb)
        print '--------------------------------------------'
        print 'Halo DM:%.2f(cm^-3 pc)'%DM_halo
        print 'DM_MK:%.2f(cm^-3 pc)'%DM_MK
        print 'DM_IGM:%.2f(cm^-3 pc)'%DM_IGM
        print 'DM_Obs:%.2f(cm^-3 pc)'%DM_obs
        print 'DM_Host(Obs):%.2f(cm^-3 pc)'%DM_host_obs
        print 'Obs redshift z = %.2f'%z
        print '********************************************'
        return DM_MK,DM_IGM,DM_host_obs


if __name__ == '__main__' :
	FRB_name = 'FRB 190520'
	z = 0.241
	Ra = '16:02:04.275'
	Dec = '-11:17:17.173'
	DM_obs = 1202.1

	DM_l = DM_cal(FRB_name, z, Ra, Dec, DM_obs)

	
