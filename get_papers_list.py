import requests
from pubmed_fetcher.fetch import fetch_paper_details

def fetch_pubmed_ids(query, max_results=5):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        id_list = data["esearchresult"]["idlist"]
        print("✅ PubMed IDs found:", id_list)
        return id_list
    else:
        print("❌ Error fetching data from PubMed API")
        return []

if __name__ == "__main__":
    search_query = "cancer treatment"
    pubmed_ids = fetch_pubmed_ids(search_query)

    if pubmed_ids:
        papers = fetch_paper_details(pubmed_ids)
        print("\n📄 Fetched Paper Details:")
        for paper in papers:
            print(paper)
