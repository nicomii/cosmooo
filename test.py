import numpy as np
import os 
from matplotlib import pyplot as plt
import matplotlib.colors as colors
import matplotlib.ticker
from matplotlib.ticker import LogFormatter
from matplotlib import rc
from scipy import integrate

def adotinv(a, om, ol, orad):
    ok = 1 - om - ol - orad
    adot = a * np.sqrt(orad * a**-4 + om * a**-3 + ok * a**-2 + ol)
    return 1.0/adot

def aadotinv(a, om, ol, orad):
    ok = 1 - om - ol - orad
    aadot = a**2 * np.sqrt(orad * a**-4 + om * a**-3 + ok * a**-2 + ol)
    return 1.0/aadot

def hubble(a, om, ol, orad):
    ok = 1 - om - ol - orad
    adotovera =  np.sqrt(orad * a**-4 + om * a**-3 + ok * a**-2 + ol)
    return 1 / adotovera

def Ez(z, om, ol, orad):
    ok = 1 - om - ol - orad
    Ez = np.sqrt(orad * (1 + z)**4 + om * (1 + z)**3 + ok * (1 + z)**2 + ol) 
    return 1 / Ez

def Sk(xx, om, ol, orad):
    ok = 1 - om - ol - orad
    if ok < 0:
        dk = np.sin(np.sqrt(-ok) * xx) / np.sqrt(-ok)
    elif ok > 0:
        dk = np.sinh(np.sqrt(ok) * xx) / np.sqrt(ok)
    else:
        dk = xx
    return dk



dir_path = os.path.dirname(os.path.realpath(__file__))

c = 299792.458 
H0kmsmpc = 70.  
H0s = H0kmsmpc * 3.2408e-20 
H0y = H0s * 3.154e7 * 1.e9 
cH0mpc = c/H0kmsmpc   
cH0Glyr = cH0mpc * 3.262 / 1000 
    



astart, astop, astep = 0, 2.1, 0.05
a_arr = np.arange(astart, astop, astep)

om, ol, orad = 0.3, 0.7, 0.00005

ok = 1 - om - ol - orad
Rscale = a_arr * c / (np.sqrt(abs(ok)) * H0kmsmpc)
t_lookback_Gyr = np.array([integrate.quad(adotinv, 1, upper_limit, args=(om,ol, orad))[0] for upper_limit in a_arr])/H0y

fig, ax = plt.subplots()
ax.plot(t_lookback_Gyr,a_arr,label='$(\Omega_M,\Omega_\Lambda)$=(%.2f,%.2f)'%(om,ol)) 
ax.axvline(x=0,linestyle=':'); plt.axhline(y=1,linestyle=':') 
ax.set_xlabel('Lookback Time (Gyr)'); ax.set_ylabel('Scalefactor ($a$)')
ax.legend(loc='lower right',frameon=False)
ax2 = ax.twinx()        
ax2.plot(t_lookback_Gyr, Rscale, alpha=0); 
fig.savefig('C:\\Users\\neha\\Documents\\GitHub\\cosmoo\\sf_lookback_close.png', dpi=200, bbox_inches='tight', pad_inches = 0.01)
plt.close(fig)



om_arr = np.arange(0,2.1,0.4)
fig, ax = plt.subplots()
ax2 = ax.twinx()
for OM in om_arr:
    t_lookback_Gyr = np.array([integrate.quad(adotinv, 1, upper_limit, args=(OM, ol, orad))[0] for upper_limit in a_arr]) / H0y  #calculates lookback time for some om 
    ax.plot(t_lookback_Gyr, a_arr, label='$(\Omega_M,\Omega_\Lambda)$=(%.1f,%.1f)'%(OM,ol))     
    ax2.plot(t_lookback_Gyr, Rscale)    

ax.axvline(x=0,linestyle=':'); ax.axhline(y=1,linestyle=':') 
ax.set_xlabel('Lookback time (Gyr)'); ax.set_ylabel('Scalefactor ($a$)')  
ax.legend(loc='upper left',frameon=False)
ax2.set_ylabel("Scale Factor $R$")
fig.savefig('C:\\Users\\neha\\Documents\\GitHub\\cosmoo\\sf_lookbaack.png', dpi=200, bbox_inches='tight', pad_inches = 0.01)
plt.close(fig)



