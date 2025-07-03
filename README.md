CSRankings Project – Personal Version
📅 June–July 2025

👋 Introduction
This project is my personal take on the CSRankings system. The goal was to understand how computer science institutions are ranked based on research output—specifically, using publication data from DBLP. Over the past few weeks, I’ve worked on data collection, database setup, and some initial analysis using Python and PostgreSQL.

✅ What I’ve Done So Far
📚 Collected and cleaned 2,100+ publication records for top researchers using the DBLP API and OpenAlex.

🧱 Set up a PostgreSQL database (csrankings_db) and imported all cleaned data into a structured table.

🐍 Wrote custom Python scripts to:

Fetch publication and affiliation data

Clean and filter results

Import data into the database for querying and analysis

📁 Key Files in This Repo
fetch_faculty.py – Pulls author publication data and affiliations from DBLP/OpenAlex

import_to_postgres.py – Loads JSON data into the PostgreSQL publications table

publications.json – Raw data dump from DBLP (sample)

output.csv – Cleaned and exported data (shortened for GitHub)

🛠️ How to Set It Up
Requirements
PostgreSQL (I used version 16.x)

Python 3.x with these packages:

php
Copy
Edit
pip install requests psycopg2-binary pandas
Setup Steps
Create a PostgreSQL database (e.g., csrankings_db)

Edit the import_to_postgres.py file with your DB credentials

Run the import script to load your data:

bash
Copy
Edit
python import_to_postgres.py
🧩 Challenges Faced
Fixed PostgreSQL connection errors and missing paths

Dealt with duplicate entries and invalid data

Recovered from table deletion issues by re-importing JSON data

🚀 What’s Next?
Clean up edge cases and filter incomplete entries

Develop logic to rank institutions by publication impact

Expand the dataset to include more faculty members and additional years

📄 License
MIT – free to use, modify, and build on.

🙋‍♂️ Contact
If you’re interested or have feedback, feel free to reach out!
GitHub: jonkenboy