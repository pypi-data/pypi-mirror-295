"""
Created on Fri Dec 15 15:24:42 2023

@author: BernardoCastro
"""

import numpy as np
import sys
import csv
import networkx as nx
import pandas as pd
from scipy import stats as st
from .PyFlow_ACDC_Results import*
from .PyFlow_ACDC_TS import *
from .PyFlow_ACDC_MarketCoeff import*

try:
    import plotly
    from .PyFlow_ACDC_GraphsPlot import*
    pyomo_imp= True
    
except ImportError:    
    pyomo_imp= False

"""
"""


def find_value_from_cdf(cdf, x):
    for i in range(len(cdf)):
        if cdf[i] >= x:
            return i
    return None


def pol2cart(r, theta):
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    return x, y


def pol2cartz(r, theta):
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    z = x+1j*y
    return z


def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return rho, theta


def cartz2pol(z):
    r = np.abs(z)
    theta = np.angle(z)
    return r, theta


def Converter_parameters(S_base, kV_base, T_R_Ohm, T_X_mH, PR_R_Ohm, PR_X_mH, Filter_uF, f=50):

    Z_base = kV_base**2/S_base  # kv^2/MVA
    Y_base = 1/Z_base

    F = Filter_uF*10**(-6)
    PR_X_H = PR_X_mH/1000
    T_X_H = T_X_mH/1000

    B = f*F*np.pi
    T_X = f*T_X_H*np.pi
    PR_X = f*PR_X_H*np.pi

    T_R_pu = T_R_Ohm/Z_base
    T_X_pu = T_X/Z_base
    PR_R_pu = PR_R_Ohm/Z_base
    PR_X_pu = PR_X/Z_base
    Filter_pu = B/Y_base

    return [T_R_pu, T_X_pu, PR_R_pu, PR_X_pu, Filter_pu]


def Cable_parameters(S_base, R, L_mH, C_uF, G_uS, A_rating, kV_base, km, N_cables=1, f=50):

    Z_base = kV_base**2/S_base  # kv^2/MVA
    Y_base = 1/Z_base

    if L_mH == 0:
        MVA_rating = N_cables*A_rating*kV_base/(1000)
    else:
        MVA_rating = N_cables*A_rating*kV_base*np.sqrt(3)/(1000)

    C = C_uF*(10**(-6))
    L = L_mH/1000
    G = G_uS*(10**(-6))

    R_AC = R*km

    B = 2*f*C*np.pi*km
    X = 2*f*L*np.pi*km

    Z = R_AC+X*1j
    Y = G+B*1j

    # Zc=np.sqrt(Z/Y)
    # theta_Z=np.sqrt(Z*Y)

    Z_pi = Z
    Y_pi = Y

    # Z_pi=Zc*np.sinh(theta_Z)
    # Y_pi = 2*np.tanh(theta_Z/2)/Zc

    R_1 = np.real(Z_pi)
    X_1 = np.imag(Z_pi)
    G_1 = np.real(Y_pi)
    B_1 = np.imag(Y_pi)

    Req = R_1/N_cables
    Xeq = X_1/N_cables
    Geq = G_1*N_cables
    Beq = B_1*N_cables

    Rpu = Req/Z_base
    Xpu = Xeq/Z_base
    Gpu = Geq/Y_base
    Bpu = Beq/Y_base

    return [Rpu, Xpu, Gpu, Bpu, MVA_rating]

def reset_all_class():
    Node_AC.reset_class()
    Node_DC.reset_class()
    Line_AC.reset_class()
    Line_DC.reset_class()
    AC_DC_converter.reset_class()
    DC_DC_converter.reset_class()
    TS_AC.reset_class()
    
def Create_grid_from_data(S_base, AC_node_data=None, AC_line_data=None, DC_node_data=None, DC_line_data=None, Converter_data=None, DCDC_conv=None, data_in_pu=True):
    
    reset_all_class()
    
    if data_in_pu == True:
        [G, res] = Create_grid_from_data_pu(
            S_base, AC_node_data, AC_line_data, DC_node_data, DC_line_data, Converter_data, DCDC_conv)
    else:
        [G, res] = Create_grid_from_data_calc(
            S_base, AC_node_data, AC_line_data, DC_node_data, DC_line_data, Converter_data, DCDC_conv)

    return [G, res]


