import struct 
import numpy as np 
import matplotlib.pyplot as plt 
import scipy.io as sio 
from lib.dataReader import *

class wingProf():
  def __init__(self,fname) -> None:
    """ Initializing the geometery of 2D Map"""
    d = sio.loadmat(fname)
    
    # Coordinates
    self.x_pts = np.array(d['x_pts']).reshape(-1,1)
    self.y_pts = np.array(d['y_pts']).reshape(-1,1)
    
    # relative angles
    self.alphau = np.array(d['alphau']).reshape(-1,1)
    self.alphal = np.array(d['alphal']).reshape(-1,1)

    # chord coordinates and yn distance
    self.xc = np.array(d['xc']).reshape(-1,1)
    self.yn = np.array(d['yn']).reshape(-1,1)

    # This hard-coded shift is based on the current mesh 
    self.x_pts -= 0.5

    # Useful Parameters
    self.npoints = d['npoints'][0][0]
    ln = len(self.yn)
    nps = int((self.npoints / ln ) / 2)
    self.np = nps 
    self.ln = ln
    
    del d 
    print(f"Summary:\n"+\
          f"Npoints = {self.npoints}\n"
          f"x_pts = {self.x_pts.shape}\n"+\
          f"y_pts = {self.y_pts.shape}\n"+\
          f"alpha_u = {self.alphau.shape}\n"+\
          f"alpha_l = {self.alphal.shape}\n"+\
          f"xc = {self.xc.shape}\n"+\
          f"yn = {self.yn.shape}\n")
  
#----------------------------------------------------------------
  def rotated_wing(self,aoa):
    """ Rotating the MAP with AoA """
    self.x_pts = self.x_pts * np.cos(aoa) - self.y_pts * np.sin(aoa)
    self.y_pts = self.x_pts * np.sin(aoa) + self.y_pts * np.cos(aoa)
    return
  
#----------------------------------------------------------------
  def split_top_bot(self):
    """ Divide the map by TOP & BOTTOM """
    print(f"ln = {self.ln}, np = {self.np}")
    self.top = [ {"x":None,"y":None,"xa":None,"ya":None,"xc":None,'yn':None,"theta":None} for i in range(self.np) ]
    self.bot = [ {"x":None,"y":None,"xa":None,"ya":None,"xc":None,'yn':None,"theta":None} for i in range(self.np) ]
    
    # For top
    ######################################################
    for il in range(self.np):
      self.top[il]['xa'] = self.x_pts[self.ln*il]
      self.top[il]['ya'] = self.y_pts[self.ln*il]
      
      self.top[il]['theta'] = self.alphau[il]
      self.top[il]['yn'] = self.yn[il]
      self.top[il]['xc'] = self.xc[il]
      
      self.top[il]['x'] = self.x_pts[self.ln*il+1:self.ln*il+self.ln ]
      self.top[il]['y'] = self.y_pts[self.ln*il+1:self.ln*il+self.ln ]

      theta = self.top[il]['theta'][0]
      self.top[il]['rmat'] = np.array([[np.cos(theta), np.sin(theta), 0.0],
                                      [-np.sin(theta), np.cos(theta), 0.0],
                                      [0.0,            0.0,           1.0]])
    
    # For bot 
    ###################################################
    self.bot[0]['xa']     = self.x_pts[0]
    self.bot[0]['ya']     = self.y_pts[0]
    self.bot[0]['x']      = self.top[0]['x']
    self.bot[0]['y']      = self.top[0]['y']
    self.bot[0]['theta']  = self.alphal[0]
    self.bot[0]['rmat']  = self.top[0]['rmat']
    self.bot[0]['xc']     = self.xc[0]
    self.bot[0]['yn']     = self.yn[0]

    for il in range(1,self.np):
      self.bot[il]['theta'] = self.alphal[il]
      theta = self.bot[il]['theta'][0]
      self.bot[il]['rmat'] = np.array([[np.cos(theta), -np.sin(theta), 0.0],
                                      [-np.sin(theta), -np.cos(theta), 0.0],
                                      [0.0,            0.0,            1.0]])

      self.bot[il]['xc']    = self.xc[il]
      self.bot[il]['yn']    = self.yn[il]
      
      self.bot[il]['xa'] = self.x_pts[self.ln*(il-1)+1+self.np*self.ln]
      self.bot[il]['ya'] = self.y_pts[self.ln*(il-1)+1+self.np*self.ln]
        
      self.bot[il]['x'] = self.x_pts[self.ln*(il-1)+1+self.np*self.ln : self.ln*(il-1)+self.ln+self.np*self.ln]
      self.bot[il]['y'] = self.y_pts[self.ln*(il-1)+1+self.np*self.ln : self.ln*(il-1)+self.ln+self.np*self.ln]

    return 
  
