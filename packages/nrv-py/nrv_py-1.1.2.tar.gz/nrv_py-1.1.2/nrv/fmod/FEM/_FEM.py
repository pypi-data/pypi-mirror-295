"""
NRV-:class:`.FEM_model` handling.
"""

from abc import abstractmethod

from ...backend._MCore import MCH
from ...backend._log_interface import pass_info, rise_warning
from ...backend._NRV_Class import NRV_class

###############
## Constants ##
###############
fem_verbose = True


###################
## Model classes ##
###################
class FEM_model(NRV_class):
    """
    A generic class for Finite Element models
    """

    @abstractmethod
    def __init__(self, Ncore=None):
        """
        Creates a instance of FEM_model

        Parameters
        ----------
        Ncore   : int
            number of cores for computation. If None is specified, this number is taken from the NRV2.ini configuration file. Byu default set to None
        """
        super().__init__()
        self.Ncore = Ncore
        self.is_multi_proc = False
        self.type = "FEM"

        # Timmers
        self.meshing_timer = 0
        self.setup_timer = 0
        self.solving_timer = 0
        self.access_res_timer = 0

        # Flags
        self.is_meshed = False
        self.is_computed = False

    def get_timers(self, verbose=False):
        """
        Returns the timers of each step of the FEM computation

        Parameters
        ----------
        verbose     : bool
            if true, timer are also passed to the log and the terminal (if verbosity level > 2)

        Returns
        -------
        meshing_timer   : float
            time spent to mesh the FEM problem, in s
        setup_timer   : float
            time spent to mesh the setup (i.e. generating variab connecting to the server), in s
        solving_timer   : float
            time spent to mesh the FEM problem, in s
        total_timer   : float
            time spent to mesh the FEM problem, in s
        """
        pass_info("mesh done in " + str(self.meshing_timer) + " s")
        pass_info("simulation setup in " + str(self.setup_timer) + " s")
        pass_info("simulation solved in " + str(self.solving_timer) + " s")
        pass_info("Time spent to access results " + str(self.access_res_timer) + " s")
        total_timer = (
            self.meshing_timer
            + self.setup_timer
            + self.solving_timer
            + self.access_res_timer
        )
        pass_info("total duration " + str(total_timer) + " s")
        return self.meshing_timer, self.setup_timer, self.solving_timer, total_timer

    def set_Ncore(self, N):
        """
        Set the number of cores to use for the FEM

        Parameters
        ----------
        N       : int
            Number of cores to set
        """
        if isinstance(N, bool):
            if N:
                N = MCH.size
            else:
                N = 1
        if N is None:
            N = 1
        self.Ncore = N
        if self.Ncore > MCH.size:
            rise_warning(
                "MCH size is " + str(MCH.size) + " cannot set FEM on more processes"
            )
            self.Ncore = MCH.size
        self.is_multi_proc = self.Ncore > 1
