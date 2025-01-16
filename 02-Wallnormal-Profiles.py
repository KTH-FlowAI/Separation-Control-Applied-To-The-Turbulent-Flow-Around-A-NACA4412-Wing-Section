"""
Visualisation of the turbulence statistics  
@yuningw
"""

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

parser = argparse.ArgumentParser()
parser.add_argument('--x',default=0.75,type=float)
parser.add_argument('--s',default="SS",type=str)
args = parser.parse_args()
plt_setUp()


AOA = 11 
Rec = 200
fldr='../../database/stsdata/' 
sides = ['SS',"PS"]
side_text = {
    "SS":f"S.S",
    "PS":f"P.S",
             
             }
#######################################
# OVER SUCTION/PRESSURE SIDE 
#######################################
for caseName in data.keys():
    name = data[caseName]['fileName']
    fname= name_file(fldr,name,AOA,Rec,'SS')+'.mat'
    data[caseName]['data_SS'] = sio.loadmat(fname)
    print(f"[IO] DATA: {fname}")
    
    fname= name_file(fldr,name,AOA,Rec,'PS')+'.mat'
    data[caseName]['data_PS'] = sio.loadmat(fname)
    print(f"[IO] DATA: {fname}")



VarList =['U','V']
scales=['inner','outer']
for scale in scales:
    for side in sides: 
        for var in VarList:
            fig,axs = plt.subplots(**single_fig_cfg)
            x_c = args.x
            var_Name = var_name_dict[var+scale]
            legend_list=[]
            
            for case_name in data.keys():

                fig,axs = plot_Vel(data[case_name][f'data_{side}'],
                                fig,axs,x_c,var,var_Name,
                                data[case_name]['style'],
                                grid_setup,
                                scale=scale)
                legend_list.append(data[case_name]['label'])
            
            axs.set(**var_name_dict[var+scale]['axs'])
            axs.set_title(rf"$x/c={x_c}$"+", "+f"{side_text[side]}")
            axs.xaxis.set_minor_locator(locmin)
            axs.xaxis.set_major_locator(locmin)
            axs.xaxis.set_minor_formatter(NullFormatter())
            
            if side == 'SS' :
                axs.legend(legend_list,loc='upper left')
            elif side == 'PS' and "U" in var:
                axs.legend(legend_list,loc='upper left')
            else:
                axs.legend(legend_list,loc='upper right')
            fig.savefig(f'Figs/03-STATS/{side}_{var}_{int(x_c*100)}_{scale}.pdf',
                    **{"bbox_inches":'tight','dpi':300}
                    )
