"""
Visualisation of the profiles, decomposing the lift and drag coeff 
@yuningw
"""
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
import copy
parser = argparse.ArgumentParser()
parser.add_argument('--x',default=0.75,type=float)
parser.add_argument('--s',default="SS",type=str)
args = parser.parse_args()
plt_setUp_Smaller()

os.makedirs('Figs',exist_ok=True)
os.makedirs('Figs/05-Supply',exist_ok=True)


def Gen_InterpMesh_interp():
  from lib.wingInterpMesh import NACA_mesh 
  N=9
  t = 12/100
  c = 1
  m = 4/100
  p = 4/10
  offset = -0.5
  aoa = 11 # deg
  aoa_= aoa*np.pi/180 
  # wall-normal profiles 
  npts = 100  # Number of points for each wall-normal profile 
  d_out= 1e-1 # outer-scaled unit length
  d_in = 5e-5 # inner-
  xc_vec = np.linspace(0.0,1.0,10)**2.5 * 0.02
  wallMesh =  NACA_mesh(xc_vec,t,m,p,c=c,aoa=aoa_,offset=offset)
  ## Use the prescribed inner- and outer-scaled length to generate wall-normal profiles 
  wallMesh.define_yn_prof(npts=npts,d_out=d_out,d_in=d_in)
  ## Create the mesh 
  wallMesh.create_BL_mesh()
  ### Extract the profiles
  interp_dict ={}
  interp_dict["x_PS"]=wallMesh.xl[0]
  interp_dict["x_SS"]=wallMesh.xu[0]
  interp_dict["th_PS"]=wallMesh.alphal_0
  interp_dict["th_SS"]=wallMesh.alphau_0
  
  ### Do interpolation for both side 
  interp_dict['coeff_SS'] = np.polyfit(interp_dict['x_SS'],interp_dict['th_SS'],N)
  interp_dict['func_SS'] = np.poly1d(interp_dict['coeff_SS'])
  interp_dict['coeff_PS'] = np.polyfit(interp_dict['x_PS'],interp_dict['th_PS'],N)
  interp_dict['func_PS'] = np.poly1d(interp_dict['coeff_PS'])
  return interp_dict


def lift_drag_distribute(data:dict,rho=1.0,Uinf=1.0):
  from copy import deepcopy
  
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
  ### Chordlength distribute 
  data['Force'] = {}

  xc = data['data_SS']['xc'].squeeze()

  ### Profiles for calculating the force. 
  x     = data['data_SS']['x'][:,0]
  y     = data['data_SS']['y'][:,0]
  theta = data['data_SS']['theta'][0,:]
  P     = data['data_SS']['P_w'][0,:]
  tau   = data['data_SS']['tau_w'][0,:]
  ## Force S.S: Horizontal and vertical  
  data['Force']["H_p_top"]     = - diffoidal2(x,y,P,theta,1)
  data['Force']["H_tauw_top"]  = diffoidal2(x,y,tau,theta,2)
  data['Force']["V_p_top"]     = diffoidal2(x,y,P,theta,3)
  data['Force']["V_tauw_top"]  = diffoidal2(x,y,tau,theta,4)
  
  # Pressure Side 
  x     = data['data_PS']['x'][:,0]
  y     = data['data_PS']['y'][:,0]
  theta = data['data_PS']['theta'][0,:]
  P     = data['data_PS']['P_w'][0,:]
  tau   = data['data_PS']['tau_w'][0,:]
  ## Force on P.S: Horizontal and vertical 
  ## Start from indx=1 as indx=0 <=> x/c=0.0
  data['Force']["H_p_bot"]    = diffoidal2(x,y,P,theta,1)[1:]
  data['Force']["H_tauw_bot"] = diffoidal2(x,y,tau,theta,2)[1:]
  data['Force']["V_p_bot"]    = -diffoidal2(x,y,P,theta,3)[1:]
  data['Force']["V_tauw_bot"] = diffoidal2(x,y,tau,theta,4)[1:]

  ## Lift and drag force distribution 
  data['Force']['L_p']    = data['Force']['H_p_top']    + data['Force']['H_p_bot']
  data['Force']['L_tauw'] = data['Force']['H_tauw_top'] + data['Force']['H_tauw_bot']
  data['Force']['L']      = data['Force']['L_p']        + data['Force']['L_tauw']
  
  data['Force']['D_p']    = data['Force']['V_p_top']    + data['Force']['V_p_bot']
  data['Force']['D_tauw'] = data['Force']['V_tauw_top'] + data['Force']['V_tauw_bot']
  data['Force']['D']      = data['Force']['D_p']        + data['Force']['D_tauw']
  data['Force']['xc']     = xc

  # At O(-1 \times 10{^-5}) the effect is negligible
  # print(data['Force']['L_tauw'])

  for k in data['Force'].keys():
    data['Force'][k] = np.expand_dims(data['Force'][k],0)

  ## A Validation: lift coefficient 
  cl = np.sum(data['Force']['H_p_top']) + np.sum(data['Force']['H_tauw_top']) +\
                    np.sum(data['Force']['H_p_bot']) + np.sum(data['Force']['H_tauw_bot'])
  cl/=p_dyn
  print(f"Database Updated -- Validation: Cl={cl:.3f}") 

  return 



