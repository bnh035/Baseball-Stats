#!/usr/bin/env python

""" Baseball Stats Headstring
    ==================
Date Started: 22 October 2020
"""

# TODO:  Breakup file into separate functions to be called when needed
# TODO:  Move name dicts to separate file
# TODO:  Git
# TODO:  Setup stat DF
# TODO:  Create output file

__author__ = "Brice Hilliard"
__version__ = "0.1"
__email__ = "bricehilliard035@gmail.com"
__production__ = "development"

import pandas as pd
import matplotlib.pyplot as plt
from BaseballNames import Players, Umpires, Grounds
from StatDicts import ResultsOpts, BatStats

def importData():
    # Import csvs
    #---------------
    RawData19 = pd.read_csv("Baseball_2019.csv")
    RawData20 = pd.read_csv("Baseball_2020.csv")

    return RawData19, RawData20

def cleanData(RawData1, RawData2):
    # Clean up 2019 data
    #---------------------
    # Strip zeroes, remove rows with #REF!
    Clean1 = RawData1[RawData1["Result"] != "0"]
    Clean1 = Clean1[Clean1["Result"] != "#REF!"]

    # Clean up 2020 data
    Clean2 = RawData2.dropna(subset=["Umpire"])
    Clean2 = Clean2[Clean2["Ground"] != "0"]
    Clean2 = Clean2[Clean2["Result"] != "0"]
    #Clean2 = Clean2[Clean2["Result"] != "DNB"]
    #Clean2 = Clean2[Clean2["Result"] != "DNP"]

    # Sanitise names
    Clean1.loc[:,"Batter"] = Clean1.loc[:, "Batter"].map(Players)
    Clean2.loc[:,"Batter"] = Clean2.loc[:, "Batter"].map(Players)
    Clean2.loc[:,"Umpire"] = Clean2.loc[:, "Umpire"].map(Umpires)
    Clean2.loc[:,"Ground"] = Clean2.loc[:, "Ground"].map(Grounds)

    # Add in any extra data
    Clean1["Season"] = 2019
    Clean2["Season"] = 2020

    # Combine the 2 dataframes
    CleanData = pd.concat([Clean1, Clean2], ignore_index=True)
    return CleanData

def addHitsCol(inDF):
    inDF.loc[:,'Hits'] = inDF.loc[:,"Result"].map(ResultsOpts)
    return inDF

def cumStatDF(inDF):
    inDF = addHitsCol(inDF)
    StatDFCols = ["Batter", "Game", "Hit", "None", "FC", "Err", "Out"]
    StatDF = pd.DataFrame(columns=StatDFCols)
    for y in inDF.Season.unique():
        inDF1 = inDF[inDF.loc[:, "Season"] == y]
        for i in inDF1.Batter.unique():
            BatterDF = inDF1[inDF1.loc[:, "Batter"] == i]
            for j in sorted(inDF1.Game.unique()):
                GameDF = BatterDF[BatterDF.loc[:, "Game"] == j]
                countDict = GameDF.Hits.value_counts()
                countDict["Batter"] = i
                countDict["Game"] = j + (y - 2019) * 16
                countDict["Year"] = y
                for k in StatDFCols:
                    if k not in countDict.keys():
                        countDict[k] = 0
                StatDF = StatDF.append(countDict, ignore_index=True)

    StatDF["AB"] = StatDF["Hit"] + StatDF["FC"] + StatDF["Err"] + StatDF["Out"]
    StatDF["CumHit"] = StatDF.groupby("Batter")["Hit"].cumsum()
    StatDF["CumAB"] = StatDF.groupby("Batter")["AB"].cumsum()
    StatDF["BA"] = StatDF["CumHit"] / StatDF["CumAB"]
    StatDF["BA"] = StatDF["BA"].round(3)
    StatDF.to_csv("statOut.csv")
    return StatDF

