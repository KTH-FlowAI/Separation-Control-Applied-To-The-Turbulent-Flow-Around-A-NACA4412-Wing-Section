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
import copy
parser = argparse.ArgumentParser()
parser.add_argument('--x',default=0.75,type=float)
parser.add_argument('--s',default="SS",type=str)
args = parser.parse_args()
plt_setUp_Smaller()


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
                    "alpha":0.5}

### ZOOM IN THE T.E For CF on S.S
var = 'cf'
fig,axs = plt.subplots(**single_fig_cfg)
# fig,axss = plt.subplots(1,2,figsize=(18,8));axs = axss[0]
axins = inset_axes(axs, 
                  width="130%", 
                  height="60%",
                  bbox_to_anchor=(  0.68,  0.57,   0.3,   0.4),
                  bbox_transform=axs.transAxes,
                          )
x_start = 0.1,
x_end  = 0.99
x_c_zoom = 0.8
x_c_end = 1.1
control_region_cfg2 = {
                    "xmin":x_c_zoom,
                    "xmax":0.86,
                    'color':cc.grays,
                    "alpha":0.5}

var_Name = var_name_dict[var]['name']
legend_list=[]
for case_name in data.keys():
  style_dict = copy.deepcopy(data[case_name]['style'])
  style_dict['marker'] = None
  style_dict['linestyle'] = "-"
  style_dict['lw'] = 3.0
  fig,axs = plot_integral_quantities(data[case_name]['data_SS'],fig,axs,
                                    x_start,x_end,
                                    var,var_Name,style_dict,interval=3)
  axs.set(**var_name_dict[var]['axs'])
  fig,axins = plot_integral_quantities(data[case_name]['data_SS'],fig,axins,
                                      x_c_zoom,x_c_end,
                                      var,var_Name,style_dict,with_set=False)

legend_list.append(Line2D([0],[0],
                        color=cc.grays,
                        linestyle="-",
                        linewidth=3.0,
                        label="SS"))
legend_list.append(Line2D([0],[0],
                        color=cc.grays,
                        linestyle="--",
                        linewidth=3.0,
                        label="PS"))

for case_name in data.keys():
  legend_list.append(Rectangle(xy=(1, 0), width=3, height=3,
                                color=data[case_name]['style']['c'],
                                label=data[case_name]['label']))

axs.yaxis.set_major_formatter(formatter2)
axs.grid(**grid_setup)
# axs.set_title('(a)',**title_setup)
axs.axvspan(**control_region_cfg)
axins.axvspan(**control_region_cfg2)
axins.set_ylim([-0.001,0.001])
axins.set_xticks([0.8,0.9,1.0])
axs.legend(handles=legend_list,
           loc='upper center', 
                        bbox_to_anchor=(0.5, 1.0, 
                                        0.1,0.1), 
                        borderaxespad=0,
                        ncol=len(legend_list)//2, 
                        frameon=False,
                        prop={"size":13}
                        )
axins.yaxis.set_major_formatter(formatter2)
axs.axhline(0,**support_line1)
axins.axhline(0,**support_line1)


#----------------------
# Pressure Side 
#----------------------
# fig,axs = plt.subplots(**single_fig_cfg)
# axs = axss[0]
var_Name = var_name_dict[var]['name']
legend_list=[]
for case_name in data.keys():
  style_dict = copy.deepcopy(data[case_name]['style'])
  style_dict['marker'] = None
  style_dict['linestyle'] = "--"
  style_dict['lw'] = 3.0
  fig,axs = plot_integral_quantities(data[case_name]['data_PS'],fig,axs,
                                    x_start,x_end,
                                    var,var_Name,style_dict,
                                    interval=3,
                                    )
  axs.set(**var_name_dict[var]['axs'])
  legend_list.append(data[case_name]['label'])
axs.grid(**grid_setup)
# axs.axvspan(**control_region_cfg)
axs.yaxis.set_major_formatter(formatter2)

fig.savefig(f'Figs/02-BL-DEVELP/cf_BothSides.jpg',
              **figkw
              )
fig.savefig(f'Figs/02-BL-DEVELP/cf_BothSides.pdf',
              **figkw
              )



#------------------------------------------
# Integral quantities : cp on both sides in one figure 
#------------------------------------------

### ZOOM IN THE T.E For CF on S.S
var = 'cp'
fig,axs = plt.subplots(**single_fig_cfg)
axins = inset_axes(axs,
                          width="200%", 
                          height="75%",
                          bbox_to_anchor=(  0.75,  0.55,   0.3,   0.4),
                          bbox_transform=axs.transAxes,
                          )
x_start = 0.0,
x_end  = 1.0
x_c_zoom_start = 0.82
x_c_zoom_end = 1.0

control_region_cfg2 = {
                    "xmin":x_c_zoom_start,
                    "xmax":0.86,
                    'color':cc.grays,
                    "alpha":0.5}

