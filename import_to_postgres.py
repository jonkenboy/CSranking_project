import psycopg2
import json

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname="csrankings_db",  # Changed from "faculty_db"
        user="postgres",        # Changed from "jjonk_user"
        password="your_password",  # Changed from "mysecurepassword"
        host="localhost",
        port="5432"            # Changed from "5434"
    )
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # Create table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS public.publications (
            id SERIAL PRIMARY KEY,
            title TEXT,
            year INT,
            authors TEXT,
            venue TEXT,
            doi TEXT
        );
    """)

    # Load and insert data from cleaned_publications.json
    with open("cleaned_publications.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        total_entries = len(data)
        inserted_count = 0
        skipped_count = 0
        for i, hit in enumerate(data):
            print(f"Processing entry {i}: {hit}")
            try:
                info = hit.get("info")
                if not info or not isinstance(info, dict):
                    print(f"Skipping invalid entry {i}: {hit}")
                    skipped_count += 1
                    continue
                try:
                    title = info.get("title") if isinstance(info.get("title"), (str, type(None))) else "No title"
                    print(f"Title check {i}: {title}, type: {type(info.get('title')) if info.get('title') else 'None'}")
                    year = int(info.get("year", "0")) if isinstance(info.get("year"), (str, int)) else 0
                    print(f"Year check {i}: {year}, type: {type(info.get('year')) if info.get('year') else 'None'}")
                    authors_data = info.get("authors", {})
                    if isinstance(authors_data, str):
                        authors = authors_data
                    elif isinstance(authors_data.get("author"), list):
                        authors = ", ".join(a.get("text", "") for a in authors_data.get("author", []) if isinstance(a, dict))
                    else:
                        authors = "Unknown"
                    print(f"Authors check {i}: {authors}, type: {type(authors_data)}")
                    venue = info.get("venue") if isinstance(info.get("venue"), (str, type(None))) else "Unknown"
                    doi = info.get("doi") if isinstance(info.get("doi"), (str, type(None))) else "Unknown"
                    cur.execute("""
                        INSERT INTO public.publications (title, year, authors, venue, doi)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (title, year, authors, venue, doi))
                    inserted_count += 1
                except Exception as e:
                    print(f"Error inserting entry {i}: {hit}: {e}")
                    skipped_count += 1
            except Exception as e:
                print(f"Error processing entry {i}: {hit}: {e}")
                skipped_count += 1
        print(f"Inserted {inserted_count} out of {total_entries} entries into PostgreSQL! Skipped {skipped_count} entries due to errors.")

except Exception as e:
    print(f"Connection or execution error: {e}")
finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()