def addCumBattingAvg(inDF):
    inDF = addHitsCol(inDF)

    for i in inDF.Batter.unique():
        BatterDF = inDF[inDF.loc[:,"Batter"] == i]
        BatterDF.loc[:,"HitSum"] = (BatterDF.loc[:,"Hits"] == "Hit").cumsum()
        BatterDF.loc[:,"ABSum"] = (BatterDF.loc[:,"Hits"] != "None").cumsum()
        BatterDF.loc[:,"CumBA"] = BatterDF.loc[:,"HitSum"] / BatterDF.loc[:,"ABSum"]
        BatterDF.loc[:,"CumBA"] = BatterDF.loc[:,"CumBA"].fillna(0)
        BatterDF.loc[:,"CumBA"] = BatterDF.loc[:,"CumBA"].round(3)
        if i == 1:
            outDF = BatterDF
        else:
            outDF = pd.concat([outDF, BatterDF], ignore_index=True)
    return outDF

def processData(inDF):
    # Process Data
    #---------------
    # Column for at bat classification
    inDF = addHitsCol(inDF)

    # Count the various batting outcomes
    BattingOutcomes = inDF["Result"].value_counts()

    Possibilities = sorted(set(ResultsOpts.values()))
    ResultList = []
    for i in Possibilities:
        ResultList.append([key for (key, value) in ResultsOpts.items() if value == i])

    Outcomes1 = []
    for j in range(5):
        Outcomes1.append(sum([BattingOutcomes[i] for i in ResultList[j]]))

    Outcomes = dict(zip(Possibilities, Outcomes1))

    return Outcomes, BattingOutcomes

def printOutcomes(Array1, Array2):
    # Batting Stats
    OutcomeDict = {}
    OutcomeDict["PA"] = sum(Array1.values())
    OutcomeDict["AB"] = OutcomeDict["PA"] - Array1["None"]
    OutcomeDict["Hit"] = Array1["Hit"]
    OutcomeDict["BA"] = round(OutcomeDict["Hit"] / OutcomeDict["AB"], 3)
    OutcomeDict["Ks"] = Array2["KC"] + Array2["K2"]
    OutcomeDict["Singles"] = Array2["Single"]
    OutcomeDict["Doubles"] = Array2["Double"]
    OutcomeDict["Triples"] = Array2["Triple"]
    OutcomeDict["HR"] = Array2["Home"]
    OutcomeDict["BB"] = Array2["BB"]
    OutcomeDict["HBP"] = Array2["HBP"]
    OutcomeDict["SLG"] = round((1 * OutcomeDict["Singles"] + 2 * OutcomeDict["Doubles"] + 3 * OutcomeDict["Triples"] + 4 * OutcomeDict["HR"]) / OutcomeDict["AB"], 3)
    OutcomeDict["OBP"] = round((OutcomeDict["Hit"] + OutcomeDict["BB"] + OutcomeDict["HBP"])/(OutcomeDict["AB"] + OutcomeDict["BB"] + OutcomeDict["HBP"]), 3)
    OutcomeDict["OPS"] = round(OutcomeDict["OBP"] + OutcomeDict["SLG"], 3)

    DesiredOrder = ["PA", "AB", "BA", "Hit", "Singles", "Doubles", "Triples", "HR", "BB", "HBP", "SLG", "OBP", "OPS"]

    for i in DesiredOrder:
        print(i + ": " + (10 - len(i)) * "." + " " + str(OutcomeDict[i]))

    return OutcomeDict, DesiredOrder

def OutputData(DFrames, FileNames):
    # Output csv files
    #-------------------
    for df, FileName in zip(Dframes, FileNames):
        df.to_csv(FileName)
    return 0

def plotAvg(inDF):
    PlayersInv = {value:key for key, value in Players.items()}
    inDF.loc[:,"Batter"] = inDF.loc[:, "Batter"].map(Players)
    # print(PlayersInv)
    l1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    batters = [PlayersInv[i] for i in l1]
    fig, ax = plt.subplots()

    for year in inDF.Year.unique():
        inDF1 = inDF[inDF.Year == year]
        for name in batters:
            #x = [i for i in range(len(inDF[inDF.Batter == name].BA))]
            plt.plot(inDF[inDF.Batter == name].Game, inDF[inDF.Batter == name].BA)
    plt.legend()
    # TODO: Type error with line 173
    # TODO: Add legend with names
    plt.show()

def main():
    a1, a2 = importData()
    a3 = cleanData(a1, a2)
    sDF = cumStatDF(a3)
    a4, a5 = processData(a3)
    printOutcomes(a4, a5)
    plotAvg(sDF)

if __name__ == '__main__':
    main()
