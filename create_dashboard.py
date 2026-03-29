import os
import pandas as pd

input_file = "data/final_jobs_for_dashboard.csv"

jobs_output = "data/dashboard_jobs_detail.csv"
skills_output = "data/dashboard_skill_summary.csv"
roles_output = "data/dashboard_role_summary.csv"
locations_output = "data/dashboard_location_summary.csv"

print("Loading final dashboard dataset...")
df = pd.read_csv(input_file)

print("Rows loaded:", len(df))

os.makedirs("data", exist_ok=True)

# ----------------------------
# 1. Save detailed jobs table
# ----------------------------
jobs_detail = df.copy()
jobs_detail.to_csv(jobs_output, index=False, encoding="utf-8-sig")
print(f"Saved detailed jobs table: {jobs_output}")

# ----------------------------
# 2. Skill summary table
# ----------------------------
skill_columns = [col for col in df.columns if col.startswith("skill_")]

skill_rows = []
for col in skill_columns:
    skill_name = col.replace("skill_", "")
    count_jobs = int(df[col].sum())
    pct_jobs = round((count_jobs / len(df)) * 100, 2) if len(df) > 0 else 0

    skill_rows.append({
        "skill_name": skill_name,
        "job_count": count_jobs,
        "job_percentage": pct_jobs
    })

skill_summary = pd.DataFrame(skill_rows).sort_values("job_count", ascending=False)
skill_summary.to_csv(skills_output, index=False, encoding="utf-8-sig")
print(f"Saved skill summary table: {skills_output}")

# ----------------------------
# 3. Role summary table
# ----------------------------
role_summary = (
    df.groupby("role_category", dropna=False)
    .agg(
        job_count=("job_post_id", "count"),
        avg_skill_count=("skill_count", "mean"),
        remote_jobs=("is_remote", "sum"),
        hybrid_jobs=("is_hybrid", "sum"),
    )
    .reset_index()
)

role_summary["avg_skill_count"] = role_summary["avg_skill_count"].round(2)
role_summary["remote_pct"] = round((role_summary["remote_jobs"] / role_summary["job_count"]) * 100, 2)
role_summary["hybrid_pct"] = round((role_summary["hybrid_jobs"] / role_summary["job_count"]) * 100, 2)

role_summary = role_summary.sort_values("job_count", ascending=False)
role_summary.to_csv(roles_output, index=False, encoding="utf-8-sig")
print(f"Saved role summary table: {roles_output}")

# ----------------------------
# 4. Location summary table
# ----------------------------
location_summary = (
    df.groupby("location_name", dropna=False)
    .agg(
        job_count=("job_post_id", "count"),
        avg_skill_count=("skill_count", "mean"),
        remote_jobs=("is_remote", "sum"),
        hybrid_jobs=("is_hybrid", "sum"),
    )
    .reset_index()
)

location_summary["avg_skill_count"] = location_summary["avg_skill_count"].round(2)
location_summary["remote_pct"] = round((location_summary["remote_jobs"] / location_summary["job_count"]) * 100, 2)
location_summary["hybrid_pct"] = round((location_summary["hybrid_jobs"] / location_summary["job_count"]) * 100, 2)

location_summary = location_summary.sort_values("job_count", ascending=False)
location_summary.to_csv(locations_output, index=False, encoding="utf-8-sig")
print(f"Saved location summary table: {locations_output}")

# ----------------------------
# 5. Print preview
# ----------------------------
print("\nTop skills:")
print(skill_summary.head(10))

print("\nRole summary:")
print(role_summary.head(10))

print("\nTop locations:")
print(location_summary.head(10))

print("\nDone.")