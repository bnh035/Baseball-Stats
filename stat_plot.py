def plot_avg(in_df):
    players_inv = {value:key for key, value in players.items()}
    in_df.loc[:,"Batter"] = in_df.loc[:, "Batter"].map(players_inv)
    # print(players_inv)
    l1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    batters = [players_inv[i] for i in l1]
    fig, ax = plt.subplots()

    for year in in_df.Year.unique():
        in_df1 = in_df[in_df.Year == year]
        for name in batters:
            #x = [i for i in range(len(in_df[in_df.Batter == name].BA))]
            if year == 2019:
                plt.plot(in_df1[in_df1.Batter == name].Game, in_df1[in_df1.Batter == name].BA, label=name, color=player_colours[name])
            else:
                plt.plot(in_df1[in_df1.Batter == name].Game, in_df1[in_df1.Batter == name].BA, label="", color=player_colours[name])
    plt.legend(loc="upper center", ncol=6)
    plt.show()