def Create_grid_from_data_calc(S_base, AC_node_data, AC_line_data, DC_node_data, DC_line_data, Converter_data, DCDC_conv):
        
   

    if AC_node_data is None:
        AC_nodes_list = None
        AC_lines_list = None
    else:
        "AC nodes data sorting"
        AC_node_data = AC_node_data.set_index('Node_id')
        AC_nodes = {}
        for index, row in AC_node_data.iterrows():
            var_name = index
            element_type = AC_node_data.at[index, 'type']

            Voltage_0 = AC_node_data.at[index, 'Voltage_0']
            theta_0 = AC_node_data.at[index, 'theta_0']
            Power_Gained = AC_node_data.at[index, 'Power_Gained']
            Reactive_Gained = AC_node_data.at[index, 'Reactive_Gained']
            Power_load = AC_node_data.at[index, 'Power_load']
            Reactive_load = AC_node_data.at[index, 'Reactive_load']
            if 'Umin' in AC_node_data.columns:
                Umin=AC_node_data.at[index, 'Umin']
            else:
                Umin=0.9
            if 'Umax' in AC_node_data.columns:
                Umax=AC_node_data.at[index, 'Umax']
            else:
                Umax=1.1
            if 'x_coord' in AC_node_data.columns:
                x_coord=AC_node_data.at[index, 'x_coord']
            else:
                x_coord=None
            if 'y_coord' in AC_node_data.columns:
                y_coord=AC_node_data.at[index, 'y_coord']
            else:
                y_coord=None    
                
            # Q_max          =AC_node_data.at[index,'Q_max']
            # Q_min          =AC_node_data.at[index,'Q_min']

            Power_Gained = Power_Gained/S_base
            Reactive_Gained = Reactive_Gained/S_base
            Power_load = Power_load/S_base
            Reactive_load = Reactive_load/S_base

            AC_nodes[var_name] = Node_AC(element_type, Voltage_0, theta_0, Power_Gained,
                                         Reactive_Gained, Power_load, Reactive_load, name=str(var_name),Umin=Umin,Umax=Umax,x_coord=x_coord,y_coord=y_coord)
        AC_nodes_list = list(AC_nodes.values())

        AC_line_data = AC_line_data.set_index('Line_id')
        AC_lines = {}
        for index, row in AC_line_data.iterrows():
            var_name = index

            fromNode = AC_line_data.at[index, 'fromNode']
            toNode = AC_line_data.at[index, 'toNode']
            R = AC_line_data.at[index, 'R_Ohm_km']
            L_mH = AC_line_data.at[index, 'L_mH_km']
            C_uF = AC_line_data.at[index, 'C_uF_km']
            G_uS = AC_line_data.at[index, 'G_uS_km']
            A_rating = AC_line_data.at[index, 'A_rating']
            kV_base = AC_line_data.at[index, 'kV_base']
            km = AC_line_data.at[index, 'Length_km']
            N_cables = AC_line_data.at[index, 'N_cables']
            if 'm' in AC_line_data.columns:
                m=AC_line_data.at[index, 'm']
            else:
                m=1
            if 'shift' in AC_line_data.columns:
                shift=np.radians(AC_line_data.at[index, 'shift'])
            else:
                shift=0
                
            [Resistance, Reactance, Conductance, Susceptance, MVA_rating] = Cable_parameters(S_base, R, L_mH, C_uF, G_uS, A_rating, kV_base, km,N_cables=N_cables)
            
            
            
            AC_lines[var_name] = Line_AC(AC_nodes[fromNode], AC_nodes[toNode], Resistance,
                                         Reactance, Conductance, Susceptance, MVA_rating, kV_base,m,shift,name=str(var_name))
        AC_lines_list = list(AC_lines.values())

    if DC_node_data is None:

        DC_nodes_list = None
        DC_lines_list = None

    else:
        DC_node_data = DC_node_data.set_index('Node_id')

        "DC nodes data sorting"
        DC_nodes = {}
        for index, row in DC_node_data.iterrows():

            var_name = index
            node_type = DC_node_data.at[index, 'type']

            Voltage_0 = DC_node_data.at[index, 'Voltage_0']
            Power_Gained = DC_node_data.at[index, 'Power_Gained']
            Power_load = DC_node_data.at[index, 'Power_load']

            Power_Gained = Power_Gained/S_base
            Power_load = Power_load/S_base
            
            if 'Umin' in DC_node_data.columns:
                Umin=DC_node_data.at[index, 'Umin']
            else:
                Umin=0.95
            if 'Umax' in DC_node_data.columns:
                Umax=DC_node_data.at[index, 'Umax']
            else:
                Umax=1.05
            if 'x_coord' in DC_node_data.columns:
                x_coord=DC_node_data.at[index, 'x_coord']
            else:
                x_coord=None
            if 'y_coord' in DC_node_data.columns:
                y_coord=DC_node_data.at[index, 'y_coord']
            else:
                y_coord=None  

            DC_nodes[var_name] = Node_DC(node_type, Voltage_0, Power_Gained, Power_load, name=str(var_name),Umin=Umin,Umax=Umax,x_coord=x_coord,y_coord=y_coord)
        DC_nodes_list = list(DC_nodes.values())

        DC_line_data = DC_line_data.set_index('Line_id')
        DC_lines = {}
        for index, row in DC_line_data.iterrows():
            var_name = index

            fromNode = DC_line_data.at[index, 'fromNode']
            toNode = DC_line_data.at[index, 'toNode']
            R = DC_line_data.at[index, 'R_Ohm_km']
            A_rating = DC_line_data.at[index, 'A_rating']
            kV_base = DC_line_data.at[index, 'kV_base']
            pol = DC_line_data.at[index, 'Mono_Bi_polar']
            km = DC_line_data.at[index, 'Length_km']
            N_cables = DC_line_data.at[index, 'N_cables']
            L_mH = 0
            C_uF = 0
            G_uS = 0
            [Resistance, Reactance, Conductance, Susceptance, MW_rating] = Cable_parameters(S_base, R, L_mH, C_uF, G_uS, A_rating, kV_base, km, N_cables=N_cables)
            
            if pol == 'm':
                pol_val = 1
            elif pol == 'b' or pol == 'sm':
                pol_val = 2
            else:
                pol_val = 1
            MW_rating=MW_rating*pol_val
            
            DC_lines[var_name] = Line_DC(
                DC_nodes[fromNode], DC_nodes[toNode], Resistance, MW_rating, kV_base, pol, name=str(var_name))
        DC_lines_list = list(DC_lines.values())

    if Converter_data is None:
        Convertor_list = None
    else:
        Converter_data = Converter_data.set_index('Conv_id')
        "Convertor data sorting"
        Converters = {}
        for index, row in Converter_data.iterrows():
            var_name         = index
            AC_type          = Converter_data.at[index, 'AC_type']       if 'AC_type'        in Converter_data.columns else 'PV'
            DC_type          = Converter_data.at[index, 'DC_type']       if 'DC_type'        in Converter_data.columns else 'Droop'
            AC_node          = Converter_data.at[index, 'AC_node']      
            DC_node          = Converter_data.at[index, 'DC_node']       
            P_AC             = Converter_data.at[index, 'P_MW_AC']       if 'P_MW_AC'        in Converter_data.columns else 0
            Q_AC             = Converter_data.at[index, 'Q_AC']          if 'Q_AC'           in Converter_data.columns else 0
            P_DC             = Converter_data.at[index, 'P_MW_DC']       if 'P_MW_DC'        in Converter_data.columns else 0
            Transformer_R    = Converter_data.at[index, 'T_R_Ohm']       if 'T_R_Ohm'        in Converter_data.columns else 0
            Transformer_X    = Converter_data.at[index, 'T_X_mH']        if 'T_X_mH'         in Converter_data.columns else 0
            Phase_Reactor_R  = Converter_data.at[index, 'PR_R_Ohm']      
            Phase_Reactor_X  = Converter_data.at[index, 'PR_X_mH']       
            Filter           = Converter_data.at[index, 'Filter_uF']     if 'Filter_uF'      in Converter_data.columns else 0
            Droop            = Converter_data.at[index, 'Droop']         if 'Droop'          in Converter_data.columns else 0
            kV_base          = Converter_data.at[index, 'AC_kV_base']    
            MVA_rating       = Converter_data.at[index, 'MVA_rating']    if 'MVA_rating'     in Converter_data.columns else S_base*1.05
            Ucmin           = Converter_data.at[index, 'Ucmin']          if 'Ucmin'          in Converter_data.columns else 0.85
            Ucmax           = Converter_data.at[index, 'Ucmax']          if 'Ucmax'          in Converter_data.columns else 1.2
            n               = Converter_data.at[index, 'Nconverter']     if 'Nconverter'     in Converter_data.columns else 1
            pol             = Converter_data.at[index, 'Nconverter']     if 'Nconverter'     in Converter_data.columns else 1

            [T_R_pu, T_X_pu, PR_R_pu, PR_X_pu, Filter_pu] = Converter_parameters(S_base, kV_base, Transformer_R, Transformer_X, Phase_Reactor_R, Phase_Reactor_X, Filter)


            MVA_max = MVA_rating
            P_AC = P_AC/S_base
            P_DC = P_DC/S_base
            
           
            Converters[var_name] = AC_DC_converter(AC_type, DC_type, AC_nodes[AC_node], DC_nodes[DC_node], P_AC, Q_AC,
                                                   P_DC, T_R_pu, T_X_pu, PR_R_pu, PR_X_pu, Filter_pu, Droop, kV_base, MVA_max=MVA_max,nConvP=1,polarity=n,Ucmin=Ucmin,Ucmax=Ucmax ,name=str(var_name))
        Convertor_list = list(Converters.values())

    if DCDC_conv is None:
        Convertor_DC_list = None
    else:
        DCDC_conv = DCDC_conv.set_index('Conv_id')
        "Convertor data sorting"
        Converters_DC = {}
        for index, row in DCDC_conv.iterrows():
            var_name = index
            element_type = DCDC_conv.at[index, 'type']

            fromNode = DCDC_conv.at[index, 'fromNode']
            toNode = DCDC_conv.at[index, 'toNode']

            PowerTo = DCDC_conv.at[index, 'P_MW']
            R_Ohm = DCDC_conv.at[index, 'R_Ohm']
            kV_base = DCDC_conv.at[index, 'kV_nodefromBase']

            Z_base = kV_base**2/S_base

            R = R_Ohm/Z_base

            PowerTo = PowerTo/S_base

            Converters_DC[var_name] = DC_DC_converter(
                element_type, DC_nodes[fromNode], DC_nodes[toNode], PowerTo, R, name=str(var_name))
        Convertor_DC_list = list(Converters_DC.values())

    G = Grid(S_base, AC_nodes_list, AC_lines_list, nodes_DC=DC_nodes_list,
             lines_DC=DC_lines_list, Converters=Convertor_list, conv_DC=Convertor_DC_list)
    res = Results(G, decimals=3)

    s = 1
    return [G, res]


