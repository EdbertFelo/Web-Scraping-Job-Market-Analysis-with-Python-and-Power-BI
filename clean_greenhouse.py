import re
import html
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

input_file = "data/greenhouse_jobs_raw.csv"
output_file = "data/greenhouse_jobs_cleaned.csv"

print("Loading raw CSV...")
df = pd.read_csv(input_file)

print("Rows loaded:", len(df))


def clean_html_text(raw_html):
    if pd.isna(raw_html):
        return np.nan

    text = html.unescape(str(raw_html))
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text(separator=" ")
    text = re.sub(r"\s+", " ", text).strip()

    return text


print("Cleaning description_html into description_text...")
df["description_text"] = df["description_html"].apply(clean_html_text)

print("Creating a shorter preview column...")
df["description_preview"] = df["description_text"].str.slice(0, 300)

print("Cleaning title and location text...")
df["title"] = df["title"].astype(str).str.strip()
df["location_name"] = df["location_name"].astype(str).str.strip()

print("Replacing empty strings with NaN...")
df = df.replace(r"^\s*$", np.nan, regex=True)

print("Dropping duplicate job postings...")
df = df.drop_duplicates(subset=["board_token", "job_post_id"])

print("Saving cleaned CSV...")
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print("\nDone.")
print("Rows after cleaning:", len(df))

preview_cols = [
    "board_token",
    "job_post_id",
    "title",
    "location_name",
    "description_preview"
]

print("\nPreview:")
print(df[preview_cols].head(5))

print(f"\nSaved cleaned file to: {output_file}")