om_arr = np.arange(0, 10, 0.1); ol_arr = np.arange(-10, 10, 0.1)
MAge_of_uni = np.zeros(len(om_arr))         
LAge_of_uni = np.zeros(len(ol_arr))        
for i, OM in enumerate(om_arr):
    MAge_of_uni[i] = integrate.quad(adotinv, 0, 1, args=(OM, ol, orad))[0] / H0y       
for i, OL in enumerate(ol_arr):
    LAge_of_uni[i] = integrate.quad(adotinv, 0, 1, args=(om, OL, orad))[0] / H0y       
fig, ax = plt.subplots()
ax.plot(om_arr, MAge_of_uni, color='g', label='Mass Density $\Omega_m$ $(\Omega_\Lambda = 0.7)$')  
ax.plot(ol_arr, LAge_of_uni, color='#307CC0', label='Cosmological Constant $\Omega_\Lambda$ \n $(\Omega_m = 0.3)$')
ax.set_xlabel("Density Parameter Value ($\Omega_i$)"); ax.set_ylabel("Age of Universe (Gyr)")  
ax.legend(loc='upper left'); 
ax.axvline(x=0,linestyle=':')
fig.savefig('C:\\Users\\neha\\Documents\\GitHub\\cosmoo\\age_density.png', dpi=200, bbox_inches='tight', pad_inches = 0.01)
plt.close(fig)


om_arr = np.arange(0, 1, 0.02); ol_arr = np.arange(0, 1.5, 0.02)
ages = np.array([[integrate.quad(adotinv, 0, 1, args=(OM, OL, orad))[0] / H0y for OM in om_arr] for OL in ol_arr])
fig, ax = plt.subplots()
age = ax.pcolormesh(om_arr, ol_arr, ages)
agemax = 0; agemin = 30
for agearray in ages:
    for age in agearray:
        if np.isnan(age):
            continue
        else:
            if age >= agemax:
                agemax = age
            if age <= agemin:
                agemin = age
pcm = ax.pcolor(om_arr, ol_arr, ages, norm = colors.LogNorm(vmin=agemin, vmax=agemax), shading = 'auto')
cb = fig.colorbar(pcm, orientation='vertical', label="Age of Universe (Gyr)", format='%2.f', ticks=[10, 15, 20, 25, 30, 40])
ax.set_xlabel("$\Omega_m$"); ax.set_ylabel("$\Omega_\Lambda$")
fig.savefig('C:\\Users\\neha\\Documents\\GitHub\\cosmoo\\age_param.png', dpi=200, bbox_inches='tight', pad_inches = 0.01)
plt.close(fig)



fig, ax = plt.subplots()
redshift = -1 + (1 / a_arr[1:])        
ax.plot(a_arr[1:], redshift)
ax.set_xlabel("Scalefactor ($a$)"); ax.set_ylabel("Redshift ($z$)")
fig.savefig('C:\\Users\\neha\\Documents\\GitHub\\cosmoo\\redshift_sf.png', dpi=200, bbox_inches='tight', pad_inches = 0.01)
plt.close(fig)



amin, amax, astep = 0.1, 1, 0.05
a_arr = np.arange(amin, amax + astep, astep)
redshift = -1 + (1 / a_arr)        
t_lookback_Gyr = np.array([integrate.quad(adotinv, 1, upper_limit, args=(om, ol, orad))[0] for upper_limit in a_arr]) / H0y
fig, ax = plt.subplots()
ax.plot(redshift, t_lookback_Gyr)
ax.set_xlabel("Redshift ($z$)"); ax.set_ylabel("Lookback Time (Gyr)")
ax.set_xlim(xmin=0); ax.set_ylim(ymax=0)
fig.savefig('C:\\Users\\neha\\Documents\\GitHub\\cosmoo\\lookback_redshift.png', dpi=200, bbox_inches='tight', pad_inches = 0.01)
plt.close(fig)



