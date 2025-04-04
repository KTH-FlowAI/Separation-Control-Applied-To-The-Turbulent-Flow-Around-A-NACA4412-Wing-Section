#script to generate wing mesh
import struct,os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numexpr as ne
from math import pi,acos,floor, cos, sin

class NACA_XXXX:
    """ Class for 4-digit NACA wing. 
        First define a point distribution (mixed_dist), then, create profile (create_NACA_prof)
        and position it w. correct AoA and offset (position_wing)"""
    def __init__(self,c,t,m,p,*args,**kwargs):
        """
        Initialize 4-digit NACA with chord (c), thickness (t), maximum camber value (m) and its position (p)      

        Parameters
        ----------
        c : float
            chord length.
        t : float
            maximum thickness.
        m : float
            maximum camber.
        p : float
            position (w.r.t. chord) of maximum camber.

        Returns
        -------
        None.

        """
        """ initialize object instance, and set variables to None, no parameters required """
        self.c=c
        self.t=t
        self.m=m
        self.p=p     
        self.x_dist=None
        self.xu=None
        self.xl=None
        self.xu_0=None
        self.xl_0=None
        self.alphau_0=None
        self.alphal_0=None
        self.alphau=None
        self.alphal=None
        super().__init__(*args,**kwargs)
        return
        
    def mixed_dist(self,dx):
        """
        generate cosine distribution for 0<x<p and equidistant for p<x<1. Defined by delta_x of rear part

        Parameters
        ----------
        dx : float
            distance between points for x>p.

        Returns
        -------
        None.

        """
        p=self.p
        delta_theta=pi/2-acos(dx/p)
        numm=round((pi/2)/delta_theta)
        dd=np.arange(numm)
        x=ne.evaluate("(1-cos(dd/(numm-1)*pi/2))*p")
        x=np.delete(x,-1)
        x=np.append(x,p)
        dx = x[-1] - x[-2]
        numm = int(floor((1-p) / dx))
        x2=x[-1]+(np.arange(numm)+1)*dx
        if x2[-1]>=1:
            x2=np.delete(x2,-1)
        x2=np.append(x2,1)
        x=np.append(x,x2)
        print("Number of points in wing:",len(x))
        self.x_dist=x*self.c

    def linear_dist(self,npoints):
        self.x_dist=np.linspace(0,1,npoints)*self.c

    def square_dist(self,npoints):
        self.x_dist=np.square(np.linspace(0,1,npoints))*self.c
    
    def create_NACA_prof(self):
        """
        Create a NACA 4 digit profile, given the parameters of used to initialize the object 
        and a previously defined point distribution (self.x_dist).
        Then, position NACA profile (first rotate AoA, then add offset in x-axis)

        Parameters
        ----------
        offset : float, optional
            Offset in x direction. The default is 0.
        aoa : float, optional
            Angle of attack (in radians). The default is 0.
            
        Returns
        -------
        xu : np.array (2 x npoints)
            coordinates of suction side.
        xl : np.array (2 x npoints)
            coordinates of pressure side.
        alphau : np.array (npoints)
            surface angle of suction side.
        alphal : np.array (npoints)
            surface angle of pressure side.

        """
        c=self.c
        t=self.t
        m=self.m
        p=self.p
        if self.x_dist is None:
            self.square_dist(int(1e4))
        x=self.x_dist
        a0 = 0.2969
        a1 = -0.1260
        a2 = -0.3516
        a3 = 0.2843
        a4 = -0.1036
        yt=ne.evaluate("5*t*c*(a0*((x/c)**0.5)+a1*x/c+a2*(x/c)**2+a3*(x/c)**3+a4*(x/c)**4)")
        dytdx = ne.evaluate("5*t*(((a0/2))/((x/c)**0.5)+a1+2*a2*(x/c)+3*a3*(x/c)**2+4*a4*(x/c)**3)")
        # Symmetric NACA profile
        if self.m == 0.0:
            self.xu_0=np.array([x,yt])
            self.xl_0=np.array([x,-yt])
        # Cambered NACA profile
        else:
            yc = ne.evaluate("where(x<=p*c,m*x/(p**2)*(2*p-x/c),m*(c-x)/((1-p)**2)*(1+x/c-2*p))")
            dycdx = ne.evaluate("where(x<=p*c,2*m/(p**2)*(p-x/c),2*m/((1-p)**2)*(p-x/c))")
            theta=ne.evaluate("arctan(dycdx)")
            xu_0=ne.evaluate("x-yt*sin(theta)")
            yu_0=ne.evaluate("yc+yt*cos(theta)")
            self.xu=np.array([xu_0,yu_0])
            xl_0=ne.evaluate("x+yt*sin(theta)")
            yl_0=ne.evaluate("yc-yt*cos(theta)")
            self.xl=np.array([xl_0,yl_0])
        self.alphau=np.arctan(np.gradient(self.xu[1],self.xu[0]))
        self.alphal=np.arctan(np.gradient(self.xl[1],self.xl[0]))
        

        self.alphau_0=np.copy(self.alphau)
        self.alphal_0=np.copy(self.alphal)
        self.xu_0=np.copy(self.xu)
        self.xl_0=np.copy(self.xl)

        return self.xu,self.xl, self.alphau,self.alphal
    
    def rotate_profile(self,aoa,x_off):
        def cart2pol(x,y):
            theta = np.arctan2(y,x)
            r = np.hypot(x,y)
            return theta, r
        def pol2cart(theta,r):
            x = r*np.cos(theta)
            y = r*np.sin(theta)
            return x, y       
        self.xu[0]+=x_off
        self.xl[0]+=x_off      
        th,r = cart2pol(self.xu[0],self.xu[1])
        self.xu[0], self.xu[1] = pol2cart(th-aoa, r)
        del th, r
        th,r = cart2pol(self.xl[0],self.xl[1])
        self.xl[0], self.xl[1] = pol2cart(th-aoa, r)        
        self.alphau = self.alphau - aoa
        self.alphal=self.alphal-aoa
        return self.xu, self.xl, self.alphau, self.alphal
    
    def wall_normal_coords(self,xc,side='SS'):
        """
        Get coordinates and surface angle for a specific x/c value

        Parameters
        ----------
        xc : float
            Required chord-wise position.
        side : String, optional
            Suction side (SS) or pressure side (PS). The default is 'SS'.

        Returns
        -------
        pos : np.array of floats
            [x,y] coordinate.
        theta : float
            surface angle.

        """
        xc=xc*self.c
        if side=="SS":
            idx=np.argmin(np.absolute(self.xu_0[0]-xc))
            pos=self.xu[:,idx]
            theta=self.alphau[idx]
        else:
            idx=np.argmin(np.absolute(self.xl_0[0]-xc))
            theta=self.alphal[idx]
            pos=self.xl[:,idx]
        return pos, theta
    
    def plot_airfoil(self):
        plt.figure()
        plt.subplot(121)
        plt.plot(self.xu[0],self.xu[1],'r-')
        plt.plot(self.xl[0],self.xl[1],'r-')
        plt.plot(self.xu_0[0],self.xu_0[1],'k-')
        plt.plot(self.xl_0[0],self.xl_0[1],'k-')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.axis('equal')
        plt.subplot(122)
        plt.plot(self.xu_0[0],self.alphau_0*180/pi)
        plt.plot(self.xl_0[0],self.alphal_0*180/pi)
        plt.xlabel('x/c')
        plt.ylabel('$\theta$ [deg]')
    
    def create_BL_prof(self,yn,xc,side='SS',plotprof=False):
        """
        Generate a wall-normal profile with a prescribed point distribution (yn) at a chord-wise position

        Parameters
        ----------
        yn : array of floats
            point distribution.
        xc : float
            chord-wise position.
        side : String, optional
            suction side (SS) and pressure side (PS). The default is 'SS'.
        plotprof : boolean, optional
            Plot or not BL profile over airfoil. The default is True.

        Returns
        -------
        xprof : array of floats
            [x,y] coords of wall-normal profile at x/c.

        """
        x,aoa=self.wall_normal_coords(xc,side)
        if side=='PS':
            aoa+=pi
        rmatrix=np.array([[np.cos(aoa),-np.sin(aoa)],[np.sin(aoa),np.cos(aoa)]])
        xprof=np.matmul(rmatrix,np.array([np.zeros(np.shape(yn)),yn]))
        xprof[0]=xprof[0]+x[0]
        xprof[1]=xprof[1]+x[1]
        if plotprof:
            plt.figure()
            plt.plot(self.xu[0],self.xu[1],'k-')
            plt.plot(self.xl[0],self.xl[1],'k-')  
            plt.plot(xprof[0],xprof[1],'r-o',markersize=3)  
            plt.xlabel('x')
            plt.ylabel('y')
            plt.axis('equal')
        return xprof, aoa