def Create_grid_from_data_pu(S_base, AC_node_data, AC_line_data, DC_node_data, DC_line_data, Converter_data, DCDC_conv):

    if AC_node_data is None:
        AC_nodes_list = None
        AC_lines_list = None
    else:
        "AC nodes data sorting"
        AC_node_data = AC_node_data.set_index('Node_id')
        AC_nodes = {}
        for index, row in AC_node_data.iterrows():
            var_name = index
            element_type = AC_node_data.at[index, 'type']

            Voltage_0 = AC_node_data.at[index, 'Voltage_0']
            theta_0 = AC_node_data.at[index, 'theta_0']
            Power_Gained = AC_node_data.at[index, 'Power_Gained']
            Reactive_Gained = AC_node_data.at[index, 'Reactive_Gained']
            Power_load = AC_node_data.at[index, 'Power_load']
            Reactive_load = AC_node_data.at[index, 'Reactive_load']
            # Q_max          =AC_node_data.at[index,'Q_max']
            # Q_min          =AC_node_data.at[index,'Q_min']
            if 'Umin' in AC_node_data.columns:
                Umin=AC_node_data.at[index, 'Umin']
            else:
                Umin=0.9
            if 'Umax' in AC_node_data.columns:
                Umax=AC_node_data.at[index, 'Umax']
            else:
                Umax=1.1
            if 'x_coord' in AC_node_data.columns:
                x_coord=AC_node_data.at[index, 'x_coord']
            else:
                x_coord=None
            if 'y_coord' in AC_node_data.columns:
                y_coord=AC_node_data.at[index, 'y_coord']
            else:
                y_coord=None 

            AC_nodes[var_name] = Node_AC(element_type, Voltage_0, theta_0, Power_Gained,
                                         Reactive_Gained, Power_load, Reactive_load, name=str(var_name),Umin=Umin,Umax=Umax,x_coord=x_coord,y_coord=y_coord)
        AC_nodes_list = list(AC_nodes.values())

        AC_line_data = AC_line_data.set_index('Line_id')
        AC_lines = {}
        for index, row in AC_line_data.iterrows():
            var_name = index

            fromNode = AC_line_data.at[index, 'fromNode']
            toNode = AC_line_data.at[index, 'toNode']
            Resistance = AC_line_data.at[index, 'Resistance']
            Reactance = AC_line_data.at[index, 'Reactance']
            Conductance = AC_line_data.at[index, 'Conductance']
            Susceptance = AC_line_data.at[index, 'Susceptance']
            MVA_rating = AC_line_data.at[index, 'MVA_rating']
            V_base = AC_line_data.at[index, 'kV_base']
            if 'm' in AC_line_data.columns:
                m=AC_line_data.at[index, 'm']
            else:
                m=1
            if 'shift' in AC_line_data.columns:
                shift=AC_line_data.at[index, 'shift']
            else:
                shift=0
            
            
            AC_lines[var_name] = Line_AC(AC_nodes[fromNode], AC_nodes[toNode], Resistance,
                                         Reactance, Conductance, Susceptance, MVA_rating, V_base,m,shift ,name=str(var_name))
        AC_lines_list = list(AC_lines.values())

    if DC_node_data is None:

        DC_nodes_list = None
        DC_lines_list = None

    else:
        DC_node_data = DC_node_data.set_index('Node_id')

        "DC nodes data sorting"
        DC_nodes = {}
        for index, row in DC_node_data.iterrows():

            var_name = index
            node_type = DC_node_data.at[index, 'type']

            Voltage_0 = DC_node_data.at[index, 'Voltage_0']
            Power_Gained = DC_node_data.at[index, 'Power_Gained']
            Power_load = DC_node_data.at[index, 'Power_load']
            
            if 'Umin' in DC_node_data.columns:
                Umin=DC_node_data.at[index, 'Umin']
            else:
                Umin=0.95
            if 'Umax' in DC_node_data.columns:
                Umax=DC_node_data.at[index, 'Umax']
            else:
                Umax=1.05
            if 'x_coord' in DC_node_data.columns:
                x_coord=DC_node_data.at[index, 'x_coord']
            else:
                x_coord=None
            if 'y_coord' in DC_node_data.columns:
                y_coord=DC_node_data.at[index, 'y_coord']
            else:
                y_coord=None 
                
            DC_nodes[var_name] = Node_DC(
                node_type, Voltage_0, Power_Gained, Power_load, name=str(var_name),Umin=Umin,Umax=Umax,x_coord=x_coord,y_coord=y_coord)
        DC_nodes_list = list(DC_nodes.values())

        DC_line_data = DC_line_data.set_index('Line_id')
        DC_lines = {}
        for index, row in DC_line_data.iterrows():
            var_name = index

            fromNode = DC_line_data.at[index, 'fromNode']
            toNode = DC_line_data.at[index, 'toNode']
            Resistance = DC_line_data.at[index, 'Resistance']
            MW_rating = DC_line_data.at[index, 'MW_rating']
            V_base = DC_line_data.at[index, 'kV_base']
            pol = DC_line_data.at[index, 'Mono_Bi_polar']

            DC_lines[var_name] = Line_DC(
                DC_nodes[fromNode], DC_nodes[toNode], Resistance, MW_rating, V_base, pol, name=str(var_name))
        DC_lines_list = list(DC_lines.values())

    if Converter_data is None:
        Convertor_list = None
    else:
        Converter_data = Converter_data.set_index('Conv_id')
        "Convertor data sorting"
        Converters = {}
        for index, row in Converter_data.iterrows():
            var_name        = index
            AC_type         = Converter_data.at[index, 'AC_type']        if 'AC_type'        in Converter_data.columns else 'PV'
            DC_type         = Converter_data.at[index, 'DC_type']        if 'DC_type'        in Converter_data.columns else 'Droop'
            AC_node         = Converter_data.at[index, 'AC_node']               
            DC_node         = Converter_data.at[index, 'DC_node']              
            P_AC            = Converter_data.at[index, 'P_AC']           if 'P_AC'           in Converter_data.columns else 0
            Q_AC            = Converter_data.at[index, 'Q_AC']           if 'Q_AC'           in Converter_data.columns else 0
            P_DC            = Converter_data.at[index, 'P_DC']           if 'P_DC'           in Converter_data.columns else 0
            Transformer_R   = Converter_data.at[index, 'T_R']            if 'T_R'            in Converter_data.columns else 0
            Transformer_X   = Converter_data.at[index, 'T_X']            if 'T_X'            in Converter_data.columns else 0
            Phase_Reactor_R = Converter_data.at[index, 'PR_R']           
            Phase_Reactor_X = Converter_data.at[index, 'PR_X']          
            Filter          = Converter_data.at[index, 'Filter']         if 'Filter'         in Converter_data.columns else 0
            Droop           = Converter_data.at[index, 'Droop']          if 'Droop'          in Converter_data.columns else 0
            V_base          = Converter_data.at[index, 'AC_kV_base']     if 'AC_kV_base'     in Converter_data.columns else 0
            MVA_max         = Converter_data.at[index, 'MVA_rating']     if 'MVA_rating'     in Converter_data.columns else 1.5
            Ucmin           = Converter_data.at[index, 'Ucmin']          if 'Ucmin'          in Converter_data.columns else 0.85
            Ucmax           = Converter_data.at[index, 'Ucmax']          if 'Ucmax'          in Converter_data.columns else 1.2
            n               = Converter_data.at[index, 'Nconverter']     if 'Nconverter'     in Converter_data.columns else 1
            pol             = Converter_data.at[index, 'Nconverter']     if 'Nconverter'     in Converter_data.columns else 1

            Converters[var_name] = AC_DC_converter(AC_type, DC_type, AC_nodes[AC_node], DC_nodes[DC_node], P_AC, Q_AC, P_DC, Transformer_R, Transformer_X, Phase_Reactor_R, Phase_Reactor_X, Filter, Droop, V_base, MVA_max=MVA_max,nConvP=n,polarity=pol, name=str(var_name))
        Convertor_list = list(Converters.values())

    if DCDC_conv is None:
        Convertor_DC_list = None
    else:
        DCDC_conv = Converter_data.set_index('Conv_id')
        "Convertor data sorting"
        Converters_DC = {}
        for index, row in Converter_data.iterrows():
            var_name = index
            element_type = DCDC_conv.at[index, 'type']

            AC_node = DCDC_conv.at[index, 'fromNode']
            DC_node = DCDC_conv.at[index, 'toNode']

            PowerTo = DCDC_conv.at[index, 'P']
            R = DCDC_conv.at[index, 'R']

            Converters_DC[var_name] = DC_DC_converter(
                element_type, DC_nodes[fromNode], DC_nodes[toNode], PowerTo, R, name=str(var_name))
        Convertor_DC_list = list(Converters.values())

    G = Grid(S_base, AC_nodes_list, AC_lines_list, nodes_DC=DC_nodes_list,
             lines_DC=DC_lines_list, Converters=Convertor_list, conv_DC=Convertor_DC_list)
    res = Results(G, decimals=3)

    s = 1
    return [G, res]


def add_market(Grid,name,price,import_pu_L=1,export_pu_G=1,a=0,b=1,c=0):
    Grid.Markets_OPF[name]=price
    if b==1:
        b= price
    M = Market(price,import_pu_L,export_pu_G,a,b,c,name)
    Grid.Markets.append(M)


def Add_TimeSeries_Market(Grid,Market_data):
    MK= Market_data
    length = len(MK)
    Grid.Markets[0]=np.zeros(length)
    for col in MK.columns:
        market_name = col
        price= MK[col].astype(float).to_numpy()
        Grid.Markets_dic[market_name]=price
        M = Market(name)
        if M not in Grid.Markets:
            Grid.Markets.append(M)
        

