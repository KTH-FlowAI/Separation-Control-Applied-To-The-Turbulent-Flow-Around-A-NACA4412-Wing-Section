# -*- coding: utf-8 -*-
"""
Fast NACA XXXX generator class based on Numexpr and Numpy libraries

Created on Wed Jul  1 20:23:11 2020

@author: Fermin Mallor
"""

import numpy as np
import numexpr as ne
from math import pi,acos,floor, cos, sin
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

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
    
if __name__ == "__main__":

    naca_4412 = NACA_XXXX(4,4,1,2)

    naca_4412.create_BL_prof()