##########
#  Class for the 
##########


class NACA_mesh(NACA_XXXX):
     """ Mesh for interpolating over wing surface.
     Inherits from NACA_XXXX class (for NACA profile definition)"""
     def __init__(self,xclocs,t,m,p,c=1,aoa=0,offset=0,npts=1):
         """
         Initialize NACA_mesh object.

         Parameters
         ----------
         xclocs : Float array
             Locations in x/c in which profiles will be created.
         t : Float
             DESCRIPTION.
         m : Float
             DESCRIPTION.
         p : Float
             DESCRIPTION.
         c : Float, optional
             Chord length. The default is 1.
         aoa : Float, optional
             Angle of attack (in radians). The default is 0.
         offset : Float, optional
             Offset applied to x coordinate. The default is 0.

         Returns
         -------
         None.

         """
         self.xcpos = xclocs
         self.aoa = aoa
         self.offset = offset
         self.data = pd.DataFrame(columns=['xc','x','y','theta','yn','prof_num','side'])#,'z'])    # add Z
         self.nprofs = 0
         super().__init__(c,t,m,p)  # initialize NACA_XXXX profile
         # self.square_dist(1e5)
         self.create_NACA_prof()    # create NACA_XXXX profile
         self.rotate_profile(self.aoa, self.offset)
         
     def create_wall_mesh(self,npts):
         """
         Create wall mesh (only points at the surface of the wing)

         Returns
         -------
         TYPE
             DESCRIPTION.
         TYPE
             DESCRIPTION.
         TYPE
             DESCRIPTION.

         """
         idx = 0
         self.square_dist(npts)
         self.create_NACA_prof()    # create NACA_XXXX profile
         self.rotate_profile(self.aoa, self.offset)
         # first suction side, then pressure side
         for side,xx,xc,theta in zip(['SS','PS'],(self.xu,self.xl),(self.xu_0,self.xl_0),(self.alphau,self.alphal)):
              # for pnt in self.xcpos:
              for i in range(npts):
                 temp_dc = pd.DataFrame({'xc': xc[0,i],'x': xx[0,i],'y': xx[1,i],
                            'theta': theta[i],'yn': 0.0,
                            'prof_num': idx+self.nprofs,
                            'side':  side },index=[1])                 
                 self.data = self.data.append(temp_dc, ignore_index=True)
                 idx+=1
         self.nprofs += idx
         return self.data
                 
     def define_yn_prof(self,npts,d_out,d_in=1e-5):
         self.yn = np.zeros((np.size(self.xcpos)*2,npts))
         if np.size(d_out)==1:
             d_out=np.ones(np.size(self.xcpos)*2)*d_out
         if np.size(d_in)==1:
             d_in=np.ones(np.size(self.xcpos)*2)*d_in
         i=0
         for d1,d2 in zip(d_in,d_out):
             prf_tmp =  np.concatenate(([0],np.logspace(np.log10(d1),np.log10(d2),npts-1)))
             self.yn[i] = prf_tmp
             i+=1
        
     def plot_mesh(self):
         """
         Plot interpolating mesh and wing profile

         Returns
         -------
         None.

         """
         plt.figure()
         plt.plot(self.xu[0],self.xu[1],'k.',lw = 0.5)
         plt.plot(self.xl[0],self.xl[1],'k.',lw = 0.5)
         plt.plot(self.data['x'],self.data['y'],'.')
         plt.axis('equal')
         plt.show()       
      
     def create_BL_mesh(self,z0=None,z1=None,nlayers=None):
         """
         Creates BL mesh (either 2D or 3D, depending on ldim)

         Parameters
         ----------
         z0 : Float, optional
             Initial Z coordinate for interpolating mesh. The default is None.
         z1 : Float, optional
             Final Z coordinate for interpolating mesh. The default is None.
         nlayers : Float or array of floats, optional
             Number of layers in Z. The default is None.

         Returns
         -------
         TYPE
             DESCRIPTION.

         """
         idx=0
         # first suction side, then pressure side
         for side in ['SS','PS']:
             for pnt in self.xcpos:
                 if pnt==0.0 and side=='SS':
                     pass
                 else:
                     prof,theta = self.create_BL_prof(self.yn[idx],pnt,side)
                     npts = np.size(self.yn[idx])
                     temp_dc = pd.DataFrame({'xc': pnt*np.ones(npts),'x': prof[0],'y': prof[1],
                               'theta': theta*np.ones(npts),'yn': self.yn[idx],
                               'prof_num': (self.nprofs+idx)*np.ones(npts),
                               'side': np.asarray([side for i in range(prof.shape[1])])})
                     self.data = self.data.append(temp_dc, ignore_index=True)
                     idx+=1
         self.nprofs += idx
         return self.data

     def create_BL_mesh_3D(self,side,xc,yn,z0=None,z1=None,nlayers=None):
         """
         Creates BL mesh (either 2D or 3D, depending on ldim)

         Parameters
         ----------
         z0 : Float, optional
             Initial Z coordinate for interpolating mesh. The default is None.
         z1 : Float, optional
             Final Z coordinate for interpolating mesh. The default is None.
         nlayers : Float or array of floats, optional
             Number of layers in Z. The default is None.

         Returns
         -------
         TYPE
             DESCRIPTION.

         """
         zvec = np.linspace(z0,z1,nlayers)
         # first suction side, then pressure side
         prof,theta = self.create_BL_prof(yn,xc,side)
         npts = np.size(yn)
         temp_dc = pd.DataFrame( {'xc': xc*np.ones(npts*nlayers),
                   'x': np.tile(prof[0],nlayers),'y': np.tile(prof[1],nlayers),
                   'z':np.repeat(zvec,npts),'theta': theta*np.ones(npts*nlayers),'yn': np.tile(yn,nlayers),
                  'prof_num': self.nprofs*np.ones(npts*nlayers),
                  'side':  np.tile(np.asarray([side for i in range(prof.shape[1])]),nlayers) } )
         self.data = self.data.append(temp_dc, ignore_index=True)
         self.nprofs += 1
         return self.data
     
     def create_singlepoint_mesh_3D(self,x0,y0,xc=None,z0=None,z1=None,nlayers=None,name='wallpoint'):

         if xc==None:
             xc=x0
         zvec = np.linspace(z0,z1,nlayers)
         temp_dc = pd.DataFrame( {'xc': xc*np.ones(nlayers),
                   'x': x0*np.ones(nlayers),'y': y0*np.ones(nlayers),
                   'z':zvec,'theta': np.zeros(nlayers),'yn': y0*np.ones(nlayers),
                  'prof_num': self.nprofs*np.ones(nlayers),
                  'side':  np.tile(np.asarray([name]),nlayers) } )
         self.data = self.data.append(temp_dc, ignore_index=True)
         self.nprofs += 1
         return self.data
        
     def create_wake_mesh_3D(self,x0,y0,npts,l,z0=None,z1=None,nlayers=None):

         
         TE=self.xu[:,-1]
         zvec = np.linspace(z0,z1,nlayers)
         y1 = np.linspace(0,1,int(npts/2))**1.3
         yvec = np.concatenate((-np.flip(y1),y1[1:]))*l/2 + y0 #+ TE[1]
         x0 += TE[0]
         # first suction side, then pressure side
         npts = np.size(yvec)
         temp_dc = pd.DataFrame( {'xc': (1+x0)*np.ones(npts*nlayers),
                   'x': x0*np.ones(npts*nlayers),'y': np.tile(yvec,nlayers),
                   'z':np.repeat(zvec,npts),'theta': np.zeros(npts*nlayers),'yn': np.tile(yvec,nlayers),
                  'prof_num': self.nprofs*np.ones(npts*nlayers),
                  'side':  np.tile(np.asarray(['wake' for i in range( npts)]),nlayers) } )
         self.data = self.data.append(temp_dc, ignore_index=True)
         self.nprofs += 1
         return self.data
        
     def save_mesh_params(self,filename):
         """
         Save interpolating mesh information into csv: x/c, x, y, (z), theta"

         Parameters
         ----------
         filename : str
             Filename.

         Returns
         -------
         None.

         """
         self.data.to_csv(filename,index=False)
        
     def write_int_pos(self,fname,wdsize,emode):
        """
         Write point positions to file

         Parameters
         ----------
         fname : str
             Filename.
         wdsize : Int
             Word (bit) size (4 or 8).
         emode : str
             Endian mode (big endian:> or little endian:>).

         Returns
         -------
         None.

         """
        if 'z' in self.data.columns:
            ldim = 3
            data = self.data[['x','y','z']].to_numpy()
        else:
            ldim = 2
            data = self.data[['x','y']].to_numpy()
        # open file
        outfile = open(fname, 'wb')
        # word size
        if (wdsize == 4):
            realtype = 'f'
        elif (wdsize == 8):
            realtype = 'd'
        # header
        npoints = np.shape(data)[0]
        header = '#iv1 %1i %1i %10i ' %(wdsize,ldim,npoints)
        header = header.ljust(32)
        outfile.write(header.encode('utf-8'))
        # write tag (to specify endianness)
        outfile.write(struct.pack(emode+'f', 6.54321))
        #write point positions
        for il in range(npoints):
            outfile.write(struct.pack(emode+ldim*realtype, *data[il]))
    
     def extrude_3D(self,z_vec):
         """
         Extrude a mesh (XY profiles), using a given z-coordinate distribution for each profile

         Parameters
         ----------
         z_vec : Z distribution for each profile: [[z_1],[z_2],... [z_N]]
             DESCRIPTION.

         Returns
         -------
         None.

         """
         nprofs = np.size(self.data['prof_num'].unique())
         if np.shape(z_vec)[0]==nprofs:
             tmp_df = self.data.loc[self.data.index.repeat([np.size(zz) for zz in z_vec])].reset_index(drop=True)
             tmp_df['z'] = [item for sublist in z_vec for item in sublist]
             self.data = tmp_df
         else:
            print('Z vector should have the same 0th dimesion as the number of streamwise profiles')
    
     def mesh_wake(self,xc,wake_center,wake_l,wake_u,npts=50):
         # x2_vec = np.linspace(0,1,int(npts/2)+1)**2.5
         x2_vec = np.logspace(-3.5,-1,int(npts/2)+1)
         x2_vec -= np.min(x2_vec)
         x2_vec = x2_vec/np.max(x2_vec)
         xTE = self.xu[-1]
         plt.figure()
         plt.plot(self.xu[0],self.xu[1],'k-')
         plt.plot(self.xl[0],self.xl[1],'k-')
         for idx, xcc in enumerate(xc):
             y1 = x2_vec*(wake_l[idx]-wake_center[idx]) + wake_center[idx]
             y2 = x2_vec*(wake_u[idx]-wake_center[idx]) + wake_center[idx]
             y = np.concatenate((np.flip(y1),y2[1:]))
             plt.plot((xcc+xTE)*np.ones(np.shape(y)),y,'o')
             temp_dc = pd.DataFrame({'xc': xcc*np.ones(np.shape(y)),'x':(xcc+xTE)*np.ones(np.shape(y)),
                       'y': y,'theta': np.zeros(np.shape(y)),'yn': y,
                       'prof_num': (self.nprofs+idx)*np.ones(np.shape(y)),
                       'side': np.asarray(['W' for i in range(np.size(y))])})
             self.data = self.data.append(temp_dc, ignore_index=True)
         self.nprofs += idx
         return self.data
     
     def grid_mesh(self,x_lims,y_lims,xpts,ypts):
         x = np.linspace(x_lims[0],x_lims[1],xpts)
         y = np.linspace(y_lims[0],y_lims[1],ypts)
         x = np.repeat(x,ypts)
         y = np.tile(y,xpts)
         self.data = pd.DataFrame({'x':x,'y':y})


