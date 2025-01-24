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
    try: 
      data[caseName]['data'] = sio.loadmat(fname)
      print(f"[IO] DATA: {fname}")
    except:
      data[caseName]['data'] = {}


fig, axs = plt.subplots(1,1,figsize=(7,7))
for caseName in data.keys():
  d = data[caseName]['data']
  style=data[caseName]['style']
  try:
    fig,axs=plot_FFT(d,fig,axs,style)
  except:
    continue
axs.set(**var_name_dict['psd']['axs'])
fig.savefig(save_dir+f'FFT_{NPROF}_{VAR}.jpg',**{"dpi":300})