#----------------------------------------------------------------
  def load_TurbStat(self, stat_fname):
    """Read int_fld data"""

    ## Read Data 
    data = read_int_fld(stat_fname)
    assert data.npoints == self.npoints, "\n[Warning] Total points must match!"
    ## Step 1 Summary 
    print_sim_data(data)
    attrs = ['re','nstat',"nderiv"]

    ### Move Attrs to this class
    for ati in attrs:
      setattr(self,ati,getattr(data,ati))
    ### Dynamic vis and density 
    self.nu  = 1/self.re
    self.rho = 1
    self.mu  = self.rho * self.nu
    print(f'    nu  = {self.nu}')
    print(f'    rho = {self.rho}')
    print(f'    mu  = {self.mu}')

    for il in range(self.np):
      self.top[il]['rho'] = self.rho
      self.top[il]['nu']  = self.nu
      self.top[il]['mu']  = self.mu

    ## Step 2 Assign the value 
    ### NOTE: Take the field list as ref 
    M_s = np.empty(shape=(data.npoints,self.nstat))
    M_d = np.empty(shape=(data.npoints,self.nderiv))
    for il in range(data.npoints):
      lptn      = data.pset[il]
      M_s[il,:] = getattr(lptn,'stat')
      M_d[il,:] = getattr(lptn,'deriv')
    print(f"Empty value in STAT =  {np.sum(np.isnan(M_s))}; Deriv = {np.sum(np.isnan(M_d))}")
    
    #-------------------------------------
    print("\n[STAT] Recording Nstat: F")
    for jl in range(self.nstat):
      for il in range(self.np):
        self.top[il][f"F{jl+1}"] = M_s[self.ln*il : self.ln*il+self.ln, jl]
  
      self.bot[0][f"F{jl+1}"] = self.top[0][f'F{jl+1}']
      for il in range(1,self.np):
        self.bot[il][f"F{jl+1}"] = M_s[self.ln*(il-1) +self.np*self.ln : self.ln*(il-1) +self.np*self.ln +self.ln, jl]
  
    #-------------------------------------
    print("\n[STAT] Recording Deriv: D")
    for jl in range(self.nderiv):
      for il in range(self.np):
        self.top[il][f"D{jl+1}"] = M_d[self.ln*il : self.ln*il+self.ln, jl]
  
      self.bot[0][f"D{jl+1}"] = self.top[0][f'D{jl+1}']
      for il in range(1,self.np):
        self.bot[il][f"D{jl+1}"] = M_d[self.ln*(il-1) +self.np*self.ln : self.ln*(il-1) +self.np*self.ln +self.ln, jl]
  
    return 

