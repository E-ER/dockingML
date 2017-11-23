# -*- coding: utf-8 -*-

import os
from .convert import Convert
from .features import *
from .gold import GoldResults
from .mol2IO import Mol2IO
from .filter_mol2 import FilterMol2
from .index import *
from .algorithms import *
from .pdbIO import *

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DEFINITIONS_ROOT = os.path.join(PROJECT_ROOT, 'sample', 'lib')