def Add_TimeSeries(Grid, Time_Series_data):
    TS = Time_Series_data
    Time_series = {}
    # check if there are nan values in Time series and change to 0
    TS.fillna(0, inplace=True)
    TS_length = len(TS)-4
    Grid.Markets[0]=np.ones(TS_length)
    for col in TS.columns:
        node_name = TS.at[0, col]
        element_MW = float(TS.at[1, col])
        market_attached = TS.at[2,col]
        element_type = TS.at[3, col]
        
        
        if element_type != 'Slack' or  element_type != 'Generator' or  element_type != 'Reactor':
            Pow = TS.loc[4:, col].astype(float).to_numpy()*element_MW/Grid.S_base
        else:
            Pow = Grid.Markets[market_attached]
            
        name = col
        
        for node in Grid.nodes_AC:
            if node_name == node.name:
                for M in Grid.Markets:
                    if market == M.name:
                           M.nodes_AC.append(node)
                Time_series[col] = TS_AC(element_type, element_MW, node, Pow,market_attached ,name)
                node.market=market_attached
                if element_type == 'Slack':
                    node.extGrid = 2
                    node.PGi=0
                    
                    node.Max_pow_gen=element_MW/Grid.S_base
                    node.Max_pow_genR=element_MW/Grid.S_base
                    node.Min_pow_gen=-element_MW/Grid.S_base
                    node.Min_pow_genR=-element_MW/Grid.S_base
                elif element_type == 'Generator':
                    node.extGrid = 2
                    node.PGi=0
                    
                    node.Max_pow_gen=element_MW/Grid.S_base
                    node.Max_pow_genR=element_MW/Grid.S_base
                    node.Min_pow_genR=-element_MW/Grid.S_base
                    
                elif element_type == 'Reactor':
                    node.extGrid = 1
                    node.QGi=0
                    node.Min_pow_genR=-element_MW/Grid.S_base
                elif element_type == 'OWPP' or element_type == 'WPP':
                    node.RenSource=True
                    Grid.OWPP_node_to_ts[node.name]=name
                    node.PGi=element_MW/Grid.S_base
                    
    TS_list = list(Time_series.values())

    Grid.Time_series.extend(TS_list)
    Grid.Time_series_ran = False
    s = 1




