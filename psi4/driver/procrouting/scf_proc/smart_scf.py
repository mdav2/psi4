from psi4.driver import p4util
from psi4.driver import constants
from psi4.driver.p4util.exceptions import ConvergenceError, ValidationError
from psi4 import core
from math import log
        
class smart_solver():
    """Purpose: enable easy extension of "smart" SCF solving capabilities.
    This class is an attribute of a wfn object ... a wfn object is also\
            an attribute of this class for easy data transfer.

    Methods:
        __init__: creates objects to hold energy and density history
        smart_iter: one stop method call placed in .iterations() function\
                makes decisions about convergence tools

        trailing_conv: is the SCF stuck in trailing convergence?\
                if so, turn on SOSCF and some damping.

        init_damp: is the guess case SAD, GWH, or CORE? if so, damp the \
                initial SCF iterations to remove wild energy changes.
                Currently set at 70%, a la ORCA, could fine tune a bit.

        smart_guess: makes a best stab at the guess density in the  case\
                that the user does not specify a guess method.

    Attributes:
        E_history: simple list of SCF energies in the current set of iterations.
        Drms_history: simple list of Drms values in the current set of iterations.
        opt_dict: Dictionary to hold convergence tools enabled at different\
                values of 'smart_level' a la OPTKING's dynamic_level
        smart_level: Level of effort to be expended to get SCF convergence\
                a la OPTKING dynamic_level

    Notes:
        smart_level and opt_dict are not necessary for initial PR, but may be nice to have later on.

        The goal with having this class exist at all is to nicely contain\
                tools for scf convergence in one spot. Extensibility\
                could go something like this:

                    1. add a method to smart_solver class:
                        def great_convergence(self):
                            great convergence tricks

                    2. simply add a call in smart_iter to incorporate it into\
                            smart_scf.

                    3. You're done!
    """

    def __init__(self, wfn):
        self.wfn=wfn
        self._validate_smart()
        self.E_history=[]
        self.Drms_history=[]
        self.smart_level=self.wfn.smart_level #not necessary
        self.opt_dict=smart_options_dict[self.smart_level] #not necessary
        pass

    def smart_iter(self,SCFE,Drms):
        """Called every iteration to update energy history,
        density history, and call decision making methods.
        """
        self.update_E_history()
        self.update_Drms_history(Drms)
        if not self.initdamp():
            self.trailing_conv()
        
    def trailing_conv(self):
        #for auto detect trailing convergence and switching on SOSCF
        if self.wfn.iteration_ > 15 and core.get_options('SCF','E_CONVERGENCE') < 1.0E-8:
            self.wfn.soscf_enabled = True
            self.wfn.damping_enabled = True
            self.wfn.damping_percentage = 25
        pass

    def initdamp(self):
        #decides whether to damp initial iterations in SCF and returns 
        #True if initial damping occured, False otherwise
        if self.wfn.iteration_ > 4:
            return False
        guess_opt = core.get_option('SCF',"GUESS")
        if (guess_opt in {'SAD','GWH','CORE'}) and self.wfn.iteration_ in range(0,4):
            self.wfn.damping_enabled=self.opt_dict['init_damp']
            self.wfn.damping_percentage=self.opt_dict['init_damp_percentage']
            return True

    def smart_guess(self):
        do_castup = self.opt_dict["CASTUP"]
        if do_castup:
            castup_basis = self.opt_dict["CASTUP_BASIS"]
            core.set_option('SCF',"BASIS_GUESS",True) 

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

#smart_options_dict is just an idea for adding 'tiers' of convergence\
        #tricks, where the key is the 'smart_level' and the value is another\
        #dictionary of various convergence options and/or values for things\
        #like damping percentage etc. 

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
            
        

                
    
