import pandas as pd
from BaseballNames import players, umpires, grounds, player_colours
from StatDicts import results_options, bat_stats

def add_hits_col(in_df, option_dict):
    """Add a column that classifies batting outcomes from the dataframe into
    hits or another category.

    Args:
        in_df (DF): the dataframe that the column will be added to.
        option_dict (dict): the dictionary that defines how the outcomes are to
                            be classified.

    Returns:
        out_df (DF): the dataframe that has the hit column added
    """
    out_df = in_df
    out_df.loc[:,'Hits'] = out_df.loc[:,"Result"].map(option_dict)

    return out_df

def add_cum_batting_avg(in_df, results_options_1):
    in_df = add_hits_col(in_df, results_options_1)

    for i in in_df.Batter.unique():
        batter_df = in_df[in_df.loc[:,"Batter"] == i]
        batter_df.loc[:,"HitSum"] = (batter_df.loc[:,"Hits"] == "Hit").cumsum()
        batter_df.loc[:,"ABSum"] = (batter_df.loc[:,"Hits"] != "None").cumsum()
        batter_df.loc[:,"CumBA"] = batter_df.loc[:,"HitSum"] / batter_df.loc[:,"ABSum"]
        batter_df.loc[:,"CumBA"] = batter_df.loc[:,"CumBA"].fillna(0)
        batter_df.loc[:,"CumBA"] = batter_df.loc[:,"CumBA"].round(3)
        if i == 1:
            out_df = batter_df
        else:
            out_df = pd.concat([out_df, batter_df], ignore_index=True)
    return out_df

def process_data(in_df, results_options_1):
    # Process Data
    #---------------
    # Column for at bat classification
    in_df = add_hits_col(in_df, results_options_1)

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

def cumstat_df(in_df, results_options_1):
    in_df = add_hits_col(in_df, results_options_1)
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

def creat_player_df(in_df, player_name):
    """Split a dataframe by player and create columns from a list.

    Args:
        in_df (DF): the input dataframe
        player_name (str): the player that the dataframe will be created for

    return:
        out_df (DF): the dataframe that the function will return
    """
    out_df = in_df[in_df.loc[:, "Batter"] == player_name]

def collate_team_df(in_df):
    """Fill
    """
    return None

def create_year_df(in_df, year):
    """Fill
    """
    return None
