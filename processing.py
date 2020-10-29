def add_cum_batting_avg(in_df):
    in_df = add_hits_col(in_df)

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

def process_data(in_df):
    # Process Data
    #---------------
    # Column for at bat classification
    in_df = add_hits_col(in_df)

    # Count the various batting outcomes
    batting_outcomes = in_df["Result"].value_counts()

    possibilities = sorted(set(ResultsOpts.values()))
    ResultList = []
    for i in possibilities:
        ResultList.append([key for (key, value) in ResultsOpts.items() if value == i])

    outcomes1 = []
    for j in range(5):
        outcomes1.append(sum([batting_outcomes[i] for i in ResultList[j]]))

    outcomes = dict(zip(possibilities, outcomes1))

    return outcomes, batting_outcomes

def cumstat_df(in_df):
    in_df = add_hits_col(in_df)
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

def add_hits_col(in_df):
    in_df.loc[:,'Hits'] = in_df.loc[:,"Result"].map(ResultsOpts)
    return in_df
