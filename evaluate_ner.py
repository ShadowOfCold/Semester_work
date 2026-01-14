import json
import os
from collections import defaultdict
import argparse

SKIP_ROWS = [0]

def text_overlap(a, b):
    a = a.lower()
    b = b.lower()
    return a in b or b in a

def evaluate_table(pred_cells, gold_cells):
    pred_dict = {(c["row"], c["col"]): c for c in pred_cells}
    gold_dict = {(c["row"], c["col"]): c for c in gold_cells}

    tp = fp = fn = 0

    for key, g_cell in gold_dict.items():
        if key[0] in SKIP_ROWS:
            continue

        p_cell = pred_dict.get(key)
        if not p_cell:
            fn += len(g_cell.get("true_entities", []))
            continue

        gold_entities = g_cell.get("true_entities", [])
        pred_entities = p_cell.get("entities", [])

        matched_gold = set()
        matched_pred = set()

        for gi, g in enumerate(gold_entities):
            for pi, p in enumerate(pred_entities):
                if pi in matched_pred:
                    continue
                if g["label"] == p["label"] and text_overlap(g["text"], p["text"]):
                    tp += 1
                    matched_gold.add(gi)
                    matched_pred.add(pi)
                    break

        fn += len(gold_entities) - len(matched_gold)
        fp += len(pred_entities) - len(matched_pred)

    return tp, fp, fn

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pred", required=True, help="JSON файл предсказаний (все таблицы)")
    parser.add_argument("--gold_dir", required=True, help="Папка с gold test_sample файлами")
    parser.add_argument("--output", required=True, help="Выходной JSON файл с результатами")
    args = parser.parse_args()

    with open(args.pred, "r", encoding="utf-8") as f:
        all_pred = json.load(f)

    pred_tables = defaultdict(list)
    for cell in all_pred:
        tid = cell.get("table_id")
        if tid is not None:
            pred_tables[tid].append(cell)

    table_ids = sorted(pred_tables.keys())

    results = {}
    total_tp = total_fp = total_fn = 0

    for t in table_ids:
        gold_file = os.path.join(args.gold_dir, f"test_sample_{t}.json")
        if not os.path.exists(gold_file):
            print(f"[WARN] Gold file missing: {gold_file}")
            continue

        with open(gold_file, "r", encoding="utf-8") as f:
            gold_cells = json.load(f)

        pred_cells = pred_tables[t]

        tp, fp, fn = evaluate_table(pred_cells, gold_cells)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        results[t] = {
            "TP": tp,
            "FP": fp,
            "FN": fn,
            "Precision": round(precision, 3),
            "Recall": round(recall, 3),
            "F1": round(f1, 3)
        }

        total_tp += tp
        total_fp += fp
        total_fn += fn

    overall_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
    overall_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
    overall_f1 = 2 * overall_precision * overall_recall / (overall_precision + overall_recall) if (overall_precision + overall_recall) > 0 else 0

    print("\n=== Partial Match Evaluation ===")
    print("Таблица | TP  | FP  | FN  | Precision | Recall | F1")
    print("-----------------------------------------------------")
    for t, metrics in results.items():
        print(f"{t:>7} | {metrics['TP']:>3} | {metrics['FP']:>3} | {metrics['FN']:>3} | {metrics['Precision']:.2f}     | {metrics['Recall']:.2f}   | {metrics['F1']:.2f}")
    print("\nОбщие показатели:")
    print(f"Precision: {overall_precision:.3f}, Recall: {overall_recall:.3f}, F1: {overall_f1:.3f}")

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nРезультаты сохранены в {args.output}")


if __name__ == "__main__":
    main()