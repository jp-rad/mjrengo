from pathlib import Path
from tools.loaders.loader_xlsx import load_mji00602_xlsx

def main():
    BASE = Path(__file__).resolve().parent
    xlsx_path = BASE / "data/test.xlsx"

    print("Absolute path:", xlsx_path)

    records = load_mji00602_xlsx(xlsx_path)

    print("Total records:", len(records))

    # dict → list に変換（順序は挿入順）
    items = list(records.items())

    print("---- first 5 records ----")
    for i, (key, rec) in enumerate(items[:5]):
        print(f"[{i}] {key}")
        print("  ucs    :", rec.ucs)
        print("  rep    :", rec.rep)
        print("  active :", rec.active)
        print("  comment:", rec.comment)
        print()

    print("---- last 5 records ----")
    last_items = items[-5:]
    # 末尾側のインデックスを分かりやすくする
    start_index = len(items) - 5
    for offset, (key, rec) in enumerate(last_items):
        i = start_index + offset
        print(f"[{i}] {key}")
        print("  ucs    :", rec.ucs)
        print("  rep    :", rec.rep)
        print("  active :", rec.active)
        print("  comment:", rec.comment)
        print()

if __name__ == "__main__":
    main()
