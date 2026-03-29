import re
import numpy as np
import pandas as pd

input_file = "data/greenhouse_jobs_cleaned.csv"
output_file = "data/greenhouse_jobs_with_skills.csv"

print("Loading cleaned dataset...")
df = pd.read_csv(input_file)

print("Rows loaded:", len(df))

# Fill missing description text so text searching does not break
df["description_text"] = df["description_text"].fillna("")

# Skill dictionary:
# key = nice column label
# value = regex pattern to search in job descriptions
skill_patterns = {
    "python": r"\bpython\b",
    "sql": r"\bsql\b",
    "excel": r"\bexcel\b",
    "power_bi": r"\bpower[\s-]?bi\b",
    "tableau": r"\btableau\b",
    "pandas": r"\bpandas\b",
    "numpy": r"\bnumpy\b",
    "r": r"\br\b",
}

print("Creating skill flag columns...")

for skill_name, pattern in skill_patterns.items():
    column_name = f"skill_{skill_name}"
    df[column_name] = df["description_text"].str.contains(
        pattern,
        case=False,
        regex=True,
        na=False
    ).astype(int)

print("Creating skills_found column...")

skill_columns = [f"skill_{skill}" for skill in skill_patterns.keys()]

def get_skills_found(row):
    found = []
    for skill in skill_patterns.keys():
        if row[f"skill_{skill}"] == 1:
            found.append(skill)
    return ", ".join(found)

df["skills_found"] = df.apply(get_skills_found, axis=1)

print("Creating skill_count column...")
df["skill_count"] = df[skill_columns].sum(axis=1)

print("Creating simple role category from title...")

df["title"] = df["title"].fillna("").astype(str)

conditions = [
    df["title"].str.contains("data analyst", case=False, na=False),
    df["title"].str.contains("business analyst", case=False, na=False),
    df["title"].str.contains("data scientist", case=False, na=False),
    df["title"].str.contains("data engineer", case=False, na=False),
    df["title"].str.contains("bi analyst|business intelligence", case=False, na=False),
]

choices = [
    "Data Analyst",
    "Business Analyst",
    "Data Scientist",
    "Data Engineer",
    "BI Analyst",
]

df["role_category"] = np.select(conditions, choices, default="Other")

print("Saving dataset with skill flags...")
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print("\nDone.")
print(f"Saved to: {output_file}")

print("\nSkill totals:")
for skill in skill_patterns.keys():
    total = df[f"skill_{skill}"].sum()
    print(f"{skill}: {total}")

print("\nPreview:")
preview_columns = [
    "title",
    "location_name",
    "skills_found",
    "skill_count",
    "role_category"
]
print(df[preview_columns].head(10))