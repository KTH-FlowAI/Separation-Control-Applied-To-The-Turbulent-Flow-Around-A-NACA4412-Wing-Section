"""
Visualisation of the profiles, decomposing the lift and drag coeff 
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

def lift_drag_distribute(data:dict,rho=1.0,Uinf=1.0):
  def diffoidal2(x,y,v,theta,ind):
    """
    Differentiation
    """
    dx = x[1:]-x[:-1]
    dy = y[1:]-y[:-1]
    dv = (v[1:]+v[:-1])/2
    dtheta = (theta[1:]+theta[:-1])/2
    if ind == 1:
        res = (dx*dv)
    elif ind==2:
        res = (dy*dv)
    elif ind==3:
        res = (dy*dv)
    elif ind==4:
        res = (dx*dv)
    elif ind==5:
        res = (dx*dv*( dx/2 + x[:-1] ))
    elif ind==6:
        res = (dx*dv*( dy/2 + y[:-1] ))
    elif ind==7:
        res = (dx*dv*np.tan(dtheta)*( dx/2+x[:-1] ))
    else:
        res = (dx*dv*np.tan(dtheta)*( dy/2+y[:-1] ))
    return res

  # Dynamic Pressure 
  p_dyn = 0.5*rho*(Uinf**2)
  
  # Suction Side 
  x     = data['data_SS']['x']
  y     = data['data_SS']['y']
  theta = data['data_SS']['theta']
  P     = data['data_SS']['P_w']
  tau   = data['data_SS']['tau_w']
  H_p_top = - diffoidal2(x,y,P,theta,1)
  H_tauw_top = diffoidal2(x,y,tau,theta,2)
  V_p_top = diffoidal2(x,y,P,theta,3)
  V_tauw_top = diffoidal2(x,y,tau,theta,4)
  
  # Pressure Side 
  x     = data['data_PS']['x']
  y     = data['data_PS']['y']
  theta = data['data_PS']['theta']
  P     = data['data_PS']['P_w']
  tau   = data['data_PS']['tau_w']
  H_p_bot    = diffoidal2(x,y,P,theta,1)
  H_tauw_bot = diffoidal2(x,y,tau,theta,2)
  V_p_bot    = -diffoidal2(x,y,P,theta,3)
  V_tauw_bot = diffoidal2(x,y,tau,theta,4)
  



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
    print(f"[IO] DATA: {fname}, {data[caseName]['data_SS'].keys()}")
    
    fname= name_file(fldr,name,AOA,Rec,'PS')+'.mat'
    data[caseName]['data_PS'] = sio.loadmat(fname)
    print(f"[IO] DATA: {fname}")

    lift_drag_distribute(data[caseName])


quit()
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
                        label="S.S"))
legend_list.append(Line2D([0],[0],
                        color=cc.grays,
                        linestyle="--",
                        linewidth=3.0,
                        label="P.S"))

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

