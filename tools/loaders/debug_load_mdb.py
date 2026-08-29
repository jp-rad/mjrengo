from pathlib import Path
from tools.core.model import GlyphRecord
from tools.loaders.load_dwpi_mdb import load_dwpi_mdb

def main():
    BASE = Path(__file__).resolve().parent.parent

    print("")

    xlsx_path = BASE / "data/deluxe文字選択DWPI明朝4.10版V2.0.mdb"
    print("Absolute path:", xlsx_path)
    records = load_dwpi_mdb(xlsx_path)
    print("Total records:", len(records))
    _print_first5_last5(records)

    xlsx_path = BASE / "data/deluxe文字選択DWPIex明朝1.2版.mdb"
    print("Absolute path:", xlsx_path)
    records = load_dwpi_mdb(xlsx_path)
    print("Total records:", len(records))
    _print_first5_last5(records)

def _print_first5_last5(items: list[GlyphRecord]):

    print("---- first 5 records ----")
    for i, rec in enumerate(items[:5]):
        print(f"[{i}] {rec.name}")
        print("  ucs    :", rec.v)
        print("  rep    :", rec.b)
        print("  active :", rec.active)
        print("  comment:", rec.comment)
        print()

    print("---- last 5 records ----")
    last_items = items[-5:]
    start_index = len(items) - 5
    for offset, rec in enumerate(last_items):
        i = start_index + offset
        print(f"[{i}] {rec.name}")
        print("  ucs    :", rec.v)
        print("  rep    :", rec.b)
        print("  active :", rec.active)
        print("  comment:", rec.comment)
        print()

if __name__ == "__main__":
    main()
