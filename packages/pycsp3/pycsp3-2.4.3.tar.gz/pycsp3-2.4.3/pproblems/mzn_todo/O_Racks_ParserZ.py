from pycsp3.problems.data.parsing import *
import re
import re


def read_value(l):
    s = l[l.index('=') + 2:-1]
    return n if s == "MAXNROFOBJECTS" else int(s)


data['usecc'] = "true" in line()
data['n'] = n = number_in(next_line())
for key in ["CLASS_Configuration_MIN",
            "CLASS_Configuration_MAX",
            "CLASS_Element_MIN",
            "CLASS_Element_MAX",
            "CLASS_ElementA_MIN",
            "CLASS_ElementA_MAX",
            "CLASS_ElementB_MIN",
            "CLASS_ElementB_MAX",
            "CLASS_ElementC_MIN",
            "CLASS_ElementC_MAX",
            "CLASS_ElementD_MIN",
            "CLASS_ElementD_MAX",
            "CLASS_Frame_MIN",
            "CLASS_Frame_MAX",
            "CLASS_Module_MIN",
            "CLASS_Module_MAX",
            "CLASS_ModuleI_MIN",
            "CLASS_ModuleI_MAX",
            "CLASS_ModuleII_MIN",
            "CLASS_ModuleII_MAX",
            "CLASS_ModuleIII_MIN",
            "CLASS_ModuleIII_MAX",
            "CLASS_ModuleIV_MIN",
            "CLASS_ModuleIV_MAX",
            "CLASS_ModuleV_MIN",
            "CLASS_ModuleV_MAX",
            "CLASS_Rack_MIN",
            "CLASS_Rack_MAX",
            "CLASS_RackDouble_MIN",
            "CLASS_RackDouble_MAX",
            "CLASS_RackSingle_MIN",
            "CLASS_RackSingle_MAX"]:
    data[key] = read_value(next_line())
