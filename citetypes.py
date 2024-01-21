entrytypes = {"article", "book", "booklet", "conference", "inbook", "incollection", "inproceedings",
              "manual", "mastersthesis", "misc", "phdthesis", "proceedings", "techreport", "unpublished"}
fieldtypes = {"address", "annote", "author", "booktitle", "Email", "chapter", "crossref", "doi", "edition", "editor", "howpublished", "institution",
              "journal", "key", "month", "note", "number", "organization", "pages", "publisher", "school", "series", "title", "type", "volume", "year"}
risentrytypes = {
    "JOUR": "article",
    "BOOK": "book",
    "CONF": "conference",
    "CHAP": "inbook",
    # Multiple BibTeX types map to THES
    "THES": ["mastersthesis", "phdthesis"],
    "GEN": "manual",
    "RPRT": "techreport",
    "UNPB": "unpublished"
}

risfieldtypes = {
    "AD": "address",
    "N1": ["annote", "note"],  # Multiple BibTeX types map to N1
    "AU": "author",
    "T2": "booktitle",
    "CN": "chapter",
    "DO": "doi",
    "ET": "edition",
    "ED": "editor",
    # Multiple BibTeX types map to A1
    "A1": ["institution", "organization", "school"],
    "JA": "journal",
    "M1": "month",
    "IS": "number",
    "SP": "pages",
    "PB": "publisher",
    "T3": "series",
    "T1": "title",
    "M3": "type",
    "VL": "volume",
    "PY": "year"
}
