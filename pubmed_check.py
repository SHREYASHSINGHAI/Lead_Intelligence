import requests
import datetime

def get_pubmed_count(search_term, years=2):
    today = datetime.datetime.today()
    start_year = today.year - years

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": search_term,
        "mindate": start_year,
        "maxdate": today.year,
        "retmode": "json"
    }

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()
    return int(data["esearchresult"]["count"])
