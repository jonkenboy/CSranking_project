import requests
import json
from time import sleep

def fetch_dblp_publications(search_token, max_retries=5):
    """Fetch publications for a given DBLP search token."""
    base_url = "https://dblp.org/search/publ/api"
    hits_per_request = 50
    all_publications = []
    start = 0

    for attempt in range(max_retries):
        url = f"{base_url}?q=author:{search_token}:&format=json&h={hits_per_request}&f={start}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                print(f"DBLP response: {data}")
                hits = data.get("result", {}).get("hits", {}).get("hit", [])
                if not hits:
                    print("No publications found. Trying alternative query...")
                    alt_url = f"{base_url}?q=author:{search_token.replace('_', ' ')}:&format=json&h={hits_per_request}&f={start}"
                    alt_response = requests.get(alt_url)
                    if alt_response.status_code == 200:
                        alt_data = alt_response.json()
                        print(f"Alternative DBLP response: {alt_data}")
                        hits = alt_data.get("result", {}).get("hits", {}).get("hit", [])
                        if not hits:
                            print("No publications found with alternative query.")
                            break
                    elif alt_response.status_code == 429:
                        print("Rate limit exceeded. Waiting before retrying...")
                        sleep(60)
                        continue
                    else:
                        print(f"Alternative query error: HTTP {alt_response.status_code}")
                        break
                all_publications.extend(hits)
                print(f"Fetched {len(hits)} publications (total: {len(all_publications)})")
                if len(hits) < hits_per_request:
                    break
                start += hits_per_request
                sleep(1)  # Avoid rate limits
            elif response.status_code == 429:
                print("Rate limit exceeded. Waiting before retrying...")
                sleep(60)
                continue
            else:
                print(f"Error: HTTP {response.status_code}")
                break
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            break

    return all_publications

def fetch_openalex_affiliation(search_name):
    """Fetch affiliation for a given author name using OpenAlex."""
    openalex_url = f"https://api.openalex.org/authors?filter=display_name.search:{search_name}"
    try:
        response = requests.get(openalex_url)
        print(f"OpenAlex response status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Raw OpenAlex data: {data}")
            authors = data.get("results", [])
            if authors:
                best_author = max(authors, key=lambda x: x.get("works_count", 0), default=None)
                if best_author and best_author.get("works_count", 0) > 0:
                    institutions = best_author.get("last_known_institutions", [])
                    institution = institutions[0].get("display_name", "Unknown") if institutions and institutions[0].get("display_name") else "Unknown"
                    if not institution or institution == "Unknown":
                        affiliations = best_author.get("affiliations", [])
                        institution = affiliations[0].get("institution", {}).get("display_name", "Unknown") if affiliations else "Unknown"
                    return institution
            print("No suitable author found with significant works.")
            return "Unknown"
        else:
            print(f"OpenAlex request failed with status: {response.status_code}")
            return "Unknown"
    except requests.RequestException as e:
        print(f"Error fetching OpenAlex data: {e}")
        return "Unknown"

def save_faculty_data(publications, affiliation, search_token):
    """Save publications and affiliation to files."""
    # Save publications to text
    with open("publications.txt", "w", encoding="utf-8") as f:
        for hit in publications:
            title = hit.get("info", {}).get("title", "No title")
            years = hit.get("info", {}).get("year")  # Could be a string or list
            year_str = years[0] if isinstance(years, list) else years if years else "No year"
            f.write(f"- {title} ({year_str})\n")
    print("Saved to publications.txt")

    # Save publications to JSON
    with open("publications.json", "w") as f:
        json.dump(publications, f, indent=2)
    print("Saved to publications.json")
    print(f"Total publications: {len(publications)}")
    for hit in publications[:5]:  # Show first 5
        title = hit.get("info", {}).get("title")
        years = hit.get("info", {}).get("year")
        year_str = years[0] if isinstance(years, list) else years if years else "No year"
        print(f"- {title} ({year_str})")

    # Save affiliation to CSV
    affiliation_filename = "faculty-affiliations.csv"
    with open(affiliation_filename, "w", encoding="utf-8") as f:
        f.write("search_token,affiliation\n")
        f.write(f"{search_token},{affiliation}\n")
    print(f"Affiliation: {affiliation}")
    print(f"Saved to {affiliation_filename}")

# Main execution
if __name__ == "__main__":
    # Example usage: Replace with the desired faculty member's search token or name
    faculty_search_token = "Michael_I_Jordan"  # Example, adjust based on PID or name
    publications = fetch_dblp_publications(faculty_search_token)
    affiliation = fetch_openalex_affiliation(faculty_search_token.replace("_", " "))
    save_faculty_data(publications, affiliation, faculty_search_token)
