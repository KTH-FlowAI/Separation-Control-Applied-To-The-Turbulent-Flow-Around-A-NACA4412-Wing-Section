"""
Visualisation of the profiles 
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
fldr='../database/stsdata/' 
sides = ['SS',"PS"]

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



#------------------------------------------
# Integral quantities : Cf 
#------------------------------------------
control_region_cfg = {
                    "xmin":0.25,
                    "xmax":0.86,
                    'color':cc.gray,
                    "alpha":0.9}

### ZOOM IN THE T.E For CF on S.S
var = 'cf'
# fig,axs = plt.subplots(**single_fig_cfg)
fig,axss = plt.subplots(**double_fig_larger)
axs = axss[0]
axins = inset_axes(axs, 
                   width="130%", 
                  height="35%",
                  bbox_to_anchor=(  0.7,  0.55,   0.3,   0.4),
                  bbox_transform=axs.transAxes,
                          )
x_start = 0.1,
x_end  = 0.95
x_c_zoom = 0.80
control_region_cfg2 = {
                    "xmin":x_c_zoom,
                    "xmax":0.86,
                    'color':cc.gray,
                    "alpha":0.9}

var_Name = var_name_dict[var]['name']
legend_list=[]
for case_name in data.keys():
  fig,axs = plot_integral_quantities(data[case_name]['data_SS'],fig,axs,
                                    x_start,x_end,
                                    var,var_Name,data[case_name]['style'],interval=3)
  axs.set(**var_name_dict[var]['axs'])
  fig,axins = plot_integral_quantities(data[case_name]['data_SS'],fig,axins,
                                      x_c_zoom,0.99,
                                      var,var_Name,data[case_name]['style'],with_set=False)
  legend_list.append(data[case_name]['label'])
axs.yaxis.set_major_formatter(formatter2)
axs.grid(**grid_setup)
axs.set_title('S.S',)
axs.axvspan(**control_region_cfg)
axins.axvspan(**control_region_cfg2)
axins.set_ylim([-0.001,0.002])
axins.yaxis.set_major_formatter(formatter2)
axs.axhline(0,**support_line1)
axins.axhline(0,**support_line1)

# axs.legend(legend_list,
#             loc='upper center',
#             bbox_to_anchor=(0.5,.5,0.0,0.5),
#             ncol=len([k for k in data.keys()]),)

# fig.savefig(f'Figs/02-BL-DEVELP/SS_{var}_Inspection.jpg',
#               **figkw
#               )
#----------------------
# Pressure Side 
#----------------------
# fig,axs = plt.subplots(**single_fig_cfg)
axs = axss[1]
var_Name = var_name_dict[var]['name']
legend_list=[]
for case_name in data.keys():
  fig,axs = plot_integral_quantities(data[case_name]['data_PS'],fig,axs,
                                    x_start,x_end,
                                    var,var_Name,data[case_name]['style'],
                                    interval=3,
                                    )
  axs.set(**var_name_dict[var]['axs'])
  legend_list.append(data[case_name]['label'])
axs.grid(**grid_setup)
axs.axvspan(**control_region_cfg)
axs.set_ylabel(' ')
axs.set_title('P.S',)
axs.yaxis.set_major_formatter(formatter2)
fig.subplots_adjust(wspace=0.1)
# axs.legend(legend_list,
#             loc='upper center',
#             bbox_to_anchor=(0.5,.65,0.0,0.5),
#             ncol=len([k for k in data.keys()]),)
fig.savefig(f'Figs/02-BL-DEVELP/{var}_BothSides.jpg',
              **figkw
              )
fig.savefig(f'Figs/02-BL-DEVELP/{var}_BothSides.pdf',
              **figkw
              )



#------------------------------------------
# Integral quantities : cp on both sides in one figure 
#------------------------------------------

### ZOOM IN THE T.E For CF on S.S
var = 'cp'
# fig,axs = plt.subplots(**single_fig_larger)
fig,axs = plt.subplots(**single_fig_cfg)
axins = inset_axes(axs,
                          width="200%", 
                          height="75%",
                         bbox_to_anchor=(  0.75,  0.2,   0.3,   0.4),
                          bbox_transform=axs.transAxes,
                          )
x_start = 0.0,
x_end  = 1.0
x_c_zoom_start = 0.75
x_c_zoom_end = 0.95

control_region_cfg2 = {
                    "xmin":x_c_zoom_start,
                    "xmax":0.86,
                    'color':cc.gray,
                    "alpha":0.9}

var_Name = var_name_dict[var]['name']
legend_list=[]
for case_name in data.keys():
  fig,axs = plot_integral_quantities(data[case_name]['data_SS'],fig,axs,
                                    x_start,x_end,
                                    var,var_Name,data[case_name]['style'])
  
  fig,axs = plot_integral_quantities(data[case_name]['data_PS'],fig,axs,
                                    x_start,x_end,
                                    var,var_Name,data[case_name]['style'])
  
  fig,axins = plot_integral_quantities(data[case_name]['data_SS'],fig,axins,
                                    x_c_zoom_start,x_c_zoom_end,
                                    var,var_Name,data[case_name]['style'])
  
  fig,axins = plot_integral_quantities(data[case_name]['data_PS'],fig,axins,
                                    x_c_zoom_start,x_c_zoom_end,
                                    var,var_Name,data[case_name]['style'])
  
  legend_list.append(Line2D([0],[0],
                            **data[case_name]['style'],
                            label=data[case_name]['label']))
axs.set(**var_name_dict[var]['axs'])
# axins.set(**var_name_dict[var]['axs'])
axins.set_xlabel("")
axins.set_ylabel("")
axins.set_aspect(0.25)
axs.grid(**grid_setup)
axs.axvspan(**control_region_cfg)
axins.axvspan(**control_region_cfg2)
axs.axhline(0,**support_line1)
axins.axhline(0,**support_line1)

# axs.legend(handles=legend_list,
#             loc='upper center',
#             bbox_to_anchor=(0.5,.65,0.0,0.5),
#             ncol=len([k for k in data.keys()]),)
fig.savefig(f'Figs/02-BL-DEVELP/{var}_BothSides.jpg',
              **figkw
              )
fig.savefig(f'Figs/02-BL-DEVELP/{var}_BothSides.pdf',
              **figkw
              )


#------------------------------------------
# Integral quantities : Others on both sides
#------------------------------------------
plt.rc("xtick",labelsize = 30)
plt.rc("ytick",labelsize = 30)
plt.rc("font",size = 35)



VarList =[
          'beta',
          'Retheta',
          "Retau",
          "H12",
          ]
AlphaList = [['(a)',"(b)","(c)","(d)"],["(e)","(f)","(g)","(h)"]]
for jl, side in enumerate(sides): 
  fig,axss = plt.subplots(**quadra_fig_larger)
  for il, var in enumerate(VarList):
    axs=axss[il]
    # fig,axs = plt.subplots(**single_fig_cfg)
    x_c = 0.16
    var_Name = var_name_dict[var]
    legend_list=[]
    for case_name in data.keys():
      if 'ref'  in case_name:
        x_end = 0.86
      else:
        x_end = 0.95
      style_dict = data[case_name]['style']
      style_dict['lw']  = 3.5
      style_dict['markersize']  = 9.0
      fig,axs = plot_integral_quantities(data[case_name][f'data_{side}'],
                                        fig,axs,x_c,x_end,
                                        var,var_Name,style_dict,
                                        interval=4
                                        )
      
      legend_list.append(data[case_name]['label'])
    axs.set(**var_name_dict[var]['axs'])
    axs.grid(**grid_setup)
    axs.axvspan(**control_region_cfg)
    axs.set_title(AlphaList[jl][il] + f" {side_text[side]}",**title_setup)
  fig.subplots_adjust(**{"hspace":0.4,"wspace":0.2})
  fig.savefig(f'Figs/02-BL-DEVELP/{side}_{il+1}VARS.jpg',
                **figkw
                )
  fig.savefig(f'Figs/02-BL-DEVELP/{side}_{il+1}VARS.pdf',
                **figkw
                )


VarList = [
          "cf",
          "cp",
          "beta",
          "Retheta",
          "Retau",
          "H12"]

xLoc  = 0.75 
for jl, side in enumerate(sides): 
  sum_table = {
        'case':[],
        'cf':[],
        'cp':[],
        'beta':[],
        'Retheta':[],
        "Retau":[],
        "H12":[],
            }
  for kl, case_name in enumerate(data.keys()):
    sum_table['case'].append(data[case_name][f'label'])
    for il, var in enumerate(VarList):
        
        data_ = data[case_name][f'data_{side}']
        
        xx = data_['xc'][0,:]
        ind = np.where(data_['xc'][0,:] > xLoc)[0][0]
        x_loc =xx[ind]
        print(ind,x_loc)
        var_x = data_[var][0,ind]
        print(f"Case {case_name} At x/c = {x_loc}: {var} = {var_x}")
        sum_table[var].append(var_x)
    
  df = pd.DataFrame(sum_table)
  df.to_csv(f'Quantities_{side}.csv',float_format='%.4f')
      