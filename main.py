from google_play_scraper import app, reviews, Sort
from datetime import datetime
import pandas as pd
import os

app_id = 'np.edu.dwit.dlc'
file_name = "daily_app_Deerwalk_learning_center.xlsx"

# Fetch app details
result = app(app_id, lang='en', country='us')

# Convert numeric rating to stars (★)
rating = result["score"]
if rating:
    stars = "★" * int(round(rating))
else:
    stars = "No rating"

# Fetch reviews (latest 100)
review_result, _ = reviews(
    app_id,
    lang='en',
    country='us',
    count=100,
    sort=Sort.NEWEST
)

# Separate positive and negative reviews
positive_reviews = [r['content'] for r in review_result if r['score'] >= 4]
negative_reviews = [r['content'] for r in review_result if r['score'] <= 2]

# Prepare today's data with Date and Time separately
now = datetime.now()
today_date = now.strftime("%Y-%m-%d")
today_time = now.strftime("%H:%M:%S")

data = {
    "Date": [today_date],
    "Time": [today_time],
    "Title": [result["title"]],
    "RealInstalls": [result["realInstalls"]],
    "Rating": [stars],
    "PositiveReview": [" | ".join(positive_reviews[:5])],
    "NegativeReview": [" | ".join(negative_reviews[:5])]
}
df_new = pd.DataFrame(data)

# Append to Excel if exists, else create new
if os.path.exists(file_name):
    existing_df = pd.read_excel(file_name)
    updated_df = pd.concat([existing_df, df_new], ignore_index=True)
    updated_df.to_excel(file_name, index=False)
else:
    df_new.to_excel(file_name, index=False)

# Print simple result
print(f"\nDate: {today_date}")
print(f"Time: {today_time}")
print(f"App: {result['title']}")
print(f"Installs: {result['realInstalls']}")
print(f"Rating: {stars}")

print("\nPositive Reviews:")
if positive_reviews:
    for review in positive_reviews[:3]:
        print( review)
else:
    print("None found")

print("\nNegative Reviews:")
if negative_reviews:
    for review in negative_reviews[:3]:
        print(review)
else:
    print(" None found ")
