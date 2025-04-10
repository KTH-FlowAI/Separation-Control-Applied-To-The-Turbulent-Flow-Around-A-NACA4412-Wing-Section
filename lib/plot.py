import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.ticker import LogLocator, NullFormatter
from    matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
import  matplotlib.ticker as ticker
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset,inset_axes

class cc:
    red = "#D23918" # luoshenzhu
    blue = "#2E59A7" # qunqing
    yellow = "#E5A84B" # huanghe liuli
    cyan = "#5DA39D" # er lv
    black = "#151D29" # lanjian
    gray    = "#DFE0D9" # ermuyu 
    grays    = "#6B6C6E" # ermuyu 
    green   = "#16A951"     # Shi Lv
    deepgreen   = "#057748" # Song Hua Lv 
    lightblue = '#3EEDE7' # Bi Lan
    pink = '#FF0097' # Yanghong 
    darkred = '#9D2933' # Yanzhi 
    deepblue = '#003371' # Qianqing
    brown  = "#9F6027"
    purple = "#A76283" # zi jing pin feng 
    orange = "#EA5514" # huang dan
    deeppurple = "#674196"

    yellow2 = '#EBD842'

def plt_setUp():
    import matplotlib.pyplot as plt
    plt.rc("font",family = "serif")
    plt.rc("text",usetex = "true")
    plt.rc("font",size = 30)
    plt.rc("axes",labelsize = 35, linewidth = 2)
    plt.rc("legend",fontsize= 15, handletextpad = 0.1)
    plt.rc("xtick",labelsize = 22)
    plt.rc("ytick",labelsize = 22)
    return 

def plt_setUp_Smaller():
    import matplotlib.pyplot as plt
    plt.rc("font",family = "serif")
    plt.rc("text",usetex = "true")
    plt.rc("font",size = 20)
    plt.rc("axes",labelsize = 25, linewidth = 2)
    plt.rc("legend",fontsize= 20, handletextpad = 0.1)
    plt.rc("xtick",labelsize = 18)
    plt.rc("ytick",labelsize = 18)
    return 

def plt_setUp_Smaller2():
    import matplotlib.pyplot as plt
    plt.rc("font",family = "serif")
    plt.rc("text",usetex = "true")
    plt.rc("font",size = 20)
    plt.rc("axes",labelsize   = 25, linewidth = 2)
    # plt.rc("legend",fontsize  = 14, handletextpad = 0.1)
    plt.rc("xtick",labelsize  = 20)
    plt.rc("ytick",labelsize  = 20)
    return 



# Setup for output 
figkw  ={
        # 'bbox_inches':'tight',
        "dpi":300,
        'transparent':True,
        }
figkw2  ={
        'transparent':True,
        "dpi":300
        }

## Ticks formats

formatter2 = ticker.ScalarFormatter(useMathText=True)
formatter2.set_powerlimits([-1,5])

formatter3 = ticker.ScalarFormatter(useMathText=True,
                                    useLocale=True)
formatter3.set_powerlimits([-2,4])

formatter4 = ticker.ScalarFormatter(useMathText=True,
                                    useLocale=True)
formatter4.set_powerlimits([0,2])

# formatter3 = ticker.ScalarFormatter(useMathText=True,
#                                     useLocale=True)
# formatter3.set_powerlimits([-3,4])

## Syntax for set log grid 
locmin = LogLocator(base=10,subs=np.arange(0,10), numticks=10)
locmin2 = LogLocator(base=10,subs=np.arange(0,10), numticks=10)
locmin3 = LogLocator(base=10,subs=np.arange(0,10), numticks=10)

title_setup ={  
                'loc':'left',
                'pad':25,
                } 

single_fig_smaller = {
                'ncols':1,
                'nrows':1,
                'figsize':(7,7)
                  }

single_fig_cfg = {
                'ncols':1,
                'nrows':1,
                'figsize':(7,7)
                  }

single_fig_larger = {
                'ncols':1,
                'nrows':1,
                'figsize':(12,6)
                  }

