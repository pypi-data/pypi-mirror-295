import os
from ftbx import list_cmd
import pandas as pd
from src.variables import ListOptions
from tqdm import tqdm
import datetime

from datetime import datetime, timedelta

# start_date = datetime(2020, 1, 1)
# end_date = datetime(2025, 1, 1)
#
# current_date = start_date
#
# while current_date < end_date:
#     # Start date for the 2-week period
#     start = current_date.strftime("%Y-%m-%d")
#
#     # Calculate the end date by adding 14 days
#     next_date = current_date + timedelta(days=14)
#     end = next_date.strftime("%Y-%m-%d")
#
#     try:
#         list_cmd(
#             object_type=ListOptions.ASSETS,
#             filters=[f"fql=objectType.id = 2 and !(mediaType = NULL) and vendorName = *WBArchive* and created >= {start} and created < {end}", "includeMetadata=true"],
#             post_filters=["metadata.instance.asset.package-status!=none", "metadata.instance.asset.mediatype!=none"],
#             name=f"REACH_{start}_TO_{end}",
#             from_="wb-prod"
#         )
#     except:
#         print(f"Skipping {start} to {end}")
#
#     # Move to the next 2-week period
#     current_date = next_date

csv_dir = 'lists/'
df_list = []

for file in tqdm(os.listdir(csv_dir)):
    if file.endswith('.csv'):
        file_path = os.path.join(csv_dir, file)
        df = pd.read_csv(file_path)
        df_list.append(df)

combined_df = pd.concat(df_list, ignore_index=True)
combined_df.to_csv('combined_file.csv', index=False)
