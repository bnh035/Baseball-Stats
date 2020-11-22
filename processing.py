#!/usr/bin/env python

""" Contains functions that are used to input and output data.
"""

__author__ = "Brice Hilliard"
__version__ = "0.1"
__email__ = "bricehilliard035@gmail.com"
__production__ = "development"

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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

def insert_row(row_number, df, row_value):
    # Slice the upper half of the dataframe
    df1 = df[0:row_number]

    # Store the result of lower half of the dataframe
    df2 = df[row_number:]

    # Inser the row in the upper half dataframe
    df1.loc[row_number]=row_value

    # Concat the two dataframes
    df_result = pd.concat([df1, df2])

    # Reassign the index labels
    df_result.index = [*range(df_result.shape[0])]

    # Return the updated dataframe
    return df_result

def add_zeroes(df):
    names = df.Batter.unique()
    for i in names:
        prerow = df[(df.loc[:,'Batter'] == i) & (df.loc[:,'Game'] == 1) & (df.loc[:,'AB#'] == 1) & (df.loc[:,'Season'] == 2019)]
        if len(prerow.index.tolist()) != 0:
            if prerow.index.tolist()[0] == 0:
                df.loc[-1] = 0
                df.index = df.index + 1
                df.loc[0, ["Batter"]] = i
            else:
                insert_row(prerow.index.tolist()[0], df, 0)
                df.loc[prerow.index.tolist()[0], ["Batter"]] = i
    df.to_csv("out.csv")
    return df

def cum_df(in_df, results_options_1):
    in_df.loc[:,'Hits'] = in_df.loc[:,"Result"].map(results_options_1)
    #in_df.loc[:,"CumHits"] = in_df.groupby(["Batter", "Hits"]).cumcount()
    cum_cols = ["CumHits", "CumOuts", "CumNones", "CumFCs", "CumErrs"]
    for i in cum_cols:
        in_df.loc[:,i] = 0
    in_df = add_zeroes(in_df)
    batters = in_df.Batter.unique()
    for i in cum_cols:
        x = i[3:-1]
        for player in batters:
            index_array = in_df[(in_df.loc[:,'Batter'] == player) & (in_df.loc[:,'Hits'] == x)].index.tolist()
            if len(index_array) != 0:
                in_df.loc[index_array, i] = np.arange(1,len(index_array)+1)
    out_df = pd.DataFrame(columns=in_df.columns)
    for player in batters:
        next_df = in_df[(in_df.loc[:,'Batter'] == player)]
        for i in cum_cols:
            next_df.loc[:,i] = next_df.loc[:,i].replace(to_replace=0, method="ffill")
        out_df = pd.concat([out_df, next_df])
        out_df.reset_index()
    in_df = out_df

    in_df.loc[:,"AB"] = in_df.loc[:,"CumHits"] + in_df.loc[:,"CumOuts"] + in_df.loc[:,"CumFCs"]
    in_df.loc[:,"BA"] = in_df.loc[:,"CumHits"] / in_df.loc[:,"AB"]
    in_df.loc[:,"BA"] = in_df.loc[:,"BA"].round(3)
    in_df.to_csv("out.csv")
    return in_df

def game_df(in_df, results_options_1):
    """Create a dataframe of stats based on games.

    Args:
        in_df (DF): the input dataframe
        player_name (str): the player that the dataframe will be created for

    return:
        out_df (DF): the dataframe that the function will return
    """
    # Create a new column with PA results categorised.
    in_df.loc[:,'Hits'] = in_df.loc[:,"Result"].map(results_options_1)

    # List of dataframe columns and a new dataframe using them.
    stat_df_col = ["Batter", "Game", "Hit", "None", "FC", "Err", "Out"]
    stat_df = pd.DataFrame(columns=stat_df_col)

    for y in in_df.Season.unique():
        # Group by season
        in_df1 = in_df[in_df.loc[:, "Season"] == y]
        for i in in_df1.Batter.unique():
            # Group by batter name
            batter_df = in_df1[in_df1.loc[:, "Batter"] == i]
            for j in sorted(in_df1.Game.unique()):
                # Group by batter game
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
    stat_df = stat_df.drop(stat_df[stat_df.Game<0].index)
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

def create_games_df(in_df):
    game_vals = []
    batter_vals = []
    year_vals = []

    for year in in_df["Season"].unique():
        for batter in in_df["Batter"].unique():
            for game in range(1, int(in_df[in_df["Season"] == year]["Game"].max())+1):
                year_vals.append(int(year))
                batter_vals.append(batter)
                game_vals.append(game)

    out_df = pd.DataFrame(columns=in_df.columns)
    out_df["Season"] = year_vals
    out_df["Batter"] = batter_vals
    out_df["Game"] = game_vals
    out_df["BA"] = in_df[(in_df["Season"].isin(year_vals)) & (in_df["Batter"].isin(batter_vals)) & (in_df["Game"].isin(game_vals))]["BA"].iloc[[-1]]
    print(out_df)

def pa_df(in_df):
    l = in_df.groupby(["Season", "Game"])["AB#"].max().tolist()
    a = 1
    year = 2019
    abs_list, game_list, year_list = [], [], []
    for i in l:
        b = 1
        for j in range(i):
            abs_list.append(b)
            game_list.append(a)
            year_list.append(year)
            b = b + 1
        if a < 16:
            a = a + 1
        else:
            year = 2020
            a = 1
    player_df = pd.DataFrame()
    player_df["Batter"] = "Brice Hilliard"
    player_df["Season"] = year_list
    player_df["Game"] = game_list
    player_df["AB"] = abs_list
    player_df["Result"] = "DNB"
    comp_df = in_df[in_df["Batter"] == "Brice Hilliard"]
    comp_df.rename(columns={'AB#':'AB'}, inplace=True)
    concat_df = pd.concat([player_df, comp_df]).drop_duplicates(["Season", "Game", "AB"], keep=False)
    concat_df["Result"] = "DNB"
    concat_df["Batter"] = "Brice Hilliard"
    comp_df = pd.concat([comp_df, concat_df])
    print(comp_df[(comp_df["Game"] == 2) & (comp_df["Season"] == 2019)])