AOA = 11 
Rec = 200
fldr='./database/stsdata/' 
sides = ['SS',"PS"]

#######################################
# OVER SUCTION/PRESSURE SIDE 
#######################################
for caseName in data.keys():
    name = data[caseName]['fileName']
    fname= name_file(fldr,name,AOA,Rec,'SS')+'.mat'
    data[caseName]['data_SS'] = sio.loadmat(fname)
    # print(f"[IO] DATA: {fname}")
    
    fname= name_file(fldr,name,AOA,Rec,'PS')+'.mat'
    data[caseName]['data_PS'] = sio.loadmat(fname)
    # print(f"[IO] DATA: {fname}")

    lift_drag_distribute(data[caseName])
    
interval_l = 8
x_start = 0.1,
x_end  = 0.99
x_c_zoom = 0.75
x_c_end = 0.9
control_region_cfg = {
                    "xmin":0.25,
                    "xmax":0.86,
                    'color':cc.gray,
                    "alpha":0.5}
control_region_cfg2 = {
                    "xmin":x_c_zoom,
                    "xmax":0.86,
                    'color':cc.grays,
                    "alpha":0.5}

#------------------------------------------
# Integral quantities Lift and drag forces as well as theirs decomposition 
#------------------------------------------
single_fig_cfg = {
                'ncols':1,
                'nrows':1,
                'figsize':(8.5,7.5)
                  }




def Plot_lift_force():
  ##### Lift force and its decomposition ######
  fig,axs = plt.subplots(**single_fig_cfg)
  axins = inset_axes(axs, 
                    width="130%", 
                    height="50%",
                    bbox_to_anchor=(  0.68,  0.57,   0.3,   0.4),
                    bbox_transform=axs.transAxes,
                            )

  Vars_dict = {
              "L":{
                  'linestyle':'-',
                  'marker':"x",
                  'lw':1.0,
                  },

              "L_p":{
                  'linestyle':'None',
                  "marker":"o"
                  },

              "L_tauw":{
                  'linestyle':'None',
                  'marker':'D',

                  },

              }

  for var,var_style in Vars_dict.items():
    var_Name = var_name_dict[var]['name']
    legend_list=[]
    for case_name in data.keys():
      style_dict = copy.deepcopy(data[case_name]['style'])
      for k in var_style.keys():
        style_dict[k] = var_style[k]
      fig,axs = plot_integral_quantities(data[case_name]['Force'],fig,axs,
                                        x_start,x_end,
                                        var,var_Name,style_dict,interval=interval_l)

      fig,axins = plot_integral_quantities(data[case_name]['Force'],fig,axins,
                                            x_c_zoom,x_c_end,
                                            var,var_Name,style_dict,interval=interval_l,with_set=False)

  axs.set(**var_name_dict["L"]['axs'])
  axins.axvspan(**control_region_cfg2)
  axins.set_ylim([0.001,0.002])
  axins.set_xticks([0.8,0.9,])
  axins.yaxis.set_major_formatter(formatter2)
  for var, var_style in Vars_dict.items():
    legend_list.append(Line2D([0],[0],
                            color=cc.grays,
                            linestyle=var_style['linestyle'],
                            marker=var_style['marker'],
                            linewidth=1.0,
                            markersize=8,
                            fillstyle="none",
                            label=var_name_dict[var]['name']))


  for case_name in data.keys():
    legend_list.append(Rectangle(xy=(1, 0), width=3, height=3,
                                  color=data[case_name]['style']['c'],
                                  label=data[case_name]['label']))

  axs.yaxis.set_major_formatter(formatter2)
  axs.grid(**grid_setup)
  axs.axvspan(**control_region_cfg)
  # axs.axhline(0,**support_line1)
  # axins.axhline(0,**support_line1)

  axs.legend(handles=legend_list,
              loc='upper center', 
                          # bbox_to_anchor=(1.0, 0.85, 
                          #                 0.2,0.1), 
                          bbox_to_anchor=(0.5, 1.0, 
                                          0.0,0.15), 
                          borderaxespad=0,
                          ncol=len(legend_list)//3, 
                          frameon=False,
                          prop={"size":14.5}
                          )
  # axs.axhline(0,**support_line1)
  fig.savefig(f'Figs/05-Suply/L_distribute.jpg',
                **{'dpi':300,'transparent':True}
                )
  fig.savefig(f'Figs/05-Suply/L_distribute.pdf',
                **{'dpi':300,'transparent':True}
                )

