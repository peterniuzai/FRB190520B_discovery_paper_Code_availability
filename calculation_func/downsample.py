import numpy as np



def downsample(data,f_down,t_down):
	'''
	Down sampling the frequency and time axis.
	f_down : new_nchans = nchans / f_down
	t_down : new_nsamples = nsamples / t_down

	'''

        f_step = f_down
        t_step = t_down
        d = data
        d_new_freq = np.zeros((d.shape[0]/f_step,d.shape[1]))
        d_new = np.zeros((d.shape[0]/f_step,d.shape[1]/t_step))
        for f in range(d.shape[0]/f_step):
                d_new_freq[f,:]=d[f*f_step:(f+1)*f_step,:].mean(axis=0)

        for t in range(d.shape[1]/t_step):
                d_new[:,t]=d_new_freq[:,t*t_step:(t+1)*t_step].mean(axis=1)
        return d_new
