"""
SUB: Nozzle
July 2020
A. Takken
"""

import numpy as np

import SUB_muPandkP
import SUB_cp

def fun1(pc,mdot,R_A,MMP,Tpo,pamb,g0,propellant,NISTP,limitsP): 

    muP = SUB_muPandkP.fun1(propellant,Tpo)[0]                                              #[Pa s], dynamic viscosity
    cpP = SUB_cp.fun1(Tpo,NISTP,limitsP,MMP)                                                #[J/kg/K], specific heat at constant pressure

    gamma = cpP/(cpP-R_A/MMP)                                                               #[-], specific heat ratio
    Gamma = np.sqrt(gamma)*(2/(gamma+1))**((gamma+1)/(2*(gamma-1)))                         #[-], Vandenkerckhove function

    #Is the flow choked?         
    pe = pamb                                                                               #[Pa], ideal expansion
    critRatio = (2/(gamma+1))**(gamma/(gamma-1))                                            #[Pa], critical ratio (pressure)
    if pamb > critRatio*pc:
        print("Not choked flow!")  
          
    At = mdot*np.sqrt(R_A/MMP*Tpo)/(Gamma*pc)                                                   #[m2], nozzle throat area                                           
    Aratio = Gamma/np.sqrt(2*gamma/(gamma-1)*(pe/pc)**(2/gamma)*(1-(pe/pc)**((gamma-1)/gamma))) #[-], area ratio (Ae/At)    
    Ae = At*Aratio                                                                              #[m2], nozzle exit area
    Ue = np.sqrt(2*gamma/(gamma-1)*R_A/MMP*Tpo*(1-(pe/pc)**((gamma-1)/gamma)))                  #[m/s], exit velocity

    Ueq = Ue + (pe-pamb)/mdot*Ae                                                            #[m/s], equivalent velocity
    F = mdot*Ueq                                                                            #[N], thrust
    Isp = Ueq/g0                                                                            #[s], specific impulse
    ReT = 4*mdot/(np.pi*np.sqrt(4*At/np.pi)*muP)                                            #[-], throat Reynolds number
    
    return(F,Isp,ReT,At,Ae)
