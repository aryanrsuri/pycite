import re
import requests
import json


class Cite(object):
    """ Generate new Citation
        raw: str -- the raw string input
        rtype: str or None -- the valid raw input type (doi or bibtex)
    """
    raw: str
    parts: dict[str, str]
    rtypes: set[str] = {"ris", "bib", "json", "enw"}

    def __init__(self, raw: str, rtype: str) -> None:
        self.parts: dict[str, str] = {}
        if rtype in self.rtypes:
            self.raw = raw
            self.parts["rtype"] = rtype
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
        entrytypes = {"article", "book", "booklet", "conference", "inbook", "incollection", "inproceedings",
                      "manual", "mastersthesis", "misc", "phdthesis", "proceedings", "techreport", "unpublished"}
        fieldtypes = {"address", "annote", "author", "booktitle", "Email", "chapter", "crossref", "doi", "edition", "editor", "howpublished", "institution",
                      "journal", "key", "month", "note", "number", "organization", "pages", "publisher", "school", "series", "title", "type", "volume", "year"}
        etf = re.search(r"@(\w+){(\w+),([^;]*)}", self.raw)
        if etf is not None:
            if etf.group(1) in entrytypes:
                self.parts["entry"] = etf.group(1)
                self.parts["tag"] = etf.group(2)
            for field in etf.group(3).splitlines():
                kv = re.search(r"(\w+)={(.+)},", field)
                if kv is not None:
                    if kv.group(1).strip() in fieldtypes:
                        self.parts[kv.group(1).strip()] = kv.group(2)
        if self.parts == {}:
            raise Exception("Parsing failed")
        return None

    def _parse_from_ris(self) -> None:
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
