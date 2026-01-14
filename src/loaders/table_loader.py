import csv
import os
from typing import List, Dict


class RF200TableLoader:
    def __init__(self, tables_dir: str, verbose: bool = True):
        self.tables_dir = tables_dir
        self.verbose = verbose

    def _find_table_file(self, table_id: int) -> str | None:
        for filename in os.listdir(self.tables_dir):
            if filename.startswith(f"{table_id}_") and filename.endswith(".csv"):
                return os.path.join(self.tables_dir, filename)
        return None

    def load_table(self, table_id: int) -> List[Dict]:
        path = self._find_table_file(table_id)

        if path is None:
            if self.verbose:
                print(f"[WARN] Таблица {table_id} отсутствует — пропуск")
            return []

        cells = []

        with open(path, encoding="utf-8") as f:
            reader = csv.reader(f)
            for row_idx, row in enumerate(reader):
                for raw_col_idx, cell in enumerate(row):
                    parts = [p.strip() for p in cell.split("|")]

                    for logical_col_idx, text in enumerate(parts):
                        if text:
                            cells.append({
                                "table_id": table_id,
                                "row": row_idx,
                                "col": logical_col_idx,
                                "text": text
                            })

        return cells

    def load_tables(self, table_ids: List[int]) -> List[Dict]:
        all_cells = []
        for table_id in table_ids:
            all_cells.extend(self.load_table(table_id))
        return all_cells