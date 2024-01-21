import re
import requests
import json
from citetypes import entrytypes, risentrytypes
from citetypes import fieldtypes


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

    def templ(self, ftype: str) -> str:
        match ftype:
            case "mla":
                return self.__templ_mla(self.parts)
            case "apa":
                return self.__templ_apa(self.parts)
            case _:
                return "Null template"

    @staticmethod
    def __templ_mla(parts: dict):
        mla_citation = {
            "author": parts.get('author', ''),
            "title": parts.get('title', ''),
            "journal": parts.get('journal', ''),
            "volume": parts.get('volume', ''),
            "number": parts.get('number', ''),
            "pages": parts.get('pages', ''),
            "publisher": parts.get('publisher', ''),
            "year": parts.get('year', '')
        }
        return f"{mla_citation['author']}. \"{mla_citation['title']}\". {mla_citation['publisher']} {mla_citation['year']}. {mla_citation['journal']}, vol. {mla_citation['volume']}, no. {mla_citation['number']}, {mla_citation['pages']}."

    @staticmethod
    def __templ_apa(parts: dict):
        apa_citation = {
            "author": parts.get('author', ''),
            "year": parts.get('year', ''),
            "title": parts.get('title', ''),
            "source": parts.get('source', ''),
            "volume": parts.get('volume', ''),
            "pages": parts.get('pages', '')
        }

        return f"{apa_citation['author']} ({apa_citation['year']}). {apa_citation['title']}. {apa_citation['source']}, {apa_citation['volume']}, {apa_citation['pages']}."
