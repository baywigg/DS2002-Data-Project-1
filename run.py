from csv_utils import *
from json_utils import *
import time
import pandas as pd
import sys

df = pd.DataFrame()

data_type = input('''
    What data type would you like to read? \n
    'CSV' or 'csv' for NBA data \n
    'JSON' or 'json' for crypto data (API) \n
''')

if data_type not in ["CSV", "csv", "JSON", "json"]:
    print(f"I'm sure {data_type} is a great data type, however I do not possess the abilities for that, goodbye.")
    sys.exit()

# Handle CSV route
if data_type in ["CSV", "csv"]:
    df = pd.read_csv(read_csv(), dtype={"GameDay": "string", "GameID" : "int", "Player" : "string", "PlayerID" : "int", 
                                "PlayerCode": "string", "TeamID" : "int", "Team" : "string", "OpponentID": "int", 
                                "Opponent" : "string", "Location" : "string", "Division" : "string", "Conference" : "string", 
                                "Playoffs" : "string", "WinOrLoss" : "string", "Starter" : "string", "PlayerType" : "string", 
                                "PerfScore" : "string", "MIN" : "string", "PTS" : "int", "FGM" : "int", "FGA" : "int", 
                                "3FM" : "int", "3FA" : "int", "FTM" : "int", "FTA" : "int", "REB" : "int", 
                                "AST" : "int", "STL" : "int", "BLK" : "int", "OREB" : "int", "TO" : "int", 
                                "PF" : "int"})
    # Removing unneccesary data
    print("Removing uneccessary data... \n")
    # Filter out only the regular season
    df = df[df["Playoffs"].isna()]
    # Drop uneeded columns
    df = df.drop(columns=["GameDay", "GameID", "PlayerID", "PlayerCode", "TeamID", "Team", "OpponentID", "Opponent", "Location", "Division", "Conference", "Playoffs", "WinOrLoss", "Starter", "PlayerType", "PerfScore", "MIN"])
    time.sleep(1)
    
    # Get the max PPG from the dataframe
    max_ppg = get_max_ppg(df)
    print(f"We will now filter out the players with a Points Per Game (PPG) average lower than what you specify! For reference, the maximum PPG is: {max_ppg} \n")
    while True:
        try:    
            # Get the PPG lower bound from the user
            ppg_lower_bound = int(input("Please input a minimum PPG: "))

            if ppg_lower_bound >= max_ppg:
                raise ValueError
            
            break

        except ValueError:
            print("\nEnsure to input an integer lower than the max PPG next time... \n")

    df = remove_low_ppg_players(df, ppg_lower_bound)
    print(df)

# Handle JSON route
else:
    df = pd.read_json(get_json("", ""))


# Save data as the user specifies