class Grid:
    def __init__(self, S_base: float, nodes_AC: list = None, lines_AC: list = None, Converters: list = None, nodes_DC: list = None, lines_DC: list = None, conv_DC: list = None):
        
        self.Graph_toPlot= nx.Graph()
        self.node_positions={}
        self.S_base = S_base

        self.nodes_AC = nodes_AC
        self.lines_AC = lines_AC
        self.slack_bus_number_AC = []
        self.slack_bus_number_DC = []

        self.iter_flow_AC = []
        self.iter_flow_DC = []

        self.OPF_run= False
        self.VarPrice = False
        self.OnlyGen = True
        self.CurtCost=False


        self.Converters_ACDC = Converters

        self.nodes_DC = nodes_DC
        self.lines_DC = lines_DC
        self.Converters_DCDC = conv_DC

        if self.nodes_AC != None:
            self.Update_Graph_AC()
        if self.nodes_DC != None:
            self.Update_Graph_DC()
     
        # AC grid

        if self.lines_AC == None:
            self.nl_AC = 0

        else:
            # number of lines
            self.nl_AC = len(self.lines_AC)
            # number of connections
            self.nc_AC = self.nl_AC

        if self.nodes_AC == None:
            self.nn_AC = 0  # number of nodes

            self.npq = 0
            self.npv = 0
        else:
            self.nn_AC = len(self.nodes_AC)  # number of nodes

            self.npq = len(self.pq_nodes)
            self.npv = len(self.pv_nodes)
            self.Ps_AC_new = np.zeros((self.nn_AC, 1))
            s = 1
            self.Update_PQ_AC()
            self.node_names_AC = {}
            for node in self.nodes_AC:
                self.node_names_AC[node.nodeNumber] = node.name
            self.names_node_AC = {value: key for key, value in self.node_names_AC.items()}    
        # DC grid
        if self.nodes_DC == None:
            self.nn_DC = 0
            self.nP = 0
            self.nDroop = 0

        else:
            self.nn_DC = len(self.nodes_DC)  # number of nodes
            self.nPAC = len(self.PAC_nodes)
            self.nP = len(self.P_nodes)
            self.nDroop = len(self.droop_nodes)
            self.nP = len(self.P_nodes)
            self.nDroop = len(self.droop_nodes)

            self.Update_P_DC()

        if self.lines_DC == None:
            self.nl_DC = 0
        else:
            self.nl_DC = len(self.lines_DC)  # number of lines

        # Converters

        if self.Converters_ACDC == None:
            self.nconv = 0
        else:
            self.nconv = len(self.Converters_ACDC)  # number of converters
            self.nconvP = len(self.P_Conv)
            self.nconvD = len(self.Droop_Conv)
            self.nconvS = len(self.Slack_Conv)
            self.conv_names_ACDC = {}
            for conv in self.Converters_ACDC:
                self.conv_names_ACDC[conv.ConvNumber] = conv.name

            for conv in self.Converters_ACDC:

                conv.basekA = S_base/(np.sqrt(3)*conv.AC_kV_base)
                conv.a_conv = conv.a_conv_og/S_base
                conv.b_conv = conv.b_conv_og*conv.basekA/S_base
                conv.c_inver = conv.c_inver_og*conv.basekA**2/S_base
                conv.c_rect = conv.c_rect_og*conv.basekA**2/S_base

        # #Call Y bus formula to fill matrix
        self.create_Ybus_AC()
        self.create_Ybus_DC()
        
        self.Time_series = []
        self.Markets =[]
        self.Markets_dic={}
        
        self.Markets_OPF = {}
        self.Markets_OPF[0]=0
        self.sigma=1.05
   
        self.OWPP_node_to_ts={}
        # Node type differentiation

    @property
    def pq_nodes(self):
        pq_nodes = [node for node in self.nodes_AC if node.type == 'PQ']
        return pq_nodes

    @property
    def pv_nodes(self):
        pv_nodes = [node for node in self.nodes_AC if node.type == 'PV']
        return pv_nodes

    @property
    def slack_nodes(self):
        slack_nodes = [node for node in self.nodes_AC if node.type == 'Slack']
        return slack_nodes

    @property
    def PAC_nodes(self):
        PAC_nodes = [node for node in self.nodes_DC if node.type == 'PAC']
        return PAC_nodes

    @property
    def P_nodes(self):
        P_nodes = [node for node in self.nodes_DC if node.type == 'P']
        return P_nodes

    @property
    def droop_nodes(self):
        droop_nodes = [node for node in self.nodes_DC if node.type == 'Droop']
        return droop_nodes

    @property
    def slackDC_nodes(self):
        slackDC_nodes = [
            node for node in self.nodes_DC if node.type == 'Slack']
        return slackDC_nodes

    @property
    def P_Conv(self):
        P_Conv = [conv for conv in self.Converters_ACDC if conv.type == 'P']
        return P_Conv

    @property
    def Slack_Conv(self):
        Slack_Conv = [
            conv for conv in self.Converters_ACDC if conv.type == 'Slack']
        return Slack_Conv

    @property
    def Droop_Conv(self):
        Droop_Conv = [
            conv for conv in self.Converters_ACDC if conv.type == 'Droop']
        return Droop_Conv

    
    

    def Update_Graph_DC(self):
        self.Graph_DC = nx.Graph()

        "Checking for un used nodes "
        used_nodes = set()

        # Iterate through lines
        for line in self.lines_DC:
            used_nodes.add(line.toNode)
            used_nodes.add(line.fromNode)

        # Iterate through converters

        if self.Converters_ACDC != None:
            for converter in self.Converters_ACDC:
                used_nodes.add(converter.Node_DC)

        # Filter out unused nodes
        nodes = [node for node in self.nodes_DC if node in used_nodes]

        for node in nodes:
            self.node_positions[node]=(node.x_coord,node.y_coord)
            
            if node in used_nodes:
                node.used = True

        self.Graph_DC_unused_nodes = [node for node in self.nodes_DC if not node.used]

        for line in self.lines_DC:
            self.Graph_toPlot.add_edge(line.fromNode, line.toNode, line=line)
            self.Graph_DC.add_edge(line.fromNode, line.toNode)

        self.Grids_DC = list(nx.connected_components(self.Graph_DC))
        self.Num_Grids_DC = len(self.Grids_DC)
        self.Graph_node_to_Grid_index_DC = {}
        self.Graph_line_to_Grid_index_DC = {}
        self.Graph_grid_to_MTDC={}
        
        self.load_grid_DC=np.zeros(self.Num_Grids_DC)
        self.rating_grid_DC=np.zeros(self.Num_Grids_DC)
        self.Graph_number_lines_DC=np.zeros(self.Num_Grids_DC)

        self.Graph_kV_base = np.zeros(self.Num_Grids_DC)
        self.num_MTDC=0
        self.MTDC = {} 
        
        for i, Grid in enumerate(self.Grids_DC):
            for node in Grid:
                
                nn= node.nodeNumber
                self.Graph_node_to_Grid_index_DC[node.nodeNumber] = i
                for line in self.lines_DC:
                    if line.fromNode == node or line.toNode == node:
                        self.Graph_line_to_Grid_index_DC[line] = i
                        self.Graph_kV_base[i] = line.V_base
        for line in self.lines_DC:
            g=self.Graph_line_to_Grid_index_DC[line]
            self.Graph_number_lines_DC[g]+=1
            self.rating_grid_DC[g]+=line.MW_rating
        
        self.num_slackDC = np.zeros(self.Num_Grids_DC)
        for i in range(self.Num_Grids_DC):
            if self.Graph_number_lines_DC[i] >=2:
                self.MTDC[self.num_MTDC]=i
                self.Graph_grid_to_MTDC[i]=self.num_MTDC
                self.num_MTDC+=1
            for node in self.Grids_DC[i]:
                if node.type == 'Slack':
                    self.num_slackDC[i] += 1

            s = 1
            if self.num_slackDC[i] == 0:
                print(
                    f'For Grid DC {i+1} no slack bus found, results may not be accurate')

            if self.num_slackDC[i] > 1:
                print(f'For Grid DC {i+1} more than one slack bus found')
                sys.exit()
         
        s = 1

   
    def Update_Graph_AC(self):
        self.Graph_AC = nx.Graph()
        

        "Checking for un used nodes "
        used_nodes = set()

        # Iterate through lines
        for line in self.lines_AC:
            used_nodes.add(line.toNode)
            used_nodes.add(line.fromNode)

        # Iterate through converters
        if self.Converters_ACDC != None:

            for converter in self.Converters_ACDC:
                used_nodes.add(converter.Node_AC)
                self.Graph_toPlot.add_node(converter.Node_AC) 

        # Filter out unused nodes
        nodes = [node for node in self.nodes_AC if node in used_nodes]

        for node in nodes:
            self.node_positions[node]=(node.x_coord,node.y_coord)
            
            if node in used_nodes:
                node.used = True

        self.Graph_AC_unused_nodes = [
            node for node in self.nodes_AC if not node.used]

        s = 1

        for node in self.nodes_AC:
            if node.type == 'Slack':
                self.Graph_AC.add_node(node)
               

        "Creating Graphs to differentiate Grids"
        for line in self.lines_AC:
            self.Graph_AC.add_edge(line.fromNode, line.toNode)
            self.Graph_toPlot.add_edge(line.fromNode, line.toNode,line=line)
            line.toNode.stand_alone = False
            line.fromNode.stand_alone = False

        self.Grids_AC = list(nx.connected_components(self.Graph_AC))
        self.Num_Grids_AC = len(self.Grids_AC)
        self.Graph_node_to_Grid_index_AC = {}
        self.Graph_line_to_Grid_index_AC = {}
        self.load_grid_AC=np.zeros(self.Num_Grids_AC)
        self.rating_grid_AC=np.zeros(self.Num_Grids_AC)
        self.Graph_number_lines_AC=np.zeros(self.Num_Grids_AC)

        for i, Grid in enumerate(self.Grids_AC):
            for node in Grid:
                self.Graph_node_to_Grid_index_AC[node.nodeNumber] = i
                for line in self.lines_AC:
                    if line.fromNode == node or line.toNode == node:
                        self.Graph_line_to_Grid_index_AC[line] = i

        for line in self.lines_AC:
            g=self.Graph_line_to_Grid_index_AC[line]
            self.rating_grid_AC[g]+=line.MVA_rating
            self.Graph_number_lines_AC[g]+=1
        "Slack identification"
        self.num_slackAC = np.zeros(self.Num_Grids_AC)

        for i in range(self.Num_Grids_AC):

            for node in self.Grids_AC[i]:
                if node.type == 'Slack':
                    self.num_slackAC[i] += 1
            if self.num_slackAC[i] == 0:
                print(f'For Grid AC {i+1} no slack bus found.')
                sys.exit()
            if self.num_slackAC[i] > 1:
                print(
                    f'For Grid AC {i+1} more than one slack bus found, results may not be accurate')
        
        
        s = 1

    def Time_series_statistics(self, curtail=0.99,over_loading=0.9):

        a = self.Time_series

        static = []  # Initialize stats as an empty DataFrame

        for ts in a:
           if ts.type !='Slack' or  ts.type !='Generator' or  ts.type != 'Reactor':
                # Calculate statistics for each time series
                mean = np.mean(ts.TS)  # Calculate mean
                median = np.median(ts.TS)  # Calculate median
                maxim = np.max(ts.TS)  # Calculate maximum
                minim = np.min(ts.TS)  # Calculate minimum
                mode, count = st.mode(np.round(ts.TS, decimals=3))
                iqr = st.iqr(ts.TS)

                sorted_data = np.sort(ts.TS)
                cumulative_prob = np.linspace(0, 1, len(sorted_data))

                i = find_value_from_cdf(cumulative_prob, curtail)
                name=ts.name
                n = sum(1 for num in ts.TS if num > over_loading*ts.element_MW/self.S_base)
                
                # Create a dictionary to store the statistics
                stats_dict = {
                    'Element': name,
                    'Mean': mean,
                    'Median': median,
                    'Maximum': maxim,
                    'Minimum': minim,
                    'Mode3dec': mode,
                    'Mode_count': count,
                    'IQR': iqr,
                    f'{curtail*100}%': sorted_data[i].item(),
                    f'Number above {over_loading*100}%': n
                }

                # Convert the dictionary to a DataFrame and append it to the stats DataFrame
                static.append(stats_dict)

        if self.Time_series_ran == True:
            df_res = self.Time_series_res
            df_line_res = self.Time_series_line_res
            df_grid_res = self.Time_series_grid_loading

            if self.VarPrice == True:
                Time_series_price_stat=self.Time_series_price.copy()
                
                new_columns = [column + '_price' for column in Time_series_price_stat.columns]
                # Rename the columns
                Time_series_price_stat.columns = new_columns
                merged_df = pd.concat(
                    [df_res, df_line_res, df_grid_res, Time_series_price_stat], axis=1)
            else:
                merged_df = pd.concat(
                    [df_res, df_line_res, df_grid_res], axis=1)

            s = 1
            for col in merged_df:
                # Calculate statistics for each column in merged_df
                mean = merged_df[col].mean()  # Calculate mean
                median = merged_df[col].median()  # Calculate median
                maxim = merged_df[col].max()  # Calculate maximum
                minim = merged_df[col].min()  # Calculate minimum
                mode, count = st.mode(merged_df[col].round(3))
                iqr = st.iqr(merged_df[col])

                sorted_data = np.sort(merged_df[col])
                cumulative_prob = np.linspace(0, 1, len(sorted_data))

                i = find_value_from_cdf(cumulative_prob, curtail)
                
                
                if 'Loading' in col:
                    n = sum(1 for num in merged_df[col] if num > over_loading)
                else:
                    n = sum(1 for num in merged_df[col] if num > over_loading*maxim)
                    
                # Create a dictionary to store the statistics
                stats_dict = {
                    'Element': col,
                    'Mean': mean,
                    'Median': median,
                    'Maximum': maxim,
                    'Minimum': minim,
                    'Mode3dec': mode,
                    'Mode_count': count,
                    'IQR': iqr,
                    f'{curtail*100}%': sorted_data[i].item(),
                   f'Number above {over_loading*100}%': n
                }

                # Convert the dictionary to a DataFrame and append it to the stats DataFrame
                static.append(stats_dict)

        # Reset index of the stats DataFrame
        stats = pd.DataFrame(static)
        stats.set_index('Element', inplace=True)
        self.Stats = stats

        return stats

    def Curtail_RE(self, curtail):
        self.Time_series_statistics(curtail=curtail)
        for ts in self.Time_series:
            if  element_type != 'Slack' or  element_type != 'Generator' or  element_type != 'Reactor':
                Element = ts.name
                cur = f'{curtail*100}%'

                value = self.Stats.loc[Element, cur]

                ts.TS[ts.TS > value] = value

    def Update_P_DC(self):

        self.P_DC = np.vstack([node.P_DC for node in self.nodes_DC])
        self.Pconv_DC = np.vstack([node.Pconv for node in self.nodes_DC])
        self.Pconv_DCDC = np.vstack([node.PconvDC for node in self.nodes_DC])
    def Update_PQ_AC(self):
        for node in self.nodes_AC:
            node.Q_s_fx=sum(self.Converters_ACDC[conv].Q_AC for conv  in node.connected_conv if self.Converters_ACDC[conv].AC_type=='PQ')
        
        # # Negative means power leaving the system, positive means injected into the system at a node                
        self.P_AC = np.vstack([node.PGi+node.PGi_ren*node.curtailment+node.PGi_opt-node.PLi for node in self.nodes_AC])
        self.Q_AC = np.vstack([node.QGi+node.QGi_opt-node.QLi +node.Q_s_fx for node in self.nodes_AC])
        self.Ps_AC = np.vstack([node.P_s for node in self.nodes_AC])
        self.Qs_AC = np.vstack([node.Q_s for node in self.nodes_AC])

        # self.P_AC_conv=np.vstack([conv.P_AC for conv in self.Converters_ACDC])
        # self.Q_AC_conv=np.vstack([conv.Q_AC for conv in self.Converters_ACDC])
        s = 1

    def create_Ybus_AC(self):
        self.Ybus_AC = np.zeros((self.nn_AC, self.nn_AC), dtype=complex)
        self.AdmitanceVec_AC = np.zeros((self.nn_AC), dtype=complex)
        Ybus_nn= np.zeros((self.nn_AC),dtype=complex)
        # off diagonal elements
        for k in range(self.nl_AC):
            line = self.lines_AC[k]
            fromNode = line.fromNode.nodeNumber
            toNode = line.toNode.nodeNumber

            tap= line.m * np.exp(1j*line.shift)            
            #Yft
            branch_ft = -(1/line.Z)/np.conj(tap)
            self.Ybus_AC[fromNode, toNode]+=branch_ft
            #Ytf
            branch_tf = -(1/line.Z)/tap
            self.Ybus_AC[toNode, fromNode]+=branch_tf
            
            
            self.AdmitanceVec_AC[fromNode] += line.Y/2
            self.AdmitanceVec_AC[toNode] += line.Y/2
            
            branch_ff=(1/line.Z+line.Y/2)/(line.m**2)
            branch_tt=(1/line.Z+line.Y/2)
            
            Ybus_nn[fromNode] += branch_ff
            Ybus_nn[toNode] += branch_tt
            
            line.Ybus_branch=np.array([[branch_ff, branch_ft],[branch_tf, branch_tt]])
            
            s=1
        
        
        Ybus_sum = self.Ybus_AC.sum(axis=0)

        for m in range(self.nn_AC):
            node = self.nodes_AC[m]

            self.AdmitanceVec_AC[m] += node.Reactor*1j
            Ybus_nn[m] += node.Reactor*1j
            # self.Ybus_AC[m, m] = -Ybus_sum[m]+self.AdmitanceVec_AC[m]
            self.Ybus_AC[m, m] = Ybus_nn[m]
            
    def create_Ybus_DC(self):
        self.Ybus_DC = np.zeros((self.nn_DC, self.nn_DC), dtype=float)

        # off diagonal elements
        for k in range(self.nl_DC):
            line = self.lines_DC[k]
            fromNode = line.fromNode.nodeNumber
            toNode = line.toNode.nodeNumber

            self.Ybus_DC[fromNode, toNode] -= 1/line.Z
            self.Ybus_DC[toNode, fromNode] = self.Ybus_DC[fromNode, toNode]

        # Diagonal elements
        for m in range(self.nn_DC):
            self.Ybus_DC[m, m] = -self.Ybus_DC[:,
                                               m].sum() if self.Ybus_DC[:, m].sum() != 0 else 1.0

    def Check_SlacknDroop(self, change_slack2Droop):
        for conv in self.Converters_ACDC:
            if conv.type == 'Slack':

                DC_node = conv.Node_DC

                node_count = 0

                P_syst = 0
                for conv_other in self.Converters_ACDC:
                    DC_node_other = conv_other.Node_DC
                    connected = nx.has_path(
                        self.Graph_DC, DC_node, DC_node_other)
                    if connected == True:
                        P_syst += -conv_other.P_DC
                    else:
                        # print(f"Nodes {DC_node.name} and {DC_node_other.name} are not connected.")
                        node_count += 1

                if change_slack2Droop == True:
                    if self.nn_DC-node_count != 2:

                        conv.type = 'Droop'
                        DC_node.type = 'Droop'
                conv.P_DC = P_syst
                DC_node.Pconv = P_syst

                self.Update_P_DC()

            elif conv.type == 'Droop':

                DC_node = conv.Node_DC

                node_count = 0

                for conv_other in self.Converters_ACDC:
                    DC_node_other = conv_other.Node_DC
                    connected = nx.has_path(self.Graph_DC, DC_node, DC_node_other)
                    if connected == False:
                        node_count += 1

                if self.nn_DC-node_count == 2:
                    g=self.Graph_node_to_Grid_index_DC[DC_node]
                    
                    if any(node.type == 'Slack' for node in self.Grids_DC[g]):
                        s=1
                    else:
                        conv.type = 'Slack'
                        DC_node.type = 'Slack'
                        print(f"Changing converter {conv.name} to Slack")
                self.Update_P_DC()

        self.nconvD = len(self.Droop_Conv)
        self.nconvS = len(self.Slack_Conv)

    
    def get_linesAC_by_node(self, nodeNumber):
        lines = [line for line in self.lines_AC if
                 (line.toNode.nodeNumber == nodeNumber or line.fromNode.nodeNumber == nodeNumber)]
        return lines

    def get_linesDC_by_node(self, nodeNumber):
        lines = [line for line in self.lines_DC if
                 (line.toNode.nodeNumber == nodeNumber or line.fromNode.nodeNumber == nodeNumber)]
        return lines

    def get_lineDC_by_nodes(self, fromNode, toNode):
        lines = [line for line in self.lines_DC if
                 (line.toNode.nodeNumber == fromNode and line.fromNode.nodeNumber == toNode) or
                 (line.toNode.nodeNumber == toNode and line.fromNode.nodeNumber == fromNode)]
        return lines[0] if lines else None

    def Line_AC_calc(self):
        try: 
            V_cart = pol2cartz(self.V_AC, self.Theta_V_AC)
        except: 
            self.V_AC =np.zeros(self.nn_AC)
            self.Theta_V_AC=np.zeros(self.nn_AC)
            for node in self.nodes_AC: 
                nAC=node.nodeNumber
                self.V_AC[nAC]=node.V
                self.Theta_V_AC[nAC]=node.theta
            V_cart = pol2cartz(self.V_AC, self.Theta_V_AC)
            
        Ybus = self.Ybus_AC
        self.I_AC_cart = np.matmul(self.Ybus_AC, V_cart)
        self.I_AC_m = abs(self.I_AC_cart)
        self.I_AC_th = np.angle(self.I_AC_cart)

        Iij_cart = np.zeros((self.nn_AC, self.nn_AC), dtype=complex)
        Sij = np.zeros((self.nn_AC, self.nn_AC), dtype=complex)
        Iij_cart2 = np.zeros((self.nn_AC, self.nn_AC), dtype=complex)
        Sij2 = np.zeros((self.nn_AC, self.nn_AC), dtype=complex)
        L_loss = np.zeros(self.nl_AC, dtype=complex)

        for line in self.lines_AC:
            i = line.fromNode.nodeNumber
            j = line.toNode.nodeNumber
            l = line.lineNumber

            # Iij_cart[i, j] = (V_cart[j]-V_cart[i]) * Ybus[i, j]+V_cart[i]*line.Y/2
            # Iij_cart[j, i] = (V_cart[i]-V_cart[j]) * Ybus[j, i]+V_cart[j]*line.Y/2
                           
         
            Iij_cart[i, j] = line.Ybus_branch[0,0]*V_cart[i]+line.Ybus_branch[0,1]*V_cart[j]
            Iij_cart[j, i] = line.Ybus_branch[1,0]*V_cart[i]+line.Ybus_branch[1,1]*V_cart[j]
            s=1
            Sij[i, j] = V_cart[i]*np.conj(Iij_cart[i, j])
            Sij[j, i] = V_cart[j]*np.conj(Iij_cart[j, i])
            
      

            L_loss[l] = Sij[i, j]+Sij[j, i]
            line.loss = Sij[i, j]+Sij[j, i]
            
            line.fromS=Sij[i,j]
            line.toS=Sij[j,i]
            Pfrom1=np.real(Sij[i,j])
            Pto1=np.real(Sij[j,i])
            Qfrom1 = np.imag(Sij[i,j])
            Qto1 = np.imag(Sij[j,i])
            

            
            Vf=self.V_AC[i]
            Vt=self.V_AC[j]
            Gff=np.real(line.Ybus_branch[0,0])
            Bff=np.imag(line.Ybus_branch[0,0])
            Gft=np.real(line.Ybus_branch[0,1])
            Bft=np.imag(line.Ybus_branch[0,1])
            thf=self.Theta_V_AC[i]
            tht=self.Theta_V_AC[j]
            Gtt=np.real(line.Ybus_branch[1,1])
            Btt=np.imag(line.Ybus_branch[1,1])
            Gtf=np.real(line.Ybus_branch[1,0])
            Btf=np.imag(line.Ybus_branch[1,0])
            
            Pfrom2=   Vf*Vf*Gff + Vf*Vt*(Gft*np.cos(thf - tht) + Bft*np.sin(thf - tht))
            Pto2=     Vt*Vt*Gtt + Vf*Vt*(Gtf*np.cos(tht - thf) + Btf*np.sin(tht - thf))
            Qfrom2 = -Vf*Vf*Bff + Vf*Vt*(Gft*np.sin(thf - tht) - Bft*np.cos(thf - tht))
            Qto2   = -Vt*Vt*Btt + Vf*Vt*(Gtf*np.sin(tht - thf) - Btf*np.cos(tht - thf))
            
            
            s=1
        [Iij, Iij_th] = cartz2pol(Iij_cart)

        self.L_loss_AC = L_loss
        self.Sij = Sij
        self.Pij_AC = np.real(Sij)
        self.Qij = np.imag(Sij)
        self.Iij_AC = Iij
        s = 1

    def Line_DC_calc(self):
        V = self.V_DC
        Ybus = self.Ybus_DC
        self.I_DC = np.matmul(Ybus, V)

        Iij = np.zeros((self.nn_DC, self.nn_DC), dtype=float)
        Pij_DC = np.zeros((self.nn_DC, self.nn_DC), dtype=float)

        s = 1
        for line in self.lines_DC:
            i = line.fromNode.nodeNumber
            j = line.toNode.nodeNumber
            pol = line.pol

            Iij[i, j] = (V[i]-V[j])*-Ybus[i, j]
            Iij[j, i] = (V[j]-V[i])*-Ybus[i, j]

            Pij_DC[i, j] = V[i]*(Iij[i, j])*pol
            Pij_DC[j, i] = V[j]*(Iij[j, i])*pol
            
            line.fromP=Pij_DC[i,j]
            line.toP=Pij_DC[j,i]

        L_loss = np.zeros(self.nl_DC, dtype=float)

        for line in self.lines_DC:
            l = line.lineNumber
            i = line.fromNode.nodeNumber
            j = line.toNode.nodeNumber

            L_loss[l] = Pij_DC[i, j]+Pij_DC[j, i]
            line.loss = Pij_DC[i, j]+Pij_DC[j, i]

        self.L_loss_DC = L_loss

        self.Pij_DC = Pij_DC

        self.Iij_DC = Iij
        s = 1