var_Name = var_name_dict[var]['name']
legend_list=[]
for case_name in data.keys():

  ## Enclose the Cp 
  data[case_name]['data_PS']['cp'][0,1] = data[case_name]['data_SS']['cp'][0,0]
  data[case_name]['data_PS']['cp'][0,:] *= -1 
  data[case_name]['data_SS']['cp'][0,:] *= -1 
  # data[case_name]['data_PS']['cp'][0,-1] = data[case_name]['data_SS']['cp'][0,-1]

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
# axs.set_title('(b)',**title_setup)
axs.legend(handles=legend_list,
           loc='upper center', 
                        bbox_to_anchor=(0.5, 1.0, 
                                        0.0,0.1), 
                        borderaxespad=0,
                        ncol=len(legend_list)//2, 
                        frameon=False,
                        prop={"size":13}
                        )
fig.subplots_adjust(wspace=0.2)
fig.savefig(f'Figs/02-BL-DEVELP/cp_BothSides.jpg',
              **figkw
              )
fig.savefig(f'Figs/02-BL-DEVELP/cp_BothSides.pdf',
              **figkw
              )


#------------------------------------------
# Integral quantities : Others on both sides
#------------------------------------------
plt_setUp_Smaller2()
single_fig_smaller = {
                'ncols':1,
                'nrows':1,
                'figsize':(8.5,6)
                  }
VarList =[
          'beta',
          'Retheta',
          "Retau",
          "H12",
          "Ue",
          "d99",
          ]

for il, var in enumerate(VarList):
  fig,axs = plt.subplots(**single_fig_smaller)
  for jl, side in enumerate(sides): 
    x_c = 0.16
    var_Name = var_name_dict[var]
    legend_list=[]

    for case_name in data.keys():
      d = data[case_name][f'data_{side}']
      if 'ref'  in case_name:
        x_end = 0.86
      else:
        x_end = 0.92
      
      label = data[case_name]['label']
      style_dict = data[case_name]['style']
      style_dict['lw']  = 2.5
      style_dict['marker']  = None
      if side == 'SS':
        style_dict['linestyle']='-'
      elif side == 'PS':
        style_dict['linestyle']='--'
      
      if 'Case C' in label and side == 'PS' and var =='beta':
        ### Smooth the spikes
        indx = np.where((d['xc'][0,:]>x_start) & (d['xc'][0,:] < x_end))[0]
        indx_list = []
        for i in indx: 
          v = d[var][0,i]
          if v > 8 or v < -18: 
            x_l = d['xc'][0,i]
            print(x_l, v)
          # if v > 8 : 
            d[var][0,i] = d[var][0,i-1] 
          #   # d[var][0,i] = np.nan 
            indx_list.append(i)

      if 'Case C' in label and side == 'PS':
          for i in indx_list:
            d[var][0,i] = d[var][0,i-1] 
          # 
      
      fig,axs = plot_integral_quantities(d,
                                        fig,axs,x_c,x_end,
                                        var,var_Name,style_dict,
                                        interval=4
                                        )
      


  axs.set(**var_name_dict[var]['axs'])
  axs.grid(**grid_setup)
  axs.axvspan(**control_region_cfg)
    
  legend_list.append(Line2D([0],[0],
                            color=cc.grays,
                            linestyle="-",
                            linewidth=3.0,
                            label="SS"))
  legend_list.append(Line2D([0],[0],
                            color=cc.grays,
                            linestyle="--",
                            linewidth=3.0,
                            label="PS"))

  for case_name in data.keys():
    legend_list.append(Rectangle(xy=(1, 0), width=3, height=3,
                                    color=data[case_name]['style']['c'],
                                    label=data[case_name]['label']))
  axs.legend(handles=legend_list,
           loc='upper center', 
                        bbox_to_anchor=(0.5, 1.0, 
                                        0.0,0.11), 
                        borderaxespad=0,
                        ncol=len(legend_list)//2, 
                        frameon=False,
                        prop={"size":14}
                        )
  fig.savefig(f'Figs/02-BL-DEVELP/BL_{var}.jpg',
                  **{'dpi':300,'transparent':True}
                  )
  fig.savefig(f'Figs/02-BL-DEVELP/BL_{var}.pdf',
                    **{'dpi':300,'transparent':True}
                    )




"""
Obtain the integral quantities at x/c = 0.75 
"""
VarList = [
          "cf",
          "cp",
          "beta",
          "Retheta",
          "Retau",
          "H12",
        ## Added after revision
          "utau",
          "Ue",
          "d99"
          ]

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
        "utau":[],
        "Ue":[],
        "d99":[],
            }
  for kl, case_name in enumerate(data.keys()):
    sum_table['case'].append(data[case_name][f'label'])
    for il, var in enumerate(VarList):
        data_ = data[case_name][f'data_{side}']
        xx = data_['xc'][0,:]
        ind = np.where(data_['xc'][0,:] > xLoc)[0][0]
        x_loc =xx[ind]
        # print(ind,x_loc)
        var_x = data_[var][0,ind]
        # print(f"Case {case_name} At x/c = {x_loc}: {var} = {var_x}")
        sum_table[var].append(var_x)
    
  df = pd.DataFrame(sum_table)
  df.to_csv(f'Quantities_{side}.csv',float_format='%.4f')
      