
# from ChemMod.equation import equation
# from ChemMod.plot import plot
# from ChemMod import ChemMod

import numpy as np
import matplotlib.pyplot as plt

__all__ = [s for s in dir() if not s.startswith("_")]


from ChemMod.plot._arrhenius_plot import arrhenius_plot
from ChemMod.plot._bjerrum_plot import bjerrum_plot
from ChemMod.plot._gibbs_plot import gibbs_plot
from ChemMod.plot._order_plot import order_plot
from ChemMod.plot._theme_data import theme_data
from ChemMod.plot._theme import theme


from ChemMod.equation import __all__

theme_list_for_formatting_of_plots = ['teal', 1, 'teal', 'teal', 'viridis', 'teal', 'teal', 'paleturquoise', 'lightcyan', 'paleturquoise']
