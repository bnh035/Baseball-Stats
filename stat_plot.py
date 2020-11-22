#!/usr/bin/env python

""" Module: stat_plot.py
    ==================
Date Started: 22 October 2020
"""

__author__ = "Brice Hilliard"
__version__ = "0.1"
__email__ = "bricehilliard035@gmail.com"
__production__ = "development"

from BaseballNames import players, umpires, grounds, player_colours
import matplotlib.pyplot as plt

def plot_avg(in_df):
    #players_inv = {value:key for key, value in players.items()}
    #in_df.loc[:,"Batter"] = in_df.loc[:, "Batter"].map(players_inv)
    #l1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    #batters = [players_inv[i] for i in l1]
    fig, ax = plt.subplots()

    for year in in_df.Year.unique():
        in_df1 = in_df[in_df.Year == year]
        for name in in_df1.Batter.unique():
            #x = [i for i in range(len(in_df[in_df.Batter == name].BA))]
            if year == 2019:
                plt.plot(in_df1[in_df1.Batter == name].Game, in_df1[in_df1.Batter == name].BA, label=name, color=player_colours[name])
                print(in_df1[in_df1.Batter == name])
            else:
                plt.plot(in_df1[in_df1.Batter == name].Game, in_df1[in_df1.Batter == name].BA, label="", color=player_colours[name])
                print(in_df1[in_df1.Batter == name])
    plt.legend(loc="upper center", ncol=6)
    plt.show()

def plot_ba_pa(df):
    plt.figure()
    for batter in df.Batter.unique():
        plot_df = df[df["Batter"] == batter]["BA"].reset_index()
        plot_df = plot_df["BA"]
        plot_df.plot(color=player_colours[batter], label=batter)
    plt.legend(loc="upper center", ncol=6)
    plt.show()
