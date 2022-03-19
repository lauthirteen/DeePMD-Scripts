#!/bin/env python3

import dpdata
import os, sys
import glob
import pathlib

def get_raw(work_path, outfile_name, outfile_frmat):
    if outfile_frmat == "QE":
        fmt_in = "qe/pw/scf"
    if outfile_frmat == "VASP":
        fmt_in = "vasp/outcar"
    if outfile_frmat == "CP2K":
        fmt_in = "cp2k/output"

    final_sys = None
    dir_list = []
    file_list = os.listdir(work_path)
    file_list.sort()

    for file in file_list:
        cur_path = os.path.join(work_path, file)
        #print(cur_path)
        if os.path.isdir(cur_path):
            dir_list.append(cur_path)
        #print(dir_list)
    #num = 0
    dir_list.sort()
    for dirs in dir_list:
        fp_outfile = dirs + '/' + outfile_name
        #print(fp_outfile)
        if pathlib.Path(fp_outfile).is_file() == False:
            print("!!! Error: '%s' No such file" % fp_outfile)
            sys.exit()
        sys_1 = dpdata.LabeledSystem(fp_outfile, fmt=fmt_in)
        #print("test")
        if len(sys_1) != 1:
            print("!!! Error: '%s' file is incorrect" % fp_outfile)
            #sys.exit()
            #file_list.remove(str("%06d" % num))
            continue
        if final_sys is None:
            final_sys = sys_1
        else:
            final_sys.append(sys_1)
    #num += 1

    if (len(final_sys) == 0):
        print("!!! Error: No raw file can be product")
        sys.exit()
    #print(file_list)
    return final_sys

if __name__ == '__main__':
    ##########################
    work_path = "./01.cp2k.fp"
    outfile_name = "output.log"
    outfile_frmat = "CP2K"   # only QE or VASP or CP2K
    ##########################
    final_sys = get_raw(work_path, outfile_name, outfile_frmat)
    print(final_sys)
    #dir_num = 0
    print("\n### Following dirs is: %s\n" % ('03.deepmd_raw/'))
    #print(final_sys[dir_num])
    print(len(final_sys))
    final_sys.to_deepmd_raw('03.deepmd_raw/')
    final_sys.to_deepmd_npy('03.deepmd_raw/', set_size=len(final_sys))
    #dir_num += 1
    #########################