minlog, maxlog = -6, 2
a_arr = np.logspace(minlog, maxlog, num=100, base=10)
ok = 1 - orad - om - ol
norm_om = (om * a_arr**-3) / ((om * a_arr**-3) + (orad * a_arr**-4) + ol)       #normalised mass density, om / otot
norm_orad = (orad * a_arr**-4) / ((om * a_arr**-3) + (orad * a_arr**-4) + ol)   #normalised radiation density, orad / otot
norm_ol = ol / ((om * a_arr**-3) + (orad * a_arr**-4) + ol)                     #normalised cosmo constant, ol / otot

fig, ax = plt.subplots()
ax.plot(a_arr, norm_om, label="$\Omega_m$")        #a nice blue colour
ax.plot(a_arr, norm_orad, label="$\Omega_r$")            #standard red colour
ax.plot(a_arr, norm_ol, label="$\Omega_\Lambda$")  #a nice purple colour
ax.set_xscale("log")
ax.xaxis.set_major_locator(matplotlib.ticker.LogLocator(base=10, numticks=(abs(minlog) + abs(maxlog) + 2))) #numticks must be > the number of ticks for some reason??
ax.xaxis.set_minor_locator(matplotlib.ticker.LogLocator(base=10.0,subs=(0.2,0.4,0.6,0.8),numticks=(abs(minlog) + abs(maxlog) + 2)))     #makes a minor tick for each increment of 0.2 between major ticks
ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter()) #this removes labels from the minor ticks
ax.set_xlabel("Scalefactor ($a$)"); ax.set_ylabel("Normalised Density ($\Omega_i / \Omega_{tot}$)")
ax.legend(loc='center right')
ax.set_ylim(ymin=-0.003, ymax=1.003); ax.set_xlim(min(a_arr), max(a_arr))   #sets ylim just below 0 so that you can see the bottom of the curves properly

ax2 = ax.twiny()
ax2.set_xscale("log")
locs = ax.get_xticks()[1:-1]
print(locs)
# ax2.ticklabel_format(axis='x', style='sci', useMathText=True)
ax2ticks = []
for i, tick in enumerate(locs):
    if tick > 1:
        ax2ticks.append("")
    else:
        ax2ticks.append(str("$10^{" + str(round(np.log10(1/tick))) + "}$")) #calculates the time associated with scale factor of a=tick
mn, mx = ax.get_xlim(); ax2.set_xlim(mn, mx)
ax2.set_xticks(locs); ax2.set_xticklabels(ax2ticks)
ax2.set_xlabel("Redshift ($z$)")

fig.savefig('C:\\Users\\neha\\Documents\\GitHub\\cosmoo\\density_sf', dpi=200, bbox_inches='tight', pad_inches = 0.01)
#fig.savefig(dir_path+'\\Part One Graphs\\Normalised Densities vs Scalefactor.pdf', dpi=200, bbox_inches='tight', pad_inches = 0.01)
plt.close(fig)



amin, amax, astep, scalestep = 0.02, 2, 0.02, 0.2
a_arr = np.arange(amin, amax + astep, astep)
times = np.zeros(len(a_arr))
fig, ax = plt.subplots()
ax2 = ax.twiny()        #create alternate x-axis to sit at the top (represents scalefactor a)
scaletickslabs, scaletickslocs = [0], [0]       #initialize lists for the alternate (top) x-axis ticks
for i, a in enumerate(a_arr):
    times[i] = integrate.quad(adotinv, 0, a, args=(om, ol, orad))[0] / H0y      #calculates age of universe at scale factor a
    if a == 1:
        ax.axvline(x=times[i],linestyle=':')        #plots a vertical line at current scale factor (age of universe)
for a in np.arange(0, amax + scalestep, scalestep):
    if a == 0:
        pass        
    else:
        time = integrate.quad(adotinv, 0, a, args=(om, ol, orad))[0] / H0y      #calculate at which time to place the scalefactor tick a
        scaletickslocs.append(time)     #location of this scalefactor tick with respect to the time axis
        scaletickslabs.append(round(a, 1))  #label of this scalefactor tick
hubble_arr = H0kmsmpc * (adotinv(a_arr, om, ol, orad) * a_arr)**-1    #inverse due to the adotinv function being the reciprocal
ax.plot(times, hubble_arr)
ax.set_xlabel("Age of Universe (Gyr)"); ax.set_ylabel("Hubble Parameter (km/s/Mpc)")
ax.set_yscale('log')
ax.axhline(y=H0kmsmpc,linestyle=':')
ax.set_xlim(xmin=min(a_arr))

