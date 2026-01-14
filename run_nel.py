import argparse
import json
from src.nel.entity_linker import EntityLinker

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Путь к JSON после NER")
    parser.add_argument("--output", required=True, help="Путь для сохранения JSON с NEL")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        ner_result = json.load(f)

    linker = EntityLinker()
    linked_result = linker.link_entities(ner_result)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(linked_result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
