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
Vars = ['U',
        'P',
        "V"
        ]

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

# data_ = data['control3'][f'data_{nprof}_{var}']
# data['control3'][f'data_{nprof}_{var}']=data['control4'][f'data_{nprof}_{var}']
# data['control4'][f'data_{nprof}_{var}']=data_
Vars = ['U',
        
        "P"
        ]
var_name = {
              'U':r'${\rm PSD}(u_t)$',
              'V':r'${\rm PSD}(v_n)$',
              'P':r"${\rm PSD}(p)$",
            }

# del data['control1']
# del data['control2']

# fig, axss = plt.subplots(2,2,figsize=(20,12))
# AlphaList = [["(a)","(c)"],["(b)","(d)"],]
for il, nprof in enumerate(Nprofs):
  for jl, var in enumerate(Vars):
    fig,axs=plt.subplots(**{'figsize':(8,4)})
    legend_list=[]

    for kl, caseName in enumerate(reversed(data.keys())):
      d = data[caseName][f'data_{nprof}_{var}']
      style_dict=data[caseName]['style']
      # if ('control1' not in caseName) or ('control2' not in caseName):
      fig,axs=plot_FFT(d,fig,axs,style_dict,
                        text_loc=(0.99-kl*0.01,0.99-kl*0.15))
      legend_list.append(Rectangle(xy=(1, 0), width=3, height=3,
                            color=style_dict['c'],
                            label=data[caseName]['label']))
      xc = d['xloc'][0][0]
    
    legend_list.append(Line2D([0],[0],
                        color=cc.grays,
                        lw  = 1.5, 
                        ls  = "None",
                        marker = "*",
                        markersize=12,
                        label='Maxima',)
                    )

    legend_list.append(Line2D([0],[0],
                        color=cc.grays,
                        lw  = 2, 
                        ls  = "-",
                        marker = "None",
                        # markersize=12,
                        label='Spectra',)
                    )
    legend_list.reverse()
    axs.grid(**grid_setup)
    axs.set(**var_name_dict['psd']['axs'])
    axs.set_ylabel(var_name[var])
    axs.xaxis.set_minor_locator(locmin2)
    axs.xaxis.set_major_locator(locmin2)   

    axs.legend(handles=legend_list,
                            loc='upper center', 
                                            bbox_to_anchor=(0.5, 1.1, 
                                                            0.0,0.1), 
                                            borderaxespad=0,
                                            ncol=len(legend_list)//2, 
                                            frameon=False,
                                            prop={"size":13}
                                            )     
    fig.savefig(save_dir+f'FFT_{nprof}_{var}.jpg',**{"dpi":300,'transparent':True,"bbox_inches":'tight'})
    fig.savefig(save_dir+f'FFT_{nprof}_{var}.pdf',**{"dpi":300,'transparent':True,"bbox_inches":'tight'})
