def import_data():
    # Import csvs
    #---------------
    raw_data_19 = pd.read_csv("Baseball_2019.csv")
    raw_data_20 = pd.read_csv("Baseball_2020.csv")

    return raw_data_19, raw_data_20

def clean_data(raw_data1, raw_data2):
    # clean up 2019 data
    #---------------------
    # Strip zeroes, remove rows with #REF!
    clean1 = raw_data1[raw_data1["Result"] != "0"]
    clean1 = clean1[clean1["Result"] != "#REF!"]

    # clean up 2020 data
    clean2 = raw_data2.dropna(subset=["Umpire"])
    clean2 = clean2[clean2["Ground"] != "0"]
    clean2 = clean2[clean2["Result"] != "0"]
    #clean2 = clean2[clean2["Result"] != "DNB"]
    #clean2 = clean2[clean2["Result"] != "DNP"]

    # Sanitise names
    clean1.loc[:,"Batter"] = clean1.loc[:, "Batter"].map(players)
    clean2.loc[:,"Batter"] = clean2.loc[:, "Batter"].map(players)
    clean2.loc[:,"Umpire"] = clean2.loc[:, "Umpire"].map(umpires)
    clean2.loc[:,"Ground"] = clean2.loc[:, "Ground"].map(grounds)

    # Add in any extra data
    clean1["Season"] = 2019
    clean2["Season"] = 2020

    # Combine the 2 dataframes
    clean_data = pd.concat([clean1, clean2], ignore_index=True)
    return clean_data

def print_outcomes(Array1, Array2):
    # Batting Stats
    outcome_dict = {}
    outcome_dict["PA"] = sum(Array1.values())
    outcome_dict["AB"] = outcome_dict["PA"] - Array1["None"]
    outcome_dict["Hit"] = Array1["Hit"]
    outcome_dict["BA"] = round(outcome_dict["Hit"] / outcome_dict["AB"], 3)
    outcome_dict["Ks"] = Array2["KC"] + Array2["K2"]
    outcome_dict["Singles"] = Array2["Single"]
    outcome_dict["Doubles"] = Array2["Double"]
    outcome_dict["Triples"] = Array2["Triple"]
    outcome_dict["HR"] = Array2["Home"]
    outcome_dict["BB"] = Array2["BB"]
    outcome_dict["HBP"] = Array2["HBP"]
    outcome_dict["SLG"] = round((1 * outcome_dict["Singles"] + 2 * outcome_dict["Doubles"] + 3 * outcome_dict["Triples"] + 4 * outcome_dict["HR"]) / outcome_dict["AB"], 3)
    outcome_dict["OBP"] = round((outcome_dict["Hit"] + outcome_dict["BB"] + outcome_dict["HBP"])/(outcome_dict["AB"] + outcome_dict["BB"] + outcome_dict["HBP"]), 3)
    outcome_dict["OPS"] = round(outcome_dict["OBP"] + outcome_dict["SLG"], 3)

    desired_order = ["PA", "AB", "BA", "Hit", "Singles", "Doubles", "Triples", "HR", "BB", "HBP", "SLG", "OBP", "OPS"]

    for i in desired_order:
        print(i + ": " + (10 - len(i)) * "." + " " + str(outcome_dict[i]))

    return outcome_dict, desired_order

def output_data(data_frames, file_names):
    # Output csv files
    #-------------------
    for df, file_name in zip(data_frames, file_names):
        df.to_csv(file_name)
    return 0
