import os
import pandas as pd
import litstudy

# Path to Zotero CSV folder
folder_path = "/home/ebrahiem/Documents/Journal Article Data"

# List of specific CSV files to load
csv_files = [
    "Autism Diagnosis.csv",    # 10
    "Interpretable AI for CDSS.csv",   # 50
    "Interpretable AI in low resource setting.csv", #7
    "Ethical and Inclusive Technology Design.csv"  #14 -> 0
]

# Load each document
docs_all = None
for filename in csv_files:
    file_path = os.path.join(folder_path, filename)
    docs = litstudy.load_csv(file_path)

    # Tag each document with its source file name
    for doc in docs:
        if not hasattr(doc, "record"):
            doc.record = {}
        doc.record["source_file"] = filename

    docs_all = docs if docs_all is None else docs_all | docs

print(len(docs_all), "papers loaded from Zotero exports")

# Filter by publication year
docs_filtered = docs_all.filter_docs(
    lambda d: d.publication_year is not None and d.publication_year >= 2000
)

# Keyword Filtering
keywords = [
    "artificial intelligence", "clinical decision support", "autism",
    "low-resource", "facilitating conditions", "performance expectancy",
    "ASD", "CDSS", "Africa", "Clinicians", "Healthcare"
]

def keyword_match(doc):
    record = getattr(doc, "record", {})

    def safe_lower(text):
        return text.lower() if isinstance(text, str) else ""

    text_fields = [
        safe_lower(getattr(doc, "title", record.get("title", ""))),
        safe_lower(getattr(doc, "abstract", record.get("abstract", ""))),
        safe_lower(record.get("keywords", ""))
    ]

    return any(kw.lower() in field for kw in keywords for field in text_fields)

docs_filtered = docs_filtered.filter_docs(keyword_match)
print(len(docs_filtered), "papers matched keyword filter")

# Convert documents to dictionaries 
results_data = []
for doc in docs_filtered:
    record = getattr(doc, "record", {})

    authors = getattr(doc, "authors", [])
    author_names = [author.name for author in authors if hasattr(author, "name")]

    raw_keywords = record.get("keywords", "")
    if isinstance(raw_keywords, str):
        keywords_list = [kw.strip() for kw in raw_keywords.split(",") if kw.strip()]
    elif isinstance(raw_keywords, (list, tuple)):
        keywords_list = raw_keywords
    else:
        keywords_list = []

    results_data.append({
        "title": getattr(doc, "title", record.get("title", "")),
        "authors": ", ".join(author_names),
        "publication_year": getattr(doc, "publication_year", record.get("publication_year", "")),
        "doi": record.get("DOI", ""),
        "library_catalog": record.get("Library Catalog", ""),
        "abstract": getattr(doc, "abstract", record.get("abstract", "")),
        "keywords": ", ".join(keywords_list),
        "source_file": record.get("source_file", "")
    })

# Save to CSV
results_df = pd.DataFrame(results_data)
results_df.to_csv("results.csv", index=False)
print("Results saved to results.csv")
