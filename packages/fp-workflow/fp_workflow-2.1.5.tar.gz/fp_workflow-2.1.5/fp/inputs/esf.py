#region: Modules.
import numpy as np 
from fp.schedulers import *
#endregion

#region: Variables.
#endregion

#region: Functions.
#endregion

#region: Classes.
class EsfInput:
    def __init__(
        self,
        job_desc,
    ):
        self.job_desc: JobProcDesc = job_desc

class EsfXctphInput:
    def __init__(
        self,
        job_desc,
        # eph_filename: str ='./eph.h5',
        # xct_filename: str ='./xct.h5',
    ):
        # self.eph_filename: str = eph_filename
        # self.xct_filename: str = xct_filename
        self.job_desc: JobProcDesc = job_desc
#endregion
