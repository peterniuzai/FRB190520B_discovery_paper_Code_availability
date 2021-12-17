import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib import gridspec
import matplotlib
from matplotlib.colors import LinearSegmentedColormap
#import powerlaw
import scipy.signal as signal

def plot_de_2D(dedata, DM, axis_freq , axis_time ,t_rsl,t_max,mjd,textplot):

	def gaussian(x,*param):
	    return abs(param[0])*np.exp(-np.power(x - param[1], 2.) / (2 * np.power(param[2], 2.)))
	def f_1(x, A, B, ):
	    return A*x + B 

        clist = ['white', 'white', 'white', 'white', 'royalblue']
	new_cmap = LinearSegmentedColormap.from_list('wb', clist)
#       startsp = []
	dedata = dedata -dedata.mean()
	dedata_1D	= dedata.sum(axis=0)
        medfilt_p       =  1
	dedata_1D = signal.medfilt(dedata_1D,medfilt_p)
	dedata_1D_p = signal.medfilt(dedata_1D,dedata_1D.size/20*2+1)
	dedata_1D = dedata_1D - dedata_1D_p
	dedata_1D = dedata_1D/dedata_1D.max()
#        plt.plot(dedata_1D)
 #       plt.show()
  #      exit()


	lo	= np.where(dedata_1D == dedata_1D.max())[0][0]

	if abs(lo - dedata_1D.size/2)> 10:
		print 'Take Center Loc'
		lo = dedata_1D.size/2
	#p_m     = [dedata_1D.max(),0,1]
	#p_m     = [dedata_1D.max(),dedata_1D.size/2,1]
	p_m     = [dedata_1D.max(),lo,1]
	fit_axis= np.arange(dedata_1D.size)
#	np.save('dedata_%s'%rank_pulse,dedata)
	#exit()
	#popt_g,pcov_g = curve_fit(gaussian,axis_time,dedata_1D,p0=p_m,maxfev=5000000)
	popt_g,pcov_g = curve_fit(gaussian,fit_axis,dedata_1D,p0=p_m,maxfev=5000000)
	sigma_p = popt_g[2]
	width_g =  sigma_p*t_rsl*1000*2
	time_max = t_max
	#dedata_1D_fit = gaussian(axis_time,*popt_g)
	dedata_1D_fit = gaussian(fit_axis,*popt_g)
	lo_half_peak = np.abs(dedata_1D_fit-dedata_1D_fit.max()/2).argmin()
	pulse_w =  (abs(lo-lo_half_peak))*2*t_rsl*1000 #ms
	
	
	print '--------------------'
	print 'Pulse Width (FWHM):%.1f(ms)'%pulse_w
	print 'Pulse Width (sigma):%.1f(ms)'%width_g
	#width_half	= abs(lo-lo_half_peak)
	
	width_half	= int(round(sigma_p))
	print 'Width Samples:',width_half *2
	print '--------------------'
	if width_half == 0 or width_half < 0 or width_half>dedata.shape[1]/2:
		width_half = 5
		print 'Taking Center '
#	onpulse_data	= dedata[:,lo-width_half:lo+width_half].mean(axis=1)
	
	offpulse_data1	= dedata[:,lo-width_half*4:lo-width_half*3].mean(axis=1)
	offpulse_data2	= dedata[:,lo+width_half*3:lo+width_half*4].mean(axis=1)
	offpulse_data   = (offpulse_data1 + offpulse_data2)/2
	freq_dedata	= dedata[:,lo-width_half:lo+width_half].mean(axis=1)
	on_off = freq_dedata - offpulse_data
	on_off = signal.medfilt(on_off,3)
#	on_off_p = signal.medfilt(on_off,on_off.size/2*6+1)
#	on_off = on_off - on_off_p
#	np.ma.set_fill_value(on_off,on_off.mean())
#	print on_off
#	print on_off.mean()
	on_off[on_off==np.nan] = np.mean(on_off)
#	plt.plot(on_off)
#	plt.show()
#	exit()
	p_1 	= [1,0]
	popt,pcov = curve_fit(f_1,axis_freq,on_off,p0=p_1,maxfev=5000000)
	on_off_fit = f_1(axis_freq,*popt)
	on_off_std1 = on_off+on_off.std()*2
        on_off_std2 = on_off-on_off.std()*2
	
	


	#Set the area for plot
	
        left_x,left_y=0.1,0.1
        width,height=0.6,0.6
        left_xh=left_x+width
        left_yh=left_y+height

        dedis_area=[left_x,left_y,width,height]
        #hist_x=[left_x,left_yh,width,0.2]
        hist_x=[left_x,left_yh,width,0.2]
        hist_y=[left_xh,left_y,0.2,height]
#        label_area =[left_xh,left_yh,0.1,0.2]

        #create combine plot with plt.axes

       # fig=plt.figure(figsize = (24,8))
        fig=plt.figure(figsize = (8,8))
	fig.text(0.71,0.78,textplot,fontsize=9,bbox=dict(facecolor='lightblue'),color='red')
        area_dedis = plt.axes(dedis_area)
        area_histx = plt.axes(hist_x,sharex=area_dedis)
        area_histy = plt.axes(hist_y,sharey=area_dedis)
