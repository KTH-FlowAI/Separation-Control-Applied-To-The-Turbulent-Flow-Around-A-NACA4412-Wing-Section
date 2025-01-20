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

# # #######################################
# # # # OVER SUCTION SIDE 
# # # #######################################
side= 'aero'
df = {
    "Name":[],
    "cl":[],
    "cd":[],
    "cd_p":[],
    "cd_tauw":[],
    "LD":[],
      }

for caseName in data.keys():
  name = data[caseName]['fileName']
  label = data[caseName]['label']
  fname= name_file(fldr,name,AOA,Rec,side)+'.mat'
  data[caseName]['data'] = sio.loadmat(fname)
  print(f"[IO] DATA: {fname}")
  print(data[caseName]['data'].keys())
  df['Name'].append(label)
  
  df['cl'].append(data[caseName]['data']['cl'][0][0])
  df['cd'].append(data[caseName]['data']['cd'][0][0])
  df['cd_p'].append(data[caseName]['data']['cd_p'][0][0])
  df['cd_tauw'].append(data[caseName]['data']['cd_tauw'][0][0])
  df['LD'].append(data[caseName]['data']['LD'][0][0])

pd.DataFrame(df).to_csv('CLCD.csv',float_format="%.6e")