#%%

if __name__ == "__main__":
    # initialise variables
    fname = 'int_pos_A'
    wdsize = 8
    # little endian
    # big endian
    emode = '<'
    
    # generate wing mesh
    t = 12/100
    c = 1
    m = 4/100
    p = 4/10
    offset = -0.5
    aoa = 11 # deg
    aoa_= aoa*np.pi/180 

    # wall-normal profiles 
    npts = 10  # Number of points for each wall-normal profile 
    d_out= 1e-1 # outer-scaled unit length
    d_in = 5e-5 # inner-scaled unit length

#%%
    # FOR TURB STAT
    if True:    
        # Boundary Layer mesh
        fldr = 'outputs/'
        if not os.path.exists(fldr):os.mkdir(fldr)
    ##########
    # Mesh generation
    ##########    
        ##  Get two arrays of x-coordinates for S.S and P.S 
        xc_vec = np.linspace(0.0,1.0,100)**2.5 * 0.02
        # quit()
        # xc_vec = np.linspace(0.0,1,91)
        # xc_vec = [0.6,0.75,0.85,0.9]
        ## Generate the Mesh based on the parameter 
        wallMesh = NACA_mesh(xc_vec,t,m,p,c=c,aoa=aoa_,offset=offset)
        ## Use the prescribed inner- and outer-scaled length to generate wall-normal profiles 
        wallMesh.define_yn_prof(npts=npts,d_out=d_out,d_in=d_in)
        ## Create the mesh 
        wallMesh.create_BL_mesh()

    ##########
    # Checking Results 
    ##########    
        ## Visualize the MAP 
        fig,axs = plt.subplots(1,1,figsize=(8,4))
        axs.plot(wallMesh.xl[0],wallMesh.alphal_0)
        axs.plot(wallMesh.xu[0],wallMesh.alphau_0)
        axs.set(**{"xlabel":"x/c","ylabel":r"$\theta$"})
        plt.savefig('Figs/05-Suply/Ncurrent_Map.jpg',bbox_inches='tight',dpi=300)
        quit()
    ##########
    # I/O 
    ##########
        ##write points to the BINARY file used in NEK5000 
        wallMesh.write_int_pos(fldr+fname,wdsize,emode)

        ## Information for profiles, which will be used for post-processing . 
        wallMesh.save_mesh_params(fldr+f'/pnts_wing_{aoa}deg_BL_1.txt')
        print(f"\n[I/O] Save data to {fldr}")

        ## An example to extract the profiles. 
        with open('wing_prof.csv','w') as f:
            f.write(f"SIDE, x, y\n")
            for il in range(len(wallMesh.xu[0])):
                f.write(f"SS, {wallMesh.xu[0][il]:.4f}, {wallMesh.xu[1][il]:.4f}\n")
            for il in range(len(wallMesh.xl[0])):
                f.write(f"PS, {wallMesh.xl[0][il]:.4f}, {wallMesh.xl[1][il]:.4f}\n")
        f.close()
        