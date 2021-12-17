import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle



###########################################
#		  RaJ2000 	DecJ2000
#1st Pulse:	16:01:58.49 , -11:17:41.82
#2nd Pulse:	16:02:01.85 , -11:17:41.92
#3rd Pulse:	16:02:08.67 , -11:17:42.02
#4th Pulse:	16:01:57.23 , -11:16:33.40

#3rd Pulse:	16:02:04.04 , -11:26:46.40(No Rotation)
#4th Pulse:     16:02:03.37 , -11:31:52.01(No Rotation)
###########################################

##################################
#Take arcmin as minimum dimension
#1 minute = 15 arcmin
#1 second = 15 arcsec
ra_1st = (16*60+1+58.49/60.)*15
ra_2nd = (16*60+2+01.85/60.)*15
ra_3rd = (16*60+2+08.67/60.)*15
ra_4th = (16*60+1+57.23/60.)*15
#ra_3rd = (16*60+2+4.04/60.)*15

dec_1st = - (11*60+17+41.82/60.)
dec_2nd = - (11*60+17+41.92/60.)
dec_3rd = - (11*60+17+42.02/60.)
dec_4th = - (11*60+16+33.40/60.)
#dec_3rd = - (11*60+26+46.40/60.)


beamwidth_1st = 2.85/2
beamwidth_2nd = 2.85/2
beamwidth_3rd = 2.95/2
beamwidth_4th = 2.95/2
#################################

fig = plt.figure(figsize=[7,7])
ax = fig.add_subplot(111)

#ell1 = Ellipse(xy = (0.0, 0.0), width = 4, height = 8, angle = 30.0, facecolor= 'yellow', alpha=0.3)
trans = 0.5
times = 4
snr_1 = 9.7
snr_2 = 9.2
snr_3 = 8.2
snr_4 = 6.6

snr_tol = (snr_1 + snr_2 +snr_3 +snr_4)
snr_1 = 9.7 /snr_tol
snr_2 = 9.2 /snr_tol
snr_3 = 8.2 /snr_tol
snr_4 = 6.6 /snr_tol

mean_ra_m = (ra_1st*snr_1+ ra_2nd*snr_2 + ra_3rd*snr_3 + ra_4th*snr_4)
mean_dec_m= (dec_1st*snr_1 + dec_2nd*snr_2 + dec_3rd*snr_3 + dec_4th*snr_4)
mean_ra = (ra_1st+ ra_2nd + ra_3rd + ra_4th)/4.
mean_dec= (dec_1st + dec_2nd + dec_3rd + dec_4th)/4.

print '==========================='
print 'Mean Weighted Location:'
print "Ra: %02d:%02d:%3.2f"%(np.int(mean_ra/15/60),np.int(mean_ra/15%60),(mean_ra/15%60-np.int(mean_ra/15%60))*60)
print "Dec:%02d:%02d:%3.2f"%(np.int(mean_dec/60),np.int(abs(mean_dec)%60),(abs(mean_dec)%60-np.int(abs(mean_dec)%60))*60)
print '---------------------------'
print 'SNR Weighted Location:'
print "Ra: %02d:%02d:%03.2f"%(np.int(mean_ra_m/15/60),np.int(mean_ra_m/15%60),(mean_ra_m/15%60-np.int(mean_ra_m/15%60))*60)
print "Dec:%02d:%02d:%03.2f"%(np.int(mean_dec_m/60),np.int(abs(mean_dec_m)%60),(abs(mean_dec_m)%60-np.int(abs(mean_dec_m)%60))*60)
print '==========================='

color ='yellow'
cir1 = Circle(xy = (ra_1st,dec_1st), radius=beamwidth_1st, alpha=trans,facecolor=color,label='1st,2nd and 3rd  Pulses from Beam 2')
cir2 = Circle(xy = (ra_2nd,dec_2nd), radius=beamwidth_2nd, alpha=trans,facecolor='green',label='2nd Pulse')
cir3 = Circle(xy = (ra_3rd,dec_3rd), radius=beamwidth_3rd, alpha=trans,facecolor= 'pink',label='3rd Pulse')
cir4 = Circle(xy = (ra_4th,dec_4th), radius=beamwidth_4th, alpha=trans,facecolor='cyan',label='4th Pulse from Beam 6')
cir_central = Circle(xy = (mean_ra,mean_dec), radius=beamwidth_3rd, edgecolor='k',linestyle='--',facecolor='None',alpha=1,lw=3)
cir_std = Circle(xy = (mean_ra,mean_dec), radius=beamwidth_3rd*2, edgecolor='k',linestyle='--',facecolor='None',alpha=0.8,lw=1)
cir_central_m = Circle(xy = (mean_ra_m,mean_dec_m), radius=beamwidth_3rd, edgecolor='r',linestyle='--',facecolor='None',alpha=1,lw=3)
cir_std_m = Circle(xy = (mean_ra_m,mean_dec_m), radius=beamwidth_3rd*2, edgecolor='green',linestyle='--',facecolor='None',alpha=0.8,lw=1)
#ax.add_patch(ell1)
ax.add_patch(cir1)
ax.add_patch(cir2)
ax.add_patch(cir3)
ax.add_patch(cir4)
ax.add_patch(cir_central)
ax.add_patch(cir_std)
ax.add_patch(cir_central_m)
ax.add_patch(cir_std_m)
#x, y = 0, 0

#plt.axis('scaled')
#plt.title('')
print ra_1st,ra_2nd,ra_3rd,ra_4th
print dec_1st,dec_2nd,dec_3rd,dec_4th

ax.plot(mean_ra ,mean_dec, 'ro')
#ax.plot(ra_1st ,dec_1st, 'ro')
#ax.plot(ra_2nd ,dec_2nd, 'go')
#ax.plot(ra_3rd ,dec_3rd, 'bo')
#ax.plot(ra_4th ,dec_4th, 'ko')
xloc = np.linspace(mean_ra-beamwidth_3rd*times,mean_ra+beamwidth_3rd*times,5)
yloc = np.linspace(mean_dec-beamwidth_3rd*times,mean_dec+beamwidth_3rd*times,5)
xticks = []
yticks = []
for i in range(5):
	xticks.append("%dh%dm%.1fs"%(np.int(xloc[i]/15/60),np.int(xloc[i]/15%60),(xloc[i]/15%60-np.int(xloc[i]/15%60))*60))
	yticks.append("-%dd%dm"%(np.int(yloc[i]/60),np.int(abs(yloc[i])%60)))

plt.xlim(mean_ra-beamwidth_3rd*times,mean_ra+beamwidth_3rd*times)
plt.ylim(mean_dec-beamwidth_3rd*times,mean_dec+beamwidth_3rd*times)
plt.xticks(xloc,xticks)
plt.yticks(yloc,yticks)
plt.xlabel('Right Ascension')
plt.ylabel('Declination')
#plt.axis('equal')   #changes limits of x or y axis so that equal increments of x and y have the same length
ax.tick_params(direction='in',width=0.7,length=2,color='k')
#plt.rcParams['xtick.direction']='in'
#plt.rcParams['ytick.direction']='in'
plt.legend()
plt.savefig('pointing.png')
plt.show()
