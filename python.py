from google_play_scraper import app
from datetime import datetime
import pandas as pd
import os

app_id = 'np.edu.dwit.dlc'
file_name = "daily_app_Deerwalk_learning_center.xlsx"

# Fetch app details
result = app(app_id, lang='en', country='us')

# Prepare today's data
today = datetime.now().strftime("%Y-%m-%d")
data = {
    "Date": [today],
    "Title": [result["title"]],
    "RealInstalls": [result["realInstalls"]],
    "AverageRating": [result["score"]]
}
df_new = pd.DataFrame(data)

# Append to Excel if exists, else create new
if os.path.exists(file_name):
    existing_df = pd.read_excel(file_name)
    updated_df = pd.concat([existing_df, df_new], ignore_index=True)
    updated_df.to_excel(file_name, index=False)
else:
    df_new.to_excel(file_name, index=False)

# ✅ Print to terminal
print(f"\nData saved for {today} in {file_name}\n")
print("Latest App Data:")
print(df_new)
