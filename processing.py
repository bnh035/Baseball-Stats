#!/usr/bin/env python

""" Contains functions that are used to input and output data.
"""

__author__ = "Brice Hilliard"
__version__ = "0.1"
__email__ = "bricehilliard035@gmail.com"
__production__ = "development"

import pandas as pd
import matplotlib.pyplot as plt
from BaseballNames import players, umpires, grounds, player_colours
from StatDicts import results_options, bat_stats

#TODO: Figure out why the cumcum is shifting

def process_data(in_df, results_options_1):
    # Process Data
    #---------------
    # Column for at bat classification
    in_df.loc[:,'Hits'] = in_df.loc[:,"Result"].map(results_options_1)

    # Count the various batting outcomes
    batting_outcomes = in_df["Result"].value_counts()

    possibilities = sorted(set(results_options.values()))
    results_list = []
    for i in possibilities:
        results_list.append([key for (key, value) in results_options.items() if value == i])

    outcomes1 = []
    for j in range(5):
        outcomes1.append(sum([batting_outcomes[i] for i in results_list[j]]))

    outcomes = dict(zip(possibilities, outcomes1))

    return outcomes, batting_outcomes

def create_df(in_df, results_options_1):
    in_df.loc[:,'Hits'] = in_df.loc[:,"Result"].map(results_options_1)
    #in_df.loc[:,"CumHits"] = in_df.groupby(["Batter", "Hits"]).cumcount()
    cum_cols = ["CumHits", "CumOuts", "CumNones", "CumFCs", "CumErrs"]
    for i in cum_cols:
        x = i[3:-1]
        in_df.loc[:,i] = in_df[in_df["Hits"] == x].groupby(["Batter"]).cumcount()
        in_df[i] = in_df[i].replace(to_replace="NaN", method="ffill")
    in_df["AB"] = in_df["CumHits"] + in_df["CumOuts"] + in_df["CumFCs"]
    in_df["BA"] = in_df["CumHits"] / in_df["AB"]
    in_df["BA"] = in_df["BA"].round(3)
    plt.figure()
    plot_df = in_df[in_df["Batter"] == "Brice Hilliard"]["BA"].reset_index()
    plot_df = plot_df["BA"]
    plot_df.plot()
    plt.show()
    print(plot_df)

def cumstat_df(in_df, results_options_1):
    in_df.loc[:,'Hits'] = in_df.loc[:,"Result"].map(results_options_1)
    #in_df = add_hits_col(in_df, results_options_1)
    stat_df_col = ["Batter", "Game", "Hit", "None", "FC", "Err", "Out"]
    stat_df = pd.DataFrame(columns=stat_df_col)
    for y in in_df.Season.unique():
        in_df1 = in_df[in_df.loc[:, "Season"] == y]
        for i in in_df1.Batter.unique():
            batter_df = in_df1[in_df1.loc[:, "Batter"] == i]
            for j in sorted(in_df1.Game.unique()):
                game_df = batter_df[batter_df.loc[:, "Game"] == j]
                count_dict = game_df.Hits.value_counts()
                count_dict["Batter"] = i
                count_dict["Game"] = j + (y - 2019) * 16
                count_dict["Year"] = y
                for k in stat_df_col:
                    if k not in count_dict.keys():
                        count_dict[k] = 0
                stat_df = stat_df.append(count_dict, ignore_index=True)

    stat_df["AB"] = stat_df["Hit"] + stat_df["FC"] + stat_df["Err"] + stat_df["Out"]
    stat_df["CumHit"] = stat_df.groupby("Batter")["Hit"].cumsum()
    stat_df["CumAB"] = stat_df.groupby("Batter")["AB"].cumsum()
    stat_df["BA"] = stat_df["CumHit"] / stat_df["CumAB"]
    stat_df["BA"] = stat_df["BA"].round(3)
    stat_df.to_csv("statOut.csv")
    return stat_df

def create_player_df(in_df, player_name):
    """Split a dataframe by player and create columns from a list.

    Args:
        in_df (DF): the input dataframe
        player_name (str): the player that the dataframe will be created for

    return:
        out_df (DF): the dataframe that the function will return
    """
    out_df = in_df[in_df.loc[:, "Batter"] == player_name]
    return out_df

def create_year_df(in_df, year):
    # Create a df of the specified year

    out_df = in_df[in_df.loc[:, "Season"] == year]
    return out_df
