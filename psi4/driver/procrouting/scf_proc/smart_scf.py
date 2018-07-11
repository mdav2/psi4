from psi4.driver import p4util
from psi4.driver import constants
from psi4.driver.p4util.exceptions import ConvergenceError, ValidationError
from psi4 import core
from math import log

def scf_check_osc(self,Ediff,Drms):
    #Drms=self.compute_orbital_gradient(False, core.get_option('SCF','DIIS_MAX_VECS'))
    print('Routed through smart_scf!')
    if abs(log(abs(Ediff/Drms))) > 3:
        print('Quotient Condition triggered')

core.HF.check_osc=scf_check_osc
