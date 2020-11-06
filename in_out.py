#!/usr/bin/env python

""" Contains functions that are used to input and output data.
"""

__author__ = "Brice Hilliard"
__version__ = "0.1"
__email__ = "bricehilliard035@gmail.com"
__production__ = "development"

import pandas as pd
from BaseballNames import players, umpires, grounds, player_colours
# TODO: Introduce error handling

def import_data():
    # Import csvs, add years, and concatenate
    #---------------------
    raw_data_19 = pd.read_csv("Baseball_2019.csv")
    raw_data_20 = pd.read_csv("Baseball_2020.csv")

    raw_data_19["Season"] = 2019
    raw_data_20["Season"] = 2020

    out_data = pd.concat([raw_data_19, raw_data_20], ignore_index=True)

    return out_data

def clean_data(unclean_data):
    """clean up 2019 data
    """
    #---------------------
    # TODO: Doc string
    #---------------------
    # Strip zeroes, remove rows with #REF!
    clean_data = unclean_data[unclean_data["Result"] != "0"]
    clean_data = clean_data.fillna(0)
    #clean_data[clean_data == "NaN"] = 0
    clean_data = clean_data[clean_data["Result"] != "#REF!"]

    # Replace names with numbers
    if False:
        clean_data.loc[:,"Batter"] = clean_data.loc[:, "Batter"].map(players)
        clean_data.loc[:,"Umpire"] = clean_data.loc[:, "Umpire"].map(umpires)
        clean_data.loc[:,"Ground"] = clean_data.loc[:, "Ground"].map(grounds)

    return clean_data

def print_outcomes(Array1, Array2):
    # Batting Stats
    #---------------------
    # TODO: Break into 2 lists and loop through with exceptions
    #---------------------
    outcome_dict = {}

    outcome_dict["Hit"] = Array1["Hit"]
    outcome_dict["Singles"] = Array2["Single"]
    outcome_dict["Doubles"] = Array2["Double"]
    outcome_dict["Triples"] = Array2["Triple"]
    outcome_dict["Home"] = Array2["Home"]
    outcome_dict["BB"] = Array2["BB"]
    outcome_dict["HBP"] = Array2["HBP"]
    outcome_dict["PA"] = sum(Array1.values())
    outcome_dict["AB"] = outcome_dict["PA"] - Array1["None"]
    outcome_dict["BA"] = round(outcome_dict["Hit"] / outcome_dict["AB"], 3)
    outcome_dict["Ks"] = Array2["KC"] + Array2["K2"]
    outcome_dict["SLG"] = round((1 * outcome_dict["Singles"] + 2 * outcome_dict["Doubles"] + 3 * outcome_dict["Triples"] + 4 * outcome_dict["Home"]) / outcome_dict["AB"], 3)
    outcome_dict["OBP"] = round((outcome_dict["Hit"] + outcome_dict["BB"] + outcome_dict["HBP"])/(outcome_dict["AB"] + outcome_dict["BB"] + outcome_dict["HBP"]), 3)
    outcome_dict["OPS"] = round(outcome_dict["OBP"] + outcome_dict["SLG"], 3)

    desired_order = ["PA", "AB", "BA", "Hit", "Singles", "Doubles", "Triples", "Home", "BB", "HBP", "SLG", "OBP", "OPS"]

    for i in desired_order:
        print(i + ": " + (10 - len(i)) * "." + " " + str(outcome_dict[i]))

    return outcome_dict

def output_data(data_frames, file_names):
    # Output csv files
    #-------------------
    for df, file_name in zip(data_frames, file_names):
        df.to_csv(file_name)
    return 0
