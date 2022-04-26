#!/usr/bin/env python3

import os
import numpy as np

total_frame = 10000
begin_frame = 0
skip_frame = 100
atom_num = 720


os.system("rm -rf 01.cp2k.fp")
os.system("mkdir 01.cp2k.fp")


i = 0
while begin_frame <= total_frame:
    begin_line = (atom_num + 9) * begin_frame + 1 + 9
    end_line = (atom_num + 9) * (begin_frame + 1)
    print("Processing: %s/%s" % (begin_frame, total_frame))
    os.system("sed -n '%s, %sp' traj.lammpstrj > %s.xyz" % (begin_line, end_line, begin_frame))
    
    file = np.loadtxt("%s.xyz" % begin_frame)
    H_list = []
    O_list = []
    Mg_list = []
    for atom_info in file:
        if int(atom_info[1]) == 1:
            H_list.append(atom_info[2:])
        elif int(atom_info[1]) == 2:
            O_list.append(atom_info[2:])
        elif int(atom_info[1]) == 3:
            Mg_list.append(atom_info[2:]) 
        else:
            print("Atom type is not in list")
            sys.exit()
    new_file=open("tmp_%s.xyz" %  begin_frame,mode='w+')
    for H in H_list:
        new_file.write("%5s%13.6f%13.6f%13.6f\n" % ("H", H[0], H[1], H[2]))
    for O in O_list:
        new_file.write("%5s%13.6f%13.6f%13.6f\n" % ("O", O[0], O[1], O[2]))
    for Mg in Mg_list:
        new_file.write("%5s%13.6f%13.6f%13.6f\n" % ("Mg", Mg[0], Mg[1], Mg[2]))
    new_file.close()
    n = str("%06d" % i)
    os.makedirs('01.cp2k.fp/%s' % n)
    os.system("mv tmp_%s.xyz  01.cp2k.fp/%s/coord.xyz" % (begin_frame, n))
    os.system("cp Water-MgOH2-SP.inp  01.cp2k.fp/%s" % (n))    
    os.system("rm %s.xyz" % begin_frame)
    i += 1
    begin_frame += skip_frame
