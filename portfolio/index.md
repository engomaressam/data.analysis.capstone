# Portfolio Index: Cyclistic Bike-Share Case Study

Welcome. This page links the report, figures, tables, and notebooks (both Python and R) and explains how to reproduce the analysis locally or on Kaggle.

## Report
- Case study report: documentation/case_study_report_template.md

## Figures (SVG gallery)
- portfolio/assets/figures/ride_duration.svg
- portfolio/assets/figures/comparative_analysis.svg
- portfolio/assets/figures/time_patterns.svg
- portfolio/assets/figures/stations.svg
- portfolio/assets/figures/member_types.svg

## Tables (CSV index)
- portfolio/assets/tables/missing_summary.csv
- portfolio/assets/tables/duration_stats.csv
- portfolio/assets/tables/hourly_usage.csv
- portfolio/assets/tables/daily_usage.csv
- portfolio/assets/tables/weekend_usage.csv
- portfolio/assets/tables/monthly_usage.csv
- portfolio/assets/tables/time_patterns.csv
- portfolio/assets/tables/top_start_stations.csv
- portfolio/assets/tables/top_end_stations.csv
- portfolio/assets/tables/top_stations_member.csv
- portfolio/assets/tables/bike_preferences.csv
- portfolio/assets/tables/bike_percentages.csv
- portfolio/assets/tables/comparison_metrics.csv
- portfolio/assets/tables/member_distribution.csv

## Notebooks (for Kaggle publishing)
- Python notebook: portfolio/kaggle_portfolio_notebook.ipynb
- R notebook: portfolio/kaggle_portfolio_notebook.Rmd

## How to reproduce (local)
1. Ensure Python 3.10+ with pip installed.
2. Install required libraries:
   - pip install pandas numpy matplotlib seaborn
3. Place cleaned dataset at data/processed/cyclistic_cleaned.csv (or build using analysis/data_cleaning/build_clean_dataset.py).
4. Run the EDA script to regenerate figures and tables:
   - python analysis/exploratory/cyclistic_eda.py
5. Outputs will be saved to analysis/exploratory and mirrored under portfolio/assets.

## How to publish on Kaggle (Python and R)
1. Upload the Python notebook (portfolio/kaggle_portfolio_notebook.ipynb) to Kaggle Notebooks.
2. Upload the R notebook (portfolio/kaggle_portfolio_notebook.Rmd) to Kaggle Notebooks.
3. Attach the relevant dataset(s) in Kaggle or reference public Divvy system data.
4. Ensure output paths inside the notebooks point to the working directory in Kaggle (adjust relative paths as needed).

## Notes
- Large raw and processed data directories are intentionally excluded from version control to keep the repository lightweight.
- When running locally, download the Divvy trip data for the analysis period and place the CSVs in data/raw or use the processed dataset in data/processed.