"""
Load and plot the Cl Cd 
@yuningw
"""
import  os
import pandas as pd 
import  numpy       as np 
import  scipy.io    as sio 
import  matplotlib.pyplot as plt 
from    lib.plot  import colorplate as cc 
from    lib.plot       import plt_setUp
import matplotlib.ticker as ticker
import argparse
figkw  ={'bbox_inches':"tight", "dpi":300}
plt_setUp()

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
fig.savefig('figs/cl_cd_bar.jpg',**figkw)


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
fig.savefig('figs/cl_VS_cd.jpg',**figkw)

