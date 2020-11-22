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
from processing import cum_df, game_df, pa_df
from stat_plot import plot_avg, plot_ba_pa
from in_out import import_data, clean_data, print_outcomes

def main():
    raw_data = import_data()
    cleaned_data = clean_data(raw_data)
    pa_df(cleaned_data)
    #cum_stat_df = cum_df(cleaned_data, results_options)
    #game_stat_df = game_df(cleaned_data, results_options)
    #plot_ba_pa(cum_stat_df)
    #plot_ba_pa(game_stat_df)
    #plot_avg(game_stat_df)
    #plot_avg(game_stat_df)
    #plot_avg(cum_stat_df)

if __name__ == '__main__':
    main()
