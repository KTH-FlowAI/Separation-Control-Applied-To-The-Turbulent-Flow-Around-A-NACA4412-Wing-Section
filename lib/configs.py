"""
A dictionary of all the cases here 
The order should be sorted by the control range and intensity 
The periodic and uniform cases are separated here. 
@yuningw
"""

"""
Rules: 
Color  === CONTROL INTENSITY / Freq
MARKER === CONTROL REGION 
LINE   === CONTROL METHOD
"""

from lib.plot import cc

lw1     = 3.0 
lw2     = 2.0 
mksize1 = 7.5 
ls0     = ':'
ls1     = '--'
ls2     = '-'
ls3     = ':'
mktype1 = 'o'
mktype2 = 'x'
mktype21 = 'X'
mktype3 = 's'
mktype4 = 'D'
mktype5 = 'v'
mktype6 = '^'

cs  = [cc.deepgreen,cc.blue,cc.purple,cc.yellow,cc.red,cc.pink]
ms = ['o','D','v','s','^']




##################### Config for Final data  ##############
data=     {
        'reference':{
                    'fileName':'NOCTRL/',
                    'style':{
                            'lw':lw1,
                            'c':cc.black,
                            'linestyle':"-",
                            'marker':None,
                            'markersize':mksize1,
                            'fillstyle':'none',
                        },
                        'label':'Ref',
                        'config':{
                        'region':[(0.0,0.0),(0,0)],
                        'intensity':[0.0,0.0],
                        "freq":[0.0,0.0],
                        'side':[False,False], # (S.S,P.S), 1==Yes, 0==No
                },
                        "d99":0.0477,
                        },
        
        'control':{
                    'fileName':'CTRL_025-086XC_0.25%Uinf_SS-SUCTION_PS-BLOWING/',
                    'style':{
                            'lw':lw2,
                            'c':cc.blue,
                            'linestyle':ls1,
                            'marker':mktype2,
                            'markersize':mksize1,
                            'fillstyle':'none',
                            },
                    'label':'Case A',
                    'config':{
                        'region':[(0.25,0.86),(0.25,0.86)],
                        'intensity':[-0.25/100,0.25/100],  
                        "freq":[0.0,0.0],
                        'side':[True,True], # (S.S,P.S), 1==Yes, 0==No
                              },
                        "d99":0.0438,
                    },
        
        'control1':{
                    'fileName':'CTRL_025-086XC_0.50%Uinf_SS-SUCTION_PS-BLOWING/',
                    'style':{
                            'lw':lw2,
                            'c':cc.yellow,
                            'linestyle':ls2,
                            'marker':mktype3,
                            'markersize':mksize1,
                            'fillstyle':'none',
                            },
                    'label':'Case B',
                    'config':{
                        'region':[(0.25,0.86),(0.25,0.86)],
                        'intensity':[-0.5/100,0.5/100],  
                        "freq":[0.0,0.0],
                        'side':[True,True], # (S.S,P.S), 1==Yes, 0==No
                              },
                        "d99":0.0493,
                    },

        'control2':{
                    'fileName':'CTRL_025-086XC_1.00%Uinf_SS-SUCTION_PS-BLOWING/',
                    'style':{
                            'lw':lw2,
                            'c':cc.red,
                            'linestyle':ls3,
                            'marker':mktype4,
                            'markersize':mksize1,
                            'fillstyle':'none',
                            },
                    'label':'Case C',
                    'config':{
                        'region':[(0.25,0.86),(0.25,0.86)],
                        'intensity':[-1.0/100,1.0/100],  
                        "freq":[0.0,0.0],
                        'side':[True,True], # (S.S,P.S), 1==Yes, 0==No
                              },
                "d99":0.1080,
                    },
        'control3':{
                    'fileName':'CTRL_025-086XC_0.25%Uinf_SS-SUCTION/',
                    'style':{
                            'lw':lw2,
                            'c':cc.green,
                            'linestyle':ls1,
                            'marker':mktype5,
                            'markersize':mksize1,
                            'fillstyle':'none',
                            },
                    'label':'Case D',
                    'config':{
                        'region':[(0.25,0.86),(0.0,0.0)],
                        'intensity':[-0.25/100,0.0],  
                        "freq":[0.0,0.0],
                        'side':[True,False], # (S.S,P.S), 1==Yes, 0==No
                              },

                    },

        'control4':{
                    'fileName':'CTRL_025-086XC_0.25%Uinf_PS-BLOWING/',
                    'style':{
                            'lw':lw2,
                            'c':cc.deeppurple,
                            'linestyle':ls1,
                            'marker':mktype6,
                            'markersize':mksize1,
                            'fillstyle':'none',
                            },
                    'label':'Case E',
                    'config':{
                        'region':[(0.0,0.0),(0.25,0.86)],
                        'intensity':[0.0,0.25/100],  
                        "freq":[0.0,0.0],
                        'side':[False,True], # (S.S,P.S), 1==Yes, 0==No
                              },

                    },
      }

