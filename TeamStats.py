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
from processing import process_data, cumstat_df, create_df, add_zeroes,create_games_df
from stat_plot import plot_avg, plot_ba_pa
from in_out import import_data, clean_data, print_outcomes

def main():
    # print(bat_stats + list(results_options.keys()))
    raw_data = import_data()
    cleaned_data = clean_data(raw_data)
    # add_zeroes(cleaned_data)
    processed_data = create_df(cleaned_data, results_options)
    #plot_ba_pa(processed_data)
    create_games_df(processed_data)
    #cum_stat_df = cumstat_df(cleaned_data, results_options)
    #processed_data1, processed_data2 = process_data(cleaned_data, results_options)
    #print_outcomes(processed_data1, processed_data2)
    #plot_avg(cum_stat_df)

if __name__ == '__main__':
    main()
