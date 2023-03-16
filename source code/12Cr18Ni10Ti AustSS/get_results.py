#!/usr/bin/python
#-- coding:utf8 --

from abaqus import getInput,getInputs
from odbAccess import *
from abaqusConstants import *
from textRepr import *

# odb file path
odb = openOdb(path = odbname)
frame_length = len(odb.steps.values()[-1].frames)

# extract data
fixSet = odb.rootAssembly.instances['PART-1-1'].nodeSets['LOAD']
fullSet = odb.rootAssembly.instances['PART-1-1'].elementSets['FULL'] #use upper case here
RF33 = [0]*frame_length
U3   = [0]*frame_length
fraction = [0]*frame_length
for j in range(0,frame_length):
    field_RF = odb.steps.values()[-1].frames[j].fieldOutputs['RF']
    field_U = odb.steps.values()[-1].frames[j].fieldOutputs['U']
    field_fraction = odb.steps.values()[-1].frames[j].fieldOutputs['SDV25']
    subField_RF = field_RF.getSubset(region = fixSet)
    subField_U = field_U.getSubset(region = fixSet)
    subField_fraction = field_fraction.getSubset(region = fullSet)
    sum_RF = 0
    sum_U = 0
    sum_f = 0
    n = 0
    nn = 0
    for val_1 in subField_RF.values:
        sum_RF = sum_RF + val_1
    for val_1 in subField_U.values:
        sum_U = sum_U + val_1
        n = n + 1
        
    for val_1 in subField_fraction.values:
        sum_f = sum_f + val_1
        nn = nn + 1

    RF = sum_RF
    U = sum_U

    # Output
    labels_RF = field_RF.componentLabels
    labels_U = field_U.componentLabels
    RF33[j] =  sum_RF.data[2]
    U3[j]   =  sum_U.data[2]
    U3[j] = U3[j]/n
    fraction[j] = sum_f.data/nn

str_RF33 = str(RF33)
str_U3   = str(U3)
str_f = str(fraction)

odb.close()