import re
import numpy as np
import pandas as pd

input_file = "data/greenhouse_jobs_cleaned.csv"
output_file = "data/final_jobs_for_dashboard.csv"

print("Loading cleaned dataset...")
df = pd.read_csv(input_file)

print("Rows loaded:", len(df))

# Make sure text columns exist
df["title"] = df["title"].fillna("").astype(str)
df["description_text"] = df["description_text"].fillna("").astype(str)
df["location_name"] = df["location_name"].fillna("").astype(str)

# ----------------------------
# 1. Create role category
# ----------------------------
print("Creating role categories...")

role_conditions = [
    df["title"].str.contains(r"data analyst|analytics analyst", case=False, regex=True, na=False),
    df["title"].str.contains(r"business analyst", case=False, regex=True, na=False),
    df["title"].str.contains(r"business intelligence|bi analyst|bi developer", case=False, regex=True, na=False),
    df["title"].str.contains(r"data scientist|machine learning scientist", case=False, regex=True, na=False),
    df["title"].str.contains(r"data engineer|analytics engineer", case=False, regex=True, na=False),
    df["title"].str.contains(r"machine learning engineer|ml engineer", case=False, regex=True, na=False),
]

role_choices = [
    "Data Analyst",
    "Business Analyst",
    "BI / Analytics",
    "Data Scientist",
    "Data Engineer",
    "ML Engineer",
]

df["role_category"] = np.select(role_conditions, role_choices, default="Other")

# ----------------------------
# 2. Keep only relevant rows
# ----------------------------
print("Filtering to relevant data-related jobs...")

relevant_titles_pattern = (
    r"data analyst|analytics analyst|business analyst|business intelligence|"
    r"\bbi\b|data scientist|data engineer|analytics engineer|"
    r"machine learning|ml engineer|reporting analyst|insights analyst"
)

df_relevant = df[
    df["title"].str.contains(relevant_titles_pattern, case=False, regex=True, na=False)
].copy()

print("Rows after relevant-role filtering:", len(df_relevant))

# ----------------------------
# 3. Better skill detection
# ----------------------------
print("Creating improved skill flags...")

skill_patterns = {
    "python": r"\bpython\b",
    "sql": r"\bsql\b|postgresql|mysql|sql server|tsql|t-sql",
    "excel": r"\bexcel\b|spreadsheets?",
    "power_bi": r"\bpower[\s-]?bi\b",
    "tableau": r"\btableau\b",
    "pandas": r"\bpandas\b",
    "numpy": r"\bnumpy\b",
    "spark": r"\bspark\b|pyspark",
    "aws": r"\baws\b|amazon web services",
    "azure": r"\bazure\b",
    "gcp": r"\bgcp\b|google cloud",
    "snowflake": r"\bsnowflake\b",
    "etl": r"\betl\b|\belf?\b|data pipeline|data pipelines",
    "dashboarding": r"dashboard|dashboards|reporting|visualization|visualisation",
    "statistics": r"statistics|statistical|hypothesis testing|a\/b testing|ab testing",
    "r": r"\brstudio\b|\br language\b|\busing r\b|\bproficiency in r\b|\bexperience with r\b",
}

for skill_name, pattern in skill_patterns.items():
    col = f"skill_{skill_name}"
    df_relevant[col] = df_relevant["description_text"].str.contains(
        pattern,
        case=False,
        regex=True,
        na=False
    ).astype(int)

# ----------------------------
# 4. Build readable skill list
# ----------------------------
print("Creating skills_found and skill_count...")

skill_cols = [f"skill_{s}" for s in skill_patterns.keys()]

def collect_skills(row):
    found = []
    for skill in skill_patterns.keys():
        if row[f"skill_{skill}"] == 1:
            found.append(skill)
    return ", ".join(found)

df_relevant["skills_found"] = df_relevant.apply(collect_skills, axis=1)
df_relevant["skill_count"] = df_relevant[skill_cols].sum(axis=1)

# ----------------------------
# 5. Seniority from title
# ----------------------------
print("Creating seniority column...")

seniority_conditions = [
    df_relevant["title"].str.contains(r"\bintern\b|\btrainee\b", case=False, regex=True, na=False),
    df_relevant["title"].str.contains(r"\bjunior\b|\bentry\b", case=False, regex=True, na=False),
    df_relevant["title"].str.contains(r"\bsenior\b|\blead\b|\bprincipal\b|\bstaff\b", case=False, regex=True, na=False),
    df_relevant["title"].str.contains(r"\bmanager\b|\bdirector\b|\bhead\b", case=False, regex=True, na=False),
]

seniority_choices = [
    "Intern / Trainee",
    "Junior / Entry",
    "Senior / Lead",
    "Manager+",
]

df_relevant["seniority"] = np.select(seniority_conditions, seniority_choices, default="Mid")

# ----------------------------
# 6. Remote / hybrid flags
# ----------------------------
print("Creating work arrangement flags...")

combined_text = (
    df_relevant["title"].fillna("") + " " +
    df_relevant["location_name"].fillna("") + " " +
    df_relevant["description_text"].fillna("")
)

df_relevant["is_remote"] = combined_text.str.contains(
    r"\bremote\b|work from home|wfh",
    case=False,
    regex=True,
    na=False
).astype(int)

df_relevant["is_hybrid"] = combined_text.str.contains(
    r"\bhybrid\b",
    case=False,
    regex=True,
    na=False
).astype(int)

# ----------------------------
# 7. Keep useful columns
# ----------------------------
final_columns = [
    "board_token",
    "job_post_id",
    "title",
    "role_category",
    "seniority",
    "location_name",
    "absolute_url",
    "updated_at",
    "language",
    "description_preview",
    "skills_found",
    "skill_count",
    "is_remote",
    "is_hybrid",
] + skill_cols

final_df = df_relevant[final_columns].copy()

# Drop duplicates just in case
final_df = final_df.drop_duplicates(subset=["board_token", "job_post_id"])

print("Saving final dashboard dataset...")
final_df.to_csv(output_file, index=False, encoding="utf-8-sig")

print("\nDone.")
print("Final rows:", len(final_df))
print(f"Saved to: {output_file}")

print("\nRole category counts:")
print(final_df["role_category"].value_counts())

print("\nTop skill totals:")
for col in skill_cols:
    print(f"{col}: {final_df[col].sum()}")

print("\nPreview:")
print(final_df.head(10))