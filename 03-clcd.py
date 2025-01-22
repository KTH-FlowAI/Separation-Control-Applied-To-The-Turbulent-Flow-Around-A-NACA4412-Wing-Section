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
fldr='../../database/stsdata/' 
sides = ['SS',"PS"]


def rel_modif(g,p,positive=True):

  if positive:
    return (100*(p-g)/g) 
  else:
    return (100*(g-p)/g)

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
fig, axs = plt.subplots(1,1,figsize = (10,6))
caselist = [c for c in df['Name']]
caselist = [c for c in df['Name']]
print(caselist)


bottom = np.zeros(shape=(len(caselist)))
b1 = axs.bar(caselist,df['cd_tauw'],bottom=bottom,color = cc.grays,label='Cf')
bottom += df['cd_tauw']
b2 = axs.bar(caselist,df['cd_p'],bottom=bottom,color = cc.gray,label='Cp')
axs.axhline(df["cd_tauw"][0],color = cc.red)
axs.axhline(df["cd"][0],color = cc.red)
axs.set_ylabel(r'$C_d = C_f + C_p$',fontsize = 20)
axs.set_xlabel(r'CASE',fontsize = 20)
axs.legend(bbox_to_anchor=(1.0,0.5,0.0,0.5))
fig.tight_layout()
fig.savefig('Figs/01-CTRL-EFFECT/cl_cd_bar.jpg',**figkw)


################
# Fig2 Scatter for Cl/Cd
################


colorList = [cc.grays, cc.green, cc.deepgreen, cc.lightblue,
            cc.deepblue, cc.pink, cc.yellow, cc.darkred, cc.red]
colorList = [cc.black,cc.red,cc.blue,cc.yellow,cc.deepgreen,cc.lightblue]
fig, axs = plt.subplots(1,1,figsize=(8,4))
for il, case in enumerate(caselist):
    if il!=0:
        axs.plot(df['cd'][il],df['cl'][il],'o',markersize = 11.5,c=colorList[il],label=f"CASE {il}")
    else:
      axs.plot(df['cd'][il],df['cl'][il],'*',markersize = 12.5,c=colorList[il],label="Ref")

    # axs.text(df['cd'][il]-(1e-4),df['cl'][il]-2e-3,case,fontsize = 12, 
              # ha='right',va='bottom',color=colorList[il])
axs.set_ylabel(r"$C_l$",fontsize = 20)
axs.set_xlabel(r"$C_d$",fontsize = 20)
axs.legend(bbox_to_anchor=(1.,0.5,0.0,0.5))
# axs.set_yticks(np.linspace(0.75,0.95,7))
# axs.set_xticks(np.linspace(0.02,0.0235,3))
axs.grid(which='major')
fig.tight_layout()
fig.savefig('Figs/01-CTRL-EFFECT/cl_VS_cd.jpg',**figkw)