double_fig_larger = {
                'ncols':2,
                'nrows':1,
                'figsize':(16,8),
                # 'sharey':True
                  }

triple_fig_larger = {
                'ncols':3,
                'nrows':1,
                'figsize':(26,6),
                # 'sharex':True
                  }


quadra_fig_larger = {
                'ncols':4,
                'nrows':1,
                # 'figsize':(24,6),
                'figsize':(40,7),
                # 'sharex':True
                  }

quadra_fig_22 = {
                'ncols':2,
                'nrows':2,
                # 'figsize':(24,6),
                'figsize':(20,15),
                # 'sharex':True
                  }
quadra_fig_22_large = {
                'ncols':2,
                'nrows':2,
                # 'figsize':(24,6),
                'figsize':(12,14),
                # 'sharex':True
                  }

quadra_fig_22_large2 = {
                'ncols':2,
                'nrows':2,
                # 'figsize':(24,6),
                'figsize':(16,12),
                # 'sharex':True
                  }

## Support lines 

support_line1 = {'color':cc.grays,
                'linestyle':'-.',
                'linewidth':2.0,
                }

## Grid setup 
grid_setup = {
                "visible":"on",
                "axis":"both",
                "color":cc.gray,
                "alpha":1.0,
                }

side_text = {
    "SS":f"S.S",
    "PS":f"P.S",
             
             }

