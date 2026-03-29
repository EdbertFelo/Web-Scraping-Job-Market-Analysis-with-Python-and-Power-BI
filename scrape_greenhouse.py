import os
import time
import requests
import pandas as pd

# Starter list of public Greenhouse board tokens to try.
# Some may fail or have zero jobs. That is normal.
board_tokens = [
    "greenhouse",
    "doordashusa",
    "axon",
    "capco",
    "oddball",
    "tatari",
    "builder",
    "growtherapy",
    "juno",
    "impact",
    "weee",
    "freshprints",
    "tebra",
    "2k",
]

skip_keywords = [
    "don't see what you're looking for",
    "dont see what you're looking for",
    "general application",
    "talent community",
    "join our talent network",
    "future opportunities",
]

all_rows = []
summary_rows = []

os.makedirs("data", exist_ok=True)

for board_token in board_tokens:
    list_endpoint = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"

    print(f"\n=== Trying board: {board_token} ===")

    try:
        list_response = requests.get(list_endpoint, timeout=30)
        list_response.raise_for_status()

        list_payload = list_response.json()
        jobs = list_payload.get("jobs", [])

        print(f"List endpoint returned {len(jobs)} rows")

        kept_count = 0

        for job in jobs:
            title = str(job.get("title", "")).strip().lower()
            internal_job_id = job.get("internal_job_id")
            job_post_id = job.get("id")

            # Skip prospect/talent-community style posts
            if internal_job_id is None:
                continue

            if any(keyword in title for keyword in skip_keywords):
                continue

            detail_endpoint = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs/{job_post_id}"

            try:
                detail_response = requests.get(detail_endpoint, timeout=30)
                detail_response.raise_for_status()
                detail = detail_response.json()

                location_dict = detail.get("location") or {}

                row = {
                    "board_token": board_token,
                    "job_post_id": detail.get("id"),
                    "internal_job_id": detail.get("internal_job_id"),
                    "title": detail.get("title"),
                    "location_name": location_dict.get("name"),
                    "absolute_url": detail.get("absolute_url"),
                    "updated_at": detail.get("updated_at"),
                    "language": detail.get("language"),
                    "description_html": detail.get("content"),
                }

                all_rows.append(row)
                kept_count += 1

                print(f"Collected: {detail.get('title')}")

                time.sleep(0.2)

            except requests.exceptions.RequestException as e:
                print(f"Failed detail request for job id {job_post_id}: {e}")

        summary_rows.append({
            "board_token": board_token,
            "list_rows_returned": len(jobs),
            "rows_kept": kept_count,
            "status": "success"
        })

        print(f"Finished {board_token}: kept {kept_count} jobs")

    except requests.exceptions.RequestException as e:
        print(f"Board failed: {board_token} -> {e}")

        summary_rows.append({
            "board_token": board_token,
            "list_rows_returned": 0,
            "rows_kept": 0,
            "status": f"failed: {e}"
        })

raw_df = pd.DataFrame(all_rows)
summary_df = pd.DataFrame(summary_rows)

# Remove duplicates across boards just in case
raw_df = raw_df.drop_duplicates(subset=["board_token", "job_post_id"])

raw_output = "data/greenhouse_jobs_raw.csv"
summary_output = "data/greenhouse_collection_summary.csv"

raw_df.to_csv(raw_output, index=False, encoding="utf-8-sig")
summary_df.to_csv(summary_output, index=False, encoding="utf-8-sig")

print("\n==============================")
print("COLLECTION FINISHED")
print("==============================")
print(f"Total jobs saved: {len(raw_df)}")
print(f"Raw dataset saved to: {raw_output}")
print(f"Summary saved to: {summary_output}")

print("\nTop 10 boards by rows kept:")
if len(summary_df) > 0:
    print(summary_df.sort_values("rows_kept", ascending=False).head(10))