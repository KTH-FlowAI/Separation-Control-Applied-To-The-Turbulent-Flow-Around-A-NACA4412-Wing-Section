"""
Check the ClCd
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
AOA = 11 
Rec = 200
fldr='../database/stsdata/' 
sides = ['SS',"PS"]
plt_setUp_Smaller()

data = data_clcd

def rel_modif(g,p,positive=True):
  """
  Calculate the relative change of Cl,Cd
  g : reference value 
  p : controlled value
  """
  if positive:
    return (100*(p-g)/g) 
  else:
    return (100*(g-p)/g)


def cal_Cmu(ctrl_config):
  """
  Calculate the momentum coefficient 

  ctrl_config: [DICT] See the configurations 
  """
  # Constant 
  rho = 1.0
  lz = 0.6 
  U0 = 1.0
  S_wing = lz * 1.0
  M = 0.5 * rho * U0**2 * S_wing

  # Suction side
  if ctrl_config['side'][0]:
    lx = ctrl_config['region'][0][0] - ctrl_config['region'][0][1]
    v_c = ctrl_config['intensity'][0]
    S = lz * lx 
    m_ss  = rho *  v_c * S
  else: 
    m_ss = 0

  # Pressure side
  if ctrl_config['side'][1]:
    lx = ctrl_config['region'][1][0] - ctrl_config['region'][1][1]
    v_c = ctrl_config['intensity'][1]
    S = lz * lx 
    m_ps  = rho *  v_c * S
  else: 
    m_ps = 0

  ms = np.abs(m_ss) + np.abs(m_ps)
  
  C_mu = ms * U0 / M 

  return  C_mu


# # #######################################
# # # # OVER SUCTION SIDE 
# # # #######################################
side= 'aero'
df = {
    "Name":[],
    "cl":[],
    "dcl":[],
    "cd_p":[],
    "dcd_p":[],
    "cd_tauw":[],
    "dcd_tauw":[],
    "cd":[],
    "dcd":[],
    "LD":[],
    "dLD":[],
      }

for caseName in data.keys():
  name = data[caseName]['fileName']
  label = data[caseName]['label']
  fname= name_file(fldr,name,AOA,Rec,side)+'.mat'
  data[caseName]['data'] = sio.loadmat(fname)
  print(f"[IO] DATA: {fname}")
  print(data[caseName]['data'].keys())
  
  cl      = data[caseName]['data']['cl'][0][0]
  cd      = data[caseName]['data']['cd'][0][0]
  cd_tauw = data[caseName]['data']['cd_tauw'][0][0]
  cd_p    = data[caseName]['data']['cd_p'][0][0]
  ld      = data[caseName]['data']['LD'][0][0]
  
  df['Name'].append(label)
  df['cl'].append(cl)
  df['cd_p'].append(cd_p)
  df['cd_tauw'].append(cd_tauw)
  df['cd'].append(cd)
  df['LD'].append(ld)

  if 'ref' in caseName:
    ref_cl      = cl 
    ref_cd      = cd 
    ref_cd_p    = cd_p 
    ref_cd_tauw = cd_tauw
    ref_ld      = ld
    df['dcl'].append(0.0)
    df['dcd_p'].append(0.0)
    df['dcd_tauw'].append(0.0)
    df['dcd'].append(0.0)
    df['dLD'].append(0.0)

  else: 
    df['dcl'].append(rel_modif(ref_cl,cl,positive=True))
    df['dcd_p'].append(rel_modif(ref_cd_p,cd_p,positive=True))
    df['dcd_tauw'].append(rel_modif(ref_cd_tauw,cd_tauw,positive=True))
    df['dcd'].append(rel_modif(ref_cd,cd,positive=True))
    df['dLD'].append(rel_modif(ref_ld,ld,positive=True))



pd.DataFrame(df).to_csv('CLCD.csv',float_format="%.5f")
pd.DataFrame(df).to_latex('CLCD.tex',float_format="%.5f")



df  =pd.read_csv('CLCD.csv')

######################
# Fig 1 Bar for Cd
########################
fig, axss = plt.subplots(1,2,figsize = (14,6))
axs = axss[0]
caselist = [c[4:] if "Case" in c else c for c in df['Name']  ]
print(caselist)
bottom = np.zeros(shape=(len(caselist)))
b1 = axs.bar(caselist,df['cd_p'],bottom=bottom,color = cc.gray,label=r'$C_{d,p}$')
bottom += df['cd_p']
b2 = axs.bar(caselist,df['cd_tauw'],bottom=bottom,color = cc.grays,label=r'$C_{d,f}$')
axs.axhline(df["cd_p"][0],linestyle='-.',color = cc.red)
axs.axhline(df["cd"][0]     ,linestyle='-.',color = cc.red)
axs.set_ylabel(r'$C_d = C_{d,f} + C_{d,p}$',fontsize = 20)
axs.set_xlabel(r'CASE',fontsize = 20)
# axs.legend(bbox_to_anchor=(1.0,0.5,0.0,0.5))
# axs.legend(loc='upper left',ncol=2)
axs.set_title("(a)",**title_setup)


################
# Fig2 Scatter for Cl/Cd
################

legend_list = []
# fig, axs = plt.subplots(1,1,figsize=(6,6))
axs = axss[1]
for il, case in enumerate(data.keys()):
    
    style_dict = data[case]['style']
    labelName  = data[case]['label']
    
    if 'Case O' not in labelName:
      axs.plot(df['cd'][il],df['cl'][il],
              linestyle='none',
              marker=style_dict['marker'],
              c=style_dict['c'],
              markersize=15)
      legend_list.append(Line2D([0],[0],
                            linestyle='none',
                            marker=style_dict['marker'],
                            c=style_dict['c'],
                            markersize=10,
                            label=labelName
                                  ))
# axs.xaxis.set_major_formatter(formatter2)
axs.grid(**grid_setup)
axs.set(**{
          'xlabel':r"$C_d$",
          # 'xlim':[0.051,0.056],
          "ylabel":r"$C_l$",
          # 'ylim':[1.310,1.345],
          })
axs.axhline(df["cl"][0]     ,linestyle='-.',color = cc.grays)
axs.axvline(df["cd"][0]     ,linestyle='-.',color = cc.grays)

axs.legend(
  handles = legend_list,
  loc ='upper left',
  ncol = len(legend_list)//2,
  # bbox_to_anchor=(1.,0.5,0.0,0.5),
  prop={'size':15}
  )
axs.set_title("(b)",**title_setup)
axs.grid(which='major')
fig.tight_layout()
fig.savefig('Figs/01-CTRL-EFFECT/cl_VS_cd.jpg',**figkw)
fig.savefig('Figs/01-CTRL-EFFECT/cl_VS_cd.pdf',**figkw)


#######################################
# Inspect the Separation points 
########################################

side = 'SS'
for caseName in data.keys():
  name = data[caseName]['fileName']
  label = data[caseName]['label']
  fname= name_file(fldr,name,AOA,Rec,side)+'.mat'
  data[caseName][f'data_{side}'] = sio.loadmat(fname)
  data[caseName][f'Cmu'] = cal_Cmu(data[caseName]['config'])
  print(f"[IO] DATA: {fname}")
  # print(data[caseName]['data'].keys())
  
# We only Care about the suction side 
VarList =['cf',]
for var in VarList:
  fig,axs = plt.subplots(**single_fig_smaller)
  # axins = zoomed_inset_axes(axs,zoom=3,loc='lower center')
  
  x_c = 0.1
  var_Name = var_name_dict[var]
  legend_list=[]
  for il, case_name in enumerate(data.keys()):
    cf = data[case_name][f'data_{side}'][var].squeeze()
    xx = data[case_name][f'data_{side}']['xc'].squeeze()
    Cmu = data[case_name]["Cmu"]
    ind = np.where((cf>=0))[0][-1]-2
    x_loc_sep = 1 - xx[ind]

    style_dict = data[case_name]['style']
    labelName = data[case_name]['label']
    print(f"{labelName}:\nMomentum Coeff: {Cmu} \t Sep Loc: {x_loc_sep}")
    axs.plot(Cmu,x_loc_sep,
            linestyle='none',
            marker=style_dict['marker'],
            c=style_dict['c'],
            markersize=25)
    
    legend_list.append(Line2D([0],[0],
                        linestyle='none',
                        marker=style_dict['marker'],
                        c=style_dict['c'],
                        markersize=8,
                        label=labelName
                              ))
axs.xaxis.set_major_formatter(formatter2)
axs.grid(**grid_setup)
axs.set(**{
          'xlabel':r"$C_{\mu}$",
          "ylabel":r"$l_{\rm sep}$",
          'ylim':[0.0,0.15],
          'xlim':[-1e-3,1.4e-2],
          # "title":"Separation Assessment " + f"($C_f < 0$)",
          })
axs.legend(
        handles=legend_list,
        loc='upper right',
        # ncol=len(legend_list)//2,
        prop={'size':15}
          )
# axs.set_title("(c)",**title_setup)
fig.savefig(f'Figs/01-CTRL-EFFECT/{side}_Separation_Points.jpg',
              **figkw
              )
fig.savefig(f'Figs/01-CTRL-EFFECT/{side}_Separation_Points.pdf',
              **figkw
              )