#        area_label = plt.axes(label_area)
#        area_label.text(0.1,0.5,fil_n+'\nstart:'+str(star_s)+'\nDM:'+str(DM)+'\nSNR:'+str(SNR)+'\nMJD:'+str(mjd))
#        area_label.text(0.1,0.5,fil_n+'\nDM:'+str(DM)+'\nSNR:'+str(SNR)+'\nMJD:'+str(mjd))

        #begin to plot
	#Central 2D plot
	axis_time = axis_time#1000.
        area_dedis.set_ylabel('Frequency(MHz)')
        area_dedis.set_xlabel('Time(ms)')
        area_dedis.set_ylim(axis_freq.min(),axis_freq.max())
        area_dedis.set_xlim(-time_max,time_max)
	vmax = dedata.mean()+dedata.std()*2
	vmin = dedata.mean()-dedata.std()*2
#	vmax = np.median(dedata)#dedata.max()
#	vmin = np.median(dedata-dedata.std())
#        im=area_dedis.pcolormesh(axis_time,axis_freq,dedata,vmax=vmax,vmin=vmin,cmap='Blues')
        im=area_dedis.pcolormesh(axis_time,axis_freq,dedata,vmax=vmax,vmin=vmin,cmap='gray_r')
#        im=area_dedis.pcolormesh(axis_time,axis_freq,dedata,vmax=vmax,vmin=vmin,cmap='copper_r')
#        im=area_dedis.pcolormesh(axis_time,axis_freq,dedata,vmax=vmax,vmin=vmin,cmap=new_cmap)
#        im=area_dedis.pcolormesh(axis_time,axis_freq,dedata,cmap='copper_r')
#        cbaxes = fig.add_axes([0.04, 0.1, 0.01, 0.65])
#        cb = plt.colorbar(im, cax = cbaxes)
#	area_dedis.axvline(width_g,color='y',linestyle='dashed')
 #       area_dedis.axvline(-width_g,color='y',linestyle='dashed')
#        area_dedis.axvline(0,color='r',linestyle='dashed')
#       plt.colorbar(im,orientation="horizontal",ax=area_dedis)
	
	#Top 1D plot
        #area_histx.plot(axis_time,dedata_1D_fit,'r:')
        area_histx.plot(axis_time,dedata_1D,'black')
        area_histx.plot(axis_time,dedata_1D_fit,'r:')
	area_histx.axhline(dedata_1D.mean()+dedata_1D.std()/2,linestyle='-.')
        area_histx.axhline(dedata_1D.mean()-dedata_1D.std()/2,linestyle='-.')
#	lo_max = np.where(dedata_1D == dedata_1D.max())
#	area_histx.plot(axis_time[lo_max],dedata_1D[lo_max],'ro',label='%.1f'%axis_time[lo_max])
	
#	area_histx.legend(frameon=False)
#        area_histx.grid(axis='x')
#       area_histx.title('Dedisperse all the File')

#        area_label.get_xaxis().set_visible(False)
#        area_label.get_yaxis().set_visible(False)
        area_histx.get_xaxis().set_visible(False)
        #area_histx.get_xaxis().set_visible(True)
        area_histx.get_yaxis().set_visible(True)
#	area_histx.axvline(width_g,color='y',linestyle='dashed')
#	area_histx.axvline(-width_g,color='y',linestyle='dashed')
#	area_histx.axvline(0,color='r',linestyle='dashed')
	xmajorLocator=[0,10*int(dedata_1D.max()/10+1)]
        #area_histx.yaxis.set_minor_locator(xmajorLocator)
#        area_histx.set_yticks(xmajorLocator)
	area_histx.set_xlim(dedata_1D.min()-0.1,1.1)
#        area_histx.set_xlim(axis_time.min(),axis_time.max())
	area_histx.set_xlim(-time_max,time_max)

	
	##Right 1D plot

        area_histy.set_ylim(axis_freq.min(),axis_freq.max())
        area_histy.set_xlim(on_off_std2.min(),on_off_std1.max())
        #area_histx.xaxis.set_minor_locator(xmajorLocator)
        area_histy.plot(on_off,(axis_freq),'k-')# , sharey = True)
        area_histy.plot(on_off_fit,(axis_freq),'k--')
	area_histy.fill_betweenx(axis_freq,on_off_std1,on_off_std2,where=on_off_std1>= on_off_std2,facecolor='gray')
        #area_histy.grid(axis='y')
#        area_histy.get_xaxis().set_visible(False)
        area_histy.get_yaxis().set_visible(False)
	#area_histy.set_xticks([0,5*int(on_off_std1.max()/5+1)])
	area_histy.set_xticks([0,round(on_off_std1.max())])
	area_histy.tick_params(top=False, bottom=True,
                   labeltop=False, labelbottom=True)
	
        a = fig
#        plt.close()
        return a
