from psi4.driver import p4util
from psi4.driver import constants
from psi4.driver.p4util.exceptions import ConvergenceError, ValidationError
from psi4 import core
from math import log

def scf_check_osc(self,Ediff,Drms):
    print('Routed through smart_scf!')
    #just an example of using last Ediff, Drms to make a decision
    if abs(log(abs(Ediff/Drms))) > 3:
        pass
    #just an example of doing something with history of energies
    if examine_energy_history():
        pass

def examine_energy_history(self):
    return sum(self.energy_history())
    pass
        

core.HF.check_osc=scf_check_osc
