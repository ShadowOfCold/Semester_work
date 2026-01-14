from typing import List, Dict
import spacy
import os

class SpacyNER:
    def __init__(self, model_name: str = "ru_core_news_lg"):
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            print(f"[INFO] Модель {model_name} не найдена. Скачиваем...")
            os.system(f"python -m spacy download {model_name}")
            self.nlp = spacy.load(model_name)

    def extract_entities(self, text: str) -> List[Dict]:
        """
        Извлекает сущности из текста одной ячейки.
        """
        doc = self.nlp(text)
        entities = []
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "source": "spacy"
            })
        return entities