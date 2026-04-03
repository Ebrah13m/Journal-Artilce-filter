# Journal-Artilce-filter
A filtration script to identify and select relevant journal articles for synthesis based on predefined inclusion and exclusion criteria

# Overview
The python script was created whilst completing my Information Systems honours thesis. It loads multiple CSV exports from Zotero, merges them into a unified dataset, and applies a series of filtering steps to identify relevant studies based on predefined criteria. The final output is a structured CSV file containing only relevant articles.

# How it works
1. Load Zotero Exports
The script reads multiple CSV files exported from Zotero and loads them into a unified document set using the litstudy library.
2. Tag Source Files
Each article is tagged with its originating CSV file to maintain traceability throughout the filtering process.
3. Merge Datasets
All loaded documents are combined into a single dataset, allowing for consistent processing across sources.
4. Filter by Publication Year
Articles published before the year 2000 are excluded to ensure relevance and recency.
5. Apply Keyword Filtering
A predefined list of keywords is used to identify relevant studies. The script searches for matches across:
  - Title
  - Abstract
  - Keywords
6. Extract and Clean Metadata
Relevant fields (e.g., title, authors, abstract, DOI, keywords) are extracted and cleaned to handle missing or inconsistent data.
7. Export Results
The filtered dataset is converted into a structured format and saved as a CSV file (results.csv).
