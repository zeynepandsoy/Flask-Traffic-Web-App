from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, types

# Define the database file name and location
db_file = Path(__file__).parent.joinpath("traffic.db")

# Create a connection to file as a SQLite database (this automatically creates the file if it doesn't exist)
engine = create_engine("sqlite:///" + str(db_file), echo=False)

# Read the paralympics event data to a pandas dataframe
traffic_file = Path(__file__).parent.joinpath("data_set_prepared.xlsx")
traffic_df = pd.read_excel(traffic_file)

# Write the data to tables in a sqlite database
dtype_traffic = {
    "record_id": types.INTEGER(),
    "holiday": types.TEXT(),
    "weather": types.TEXT(),
    "traffic_volume": types.INTEGER(),
    "year": types.INTEGER(),
    "month": types.INTEGER(),
    "day": types.INTEGER(),
    "hour": types.INTEGER(),
    "categorized_hour": types.TEXT(),
    "categorized_weekday": types.TEXT(),
}

#CHANGE EVENT TO YOUR MODEL
traffic_df.to_sql(
    "query", engine, if_exists="append", index=False, dtype=dtype_traffic
)

