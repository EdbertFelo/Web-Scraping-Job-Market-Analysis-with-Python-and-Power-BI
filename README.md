# Web-Scraping-Job-Market-Analysis-with-Python-and-Power-BI
End-to-end job market analysis project using web scraping, Python, Pandas, NumPy, and Power BI.

# Job Market Analysis using Web Scraping, Python, and Power BI

## Project Overview

This project analyzes public data-related job postings collected from company career pages to identify in-demand skills, role distribution, and hiring locations.

The project was built as an end-to-end data analytics workflow using web scraping, Python, Pandas, NumPy, and Power BI.

## Project Objective

The goal of this project was to build a real-world data analyst portfolio project using live public job-posting data instead of a static dataset.

This project answers questions such as:
- Which technical skills appear most frequently in data-related roles?
- Which role categories appear most often?
- Which locations are hiring the most?
- Which roles require more skills on average?

## Tools Used

- Python
- Requests
- BeautifulSoup
- Pandas
- NumPy
- Power BI

## Project Workflow

1. Collected public job postings from company career pages using Python
2. Cleaned raw job description text and removed HTML formatting
3. Extracted skill keywords such as Python, SQL, Excel, Power BI, Tableau, Spark, AWS, and more
4. Categorized jobs by role type and seniority
5. Built summary tables for dashboard reporting
6. Created an interactive Power BI dashboard to visualize insights

## Dataset Summary

- 2,000+ raw public job postings collected
- 139 filtered data-related job postings used for dashboard analysis
- Multiple role categories including Business Analyst, Data Engineer, Data Scientist, Data Analyst, ML Engineer, and BI / Analytics

## Key Insights

- Python and SQL were the most frequently mentioned skills in the filtered dataset
- Business Analyst and Data Engineer roles appeared most often
- Data Engineer roles showed higher average skill requirements than several other role categories
- The dashboard also highlighted top hiring locations across the filtered dataset

## Dashboard Preview

Add your dashboard screenshots here after uploading them.

## Repository Structure

- `src/` → Python scripts
- `data/` → cleaned and dashboard-ready data files
- `images/` → dashboard screenshots
- `job_market_dashboard.pbix` → Power BI dashboard file

## How to Run

1. Install packages:
   `pip install requests pandas numpy beautifulsoup4`

2. Run the scripts in order:
   - `01_collect_greenhouse_jobs.py`
   - `02_clean_greenhouse_jobs.py`
   - `03_extract_skills.py`
   - `04_prepare_dashboard_dataset.py`
   - `05_create_dashboard_tables.py`

3. Open the Power BI file:
   - `job_market_dashboard.pbix`

## Author

This project was created as a portfolio project for data analyst internship applications, with a focus on building a real-world analytics workflow from web scraping to dashboard storytelling.