def Plot_drag_force():
  plt_setUp_Smaller()
  ##### Lift force and its decomposition ######
  fig,axs = plt.subplots(**single_fig_cfg)
  axins = inset_axes(axs, 
                    width="100%", 
                    height="60%",
                    # bbox_to_anchor=(  0.68,  0.57,   0.3,   0.4),
                    bbox_to_anchor=(  0.69,  0.57,   0.3,   0.4),
                    bbox_transform=axs.transAxes,
                            )

  Vars_dict = {
              "D":{
                  'linestyle':'-',
                  'marker':"x",
                  'lw':1.0,
                  },

              "D_p":{
                  'linestyle':'None',
                  "marker":"o"
                  },

              "D_tauw":{
                  'linestyle':'None',
                  'marker':'D',

                  },

              }

  for var,var_style in Vars_dict.items():
    var_Name = var_name_dict[var]['name']
    legend_list=[]
    for case_name in data.keys():
      style_dict = copy.deepcopy(data[case_name]['style'])
      for k in var_style.keys():
        style_dict[k] = var_style[k]
      fig,axs = plot_integral_quantities(data[case_name]['Force'],fig,axs,
                                        x_start,x_end,
                                        var,var_Name,style_dict,interval=interval_l)

      fig,axins = plot_integral_quantities(data[case_name]['Force'],fig,axins,
                                            x_c_zoom,x_c_end,
                                            var,var_Name,style_dict,interval=interval_l,with_set=False)

  axs.set(**var_name_dict["D"]['axs'])
  axins.axvspan(**control_region_cfg2)
  # axins.set_ylim([0.001,0.002])
  axins.set_xticks([0.8,0.9])
  axins.yaxis.set_major_formatter(formatter2)
  for var, var_style in Vars_dict.items():
    legend_list.append(Line2D([0],[0],
                            color=cc.grays,
                            linestyle=var_style['linestyle'],
                            marker=var_style['marker'],
                            linewidth=1.0,
                            markersize=8,
                            fillstyle="none",
                            label=var_name_dict[var]['name']))


  for case_name in data.keys():
    legend_list.append(Rectangle(xy=(1, 0), width=3, height=3,
                                  color=data[case_name]['style']['c'],
                                  label=data[case_name]['label']))

  axs.yaxis.set_major_formatter(formatter2)
  axs.grid(**grid_setup)
  axs.axvspan(**control_region_cfg)
  axs.legend(handles=legend_list,
              loc='upper center', 
                          # bbox_to_anchor=(1.0, 0.85, 
                          #                 0.2,0.1), 
                          bbox_to_anchor=(0.5, 1.0, 
                                          0.0,0.15), 
                          borderaxespad=0,
                          ncol=len(legend_list)//3, 
                          frameon=False,
                          prop={"size":14.5}
                          )
  # axs.axhline(0,**support_line1)
  fig.savefig(f'Figs/05-Suply/D_distribute.jpg',
                **{'dpi':300,'transparent':True}
                )
  fig.savefig(f'Figs/05-Suply/D_distribute.pdf',
                **{'dpi':300,'transparent':True}
                )

if __name__ == "__main__":
  Plot_drag_force()
  Plot_lift_force()