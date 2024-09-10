#region: Modules.
import numpy as np 
from fp.schedulers import *
from fp.structure.kpath import KPath
from ase.dft.kpoints import get_special_points
#endregion

#region: Variables.
#endregion

#region: Functions.
#endregion

#region: Classes.
class PhbandsInput:
    def __init__(
        self,
        kpath,
        job_desc,
    ):
        self.kpath: KPath = kpath
        self.job_desc: JobProcDesc = job_desc
        
    def get_kpath_str(self):
        # TODO. 
        pass 
        # output = ''
        # output += f'{self.kpath.shape[0]}\n'
        
        # for row in self.kpath:
        #     output += f'{row[0]:15.10f} {row[1]:15.10f} {row[2]:15.10f}\n'
        
        special_points = get_special_points(self.kpath.atoms.cell)

        output = ''
        output += f'{len(self.kpath.path_special_points)}\n'

        for path_special_point in self.kpath.path_special_points:
            coord = special_points[path_special_point]
            output += f'{coord[0]:15.10f} {coord[1]:15.10f} {coord[2]:15.10f} {self.kpath.path_segment_npoints} !{path_special_point}\n'
        
        return output 
#endregion
