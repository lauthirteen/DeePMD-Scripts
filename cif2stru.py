#1 git clone https://gitlab.com/1041176461/ase-abacus.git
#2 cd ase-abacus
#3 python3 setup.py install
from ase.calculators.abacus import Abacus
from ase.io import read, write
from pathlib import Path

cs_dir = './'
cs_vasp = Path(cs_dir, 'Si.cif')
cs_atoms = read(cs_vasp, format='cif')
cs_stru = Path(cs_dir, 'STRU')
pp = {'Si':'./Si_ONCV_PBE-1.0.upf'}
basis = {'Si':'./Si_gga_8au_100Ry_3s3p2d.orb'}
write(cs_stru, cs_atoms, format='abacus', pp=pp, basis=basis)