class Node_AC:
    nodeNumber = 0
    names = set()
    
    @classmethod
    def reset_class(cls):
        cls.nodeNumber = 0
        cls.names = set()
        
    @property
    def name(self):
        return self._name

    def __init__(self, node_type: str, Voltage_0: float, theta_0: float, Power_Gained: float, Reactive_Gained: float, Power_load: float, Reactive_load: float, name=None, used=False, Umin=0.9, Umax=1.1,x_coord=None,y_coord=None):
        # type: (1=PQ, 2=PV, 3=Slack)
        self.nodeNumber = Node_AC.nodeNumber
        Node_AC.nodeNumber += 1
        self.type = node_type

        self.V_ini = Voltage_0
        self.theta_ini = theta_0
        self.V = np.copy(self.V_ini)
        self.theta = np.copy(self.theta_ini)
        self.PGi = Power_Gained
        self.PGi_opt =0
        self.PGi_ren_base=0
        self.PGi_ren= 0 
        self._PGi_available=1
        self.RenSource=False
        self.PLi= Power_load
        self.PLi_base = Power_load
        self._PLi_factor =1
        
        self.QGi = Reactive_Gained
        self.QGi_opt =0
        self.QLi = Reactive_load

        self.Qmin = 0
        self.Qmax = 0
        self.Reactor = 0
        # self.Q_max = Q_max
        # self.Q_min = Q_min
        # self.P_AC = self.PGi-self.PLi
        # self.Q_AC = self.QGi-self.QLi
        self.P_s = 0
        self.Q_s = 0
        self.Q_s_fx = 0  # reactive power by converters in PQ mode
        self.P_s_new = np.copy(self.P_s)
        self.used = used
        self.stand_alone = True
        self.extGrid = 0
       

        self.price = 0.0
        self.Num_conv_connected=0
        self.connected_conv=set()
        self.curtailment=1

        self.Max_pow_gen=0
        self.Min_pow_gen=0
        self.Max_pow_genR=0
        self.Min_pow_genR=0
        
        self.Umax= Umax
        self.Umin=Umin
        
        self.x_coord=x_coord
        self.y_coord=y_coord


        if name in Node_AC.names:
            Node_AC.nodeNumber -= 1
            raise NameError("Already used name '%s'." % name)
        if name is None:
            self._name = str(self.nodeNumber)
        else:
            self._name = name

        Node_AC.names.add(self.name)
  
    @property
    def PGi_available(self):
        return self._PGi_available

    @PGi_available.setter
    def PGi_available(self, value):
        self._PGi_available = value
        if self.RenSource:
            self.update_PGi_ren()
            
    @property
    def PLi_factor(self):
        return self._PLi_factor

    @PGi_available.setter
    def PLi_factor(self, value):
        self._PLi_factor = value
        self.update_PLi()        
       
    def update_PLi(self):
        self.PLi = self.PLi_base * self._PLi_factor
        
    def update_PGi_ren(self):
        self.PGi_ren = self.PGi_ren_base * self._PGi_available
    def set_renewable_source(self, base, S_base):
        self.PGi_ren_base = base / S_base
        self.RenSource = True
        self.update_PGi_ren()