mn, mx = ax.get_xlim()
ax2.set_xlim(mn, mx)  
ax2.set_xlabel("Scalefactor ($a$)")
fig.savefig('C:\\Users\\neha\\Documents\\GitHub\\cosmoo\\h_t', dpi=200, bbox_inches='tight', pad_inches = 0.01)
plt.close(fig)




zstart, zstop, zstep = 0, 4, 0.01
zarr = np.arange(zstart, zstop + zstep, zstep)

xarr = np.zeros(len(zarr))
axarr = np.zeros(len(zarr))
for i, z in enumerate(zarr):
    xarr[i] = integrate.quad(Ez, 0, z, args=(om, ol, orad))[0] 
    axarr[i] = (1 / (1 + z)) * integrate.quad(Ez, 0, z, args=(om, ol, orad))[0]     #this is effectively a * R0x - distance to light source seen at redshift z at time of light emission
    
R0X = xarr * cH0Glyr # Distance in Glyr
aR0X = axarr * cH0Glyr # Distance in Glyr

fig, ax = plt.subplots()
ax.plot(zarr,R0X)
ax.set_xlabel('Redshift ($z$)'); ax.set_ylabel('$R_0\chi$ (Glyr)')
ax.set_xlim(xmin=0); ax.set_ylim(ymin=0)
fig.savefig('C:\\Users\\neha\\Documents\\GitHub\\cosmoo\\', dpi=200, bbox_inches='tight', pad_inches = 0.01)
plt.close(fig)

fig, ax = plt.subplots()
ax.plot(zarr,aR0X)
ax.set_xlabel('Redshift ($z$)'); ax.set_ylabel('Light Emission Distance $aR_0\chi$ (Glyr)')
ax.set_xlim(xmin=0); ax.set_ylim(ymin=0)
fig.savefig('C:\\Users\\neha\\Documents\\GitHub\\cosmoo\\dist_redshift', dpi=200, bbox_inches='tight', pad_inches = 0.01)
plt.close(fig)



om, ol, orad = 0.3, 0.7, 0.00005
DD = R0X                                                     # Proper distance
DL = cH0Glyr * Sk(xarr, om, ol, orad) * (1 + zarr)           # Luminosity distance
DA = cH0Glyr * Sk(xarr, om, ol, orad) / (1 + zarr)           # Angular diameter distance

fig, ax = plt.subplots()
ax.plot(zarr, DD, label='Proper Distance')
ax.plot(zarr, DL, label='Luminosity Distance')
plt.plot(zarr, DA, label='Angular Diameter Distance')
ax.legend()
ax.set_xlabel('Redshift ($z$)'); ax.set_ylabel('Distances (Glyr)')
ax.set_xlim(xmin=0)
fig.savefig('C:\\Users\\neha\\Documents\\GitHub\\cosmoo\\redshift_da', dpi=200, bbox_inches='tight', pad_inches = 0.01)
plt.close(fig)



#the following (huge bit of) code creates the spacetime diagram :)
om, ol, orad = 0.3, 0.7, 0.00005
scalemin, scalemax, scalestep = 0.00001, 2, 0.001
ScaleArr = np.arange(scalemin, scalemax + scalestep, scalestep)

ParticleHoriz = np.zeros(len(ScaleArr))
EventHoriz = np.zeros(len(ScaleArr))
HubbleHoriz = np.zeros(len(ScaleArr))
LightCone = np.zeros(len(ScaleArr))
for i, a in enumerate(ScaleArr):
    ParticleHoriz[i] = integrate.quad(aadotinv, 0, a, args=(om, ol, orad))[0]
    EventHoriz[i] = integrate.quad(aadotinv, a, np.inf, args=(om, ol, orad))[0]
    HubbleHoriz[i] = adotinv(a, om, ol, orad)
    
ParticleHoriz = ParticleHoriz * cH0Glyr # Distance in Glyr
EventHoriz = EventHoriz * cH0Glyr
HubbleHoriz = HubbleHoriz * cH0Glyr
Lightcone = np.array([integrate.quad(aadotinv, lower_limit, 1, args=(om,ol, orad))[0] for lower_limit in np.arange(0.001, 1, 0.001)]) * cH0Glyr     #light cone is only defined for a<=1

