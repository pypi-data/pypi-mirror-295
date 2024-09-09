
# from ChemMod.equation import equation
# from ChemMod.plot import plot
# from ChemMod import ChemMod

import numpy as np
import matplotlib.pyplot as plt

__all__ = [s for s in dir() if not s.startswith("_")]


from ChemMod.plot import _arrhenius_plot
from ChemMod.equation import __all__

theme_list_for_formatting_of_plots = ['teal', 1, 'teal', 'teal', 'viridis', 'teal', 'teal', 'paleturquoise', 'lightcyan', 'paleturquoise']