class Node_DC:
    nodeNumber = 0
    names = set()
    
    @classmethod
    def reset_class(cls):
        cls.nodeNumber = 0
        cls.names = set()
    
    @property
    def name(self):
        return self._name

    def __init__(self, node_type: str, Voltage_0: float, Power_Gained: float, Power_load: float, name=None, used=False,Umin=0.95, Umax=1.05,x_coord=None,y_coord=None):
        # type: (1=P, 2=Droop, 3=Slack)
        self.nodeNumber = Node_DC.nodeNumber
        Node_DC.nodeNumber += 1

        self.V_ini = Voltage_0
        self.type = node_type

        self.PGi = Power_Gained
        self.PLi = Power_load
        self.P_DC = self.PGi-self.PLi
        self.V = np.copy(self.V_ini)
        self.P_INJ = 0
        self.Pconv = 0
        self.used = used
        self.PconvDC = 0
        
        self.Umax=Umax
        self.Umin=Umin
        
        self.x_coord=x_coord
        self.y_coord=y_coord
        
        
        if name in Node_DC.names:
            Node_DC.nodeNumber -= 1
            raise NameError("Already used name '%s'." % name)
        if name is None:
            self._name = str(self.nodeNumber)
        else:
            self._name = name

        Node_DC.names.add(self.name)


class Line_AC:
    lineNumber = 0
    names = set()

    @classmethod
    def reset_class(cls):
        cls.lineNumber = 0
        cls.names = set()
        
    @property
    def name(self):
        return self._name

    def __init__(self, fromNode: Node_AC, toNode: Node_AC, Resistance: float, Reactance: float, Conductance: float, Susceptance: float, MVA_rating: float, V_base: float,m:float=1, shift:float=0, name=None):
        self.lineNumber = Line_AC.lineNumber
        Line_AC.lineNumber += 1

        self.fromNode = fromNode
        self.toNode = toNode
        self.R = Resistance
        self.X = Reactance
        self.G = Conductance
        self.B = Susceptance
        self.Z = self.R + self.X * 1j
        self.Y = self.G + self.B * 1j
        self.V_base = V_base
        self.MVA_rating = MVA_rating
        
        self.m =m
        self.shift = shift
        
        self.fromS=0
        self.toS=0
        
        self.fromNode.kV_base=V_base
        self.toNode.kV_base=V_base

        if name in Line_AC.names:
            Line_AC.lineNumber -= 1
            raise NameError("Already used name '%s'." % name)

        if name is None:
            self._name = str(self.lineNumber)
        else:
            self._name = name

        Line_AC.names.add(self.name)