var_name_dict={
              'Uinner':{"name":r"$U^+_t$",
                    'axs':{
                        'xlabel':r'$y^+_n$',
                        'xscale':"log",
                        "xlim":[1.0,1200],
                        'ylabel':r'$U^+_t$',
                          },
                  },
                  
              'Uouter':{"name":r"$U_t/U_e$",
                    'axs':{
                        'xlabel':r'$y^+_n$',
                        'xscale':"log",
                        "xlim":[1.0,1200],
                        'ylabel':r'$U_t/U_e$',
                          },
                  },
              
              'Uouter_y':{"name":r"$U_t/U_e$",
                    'axs':{
                        'xlabel':r'$y_n$',
                        # 'xscale':"log",
                        # "xlim":[1.0,1200],
                        'ylabel':r'$U_t$',
                        'xlim':[-0.0005,0.002],
                        'ylim':[-0.15,0.05],
                          },
                  },
              
              'Uouter_norotate':{"name":r"$U$",
                    'axs':{
                        'xlabel':r'$y$',
                        # 'xscale':"log",
                        # "xlim":[1.0,1200],
                        'ylabel':r'$U$',
                        'xlim':[0.1380,0.1405],
                        'ylim':[-0.15,0.1],
                          },
                  },

              
              'Vinner'      :{'name':r"$V^+_n$",
                          "axs":{
                            'xlabel':r'$y^+_n$',
                            'xscale':"log",
                            "xlim":[1.0,1200],
                            'ylabel':r"$V^+_n$",
                          },
                        
                        },
              'Vouter'      :{'name':r"$V_n/U_e$",
                          "axs":{
                            'xlabel':r'$y^+_n$',
                            'xscale':"log",
                            "xlim":[1.0,1200],
                            'ylabel':r"$V_n/U_e$",
                          },
                        
                        },

              'uuinner'     :{ "name":r"$\overline{u^2_t}^+$",
                          "axs":{
                            'xlabel':r'$y^+_n$',
                            'xscale':"log",
                            'xlim':[0.5,800],
                            'ylabel':r"$\overline{u^2_t}^+$",
                          },
                          },
              'uuouter'     :{ "name":r"$\overline{u^2_t}/U^2_e$",
                          "axs":{
                            'xlabel':r'$y^+_n$',
                            'xscale':"log",
                            'xlim':[0.5,800],
                            'ylabel':r"$\overline{u^2_t}/U^2_e$",
                          },
                          },

              'vvinner'     :{"name":r"$\overline{v^2_n}^+$",
                          "axs":{
                            'xlabel':r'$y^+_n$',
                            'xscale':"log",
                            'ylabel':r"$\overline{v^2_n}^+$",
                          }
                          },
              'vvouter'     :{"name":r"$\overline{v^2_n}/U^2_e$",
                          "axs":{
                            'xlabel':r'$y^+_n$',
                            'xscale':"log",
                            'ylabel':r"$\overline{v^2_n}/U^2_e$",
                          }
                          },
              'wwinner'     :{"name":r"$\overline{w^2_n}^+$",
                          "axs":{
                            'xlabel':r'$y^+_n$',
                            'xscale':"log",
                            'ylabel':r"$\overline{w^2_n}^+$",
                          }
                          },
              'wwouter'     :{"name":r"$\overline{w^2_n}/U^2_e$",
                          "axs":{
                            'xlabel':r'$y^+_n$',
                            'xscale':"log",
                            'ylabel':r"$\overline{w^2_n}/U^2_e$",
                          }
                          },

              'uvinner'     :{"name":   r"$-\overline{u_tv_n}^+$",
                          "axs":{
                            'xlabel':r'$y^+_n$',
                            'xscale':"log",
                            'ylabel':r"$-\overline{u_tv_n}^+$",
                          }
                          },
              'uvouter'     :{"name":   r"$-\overline{u_tv_n}/U^2_e$",
                          "axs":{
                            'xlabel':r'$y^+_n$',
                            'xscale':"log",
                            'ylabel':r"$-\overline{u_tv_n}/U^2_e$",
                          }
                          },

              'uiujinner'     :{"name":   r"$\overline{u_iu_j}^+$",
                          "axs":{
                            'xlabel':r'$y^+_n$',
                            'xscale':"log",
                            'xlim':[0.5,500],
                            'ylabel':
                                    r"$\overline{u_t^2}^+$" + ", " + \
                                    r"$\overline{v_n^2}^+$" + ", " + \
                                    r"$\overline{w^2}^+$" + ", " +\
                                    r"$\overline{u_tv_n}^+$",
                          }
                          },
              
              'uiujouter'     :{"name":   r"$\overline{u_iu_j}/U^2_e$",
                          "axs":{
                            'xlabel':r'$y^+_n$',
                            'xscale':"log",
                            'xlim':[0.5,800],
                            'ylabel':
                                    r"$\overline{u_t^2}/U^2_e$" + ", " + \
                                    r"$\overline{v_n^2}/U^2_e$" + ", " + \
                                    r"$\overline{w^2}/U^2_e$" + ", " +\
                                    r"$\overline{u_tv_n}/U^2_e$",
                          }
                          },
              
              
              'cf'     :{"name":r"$c_f$",
                          "axs":{
                            'xlabel':r'$x/c$',
                            'xlim':[0.11,0.99],
                            'ylabel':r'$c_f$',
                            'ylim':[-0.2e-2,2.8e-2]
                          }
                          },
              'cp'     :{"name":r"$c_p$",
                          "axs":{
                            'xlabel':r'$x/c$',
                            # 'ylabel':r'$c_p$',
                            'ylabel':r'$- c_p$',
                            # 'ylim':[-4,1.1],
                            'ylim':[-1.1,4],
                            
                          }
                          },
              'beta'   :{"name":r"$\beta$",
                          "axs":{
                            'xlabel':r'$x/c$',
                            # "xlim":[0.11,0.95],
                            'ylabel':r'$\beta$',
                            'yscale':"symlog",
                          }
                          },
              'Retau'  :{"name":r"$Re_{\tau}$",
                          "axs":{
                            'xlabel':r'$x/c$',
                            'ylabel':r'$Re_{\tau}$',
                            'yscale':'log',
                            # "xlim":[0.11,0.95],
                          }
                          },
              'Retheta':{"name":            r"$Re_{\theta}$",
                          "axs":{
                            'xlabel':r'$x/c$',
                            # "xlim":[0.11,0.95],
                            'ylabel':r'$Re_{\theta}$',
                            'yscale':'log',
                          }
                          },
              
              'H12':{"name":            r"$H_{12}$",
                          "axs":{
                            'xlabel':r'$x/c$',
                            # "xlim":[0.11,0.95],
                            'ylabel':r'$H_{12}$',
                          }
                          },
              
              'Ue':{"name":            r"$U_e$",
                          "axs":{
                            'xlabel':r'$x/c$',
                            # "xlim":[0.11,0.95],
                            'ylabel':r'$U_e$',
                          }
                          },
              
              'd99':{"name":            r"$\delta_{99}$",
                          "axs":{
                            'xlabel':r'$x/c$',
                            # "xlim":[0.11,0.95],
                            'ylabel':r'$\delta_{99}$',
                            'yscale':'log'
                          }
                          },
              

              'L':{"name": r"$\Gamma_l$",
                          "axs":{
                            'xlabel':r"$x/c$",
                            'ylabel':r"$\Gamma_l = \Gamma_{l,f} + \Gamma_{l,p}$",
                            # 'yscale':'symlog',
                          },
                          },
              
              'L_tauw':{"name": r"$\Gamma_{l,f}$",
                          "axs":{
                            'xlabel':r"$x/c$",
                            'ylabel':r"$f'_{l,x}$",
                            # 'yscale':'symlog',
                          },
                          },
              
              'L_p':{"name": r"$\Gamma_{l,p}$",
                          "axs":{
                            'xlabel':r"$x/c$",
                            'ylabel':r"$f'_{l,y}$",
                            # 'yscale':'log',
                          },
                          },

              'D':{"name": r"$\Gamma_d$",
                          "axs":{
                            'xlabel':r"$x/c$",
                            'ylabel':r"$\Gamma_d=\Gamma_{d,f}+\Gamma_{d,p}$",
                          },
                          },
              
              'D_tauw':{"name": r"$\Gamma_{d,f}$",
                          "axs":{
                            'xlabel':r"$x/c$",
                            'ylabel':r"$f'_{d,x}$",
                          },
                          },
              
              'D_p':{"name": r"$\Gamma_{d,p}$",
                          "axs":{
                            'xlabel':r"$x/c$",
                            'ylabel':r"$f'_{d,y}$",
                          },
                          },
              

              "psd":{'name': "Time-PSD",
                    
                    'axs':{
                      "xlabel":r"$fc/U_{\infty}$",
                      "xscale":'log',
                      "yscale":'log',
                      # "xlim":[1.5,1.5e2],
                      "xlim":[1.2,3e2],
                      "ylim":[1e-4,5e4],
                      # "xlim":[1e0,5e1],
                      "ylabel":'PSD'
                    }
                    },

              }


