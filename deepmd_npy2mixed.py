import dpdata

file = dpdata.LabeledSystem("SiC", fmt="deepmd/npy")
file.to_deepmd_npy_mixed("SiC_mixed")
