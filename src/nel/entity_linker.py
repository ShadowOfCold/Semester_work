import requests

class EntityLinker:
    def search_wikidata(self, query: str):
        url = "https://www.wikidata.org/w/api.php"
        params = {
            "action": "wbsearchentities",
            "search": query,
            "language": "ru",
            "format": "json",
            "limit": 1
        }

        headers = {
            "User-Agent": "NER-NEL-Semester-Work/1.0"
        }

        try:
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            data = resp.json()

            results = data.get("search", [])
            if results:
                return results[0]["concepturi"]
        except Exception as e:
            print(f"[WARN] Wikidata API search failed for '{query}': {e}")

        return None

    def link_entities(self, ner_json):
        for cell in ner_json:
            if "entities" in cell:
                for entity in cell["entities"]:
                    text = entity["text"]
                    kb_uri = self.search_wikidata(text)
                    entity["kb_id"] = kb_uri
        return ner_json