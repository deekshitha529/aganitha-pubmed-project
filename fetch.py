import requests
from typing import List, Dict
from xml.etree import ElementTree as ET

def fetch_paper_details(pubmed_ids: List[str]) -> List[Dict]:
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml"
    }

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print("❌ Failed to fetch paper details.")
        return []

    root = ET.fromstring(response.content)
    results = []

    for article in root.findall(".//PubmedArticle"):
        try:
            pmid = article.findtext(".//PMID")
            title = article.findtext(".//ArticleTitle")
            pub_date = article.findtext(".//PubDate/Year") or "N/A"
            authors = article.findall(".//Author")
            emails = article.findall(".//AffiliationInfo")

            non_academic_authors = []
            companies = []
            email = "N/A"

            for author in authors:
                lastname = author.findtext("LastName") or ""
                for aff in author.findall(".//AffiliationInfo/Affiliation"):
                    aff_text = aff.text or ""
                    if not any(word in aff_text.lower() for word in ["university", "college", "institute", "school", "dept"]):
                        non_academic_authors.append(lastname)
                        companies.append(aff_text)
                    if "@" in aff_text:
                        email = aff_text.split()[-1]

            results.append({
                "PubmedID": pmid,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": ", ".join(set(non_academic_authors)),
                "Company Affiliation(s)": ", ".join(set(companies)),
                "Corresponding Author Email": email
            })
        except Exception as e:
            print("⚠️ Error parsing article:", e)
            continue

    return results