w, h = plt.figaspect(0.333)  #aspect ratio of about 3:1 for width:height, so it's a nice, wide image
fig, ax = plt.subplots(figsize=(w, h)); ax2 = ax.twinx()
ParticleColour = 'g'; EventColour = 'r'; HubbleColour = '#307CC0'; LightColour = '#8F4F9F'; DarkColour = 'gray'

ax.plot(ParticleHoriz, ScaleArr, color=ParticleColour, label="Particle Horizon"); ax.plot(-ParticleHoriz, ScaleArr, color=ParticleColour)
ax.plot(EventHoriz, ScaleArr, color=EventColour, label="Event Horizon"); ax.plot(-EventHoriz, ScaleArr, color=EventColour)
ax.plot(HubbleHoriz, ScaleArr, color=HubbleColour, label="Hubble Sphere"); ax.plot(-HubbleHoriz, ScaleArr, color=HubbleColour)
ax.plot(Lightcone, np.arange(0.001, 1, 0.001), color=LightColour, label="Light Cone"); ax.plot(-Lightcone, np.arange(0.001, 1, 0.001), color=LightColour);

plt.fill_betweenx(ScaleArr, EventHoriz, HubbleHoriz, color=EventColour, alpha=0.15);  plt.fill_betweenx(ScaleArr, -EventHoriz, -HubbleHoriz, color=EventColour, alpha=0.15);

ax.legend(loc="lower right"); ax.grid(which="major")
ax.axhline(y=1, linestyle='-', color='k', alpha=0.7)
ax.set_xlabel('Comoving Distance $R_0 \chi$ (Glyr)'); ax.set_ylabel('Scalefactor ($a$)')
ax.set_ylim(0, max(ScaleArr)); ax.set_xlim(-max(EventHoriz), max(EventHoriz))

#the following code creates the time y-axis on the right hand side
locs = ax.get_yticks()[:-1]
ax2ticks = np.zeros(len(locs))
for i, tick in enumerate(locs):
    if tick == 0:
        ax2ticks[i] = "0"
    else:
        ax2ticks[i] = str(round(integrate.quad(adotinv, 0, tick, args=(om,ol, orad))[0]/H0y, 1)) #calculates the time associated with scale factor of a=tick
mn, mx = ax.get_ylim(); ax2.set_ylim(mn, mx)
ax2.set_yticks(locs); ax2.set_yticklabels(ax2ticks)
ax2.set_ylabel("Time (Gyr)")

#now to create the redshift ticks on the top x-axis
ax3 = ax.twiny()
mn, mx = ax.get_xlim()
ax3.set_xlabel("Redshift (z)")
ax3.set_xlim(mn, mx)        #set redshift x-axis to be same width as comoving coord x-axis
redshifts = np.array([0, 1, 2, 5, 10, 50, 1000])
CoMovCoord = np.zeros(len(redshifts))
for i, z in enumerate(redshifts):
    CoMovCoord[i] = cH0Glyr * integrate.quad(Ez, 0, z, args=(om, ol, orad))[0]      #calculates the comoving coord at which to put the redshift tick 
    ax3.axvline(CoMovCoord[i], linestyle=":", alpha=0.5)      #puts a dotted vertical line at redshift z
    ax3.axvline(-CoMovCoord[i], linestyle=":", alpha=0.5)     #as above but in the negative x-axis

CoMovCoord = np.append(-CoMovCoord[::-1], CoMovCoord)
redshifts = np.append(redshifts[::-1], redshifts)
ax3.set_xticks(CoMovCoord); ax3.set_xticklabels(redshifts)

#now to save the graph
plt.fill_between(EventHoriz, mx * np.ones(len(ScaleArr)), ScaleArr, alpha=0.2)    #colours in the area between a horizontal line high up and the event horizon
plt.fill_between(-EventHoriz, mx * np.ones(len(ScaleArr)), ScaleArr,  alpha=0.2)   #as above but on the negative x-axis
fig.savefig('C:\\Users\\neha\\Documents\\GitHub\\cosmoo\\sptime.png', dpi=200, bbox_inches='tight', pad_inches = 0.01)
plt.close(fig)