data_clcd=     {
        'reference':{
                    'fileName':'NOCTRL/',
                    'style':{
                            'lw':lw1,
                            'c':cc.black,
                            'linestyle':"-",
                            'marker':mktype1,
                        #     'markersize':6.0,
                        #     'fillstyle':'none',
                            },
                    'label':'Ref',
                    'config':{
                        'region':[(0.0,0.0),(0,0)],
                        'intensity':[0.0,0.0],
                        "freq":[0.0,0.0],
                        'side':[False,False], # (S.S,P.S), 1==Yes, 0==No
                },
                    },
        
        'control':{
                    'fileName':'CTRL_025-086XC_0.25%Uinf_SS-SUCTION_PS-BLOWING/',
                    'style':{
                        'lw':lw2,
                        'c':cc.blue,
                        'linestyle':ls1,
                        'marker':mktype21,
                        'markersize':mksize1,
                        'fillstyle':'none',
                        },
                    'label':'Case A',
                    'config':{
                        'region':[(0.25,0.86),(0.25,0.86)],
                        'intensity':[-0.25/100,0.25/100],  
                        "freq":[0.0,0.0],
                        'side':[True,True], # (S.S,P.S), 1==Yes, 0==No
                              },
                    },
        
        'control1':{
                    'fileName':'CTRL_025-086XC_0.50%Uinf_SS-SUCTION_PS-BLOWING/',
                    'style':{
                            'lw':lw2,
                            'c':cc.yellow,
                            'linestyle':ls2,
                            'marker':mktype3,
                            'markersize':mksize1,
                            'fillstyle':'none',
                            },
                    'label':'Case B',
                    'config':{
                        'region':[(0.25,0.86),(0.25,0.86)],
                        'intensity':[-0.5/100,0.5/100],  
                        "freq":[0.0,0.0],
                        'side':[True,True], # (S.S,P.S), 1==Yes, 0==No
                              },

                    },

        'control2':{
                    'fileName':'CTRL_025-086XC_1.00%Uinf_SS-SUCTION_PS-BLOWING/',
                    'style':{
                            'lw':lw2,
                            'c':cc.red,
                            'linestyle':ls3,
                            'marker':mktype4,
                            'markersize':mksize1,
                            'fillstyle':'none',
                            },
                    'label':'Case C',
                    'config':{
                        'region':[(0.25,0.86),(0.25,0.86)],
                        'intensity':[-1.0/100,1.0/100],  
                        "freq":[0.0,0.0],
                        'side':[True,True], # (S.S,P.S), 1==Yes, 0==No
                              },

                    },
        
        'control3':{
                    'fileName':'CTRL_025-086XC_0.25%Uinf_SS-SUCTION/',
                    'style':{
                            'lw':lw2,
                            'c':cc.green,
                            'linestyle':ls3,
                            'marker':mktype5,
                            'markersize':mksize1,
                            'fillstyle':'none',
                            },
                    'label':'Case D',
                    'config':{
                        'region':[(0.25,0.86),(0.0,0.0)],
                        'intensity':[-0.25/100,0.0],  
                        "freq":[0.0,0.0],
                        'side':[True,False], # (S.S,P.S), 1==Yes, 0==No
                              },

                    },

        'control4':{
                    'fileName':'CTRL_025-086XC_0.25%Uinf_PS-BLOWING/',
                    'style':{
                            'lw':lw2,
                            'c':cc.deeppurple,
                            'linestyle':ls3,
                            'marker':mktype6,
                            'markersize':mksize1,
                            'fillstyle':'none',
                            },
                    'label':'Case E',
                    'config':{
                        'region':[(0.0,0.0),(0.25,0.86)],
                        'intensity':[0.0,0.25/100],  
                        "freq":[0.0,0.0],
                        'side':[False,True], # (S.S,P.S), 1==Yes, 0==No
                              },

                    },

      }


