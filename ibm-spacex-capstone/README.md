# Falcon 9 Landing Prediction

Reproduced analysis of the public IBM Applied Data Science Capstone course snapshots.

## Run
```bash
pip install -r requirements.txt
python analysis.py
python create_map.py
python dashboard.py
```
Open http://127.0.0.1:8050 for Dash. Open launch_map.html for Folium.
The map needs an internet connection for map tiles and JavaScript assets.

## Files
- capstone_analysis.ipynb: executed analysis with outputs
- analysis.py: SQL, EDA summaries and reproducible classification
- results.json: computed metrics and query outputs
- queries.sql: all ten SQL exercise queries
- dashboard.py: working Dash application with site and payload filters
- create_map.py and launch_map.html: Folium map and generator
- data/: unchanged public course snapshots

## Project location
https://github.com/shyrradev/PYTHON/tree/ibm-spacex-capstone/ibm-spacex-capstone

## Notebooks
1. 01_data_collection.ipynb
2. 02_web_scraping.ipynb
3. 03_data_wrangling.ipynb
4. 04_eda_visualization.ipynb
5. 05_eda_sql.ipynb
6. 06_folium_map.ipynb
7. 07_predictive_analysis.ipynb

## Sources
All CSVs come from https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/
The dataset_part_1.csv, dataset_part_2.csv, dataset_part_3.csv, spacex_launch_dash.csv and spacex_launch_geo.csv files are under datasets/. Spacex.csv is under labs/module_2/data/.

The 90-row main dataset differs from the 101-row SQL and 56-row interactive datasets. The course binary target includes successful ocean outcomes and treats no attempt or unknown outcomes as class 0. Results describe historical course data.
