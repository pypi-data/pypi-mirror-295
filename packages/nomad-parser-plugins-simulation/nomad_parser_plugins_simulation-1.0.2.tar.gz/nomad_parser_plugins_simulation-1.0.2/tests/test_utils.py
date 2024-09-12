# Copyright 2018 Markus Scheidgen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an"AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
import numpy as np

from nomad.units import ureg
from nomad.datamodel import EntryArchive
from simulationparsers.utils import BasicParser

class TestBasicParser:
    @pytest.fixture(scope='class')
    def onetep_parser(self):
        re_f = r'\-*\d+\.\d+E*\-*\+*\d+'
        return BasicParser(
            'ONETEP',
            units_mapping=dict(energy=ureg.hartree, length=ureg.bohr),
            auxilliary_files=r'([\w\-]+\.dat)',
            program_version=r'Version\s*([\d\.]+)',
            lattice_vectors=r'\%block lattice_cart\s*([\s\S]+?)\%endblock lattice_cart',
            atom_labels_atom_positions=rf'\%block positions\_abs\s*(\w+\s+{re_f}\s+{re_f}\s+{re_f}[\s\S]+?)\%endblock positions\_abs',
            XC_functional=r'xc\_functional\s*\:\s*(\w+)',
            energy_total=rf'Total energy\s*=\s*({re_f})\s*Eh')

    def test_onetep_parser(self, onetep_parser):
        archive = EntryArchive()
        onetep_parser.parse('tests/data/onetep/fluor/12-difluoroethane.out', archive, None)

        assert archive.run[0].program.version == '4.5.3.32'
        assert len(archive.run[0].calculation) == 4
        sec_system = archive.run[0].system[0]
        assert sec_system.atoms.labels[7] == 'H'
        assert np.shape(sec_system.atoms.positions) == (8, 3)