#----------------------------------------------------------------  
  def calculate_profs(self):
    """Based on the Statistisc compute the profiles"""

    def rot_tensor1(T,rmat):
            """T = quantities, rmat = rotation matrix"""
            return rmat @ T

    def rot_tensor2(T,rmat):
            return rmat @ T @ rmat.T
    
    lzeros = np.zeros((self.ln,1))

    for il in range(self.np):
      print(f"At X/C = {self.xc[il]}")
      
      # UVW
      #-------------------------------------
      Varlist = ['U',"V",'W']
      for v in Varlist:
        self.top[il][v] = np.zeros_like(lzeros)
        self.bot[il][v] = np.zeros_like(lzeros)
      
      for jl in range(self.ln):
        Vec_top = np.stack((  self.top[il]['F1'][jl],
                              self.top[il]['F2'][jl],
                              self.top[il]['F3'][jl],))
      
        Vec_bot = np.stack((  self.bot[il]['F1'][jl],
                              self.bot[il]['F2'][jl],
                              self.bot[il]['F3'][jl],))

        prod_top = rot_tensor1(T=Vec_top,rmat=self.top[il]['rmat'])
        prod_bot = rot_tensor1(T=Vec_bot,rmat=self.bot[il]['rmat'])
        
        
        self.top[il]["U"][jl] = prod_top[0]
        self.top[il]["V"][jl] = prod_top[1]
        self.top[il]["W"][jl] = prod_top[2]
        
        self.bot[il]["U"][jl] = prod_bot[0]
        self.bot[il]["V"][jl] = prod_bot[1]
        self.bot[il]["W"][jl] = prod_bot[2]

      #-------------------------------------
    
      # Pressure gradient: dPdx dPdy dPdz
      #-------------------------------------
      Varlist = ['dPdx',"dPdy",'dPdz']
      for v in Varlist:
        self.top[il][v] = np.zeros_like(lzeros)
        self.bot[il][v] = np.zeros_like(lzeros)
      
      for jl in range(self.ln):
        Vec_top = np.stack((
                              self.top[il]['D7'][jl],
                              self.top[il]['D8'][jl],
                              self.top[il]['D8'][jl]*0,
                                        ))
      
        Vec_bot = np.stack((
                              self.bot[il]['D7'][jl],
                              self.bot[il]['D8'][jl],
                              self.bot[il]['D8'][jl]*0,
                                        ))

        prod_top = rot_tensor1(T  =Vec_top,
                          rmat=self.top[il]['rmat']            
                          )
        
        
        prod_bot = rot_tensor1(T  =Vec_bot,
                          rmat=self.bot[il]['rmat']            
                          )
        for vi, v in enumerate(Varlist):
          self.top[il][v][jl] = prod_top[vi]
          self.bot[il][v][jl] = prod_bot[vi]
        Vec_top, Vec_bot, prod_top, prod_bot = 0, 0,0,0
      #-------------------------------------
      
      # Reynolds Stress tensor 
      #-------------------------------------
      Varlist = [
                'uu',"vv",'ww',
                'uv',"uw",'vw',
                ]
      for v in Varlist:
        self.top[il][v] = np.zeros_like(lzeros)
        self.bot[il][v] = np.zeros_like(lzeros)
      
      for jl in range(self.ln):
        Vec_top = np.array([[ self.top[il]['F5'][jl]  - self.top[il]['F1'][jl]*self.top[il]['F1'][jl],
                              self.top[il]['F9'][jl]  - self.top[il]['F1'][jl]*self.top[il]['F2'][jl],
                              self.top[il]['F11'][jl] - self.top[il]['F1'][jl]*self.top[il]['F3'][jl],
                            ],
                            [ self.top[il]['F9'][jl]  - self.top[il]['F1'][jl]*self.top[il]['F2'][jl],
                              self.top[il]['F6'][jl]  - self.top[il]['F2'][jl]*self.top[il]['F2'][jl],
                              self.top[il]['F10'][jl] - self.top[il]['F2'][jl]*self.top[il]['F3'][jl],
                            ],
                            [ self.top[il]['F11'][jl]  - self.top[il]['F1'][jl]*self.top[il]['F3'][jl],
                              self.top[il]['F10'][jl]  - self.top[il]['F2'][jl]*self.top[il]['F3'][jl],
                              self.top[il]['F7'][jl]   - self.top[il]['F3'][jl]*self.top[il]['F3'][jl],
                            ],
                            ]
                            )
        
        Vec_bot = np.array([[ self.bot[il]['F5'][jl]  - self.bot[il]['F1'][jl]*self.bot[il]['F1'][jl],
                              self.bot[il]['F9'][jl]  - self.bot[il]['F1'][jl]*self.bot[il]['F2'][jl],
                              self.bot[il]['F11'][jl] - self.bot[il]['F1'][jl]*self.bot[il]['F3'][jl],
                            ],
                            [ self.bot[il]['F9'][jl]  - self.bot[il]['F1'][jl]*self.bot[il]['F2'][jl],
                              self.bot[il]['F6'][jl]  - self.bot[il]['F2'][jl]*self.bot[il]['F2'][jl],
                              self.bot[il]['F10'][jl] - self.bot[il]['F2'][jl]*self.bot[il]['F3'][jl],
                            ],
                            [ self.bot[il]['F11'][jl]  - self.bot[il]['F1'][jl]*self.bot[il]['F3'][jl],
                              self.bot[il]['F10'][jl]  - self.bot[il]['F2'][jl]*self.bot[il]['F3'][jl],
                              self.bot[il]['F7'][jl]   - self.bot[il]['F3'][jl]*self.bot[il]['F3'][jl],
                            ],
                            ]
                            )
      
        prod_top = rot_tensor2(T=Vec_top,rmat=self.top[il]['rmat'])
        prod_bot = rot_tensor2(T=Vec_bot,rmat=self.bot[il]['rmat'])
        
        self.top[il]['uu'][jl] = prod_top[0,0]
        self.top[il]['vv'][jl] = prod_top[1,1]
        self.top[il]['ww'][jl] = prod_top[2,2]
        self.top[il]['uv'][jl] = prod_top[0,1]
        self.top[il]['uw'][jl] = prod_top[0,2]
        self.top[il]['vw'][jl] = prod_top[1,2]
        
        self.bot[il]['uu'][jl] = prod_bot[0,0]
        self.bot[il]['vv'][jl] = prod_bot[1,1]
        self.bot[il]['ww'][jl] = prod_bot[2,2]
        self.bot[il]['uv'][jl] = prod_bot[0,1]
        self.bot[il]['uw'][jl] = prod_bot[0,2]
        self.bot[il]['vw'][jl] = prod_bot[1,2]
      #-------------------------------------


      # Velocity Gradient Tensor RANK 2 
      #-------------------------------------
      Varlist = [
                'dUdx',"dVdx",'dWdx',
                'dUdy',"dVdy",'dWdy',
                ]
      for v in Varlist:
        self.top[il][v] = np.zeros_like(lzeros)
        self.bot[il][v] = np.zeros_like(lzeros)
      
      for jl in range(self.ln):
        Vec_top = np.array([[ self.top[il]['D1'][jl] ,self.top[il]['D2'][jl] , 0],    # dUdx, dUdy, dUdz
                            [ self.top[il]['D3'][jl] ,self.top[il]['D4'][jl] , 0],    # dVdx, dVdy, dVdz
                            [ self.top[il]['D5'][jl] ,self.top[il]['D6'][jl] , 0],])  # dWdx, dWdy, dWdz
        
        Vec_bot = np.array([[ self.bot[il]['D1'][jl] ,self.bot[il]['D2'][jl] , 0],
                            [ self.bot[il]['D3'][jl] ,self.bot[il]['D4'][jl] , 0],
                            [ self.bot[il]['D5'][jl] ,self.bot[il]['D6'][jl] , 0],])

        prod_top = rot_tensor2(T=Vec_top,rmat=self.top[il]['rmat'])
        prod_bot = rot_tensor2(T=Vec_bot,rmat=self.bot[il]['rmat'])

        self.top[il]['dUdx'][jl] = prod_top[0,0]
        self.top[il]['dUdy'][jl] = prod_top[0,1]
        self.top[il]['dVdx'][jl] = prod_top[1,0]
        self.top[il]['dVdy'][jl] = prod_top[1,1]
        self.top[il]['dWdx'][jl] = prod_top[2,0]
        self.top[il]['dWdy'][jl] = prod_top[2,1]
        
        self.bot[il]['dUdx'][jl] = prod_bot[0,0]
        self.bot[il]['dUdy'][jl] = prod_bot[0,1]
        self.bot[il]['dVdx'][jl] = prod_bot[1,0]
        self.bot[il]['dVdy'][jl] = prod_bot[1,1]
        self.bot[il]['dWdx'][jl] = prod_bot[2,0]
        self.bot[il]['dWdy'][jl] = prod_bot[2,1]
      #------------------------------------

      #------------------------------------
      # TKE Budgets term
      #------------------------------------
      ## Production tensor 
      Varlist = [
                'Pxx',"Pyy",'Pzz',
                'Pxy',"Pxz",'Pyz',
                ]
      for v in Varlist:
        self.top[il][v] = np.zeros_like(lzeros)
        self.bot[il][v] = np.zeros_like(lzeros)
      
      for jl in range(self.ln):

        Vec_top = np.array([
                            [ 
                            -2*self.top[il]['uu'][jl]*self.top[il]['dUdx'][jl] + self.top[il]['uv'][jl]*self.top[il]['dUdy'][jl],
                            -(self.top[il]['uu'][jl]*self.top[il]['dVdx'][jl] + self.top[il]['uv'][jl]*self.top[il]['dVdy'][jl] + self.top[il]['uv'][jl]*self.top[il]['dUdx'][jl] + self.top[il]['vv'][jl]*self.top[il]['dUdy'][jl]),
                            -(self.top[il]['uu'][jl]*self.top[il]['dWdx'][jl] + self.top[il]['uv'][jl]*self.top[il]['dWdy'][jl] + self.top[il]['uw'][jl]*self.top[il]['dUdx'][jl] + self.top[il]['vw'][jl]*self.top[il]['dUdy'][jl]),
                            ],
                            [ 
                            -(self.top[il]['uu'][jl]*self.top[il]['dVdx'][jl] + self.top[il]['uv'][jl]*self.top[il]['dVdy'][jl] + self.top[il]['uv'][jl]*self.top[il]['dUdx'][jl] + self.top[il]['vv'][jl]*self.top[il]['dUdy'][jl]),
                            -2*self.top[il]['uv'][jl]*self.top[il]['dVdx'][jl] + self.top[il]['vv'][jl]*self.top[il]['dVdy'][jl],
                            -(self.top[il]['uv'][jl]*self.top[il]['dWdx'][jl] + self.top[il]['vv'][jl]*self.top[il]['dWdy'][jl] + self.top[il]['uw'][jl]*self.top[il]['dVdx'][jl] + self.top[il]['vw'][jl]*self.top[il]['dVdy'][jl]),
                            ],
                            [
                            -(self.top[il]['uu'][jl]*self.top[il]['dWdx'][jl] + self.top[il]['uv'][jl]*self.top[il]['dWdy'][jl] + self.top[il]['uv'][jl]*self.top[il]['dUdx'][jl] + self.top[il]['vw'][jl]*self.top[il]['dUdy'][jl]),
                            -(self.top[il]['uv'][jl]*self.top[il]['dWdx'][jl] + self.top[il]['vv'][jl]*self.top[il]['dWdy'][jl] + self.top[il]['uw'][jl]*self.top[il]['dVdx'][jl] + self.top[il]['vw'][jl]*self.top[il]['dVdy'][jl]),
                            -2*self.top[il]['uw'][jl]*self.top[il]['dWdx'][jl] + self.top[il]['uv'][jl]*self.top[il]['dWdy'][jl]
                            ]
                            ])
        Vec_bot = np.array([
                            [ 
                            -2*self.bot[il]['uu'][jl]*self.bot[il]['dUdx'][jl] + self.bot[il]['uv'][jl]*self.bot[il]['dUdy'][jl],
                            -(self.bot[il]['uu'][jl]*self.bot[il]['dVdx'][jl] + self.bot[il]['uv'][jl]*self.bot[il]['dVdy'][jl] + self.bot[il]['uv'][jl]*self.bot[il]['dUdx'][jl] + self.bot[il]['vv'][jl]*self.bot[il]['dUdy'][jl]),
                            -(self.bot[il]['uu'][jl]*self.bot[il]['dWdx'][jl] + self.bot[il]['uv'][jl]*self.bot[il]['dWdy'][jl] + self.bot[il]['uw'][jl]*self.bot[il]['dUdx'][jl] + self.bot[il]['vw'][jl]*self.bot[il]['dUdy'][jl]),
                            ],
                            [ 
                            -(self.bot[il]['uu'][jl]*self.bot[il]['dVdx'][jl] + self.bot[il]['uv'][jl]*self.bot[il]['dVdy'][jl] + self.bot[il]['uv'][jl]*self.bot[il]['dUdx'][jl] + self.bot[il]['vv'][jl]*self.bot[il]['dUdy'][jl]),
                            -2*self.bot[il]['uv'][jl]*self.bot[il]['dVdx'][jl] + self.bot[il]['vv'][jl]*self.bot[il]['dVdy'][jl],
                            -(self.bot[il]['uv'][jl]*self.bot[il]['dWdx'][jl] + self.bot[il]['vv'][jl]*self.bot[il]['dWdy'][jl] + self.bot[il]['uw'][jl]*self.bot[il]['dVdx'][jl] + self.bot[il]['vw'][jl]*self.bot[il]['dVdy'][jl]),
                            ],
                            [
                            -(self.bot[il]['uu'][jl]*self.bot[il]['dWdx'][jl] + self.bot[il]['uv'][jl]*self.bot[il]['dWdy'][jl] + self.bot[il]['uv'][jl]*self.bot[il]['dUdx'][jl] + self.bot[il]['vw'][jl]*self.bot[il]['dUdy'][jl]),
                            -(self.bot[il]['uv'][jl]*self.bot[il]['dWdx'][jl] + self.bot[il]['vv'][jl]*self.bot[il]['dWdy'][jl] + self.bot[il]['uw'][jl]*self.bot[il]['dVdx'][jl] + self.bot[il]['vw'][jl]*self.bot[il]['dVdy'][jl]),
                            -2*self.bot[il]['uw'][jl]*self.bot[il]['dWdx'][jl] + self.bot[il]['uv'][jl]*self.bot[il]['dWdy'][jl]
                            ]
                            ])

        prod_top = rot_tensor2(T=Vec_top.squeeze(),rmat=self.top[il]['rmat'])
        prod_bot = rot_tensor2(T=Vec_bot.squeeze(),rmat=self.bot[il]['rmat'])

        self.top[il]['Pxx'][jl] = prod_top[0,0]
        self.top[il]['Pyy'][jl] = prod_top[1,1]
        self.top[il]['Pzz'][jl] = prod_top[2,2]  
        self.top[il]['Pxy'][jl] = prod_top[0,1]
        self.top[il]['Pxz'][jl] = prod_top[0,2]
        self.top[il]['Pyz'][jl] = prod_top[1,2]

        self.bot[il]['Pxx'][jl] = prod_bot[0,0]
        self.bot[il]['Pyy'][jl] = prod_bot[1,1]
        self.bot[il]['Pzz'][jl] = prod_bot[2,2]  
        self.bot[il]['Pxy'][jl] = prod_bot[0,1]
        self.bot[il]['Pxz'][jl] = prod_bot[0,2]
        self.bot[il]['Pyz'][jl] = prod_bot[1,2]
      #------------------------------------
      
      
      #------------------------------------
      # Dissipation 
      Varlist = [
                'Dxx',"Dyy",'Dzz',
                'Dxy',"Dxz",'Dyz',
                ]
      for v in Varlist:
        self.top[il][v] = np.zeros_like(lzeros)
        self.bot[il][v] = np.zeros_like(lzeros)

      for jl in range(self.ln):
        
        Vec_top = np.array([
                            [self.top[il]['F39'][jl], self.top[il]['F42'][jl],                       0], #e11, e12, e13
                            [self.top[il]['F42'][jl], self.top[il]['F40'][jl], self.top[il]['F44'][jl]], #e12, e22, e23
                            [self.top[il]['F43'][jl], self.top[il]['F44'][jl], self.top[il]['F41'][jl]], #e13, e23, e33
                            ])
        
        Vec_bot = np.array([
                            [self.bot[il]['F39'][jl], self.bot[il]['F42'][jl],                       0], #e11, e12, e13
                            [self.bot[il]['F42'][jl], self.bot[il]['F40'][jl], self.bot[il]['F44'][jl]], #e12, e22, e23
                            [self.bot[il]['F43'][jl], self.bot[il]['F44'][jl], self.bot[il]['F41'][jl]], #e13, e23, e33
                            ])
        
        prod_top = rot_tensor2(T=Vec_top,rmat=self.top[il]['rmat'])
        prod_bot = rot_tensor2(T=Vec_bot,rmat=self.bot[il]['rmat'])

        self.top[il]['Dxx'][jl] = prod_top[0,0]
        self.top[il]['Dyy'][jl] = prod_top[1,1]
        self.top[il]['Dzz'][jl] = prod_top[2,2]  
        self.top[il]['Dxy'][jl] = prod_top[0,1]
        self.top[il]['Dxz'][jl] = prod_top[0,2]
        self.top[il]['Dyz'][jl] = prod_top[1,2]

        self.bot[il]['Dxx'][jl] = prod_bot[0,0]
        self.bot[il]['Dyy'][jl] = prod_bot[1,1]
        self.bot[il]['Dzz'][jl] = prod_bot[2,2]  
        self.bot[il]['Dxy'][jl] = prod_bot[0,1]
        self.bot[il]['Dxz'][jl] = prod_bot[0,2]
        self.bot[il]['Dyz'][jl] = prod_bot[1,2]
      #-------------------------------------


      #-------------------------------------
      ## Mean convection 
      Varlist = [
                'Cxx',"Cyy",'Czz',
                'Cxy',"Cxz",'Cyz',
                ]
      for v in Varlist:
        self.top[il][v] = np.zeros_like(lzeros)
        self.bot[il][v] = np.zeros_like(lzeros)

      # for jl in range(self.ln):
      #   return

    # # Pressure 
    # #-------------------------------------
    #   self.top[il]['P'] = self.top[il]['F4']
    #   self.bot[il]['P'] = self.bot[il]['F4']
      

    return