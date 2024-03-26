import dpdata

file = dpdata.LabeledSystem("./SiC_scf", fmt="abacus/scf")
file.to_deepmd_raw("SiC")
file.to_deepmd_npy("SiC")