class Line_DC:
    lineNumber = 0
    names = set()

    @classmethod
    def reset_class(cls):
        cls.lineNumber = 0
        cls.names = set()    

    @property
    def name(self):
        return self._name

    def __init__(self, fromNode: Node_DC, toNode: Node_DC, Resistance: float, MW_rating: float, V_base: float, polarity='m', name=None):
        self.lineNumber = Line_DC.lineNumber
        Line_DC.lineNumber += 1

        self.m_sm_b = polarity

        if polarity == 'm':
            self.pol = 1
        elif polarity == 'b' or polarity == 'sm':
            self.pol = 2
        else:
            print('No viable polarity inserted pol =1')
            self.pol = 1

        self.fromNode = fromNode
        self.toNode = toNode
        self.R = Resistance
        self.MW_rating = MW_rating
        self.fromNode.kV_base=V_base
        self.toNode.kV_base=V_base
        self.Z = self.R

        self.fromP=0
        self.toP=0        

        self.V_base = V_base

        if name in Line_DC.names:
            Line_DC.lineNumber -= 1
            raise NameError("Already used name '%s'." % name)

        if name is None:
            self._name = str(self.lineNumber)
        else:
            self._name = name

        Line_DC.names.add(self.name)


class AC_DC_converter:
    ConvNumber = 0
    names = set()
    
    @classmethod
    def reset_class(cls):
        cls.ConvNumber = 0
        cls.names = set()
    
    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value
        self.Node_DC.type = value  # Update DC_node type when converter type changes


    def __init__(self, AC_type: str, DC_type: str, AC_node: Node_AC, DC_node: Node_DC, P_AC: float, Q_AC: float, P_DC: float, Transformer_resistance: float, Transformer_reactance: float, Phase_Reactor_R: float, Phase_Reactor_X: float, Filter: float, Droop: float, V_base: float, MVA_max: float = 1.05,nConvP: int =1,polarity: int =1 ,Ucmin: float = 0.85, Ucmax: float = 1.2, name=None):
        self.ConvNumber = AC_DC_converter.ConvNumber
        AC_DC_converter.ConvNumber += 1
        # type: (1=P, 2=droop, 3=Slack)
        
        self.NumConvP= nConvP
        self.cn_pol=   polarity 
        
        self.Droop_rate = Droop
        
        self.AC_type = AC_type

        self.AC_kV_base = V_base

        self.Node_AC = AC_node
        self.Node_AC.kV_base = V_base
        AC_node.Num_conv_connected+=1
        self.Node_DC = DC_node
        # if self.AC_type=='Slack':
        #     # print(name)
        #     self.type='PAC'
        
        self.type = DC_type

        self.R_t = Transformer_resistance/self.cn_pol
        self.X_t = Transformer_reactance /self.cn_pol
        self.PR_R = Phase_Reactor_R /self.cn_pol
        self.PR_X = Phase_Reactor_X /self.cn_pol
        self.Bf = Filter * self.cn_pol
        self.P_DC = P_DC
        self.P_AC = P_AC
        self.Q_AC = Q_AC
        
        self.Node_DC.type = self.type
        self.Node_DC.Droop_rate = self.Droop_rate
        self.Node_DC.Pconv = self.P_DC
        
        self.a_conv_og = 1.103  * self.cn_pol # MVA
        self.b_conv_og = 0.887                  # kV
        self.c_rect_og = 2.885  /self.cn_pol  # Ohm
        self.c_inver_og = 4.371 /self.cn_pol  # Ohm

        # 1.103 0.887  2.885    4.371

        self.P_loss = 0

        self.U_s = 1
        if P_DC > 0:
            self.U_c = 0.98
            self.U_f = 0.99
        else:
            self.U_c = 1.1
            self.U_f = 1.05
        self.th_s = 0.09
        self.th_f = 0.1
        self.th_c = 0.11

        self.MVA_max = MVA_max * self.cn_pol
        self.Ucmin = Ucmin
        self.Ucmax = Ucmax
        self.OPF_fx=False
        self.OPF_fx_type='PDC'
        if self.AC_type=='Slack' or self.type=='Slack':
            self.OPF_fx_type='None'
        if self.AC_type == 'PV':
            if self.type == 'PAC':
                self.OPF_fx_type='PV'
            if self.Node_AC.type == 'PQ':
                self.Node_AC.type = 'PV'
        if self.AC_type == 'PQ':
            if self.type == 'PAC':
                self.OPF_fx_type='PQ'
            self.Node_AC.Q_s_fx += self.Q_AC
           

        self.Qc = 0
        self.Pc = 0

        self.Ztf = self.R_t+1j*self.X_t
        self.Zc = self.PR_R+1j*self.PR_X
        if self.Bf != 0:
            self.Zf = 1/(1j*self.Bf)
        else:
            self.Zf = 0

        if self.R_t != 0:
            self.Y_tf = 1/self.Ztf
            self.Gtf = np.real(self.Y_tf)
            self.Btf = np.imag(self.Y_tf)
        else:
            self.Gtf = 0
            self.Btf = 0

        if self.PR_R != 0:
            self.Y_c = 1/self.Zc
            self.Gc = np.real(self.Y_c)
            self.Bc = np.imag(self.Y_c)
        else:
            self.Gc = 0
            self.Bc = 0

        if self.Zf != 0:
            self.Z2 = (self.Ztf*self.Zc+self.Zc *
                       self.Zf+self.Zf*self.Ztf)/self.Zf
        if self.Zc != 0:
            self.Z1 = (self.Ztf*self.Zc+self.Zc *
                       self.Zf+self.Zf*self.Ztf)/self.Zc
        if self.Ztf != 0:
            self.Z3 = (self.Ztf*self.Zc+self.Zc *
                       self.Zf+self.Zf*self.Ztf)/self.Ztf




        if name in AC_DC_converter.names:
            AC_DC_converter.ConvNumber -= 1
            raise NameError("Already used name '%s'." % name)

        if name is None:
            self._name = str(self.ConvNumber)
        else:
            self._name = name

        AC_DC_converter.names.add(self.name)
        self.Node_AC.connected_conv.add(self.ConvNumber)

        
    

class DC_DC_converter:
    ConvNumber = 0
    names = set()

    @classmethod
    def reset_class(cls):
        cls.ConvNumber = 0
        cls.names = set()

    
    @property
    def name(self):
        return self._name

    def __init__(self, element_type: str, fromNode: Node_DC, toNode: Node_DC, PowerTo: float, R: float, name=None):
        self.ConvNumber = DC_DC_converter.ConvNumber
        DC_DC_converter.ConvNumber += 1
        # type: (1=P, 2=droop, 3=Slack)
        self.type = element_type
        self.ConvNumber = DC_DC_converter.ConvNumber
        self.fromNode = fromNode
        self.toNode = toNode
        self.PowerTo = PowerTo
        self.R = R

        toNode.PconvDC += self.PowerTo
        self.Powerfrom = self.PowerTo+self.PowerTo**2*R

        fromNode.PconvDC -= self.Powerfrom

        
        if name is None:
            self._name = str(self.ConvNumber)
        else:
            self._name = name

        DC_DC_converter.names.add(self.name)

class Market:
    market_num = 0
    names = set()
    
    @classmethod
    def reset_class(cls):
        cls.market_num = 0
        cls.names = set()
    
    @property
    def name(self):
        return self._name
    
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value
        for node in self.nodes_AC:
            node.price=value
    
    def __init__(self,price=1,import_pu_L=1,export_pu_G=1,a=0,b=1,c=0,name=None):
        self.market_num = Market.market_num
        Market.market_num += 1
        
        self.import_pu_L=import_pu_L
        self.export_pu_G=export_pu_G
        self.nodes_AC=[]
        self._price=price
        self.a=a
        self.b=b
        self.c=c
        self.PGL_min=-np.inf
        self.PGL_max=np.inf
        self.df= pd.DataFrame(columns=['time','a', 'b', 'c','price','PGL_min','PGL_max'])        
        self.df.set_index('time', inplace=True)


        self.ImportExpand=0
        if name is None:
            self._name = str(self.TS_AC_num)
        else:
            self._name = name

        Market.names.add(self.name)

class TS_AC:
    TS_AC_num = 0
    names = set()
    
    @classmethod
    def reset_class(cls):
        cls.TS_AC_num = 0
        cls.names = set()
    
    @property
    def name(self):
        return self._name

    def __init__(self, element_type: str, element_MW: float, node: Node_AC, TS: float,market_attached, name=None):
        self.TS_AC_num = TS_AC.TS_AC_num
        TS_AC.TS_AC_num += 1
        
        
        self.type = element_type
        # type(Solar,WPP,Load)
        self.TS_AC_num = TS_AC.TS_AC_num
        self.node = node
        self.TS = TS
        self.market = market_attached

        self.element_MW = element_MW
       
        s = 1
        if name is None:
            self._name = str(self.TS_AC_num)
        else:
            self._name = name

        TS_AC.names.add(self.name)