def name_file(fldr,usrname,aoa,rec,side):
  name = f'Re{rec}k_AoA{aoa}'
  if side =='SS' or side =='PS':
    return fldr + usrname + name + "_" + side  
  elif side=='aero':
    return fldr + usrname + name + "_" + side
  else:
    return fldr + usrname + name  


################################################
# Functions for Visualizaing Single Pannel 
###############################################

def plot_Vel(d,fig,axs,x_c,var,
              var_Name,
              style,grid_setup,
              scale='inner',
              interval=30):
  xc = d['xc'].squeeze()
  idx = np.where(xc>=x_c)[0][0]
  
  if scale == 'inner':
    utau  = d['utau'][0,idx]
    lstar = d['lstar'][0,idx]
    axs.plot(d['yn'][idx,:]/lstar,d[var][idx,:]/utau,
            **style,
            markevery=interval)
  
  elif scale == 'outer':
    Ue  = d['Ue'][0,idx]
    lstar = d['lstar'][0,idx]
    axs.plot(d['yn'][idx,:]/lstar,d[var][idx,:]/Ue,
            **style,
            markevery=interval)
  
  elif scale == 'outer_y':
    Ue  = d['Ue'][0,idx]
    lstar = d['lstar'][0,idx]
    lstar = d['d99'][0,idx]
    print(f"Ue = {Ue}, d99={lstar}")
    axs.plot(d['yn'][idx,:],d[var][idx,:],
            **style,
            markevery=interval)
  
  elif scale == 'outer_norotate':
    axs.plot(d['y'][idx,:],d[var][idx,:],
            **style,
            markevery=interval)
  

  
    
  axs.grid(**grid_setup)
  return fig,axs


