import matplotlib.pyplot as plt
import struct,os
import numpy as np
import pandas as pd
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
parser.add_argument('--scale',default="inner",type=str)
args = parser.parse_args()

plt.rc("font",family = "serif")
plt.rc("text",usetex = "true")
plt.rc("font",size = 18)
plt.rc("axes",labelsize = 18, linewidth = 2)
plt.rc("legend",fontsize= 15, handletextpad = 0.1)
plt.rc("xtick",labelsize = 15)
plt.rc("ytick",labelsize = 15)
    

AOA = 11 
Rec = 200
fldr='./database/tsrs/002-SP-1D/' 
save_dir = 'Figs/04-FFT/'
os.makedirs("Figs",exist_ok=True)
os.makedirs(save_dir,exist_ok=True)
sides = ['SS',"PS"]
AlphaList = [['(a)',"(b)","(c)","(d)"],["(e)","(f)","(g)","(h)"]]

def name_file(fldr,name,nprof,var):
    data_to_load= fldr + f"SP1D_{name}_{nprof}.mat"
    return data_to_load


def post_process_Spectra(out):
    lstar = out['lstar'].squeeze()
    # d99 = out['d99']
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
        'lmd_inner':lmd[1:]/lstar,
        'yn_inner':yn/lstar,
        'puu':puu[:,1:],
        }
    return data

NPROF = args.prof 
VAR   = args.var
scale = args.scale
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
    d = sio.loadmat(fname)
    data[caseName][f'data'] = post_process_Spectra(d)
    print(f"[IO] DATA: {fname}")

data_ = data['control3']['data']
data['control3']['data']=data['control4']['data']
data['control4']['data']=data_



levels = np.array([0.2,0.8])
fig,axs = plt.subplots(1,1)

legend_list = []
for kl, case_name in enumerate(reversed(data.keys())):
    d = data[case_name]['data']
    style_dict = data[case_name]['style']
    style_dict['marker']= "None"
    style_dict['ls']= "-"
    text_loc=(0.9-kl*0.1,0.9-kl*0.1)
    fig,axs = plot_1DPSD(d,fig,axs,style_dict,levels,text_loc,scale)

    legend_list.append(Rectangle(xy=(1, 0), width=3, height=3,
                            color=style_dict['c'],
                            label=data[case_name]['label']))

axs.xaxis.set_minor_locator(locmin)
axs.xaxis.set_major_locator(locmin)        
axs.yaxis.set_minor_locator(locmin)
axs.yaxis.set_major_locator(locmin)
axs.grid(**grid_setup)

#### Add Legend here

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
                    label='Spectra',)
                )
legend_list.reverse()

if scale == "inner":
    axs.set(**{
        'xscale':'log',
        'xlabel':r'$\lambda^+_z$',
        'xlim':[20,2000],
        'yscale':'log',    
        'ylabel':r'$y^+_n$',
        'ylim':[1,500],
                })
elif scale == "outer":
    axs.set(**{
        'xscale':'log',
        'xlabel':r'$\lambda_z/\delta_{99}$',
        'yscale':'log',    
        'ylabel':r'$y_n/\delta_{99}$',
        'ylim':[1e-3,1e0],
                })

axs.legend(handles=legend_list,
                            loc='upper center', 
                                            bbox_to_anchor=(0.5, 1.05, 
                                                            0.0,0.1), 
                                            borderaxespad=0,
                                            ncol=len(legend_list)//2, 
                                            frameon=False,
                                            prop={"size":12}
                                            )



fig.savefig(f'Figs/04-FFT/Prof_SP1D_Prof{args.prof}.jpg',**{'dpi':300,'transparent':True,'bbox_inches':'tight'})
fig.savefig(f'Figs/04-FFT/Prof_SP1D_Prof{args.prof}.pdf',**{'dpi':300,'transparent':True,'bbox_inches':'tight'})
print('[IO] Spectra Figure Saved')
