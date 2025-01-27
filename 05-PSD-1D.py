import matplotlib.pyplot as plt
import struct
import numpy as np
import pandas as pd
from   tqdm import tqdm
from   scipy import io as sio
from   scipy.interpolate import interp1d
from   scipy.integrate import quad
from  lib.plot import *  
from  lib.configs import *
import argparse

"""
Available: Prof#2,6,7,8,9
"""

parser = argparse.ArgumentParser()
parser.add_argument('--prof',default=4,type=int)
parser.add_argument('--var',default="U",type=str)
args = parser.parse_args()
plt_setUp_Smaller()

AOA = 11 
Rec = 200
fldr='../database/tsrs/002-SP-1D/' 
save_dir = 'Figs/04-FFT/'
sides = ['SS',"PS"]
AlphaList = [['(a)',"(b)","(c)","(d)"],["(e)","(f)","(g)","(h)"]]

def name_file(fldr,name,nprof,var):
    data_to_load= fldr + f"SP1D_{name}_{nprof}.mat"
    return data_to_load



def post_process_Spectra(out):
    lstar = out['lstar'].squeeze()
    utau  = out['utau'].squeeze()
    lmd = out['lambda'].squeeze()
    yn  = out['yn'].squeeze()
    puu = np.abs(out['Puu'])
    z= out['z']
    Nz = z.shape[1]
    Lz = z.max()
    fact = z.max()/Nz
    prem = np.linspace(0,Lz,Nz//2+1)

    for iy in range(len(yn)):
      puu[iy,:] = fact * prem * puu[iy,:]/utau**2


    data = {
          'lmd':lmd[1:]/lstar,
          'yn':yn/lstar,
          'puu':puu[:,1:],
              }
    
    return data

NPROF = args.prof 
VAR   = args.var
#######################################
# OVER SUCTION/PRESSURE SIDE 
#######################################
for caseName in data.keys():
    name = data[caseName]['label']
    print(name)
    if 'Case' in name:
      loc = name.find('e')
      name = name[:loc+1]+name[-1]

    fname= name_file(fldr,name,NPROF,VAR)
    print(fname)
    data[caseName][f'data'] = post_process_Spectra(sio.loadmat(fname))
    print(f"[IO] DATA: {fname}")



levels = np.array([0.2,0.8])
fig,axs = plt.subplots(1,1)
for kl, case_name in enumerate(reversed(data.keys())):
    d = data[case_name]['data']
    style_dict = data[case_name]['style']
    text_loc=(0.9-kl*0.1,0.9-kl*0.1)
    fig,axs = plot_1DPSD(d,fig,axs,style_dict,levels,text_loc)


axs.set(**{
      'xscale':'log',
      'xlabel':r'$\lambda^+_z$',
      'xlim':[20,2000],
      'yscale':'log',    
      'ylabel':r'$y^+_n$',
      'ylim':[1,500],
            })

axs.xaxis.set_minor_locator(locmin)
axs.xaxis.set_major_locator(locmin)        
axs.yaxis.set_minor_locator(locmin)
axs.yaxis.set_major_locator(locmin)
axs.grid(**grid_setup)

fig.savefig(f'Figs/04-FFT/Prof_SP1D_Prof4.jpg',**{'dpi':300,'transparent':True,'bbox_inches':'tight'})
fig.savefig(f'Figs/04-FFT/Prof_SP1D_Prof4.pdf',**{'dpi':300,'transparent':True,'bbox_inches':'tight'})
print('[IO] Spectra Figure Saved')