def plot_ReynoldStress(d,fig,axs,x_c,var,
              var_Name,
              style,grid_setup,
              scale='inner',
              interval=30):
  xc = d['xc'].squeeze()
  idx = np.where(xc>=x_c)[0][0]
  
  if scale == 'inner':
    utau  = d['utau'][0,idx]
    lstar = d['lstar'][0,idx]
    axs.plot(d['yn'][idx,:]/lstar,d[var][idx,:]/utau**2,
             **style,
            markevery = interval,
            )
  
  elif scale == 'outer':
    Ue  = d['Ue'][0,idx]
    lstar = d['lstar'][0,idx]
    axs.plot(d['yn'][idx,:]/lstar,d[var][idx,:]/Ue**2,
             **style,
            markevery = interval,
            )
  axs.grid(**grid_setup)
  return fig,axs

def plot_integral_quantities(d,fig,axs,
                            x_start,x_end,var,var_Name,
                            style,with_set=True,interval=5):
  indx = np.where((d['xc'][0,:]>x_start) & (d['xc'][0,:] < x_end))[0]
  axs.plot(d['xc'][0,indx],d[var][0,indx],**style,
          markevery = interval
          )
  if with_set:
    axs.set(**{'xlabel':'x/c','ylabel':var_Name})
  return fig,axs


def plot_FFT(d,fig,axs,
              style,
              text_loc=(0.9,0.96)
              ):
  
  freq = np.squeeze(d['freq'])
  psd  = np.squeeze(d['psd'])

  axs.plot(freq,psd,
          # linestyle=style['linestyle'],
          linestyle="-",
          lw=style['lw'],
          c=style['c'],

          )
  
  psd  =  psd[np.where((freq>1.6)&(freq<80))]
  freq = freq[np.where((freq>1.6)&(freq<80))]
  
  axs.plot(freq[np.argmax(psd)],psd.max(),"*",
          markersize=25,
          c=style['c'],
          # fillstyle='none',
          # linewidth=2,
          )
  
  xmax = freq[np.argmax(psd)]
  ymax = psd.max()
  text = r"$fc/U_{\infty}$ = "+"{:.1f}".format(xmax)
  axs = annot_max(xmax,ymax,text,text_loc=text_loc,c=style['c'],ax=axs)

  return fig,axs


def annot_max(xmax,ymax,text,c,text_loc, ax=None,):
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec=c, lw=0.9)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=75",color=c)
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops,
              bbox=bbox_props, ha="right", va="top",fontsize=18)
    ax.annotate(text, xy=(xmax, ymax), 
                xytext=text_loc,
                color=c, 
                **kw)

    return ax


def plot_1DPSD(d,fig,axs,
              style,
              levels,
              text_loc=(0.9,0.96),
              scale='inner'
              ):
  lmd = d[f'lmd_{scale}']
  yn  = d[f'yn_{scale}']
  puu = d[f'puu']
  
  axs.contour(
                  lmd,
                  yn,
                  puu,
                  colors=style['c'],
                  levels=levels*np.max(d['puu'],(0,1))
              )

  ind_  = np.unravel_index(np.argmax(np.abs(puu)),
                          shape=puu.shape)
  xx_max = lmd[ind_[1]]
  yy_max = yn[ind_[0]]
  print(f"energy peak: LambdaZ = {xx_max}; y_n = {yy_max}")
  axs.plot(xx_max,yy_max,"*",
          markersize=25,
          c=style['c'],
          zorder=30,
          fillstyle='full'
          )
  
  puu_max = np.max(puu)
  text = "{:.2e}".format(puu_max)
  # axs = annot_max(xx_max,yy_max,
  #                 text=text,
  #                 text_loc=text_loc,
  #                 c=style['c'],ax=axs)

  return fig,axs

