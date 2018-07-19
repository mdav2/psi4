from psi4.driver import p4util
from psi4.driver import constants
from psi4.driver.p4util.exceptions import ConvergenceError, ValidationError
from psi4 import core
from math import log

#def scf_check_osc(self,Ediff,Drms):
#    print('Routed through smart_scf!')
#    #just an example of using last Ediff, Drms to make a decision
#    if abs(log(abs(Ediff/Drms))) > 3:
#        pass
#    #just an example of doing something with history of energies
#    if examine_energy_history():
#        pass
#
#def examine_energy_history(self):
#    return sum(self.energy_history())
#    pass
        
class smart_solver():
    """How do I write a class description"""

    def __init__(self, wfn):
        self.wfn=wfn
        self._validate_smart()
        self.E_history=[]
        self.Drms_history=[]
        self.smart_level=self.wfn.smart_level
        self.opt_dict=smart_options_dict[self.smart_level]
        pass

    def smart_iter(self,SCFE,Drms):
        """Called every iteration to update energy history,
        density history, and call decision making methods.
        """
        self.update_E_history()
        self.update_Drms_history(Drms)
        if not self.initdamp():
            self.noise_damp()
            #self.osc_damp
            self.trailing_conv()
            
        
    def dyn_damp(self):
        #dynamic damping based off energy and drms history

    def noise_damp(self):
        #for automatically detecting noisy scf and switching on dynamic damping

    def trailing_conv(self):
        #for auto detect trailing convergence and switching on SOSCF

    def osc_detect(self):
        #for auto detect oscillations (two point first, later others)
        #Wouldn't this be picked up by noise_damp anyway?

    def smart_guess(self):
        basis_guess = core.get_option('SCF',"BASIS_GUESS")
        guess_opt = core.get_option('SCF',"GUESS")
        do_castup = self.opt_dict["CASTUP"]
        if do_castup:
            castup_basis = self.opt_dict["CASTUP_BASIS"]
            core.set_option('SCF',"BASIS_GUESS",True) 

    def initdamp(self):
        #decides whether to damp initial iterations in SCF and returns 
        #True if initial damping occured, False otherwise
        if self.wfn.iteration > 4:
            return False
        guess_opt = core.get_option('SCF',"GUESS")
        if (guess_opt == 'SAD' or guess_opt == 'GWH' or guess_opt == 'CORE')\
            and (self.wfn.iteration_ < 4 and self.wfn.iteration_ > 1):
            self.wfn.damping_enabled=self.opt_dict['init_damp']
            self.wfn.damping_percentage=self.opt_dict['init_damp_percentage']
            return True

    def update_E_history(self):
        self.E_history.append(self.wfn.get_energies("Total Energy"))

    def update_Drms_history(self,Drms):
        self.Drms_history.append(Drms)

    def _validate_smart(self):

        """Sanity-check smartSCF options

        Raises
        ------
        ValidationError
            If soscf, damping, DIIS, or other convergence settings don't match
            between user defined settings and smart recommendations, do:
                smart=0 -> no action, smart is desabledchange local.
                smart=1 -> resolve diff by falling to smartscf recommendations, print a notice in output.
                smart>=2 -> resolve diff by falling back to user defined settings
                            for non-smartscf defined values.
        Returns
        -------
        bool
            whether smart was able to resolve differences. Changes local scfiter options if discrepancy. 
        """

        pass

smart_options_dict = {
            1:
            {
                "CASTUP":True,
                "CASTUP_BASIS":'3-21G',
                "SOSCF_dE":1e-5,
                "SOSCF_quotient":3,
                "init_damp":True,
                "init_damp_percentage":40.0,
                "noise_crit_damp":5e-2,#STDEV(last 3 iterations)/AVG(last 3 iterations)
                "SOSCF_maxiter":25,
                "SOSCF_maxiter_dynamic":True,
                "oscillation_detect":True,#currently only 2 point oscillation detected
                "oscillation_thresh":1e-5
            },
            2: 
            {
                "SOSCF_dE":1e-5,
                "SOSCF_quotient":3
            },
            'COMMON':
            {
                "tight_e_conv":1e-9,
                "tight_d_conv":1e-9
            }
        }
            
        

                
    
