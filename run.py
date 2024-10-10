from csv_utils import *
from json_utils import *
import time
import pandas as pd
import sqlite3
import sys
import json

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
    try:
        df = pd.read_csv(read_csv(), dtype={"GameDay": "string", "GameID" : "int", "Player" : "string", "PlayerID" : "int", 
                                    "PlayerCode": "string", "TeamID" : "int", "Team" : "string", "OpponentID": "int", 
                                    "Opponent" : "string", "Location" : "string", "Division" : "string", "Conference" : "string", 
                                    "Playoffs" : "string", "WinOrLoss" : "string", "Starter" : "string", "PlayerType" : "string", 
                                    "PerfScore" : "string", "MIN" : "string", "PTS" : "int", "FGM" : "int", "FGA" : "int", 
                                    "3FM" : "int", "3FA" : "int", "FTM" : "int", "FTA" : "int", "REB" : "int", 
                                    "AST" : "int", "STL" : "int", "BLK" : "int", "OREB" : "int", "TO" : "int", 
                                    "PF" : "int"})
    except Exception as e:
        print(f"Failed to read CSV: {e}")
        sys.exit()

    print(f"\nNumber of records in ingested data: {len(df)}")
    time.sleep(1)

    print(f"\nNumber of columns in ingested data: {len(df.columns)}")
    time.sleep(1)

    try:
        # Removing unneccesary data
        print("Removing unnecessary data... \n")
        # Filter out only the regular season
        df = df[df["Playoffs"].isna()]
        # Drop uneeded columns
        df = df.drop(columns=["GameDay", "GameID", "PlayerID", "PlayerCode", "TeamID", "Team", "OpponentID", "Opponent", "Location", "Division", "Conference", "Playoffs", "WinOrLoss", "Starter", "PlayerType", "PerfScore", "MIN"])
        time.sleep(1)
    except Exception as e:
        print(f"Failed to remove unnecessary data: {e}")
        sys.exit()
    
    # Get the max PPG from the dataframe
    try:
        max_ppg = get_max_ppg(df)
    except Exception as e:
        print(f"Failed to get max PPG: {e}")
        sys.exit()

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

    print("\nCalculating efficiency rating (EFF)... \n")
    try:
    # Calculate the efficiency rating for each of the games present
        df["EFF"] = df.apply(get_efficiency_rating, axis=1, result_type="expand")
        time.sleep(1)
    except Exception as e:
        print(f"Failed to calculate EFF: {e}")
        sys.exit()

    print("\nCalculating averages for each player and ordering by EFF...\n")
    try:
        df = df.groupby("Player")[['PTS', 'FGM', 'FGA', '3FM', '3FA', 'FTM', 'FTA', 'REB', 'AST', 'STL', 'BLK', 'OREB', 'TO', 'PF', 'EFF']].mean().sort_values(by="EFF", ascending=False).reset_index()
        time.sleep(1)
    except Exception as e:
        print(f"Failed to calculate player averages: {e}")
        sys.exit()

    print(f"\nNumber of records in modified data: {len(df)}")
    time.sleep(1)

    print(f"\nNumber of columns in modified data: {len(df.columns)}")
    print(f"Columns: {list(df.columns)}")
    time.sleep(1)
    
# Handle JSON route
else:
    asset = input("\nChoose your cryptocurrency asset to receive data on (bitcoin, ethereum, dogecoin, etc.): ").lower()
    interval = input("\nChoose the interval in which you would like to receive data (m1, m5, m15, m30, h1, h2, h6, h12, d1): ")

    if interval not in ["m1", "m5", "m15", "m30", "h1", "h2", "h6", "h12", "d1"]:
        print("\nInterval must be in (m1, m5, m15, m30, h1, h2, h6, h12, d1)")
        sys.exit()

    print("\nReceiving data from CoinCap API...")
    response = get_json(asset, interval)

    if not response:
        print("\nYour asset or interval were not correct. Ensure the interval matches the format and the crypto exists.")
        sys.exit()

    df = pd.DataFrame(response["data"])
    pd.to_numeric(df["priceUsd"])
    pd.to_numeric(df["time"])

    print(f"\nNumber of records in ingested data: {len(df)}")
    time.sleep(1)

    print(f"\nNumber of columns in ingested data: {len(df.columns)}")
    time.sleep(1)

    # Add column indicating the type of crypto being accessed
    print("\nAdding asset column...")
    time.sleep(1)
    df["Asset"] = asset

    # Add columns to track the time and price change between the previous row
    print("\nCalculating the price and time changes...")
    time.sleep(1)
    try:
        price_change, time_change = get_price_and_time_change(df)
    except Exception as e:
        print(f"Failed to calculate the price and time change: {e}")
    
    df["priceChange"] = price_change
    df["timeChange"] = time_change

    print(f"\nNumber of records in modified data: {len(df)}")
    time.sleep(1)

    print(f"\nNumber of columns in modified data: {len(df.columns)}")
    print(f"Columns: {list(df.columns)}")
    time.sleep(1)


# Handle output
while True:
    try:    
        # Save data as the user specifies
        output_type = int(input('''
How would you like the output formatted?
    1: JSON
    2: CSV
    3: SQLite
Choose an option from above: '''))

        if output_type not in [1, 2, 3]:
            raise ValueError

        break
    except ValueError:
        print("\n Choose a value from the list.")
        time.sleep(0.5)

# JSON
if output_type == 1:
    try:
        file_path = input("\nChoose a file name for JSON file: ")
        df.to_json(f"output/{file_path}.json", index=False)
    except Exception as e:
        print(f"Failed to output JSON file: {e}")
        sys.exit()
# CSV
elif output_type == 2:
    try:
        file_path = input("\nChoose a file name for CSV file: ")
        df.to_csv(f"output/{file_path}.csv", index=False)
    except Exception as e:
        print(f"Failed to output CSV file: {e}")
        sys.exit()
# SQLite
else:
    try:
        file_path = input("\nChoose a file name for the SQLite database: ")
        table_name = input("\nChoose a table name for the SQLite database: ")
        conn = sqlite3.connect(f"output/{file_path}.db")
        df.to_sql(table_name, conn, if_exists="replace", index=False)
    except Exception as e:
        print(f"Failed to output to SQLite database: {e}")
        conn.close()
        sys.exit()

time.sleep(1)
print("\nSuccess!")