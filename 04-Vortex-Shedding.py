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
parser.add_argument('--prof',default=9,type=int)
parser.add_argument('--var',default="U",type=str)
args = parser.parse_args()
plt_setUp_Smaller()


AOA = 11 
Rec = 200
fldr='../database/tsrs/001-shedding-data/' 
save_dir = 'Figs/04-FFT/'
sides = ['SS',"PS"]
AlphaList = [['(a)',"(b)","(c)","(d)"],["(e)","(f)","(g)","(h)"]]

def name_file(fldr,name,nprof,var):
    data_to_load= fldr + f"signal_{name}_{nprof}_{var}.mat"
    return data_to_load


NPROF = args.prof 
VAR   = args.var

Nprofs = [7,9]
Vars = ['U','P']
#######################################
# OVER SUCTION/PRESSURE SIDE 
#######################################
for caseName in data.keys():
    name = data[caseName]['label']
    print(name)
    if 'Case' in name:
      loc = name.find('e')
      name = name[:loc+1]+name[-1]
    for nprof in Nprofs:
      for var in Vars:
        fname= name_file(fldr,name,nprof,var)
        print(fname)
        data[caseName][f'data_{nprof}_{var}'] = sio.loadmat(fname)
        print(f"[IO] DATA: {fname}")


var_name = {
              'U':r'$u_t$',
              'P':r"$p'$",
            }

fig, axss = plt.subplots(2,2,figsize=(16,10))
AlphaList = [["(a)","(c)"],["(b)","(d)"],]
for caseName in data.keys():
  for il, nprof in enumerate(Nprofs):
    for jl, var in enumerate(Vars):
      axs = axss[jl,il]
      d = data[caseName][f'data_{nprof}_{var}']
      style=data[caseName]['style']
      fig,axs=plot_FFT(d,fig,axs,style)
      xc = d['xloc'][0][0]
      
      axs.grid(**grid_setup)
      axs.set(**var_name_dict['psd']['axs'])
      axs.set_title( AlphaList[il][jl]  +\
                    " " + f"{var_name[var]}" + ",  " + \
                    rf'$x/c = {xc} $',**title_setup)
fig.subplots_adjust(**{"wspace":0.2,'hspace':0.5})

fig.savefig(save_dir+f'FFT_4.jpg',**{"dpi":300,'transparent':True,'bbox_inches':'tight'})
fig.savefig(save_dir+f'FFT_4.pdf',**{"dpi":300,'transparent':True,'bbox_inches':'tight'})