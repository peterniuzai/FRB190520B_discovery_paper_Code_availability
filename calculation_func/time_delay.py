import numpy as np

def time_delay(DM,fbot,ftop):
        '''
	Calculate time delay according to top frequency and bottom frequency with max DM
	prarameters:
		DM: 	pc^-3 pc
		fbot:	MHz
		ftop:	MHz
	return:
		time_delay (ms)
		

	'''
        C     = 4.148908e6 # (ms)
        t_delay   = C * DM * (fbot**-2  -  ftop**-2)
        return t_delay


if __name__ == '__main__':
	dm = 5000
	fbot = 1000
	ftop = 1500
	print time_delay(dm,fbot,ftop)
	
