#1 git clone https://gitlab.com/1041176461/ase-abacus.git
#2 cd ase-abacus
#3 python3 setup.py install
from ase.calculators.abacus import Abacus
from ase.io import read, write
from pathlib import Path

from ase.io import read, write
from pathlib import Path

cs_dir = './'
cs_stru = Path(cs_dir, 'STRU')
cs_atoms= read( cs_stru, format='abacus')
cs_vasp = Path(cs_dir, 'STRU.cif')
write(cs_vasp, cs_atoms, format='cif')
