import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.ticker import LogLocator, NullFormatter
from    matplotlib.lines import Line2D
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
    plt.rc("xtick",labelsize = 18)
    plt.rc("ytick",labelsize = 18)
    return 



# Setup for output 
figkw  ={
        'bbox_inches':'tight',
        "dpi":300
        }

## Ticks formats
formatter2 = ticker.ScalarFormatter(useMathText=True)
formatter2.set_powerlimits([-2,5])

formatter3 = ticker.ScalarFormatter(useMathText=True,
                                    useLocale=True)
formatter3.set_powerlimits([-2,4])

## Syntax for set log grid 
locmin = LogLocator(base=10,subs=np.arange(0,10), numticks=10)

title_setup ={  
                'loc':'left',
                'pad':22,
                } 

single_fig_cfg = {
                'ncols':1,
                'nrows':1,
                'figsize':(8,8)
                  }

single_fig_larger = {
                'ncols':1,
                'nrows':1,
                'figsize':(12,6)
                  }

double_fig_larger = {
                'ncols':2,
                'nrows':1,
                'figsize':(12,8),
                # 'sharey':True
                  }

quadra_fig_larger = {
                'ncols':4,
                'nrows':1,
                'figsize':(26,6),
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
                        "xlim":[1.0,2000],
                        'ylabel':r'$U^+_t$',
                          },
                  },
                  
              'Uouter':{"name":r"$U_t/U_e$",
                    'axs':{
                        'xlabel':r'$y^+_n$',
                        'xscale':"log",
                        "xlim":[1.0,2000],
                        'ylabel':r'$U_t/U_e$',
                          },
                  },

              
              'Vinner'      :{'name':r"$V^+_n$",
                          "axs":{
                            'xlabel':r'$y^+_n$',
                            'xscale':"log",
                            "xlim":[1.0,2000],
                            'ylabel':r"$V^+_n$",
                          },
                        
                        },
              'Vouter'      :{'name':r"$V_n/U_e$",
                          "axs":{
                            'xlabel':r'$y^+_n$',
                            'xscale':"log",
                            "xlim":[1.0,2000],
                            'ylabel':r"$V_n/U_e$",
                          },
                        
                        },

              'uu'     :{ "name":r"$\overline{u^2_t}^+$",
                          "axs":{
                            'xlabel':r'$y^+_n$',
                            'xscale':"log",
                            'ylabel':r"$\overline{u^2_t}^+$",
                          },
                          },

              'vv'     :{"name":r"$\overline{v^2_n}^+$",
                          "axs":{
                            'xlabel':r'$y^+_n$',
                            'xscale':"log",
                            'ylabel':r"$\overline{v^2_n}^+$",
                          }
                          },
              'uv'     :{"name":   r"$-\overline{u_tv_n}^+$",
                          "axs":{
                            'xlabel':r'$y^+_n$',
                            'xscale':"log",
                            'ylabel':r"$-\overline{u_tv_n}^+$",
                          }
                          },

              'cf'     :{"name":r"$c_f$",
                          "axs":{
                            'xlabel':r'$x/c$',
                            'xlim':[0.11,0.95],
                            'ylabel':r'$c_f$',
                          }
                          },
              'cp'     :{"name":r"$c_p$",
                          "axs":{
                            'xlabel':r'$x/c$',
                            'ylabel':r'$c_p$',
                          }
                          },
              'beta'   :{"name":r"$\beta$",
                          "axs":{
                            'xlabel':r'$x/c$',
                            "xlim":[0.11,0.95],
                            'ylabel':r'$\beta$',
                            'yscale':"symlog",
                          }
                          },
              'Retau'  :{"name":r"$Re_{\tau}$",
                          "axs":{
                            'xlabel':r'$x/c$',
                            'ylabel':r'$Re_{\tau}$',
                          }
                          },
              'Retheta':{"name":            r"$Re_{\theta}$",
                          "axs":{
                            'xlabel':r'$x/c$',
                            'ylabel':r'$Re_{\theta}$',
                          }
                          },
              
              'H12':{"name":            r"$H_{12}$",
                          "axs":{
                            'xlabel':r'$x/c$',
                            'ylabel':r'$H_{12}$',
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

def plot_Vel(d,fig,axs,x_c,var,
              var_Name,
              style,grid_setup,
              scale='inner',
              interval=20):
  xc = d['xc'].squeeze()
  idx = np.where(xc>=x_c)[0][0]
  
  if scale == 'inner':
    utau  = d['utau'][0,idx]
    lstar = d['lstar'][0,idx]
    axs.plot(d['yn'][idx,::interval]/lstar,d[var][idx,::interval]/utau,**style)
  
  elif scale == 'outer':
    Ue  = d['Ue'][0,idx]
    lstar = d['lstar'][0,idx]
    axs.plot(d['yn'][idx,::interval]/lstar,d[var][idx,::interval]/Ue,**style)
  
  
    
  axs.grid(**grid_setup)
  return fig,axs

def plot_Reynolds_Stress(d,fig,axs,x_c,var,var_Name,style,grid_setup):
  xc = d['xc'].squeeze()
  idx = np.where(xc>=x_c)[0][0]
  # print(f"x/c={x_c};idx={idx};x/c = {xc[idx]}")
  utau  = d['utau'][0,idx]
  lstar = d['lstar'][0,idx]
  axs.plot(d['yn'][idx,:]/lstar,np.abs(d[var][idx,:]/utau**2),**style)
  axs.set(**{"xlabel":r"$y^+_{n}$",
                    'xlim':[3e-1,500],
                    "xscale":'log',
                    "ylabel":var_Name,
                    'title':r"$x/c = $" + f'{x_c}'})
  
  axs.xaxis.set_minor_locator(locmin)
  axs.xaxis.set_major_locator(locmin)
  axs.xaxis.set_minor_formatter(NullFormatter())
  axs.grid(**grid_setup)
  return fig,axs

def plot_integral_quantities(d,fig,axs,x_start,x_end,var,var_Name,style,with_set=True):
  indx = np.where((d['xc'][0,:]>x_start) & (d['xc'][0,:] < x_end))[0]
  axs.plot(d['xc'][0,indx],d[var][0,indx],**style)
  if with_set:
    axs.set(**{'xlabel':'x/c','ylabel':var_Name})
  return fig,axs

