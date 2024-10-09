import csv
from io import StringIO

def read_csv():
    with open("data/NatStat-NBA2012-Player_Statlines-2024-09-17-h13.csv") as file:
        c = file.read()

    return StringIO(c)

def get_max_ppg(df):
    return int(df.groupby("Player")["PTS"].mean().reset_index().sort_values(by="PTS", ascending=False).iloc[0]["PTS"])

def remove_low_ppg_players(df, lower_bound):
    ppg = df.groupby('Player')["PTS"].mean().reset_index()
    players_to_remove = set(ppg[ppg["PTS"] < lower_bound]["Player"].to_list())

    return df[~df["Player"].isin(players_to_remove)]

def get_efficiency_rating(row):
    pass