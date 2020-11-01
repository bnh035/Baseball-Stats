#!/usr/bin/env python

""" Baseball Stats Headstring
    ==================
Date Started: 22 October 2020
"""

__author__ = "Brice Hilliard"
__version__ = "0.1"
__email__ = "bricehilliard035@gmail.com"
__production__ = "development"

import pandas as pd
import matplotlib.pyplot as plt
from BaseballNames import players, umpires, grounds, player_colours
from StatDicts import ResultsOpts, BatStats
from processing import add_cum_batting_avg, process_data, cumstat_df
from stat_plot import plot_avg
from in_out import import_data, clean_data, print_outcomes

def main():
    a1, a2 = import_data()
    a3 = clean_data(a1, a2)
    sDF = cumstat_df(a3)
    a4, a5 = process_data(a3)
    print_outcomes(a4, a5)
    plot_avg(sDF)

if __name__ == '__main__':
    main()
