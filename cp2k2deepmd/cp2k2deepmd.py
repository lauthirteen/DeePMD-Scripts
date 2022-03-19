#!/usr/bin/env python3

from ase.io import read
import numpy as np
import os, sys
import glob
import shutil


#############################
# USER INPUT PARAMETER HERE #
#############################

# input data path here, string, this directory should contains
#   ./data/*frc-1.xyz ./data/*pos-1.xyz ./data/*-1.cell ./data/*-1.stress 
data_path = "./"
# input atom type map
atom_type_map = ["H", "O", "Mg"]


# conversion unit here, modify if you need
au2eV = 2.72113838565563E+01
au2A = 5.29177208590000E-01
bar2GPa = 1.00E-04
# "eV/angstrom^3" to "GPa"
GPa = 160.2176634
####################
# START OF PROGRAM #
####################

def xyz2npy(pos, atom_num, output, name, unit_convertion=1.0):
    total = np.empty((0,atom_num*3), float)
    for single_pos in pos:
        tmp=single_pos.get_positions()
        tmp=np.reshape(tmp,(1,atom_num*3))
        total = np.concatenate((total,tmp), axis=0)
    total = total * unit_convertion
    np.savetxt(name, total, delimiter=' ', fmt='%.18e')
    np.save(output, total)
    return len(total)

def energy2npy(pos, output, name, unit_convertion=1.0):
     total = np.empty((0), float)
     for single_pos in pos:
         tmp=single_pos.info.pop('E')
         tmp=np.array(tmp,dtype="float64")
         tmp=np.reshape(tmp,1)
         total = np.concatenate((total,tmp), axis=0)
     total = total * unit_convertion
     np.savetxt(name, total, delimiter=' ', fmt='%.18e')
     np.save(output,total)
     return len(total)

def cell2npy(output, cell, name, unit_convertion=1.0):
    total = cell * unit_convertion
    np.savetxt(name, total, delimiter=' ', fmt='%.18e')
    np.save(output,total)
    return len(total)

def type_raw(single_pos, output_type, output_type_map, atom_type_map):
    element = single_pos.get_chemical_symbols()
    type_list = []
    for index, atom1 in enumerate(atom_type_map):
        for atom2 in element:
            if atom1 == atom2:
                type_list.append(index)
    np.savetxt(output_type, np.array(type_list), delimiter=' ', fmt='%s')
    np.savetxt(output_type_map, np.array(atom_type_map), delimiter=' ', fmt='%s')

def virial2npy(output_npy, output_raw, volume, stress, unit_convertion):
    # bar to GPa
    stress = stress * unit_convertion
    assert(len(stress) == len(volume))
    for i in range(len(stress)):
        stress[i] = stress[i] * volume[i]
    np.savetxt(output_raw, stress, delimiter=' ', fmt='%.18e')
    np.save(output_npy, stress)
    return len(stress)

# read the pos and frc
data_path = os.path.abspath(data_path)
pos_path = os.path.join(data_path, "*pos-1.xyz")
frc_path = os.path.join(data_path, "*frc-1.xyz")
cell_path = os.path.join(data_path, "*-1.cell")
stress_path = os.path.join(data_path, "*-1.stress")
#print(data_path)
pos_path = glob.glob(pos_path)[0]
frc_path = glob.glob(frc_path)[0]
cell_path = glob.glob(cell_path)[0]
stress_path = glob.glob(stress_path)[0]


#print(pos_path)
#print(frc_path)
pos = read(pos_path, index = ":" )
frc = read(frc_path, index = ":" )
cell1 = np.loadtxt(cell_path)
stress1 = np.loadtxt(stress_path)

cell = cell1[:, 2:11]
stress = stress1[:, 2:11]
volume = cell1[:, 11]
# numpy path
set_path = os.path.join(data_path, "set.000")
if os.path.isdir(set_path):
    print("detect directory exists: %s\n now remove it" % "set.000")
    shutil.rmtree(set_path)
    os.mkdir(set_path)
else:
    print("detect directory doesn't exist: %s \n now create it" % "set.000")
    os.mkdir(set_path)

raw_path = os.path.join(data_path, "03.deepmd_raw")
if os.path.isdir(raw_path):
    print("detect directory exists: %s \n now remove it" % "03.deepmd_raw")
    shutil.rmtree(raw_path)
    os.mkdir(raw_path)
else:
    print("detect directory doesn't exist: %s \n now create it" % "03.deepmd_raw")
    os.mkdir(raw_path)


type_raw_path = os.path.join(raw_path, "type.raw")
type_map_raw_path = os.path.join(raw_path, "type_map.raw")
coord_raw_path = os.path.join(raw_path, "coord.raw")
force_raw_path = os.path.join(raw_path, "force.raw")
energy_raw_path = os.path.join(raw_path, "energy.raw")
box_raw_path = os.path.join(raw_path, "box.raw")
virial_raw_path = os.path.join(raw_path, "virial.raw")

coord_path = os.path.join(set_path, "coord.npy")
force_path = os.path.join(set_path, "force.npy")
virial_path = os.path.join(set_path, "virial.npy")
box_path = os.path.join(set_path, "box.npy")
energy_path = os.path.join(set_path, "energy.npy")


#input the number of atom in system
with open(pos_path) as f:
    atom_num = int(f.readline())

#tranforrmation
pos_len = xyz2npy(pos, atom_num, coord_path, coord_raw_path)
frc_len = xyz2npy(frc, atom_num, force_path, force_raw_path, au2eV/au2A)
virial_len = virial2npy(virial_path, virial_raw_path, volume, stress, bar2GPa/GPa)
ener_len = energy2npy(pos, energy_path, energy_raw_path, au2eV)
box_len = cell2npy(box_path, cell, box_raw_path)
type_raw(pos[0], type_raw_path, type_map_raw_path, atom_type_map)
shutil.move("set.000", "03.deepmd_raw")

assert(pos_len == frc_len)
assert(pos_len == box_len)
assert(pos_len == virial_len)
