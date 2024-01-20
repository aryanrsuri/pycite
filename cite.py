import re
import requests
import json


class Cite(object):
    """ Generate new Citation
        raw: str -- the raw string input
        rtype: str or None -- the valid raw input type (doi or bibtex)
    """
    entrytypes = {"article", "book", "booklet", "conference", "inbook", "incollection", "inproceedings",
                  "manual", "mastersthesis", "misc", "phdthesis", "proceedings", "techreport", "unpublished"}
    fieldtypes = {"address", "annote", "author", "booktitle", "Email", "chapter", "crossref", "doi", "edition", "editor", "howpublished", "institution",
                  "journal", "key", "month", "note", "number", "organization", "pages", "publisher", "school", "series", "title", "type", "volume", "year"}
    raw: str
    parts: dict[str, str]
    rtypes: set[str] = {"ris", "bib", "json", "enw"}

    def __init__(self, raw: str, rtype: str) -> None:
        self.parts: dict[str, str] = {}
        if rtype in self.rtypes:
            self.raw = raw.strip()
            self.rtype = rtype
            match rtype:
                case "bib":
                    self._parse_from_bibtex()
                case "ris":
                    self._parse_from_ris()
                case "json":
                    self._parse_from_json()
                case "enw":
                    self._parse_from_enw()
                case _:
                    raise Exception("Invalid input type")

    def _parse_from_bibtex(self) -> None:
        etf = re.search(r"@(\w+){(\w+),([^;]*)}", self.raw)
        if etf is not None:
            if etf.group(1) in self.entrytypes:
                self.parts["entry"] = etf.group(1)
                self.parts["tag"] = etf.group(2)
            for field in etf.group(3).splitlines():
                kv = re.search(r"(\w+)={(.+)},", field)
                if kv is not None:
                    if kv.group(1).strip() in self.fieldtypes:
                        self.parts[kv.group(1).strip()] = kv.group(2)
        if self.parts == {}:
            raise Exception("Parsing failed")
        return None

    def _parse_from_ris(self) -> None:
        risentrytypes= {
            "JOUR": "article",
            "BOOK": "book",
            "CONF": "conference",
            "CHAP": "inbook",
            "THES": ["mastersthesis", "phdthesis"],  # Multiple BibTeX types map to THES
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
            "A1": ["institution", "organization", "school"],  # Multiple BibTeX types map to A1
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
        rtype = re.search(r"TY\s+-\s+(\w+)", self.raw)
        if rtype is not None:
            if rtype.group(1) in risentrytypes:
                self.parts["entry"] = rtype.group(1)
        etf = re.findall(r"([^TY]\w{2})\s+-\s+(.*)", self.raw)
        if etf is not None:
            for match in etf:
                self.parts[match[0][1:]] = match[1]
        return None

    def _parse_from_json(self) -> None:
        return None

    def _parse_from_enw(self) -> None:
        return None

    def _fetch_doi(self) -> None:
        response = requests.get(
            'https://doi.org/api/handles/%s' % self.raw.strip())
        if response.status_code == 200:
            data: str = json.loads(response.text)['values'][0]
            self.parts["entry"] = data
            return None
        raise Exception("Invalid DOI")


if __name__ == "__main__":
    pass
