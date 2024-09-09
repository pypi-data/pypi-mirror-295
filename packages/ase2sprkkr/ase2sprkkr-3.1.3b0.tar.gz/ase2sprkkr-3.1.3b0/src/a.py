
from dataclasses import is_dataclass

import numpy as np

from ase.build import bulk, cut, fcc111
from ase.cell import Cell
from ase.geometry import get_layers, wrap_positions
from ase.spacegroup import crystal, get_spacegroup
from ase.spacegroup import crystal
from ase.utils import atoms_to_spglib_cell


ag = crystal(['Ag'], basis=[(0, 0, 0)], spacegroup=225, cellpar=4.09)
si = crystal(['Si'], basis=[(0, 0, 0)], spacegroup=227, cellpar=5.43)
assert get_spacegroup(ag).no == 225
assert get_spacegroup(si).no == 227
import spglib
for atoms, no_ref in zip([ag, si], [225, 227]):
    dataset = spglib.get_symmetry_dataset(atoms_to_spglib_cell(atoms))
    breakpoint()
