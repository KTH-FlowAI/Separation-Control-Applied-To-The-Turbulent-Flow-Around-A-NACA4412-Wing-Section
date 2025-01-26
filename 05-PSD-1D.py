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

out =  sio.loadmat('002-SP-1D/SP1D_Ref_4.mat')  
data = post_process_Spectra(out)

out =  sio.loadmat('002-SP-1D/SP1D_CaseA_4.mat')  
data2 = post_process_Spectra(out)

out =  sio.loadmat('002-SP-1D/SP1D_CaseB_4.mat')  
data3 = post_process_Spectra(out)

out =  sio.loadmat('002-SP-1D/SP1D_CaseC_4.mat')  
data4 = post_process_Spectra(out)

levels = np.array([0.25,0.85])
fig,axs = plt.subplots(1,1)
axs.contour(
              data['lmd'],
              data['yn'],
              data['puu'],
              colors=cc.black,
              levels=levels*np.max(data['puu'],(0,1))
              )
axs.contour(
              data2['lmd'],
              data2['yn'],
              data2['puu'],
              colors=cc.blue,
              levels=levels*np.max(data2['puu'],(0,1))
              )
axs.contour(
              data3['lmd'],
              data3['yn'],
              data3['puu'],
              colors=cc.yellow,
              levels=levels*np.max(data3['puu'],(0,1))
              )
axs.contour(
              data4['lmd'],
              data4['yn'],
              data4['puu'],
              colors=cc.red,
              levels=levels*np.max(data4['puu'],(0,1))
              )

axs.set(**{
      'xscale':'log',
      'xlabel':r'$\lambda^+_z$',
      'xlim':[20,1500],
      'yscale':'log',    
      'ylabel':r'$y^+_n$',
      'ylim':[1,500],
            })
fig.savefig(f'figs/Prof_SP1D_Prof4.jpg',**{'dpi':300,'bbox_inches':'tight'})
print('[IO] Spectra Figure Saved')

