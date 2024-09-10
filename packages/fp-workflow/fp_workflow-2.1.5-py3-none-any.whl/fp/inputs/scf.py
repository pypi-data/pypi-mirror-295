#region: Modules.
import numpy as np 
from fp.schedulers import *
#endregion

#region: Variables.
#endregion

#region: Functions.
#endregion

#region: Classes.
class ScfInput:
    def __init__(
        self,
        kdim,
        ecutwfc, 
        job_desc,
        is_spinorbit: bool=False,
        num_bands: int =None,
    ):
        self.kdim:np.ndarray = np.array(kdim) 
        self.ecutwfc:float = ecutwfc
        self.is_spinorbit: bool = is_spinorbit
        self.job_desc: JobProcDesc = job_desc
        self.num_bands: int = num_bands

    def get_kgrid(self):
        output = ''
        output += 'K_POINTS automatic\n'
        output += f'{int(self.kdim[0])} {int(self.kdim[1])} {int(self.kdim[2])} 0 0 0\n'
        
        return output 
#endregion
