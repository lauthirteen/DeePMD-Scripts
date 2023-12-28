import dpdata

# 会遍历所有文件夹下面的npy，并以list存在fp_data里面。每种化学式结构为一个列表值。
fp_data = dpdata.MultiSystems().load_systems_from_file("./", fmt="deepmd/npy/mixed")
for mol in fp_data:
    for frame in mol:
        energy = frame["energies"]
        atom_num = len(frame["atom_types"])
        energy_per_atom = energy[0]/atom_num
        if atom_num == 71 and energy_per_atom < -120 and energy_per_atom > -133:
            #print(energy_per_atom)
            frame.to("vasp/poscar", "POSCAR71")
