import argparse
import os
import json

from src.loaders.table_loader import RF200TableLoader
from src.ner.ner_spacy import SpacyNER
from src.ner.ner_gigachat import GigaChatNER

def run_ner(args):
    table_range = args.tables
    if "-" in table_range:
        start, end = map(int, table_range.split("-"))
        table_ids = range(start, end + 1)
    else:
        table_ids = [int(table_range)]

    loader = RF200TableLoader("./data/rf-200/csv/all-tables")
    cells = loader.load_tables(table_ids)

    if args.method == "spacy":
        ner_model = SpacyNER()
    elif args.method == "gigachat_zero":
        from src.ner.ner_gigachat import GigaChatNER
        ner_model = GigaChatNER(mode="zero")
    elif args.method == "gigachat_few":
        from src.ner.ner_gigachat import GigaChatNER
        ner_model = GigaChatNER(mode="few")

    results = []
    for cell in cells:
        entities = ner_model.extract_entities(cell["text"])
        results.append({**cell, "entities": entities})

    os.makedirs("results/ner", exist_ok=True)
    output_file = f"results/ner/ner_{args.method}_{table_ids[0]}_{table_ids[-1]}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"[INFO] NER ({args.method}) завершён, результаты сохранены в {output_file}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=["ner", "evaluate"], required=True)
    parser.add_argument("--method", choices=["spacy", "gigachat_zero", "gigachat_few"])
    parser.add_argument("--tables", required=True)
    args = parser.parse_args()

    if args.task == "ner":
        run_ner(args)
    elif args.task == "evaluate":
        print("[INFO] Оценка пока не реализована")

if __name__ == "__main__":
    main()