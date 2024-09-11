"""
Minizinc 2016 and 2018

TODO : Not finished ; very complex to understand and to translate
"""

from pycsp3 import *

print(data)
(usecc, MAXNROFOBJECTS, CLASS_Configuration_MIN, CLASS_Configuration_MAX, CLASS_Element_MIN, CLASS_Element_MAX, CLASS_ElementA_MIN, CLASS_ElementA_MAX,
 CLASS_ElementB_MIN,
 CLASS_ElementB_MAX, CLASS_ElementC_MIN, CLASS_ElementC_MAX, CLASS_ElementD_MIN, CLASS_ElementD_MAX, CLASS_Frame_MIN, CLASS_Frame_MAX, CLASS_Module_MIN,
 CLASS_Module_MAX, CLASS_ModuleI_MIN, CLASS_ModuleI_MAX, CLASS_ModuleII_MIN, CLASS_ModuleII_MAX, CLASS_ModuleIII_MIN, CLASS_ModuleIII_MAX, CLASS_ModuleIV_MIN,
 CLASS_ModuleIV_MAX, CLASS_ModuleV_MIN, CLASS_ModuleV_MAX, CLASS_Rack_MIN, CLASS_Rack_MAX, CLASS_RackDouble_MIN, CLASS_RackDouble_MAX, CLASS_RackSingle_MIN,
 CLASS_RackSingle_MAX) = data

NROFCLASSES = 16
(CLASS_Configuration, CLASS_Element, CLASS_ElementA, CLASS_ElementB, CLASS_ElementC, CLASS_ElementD, CLASS_Frame, CLASS_Module, CLASS_ModuleI, CLASS_ModuleII, \
 CLASS_ModuleIII, CLASS_ModuleIV, CLASS_ModuleV, CLASS_Rack, CLASS_RackDouble, CLASS_RackSingle) = range(16)  # 1, 17)

nClasses = NROFCLASSES + 1  # +1 for unused class
nObjects = MAXNROFOBJECTS + 1


def isA(CLASS, object):
    return (object >= start[leafclass_min[CLASS]]) & (object < start[leafclass_max[CLASS] + 1])


# def isA3(object, assoc, CLASS):
#   forall(o in OBJECTS) (if (assoc[o] = object) then isA(CLASS,o) else true endif);


leafclass_min = VarArray(size=nClasses, dom=range(nClasses))

leafclass_max = VarArray(size=nClasses, dom=range(nClasses))

# first possible index for class
start = VarArray(size=nClasses, dom=range(nObjects))

# nr of instances of class
nrofobjects = VarArray(size=nClasses, dom=range(nObjects))

Module_element = VarArray(size=nObjects - 1, dom=range(nObjects))

Element_modules_count = VarArray(size=nObjects - 1, dom=range(nObjects))

satisfy(
    # ensuring that start indices are ordered
    [Increasing(start), start[0] == 0],

    # first objectid is at first leafclass object id
    [start[c] == start[leafclass_min[c]] for c in range(nClasses)],

    # nrofobjects is the difference between start of first leafclass and start of next leafclass
    [nrofobjects[c] == start[leafclass_max[c] + 1] - start[leafclass_min[c]] for c in range(nClasses - 1)],

    # the remaining objects are unused
    nrofobjects[-1] == nObjects - start[-1],

    # root class
    nrofobjects[CLASS_Configuration] == 1,

    # [(isA(CLASS_ElementA,o) == 0) | (isA(o,Module_element,CLASS_ModuleI)) for o in range(nObjects-1)],

)
