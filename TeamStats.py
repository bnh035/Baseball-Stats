#!/usr/bin/env python

""" Baseball Stats Headstring
    ==================
Date Started: 22 October 2020
"""

__author__ = "Brice Hilliard"
__version__ = "0.1"
__email__ = "bricehilliard035@gmail.com"
__production__ = "development"

import matplotlib.pyplot as plt
from BaseballNames import players, umpires, grounds, player_colours
from StatDicts import results_options, bat_stats
from processing import add_cum_batting_avg, process_data, cumstat_df
from stat_plot import plot_avg
from in_out import import_data, clean_data, print_outcomes

def main():
    # print(bat_stats + list(results_options.keys()))
    raw_data = import_data()
    cleaned_data = clean_data(raw_data)
    cum_stat_df = cumstat_df(cleaned_data, results_options)
    processed_data1, processed_data2 = process_data(cleaned_data, results_options)
    print_outcomes(processed_data1, processed_data2)
    plot_avg(cum_stat_df)

if __name__ == '__main__':
    main()
