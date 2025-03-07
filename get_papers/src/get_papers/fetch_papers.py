import requests
import pandas as pd
from typing import List, Dict, Optional

PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def fetch_papers(query: str, max_results: int = 10) -> List[Dict]:
    """Fetch papers from PubMed based on a query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
    }
    response = requests.get(PUBMED_API_URL, params=params)
    response.raise_for_status()
    data = response.json()
    paper_ids = data.get("esearchresult", {}).get("idlist", [])
    
    papers = []
    for paper_id in paper_ids:
        paper_details = fetch_paper_details(paper_id)
        if paper_details:
            papers.append(paper_details)
    return papers

def fetch_paper_details(paper_id: str) -> Optional[Dict]:
    """Fetch details for a single paper using its PubMed ID."""
    params = {
        "db": "pubmed",
        "id": paper_id,
        "retmode": "xml",
    }
    response = requests.get(PUBMED_FETCH_URL, params=params)
    response.raise_for_status()
    # Parse XML response (you can use `xml.etree.ElementTree` or `lxml`)
    # Extract title, authors, affiliations, publication date, etc.
    # Example placeholder:
    return {
        "PubmedID": paper_id,
        "Title": "Sample Title",
        "Publication Date": "2023-10-01",
        "Non-academic Author(s)": ["Author 1", "Author 2"],
        "Company Affiliation(s)": ["Company A", "Company B"],
        "Corresponding Author Email": "author@example.com",
    }

def filter_non_academic_authors(authors: List[Dict]) -> List[str]:
    """Filter authors with non-academic affiliations."""
    non_academic_authors = []
    for author in authors:
        affiliations = author.get("affiliations", [])
        if any("pharma" in affil.lower() or "biotech" in affil.lower() for affil in affiliations):
            non_academic_authors.append(author.get("name", ""))
    return non_academic_authors