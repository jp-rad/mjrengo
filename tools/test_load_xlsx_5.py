from pathlib import Path
from tools.loaders.loader_xlsx import load_mji_00602_xlsx, load_mji_00602_xlsx_as_zip

import zipfile
import xml.etree.ElementTree as ET

def main():
    BASE = Path(__file__).resolve().parent
    # xlsx_path = BASE / "data/test.xlsx"
    xlsx_path = BASE / "data/mji.00602.xlsx"

    print("Absolute path:", xlsx_path)


    with zipfile.ZipFile(xlsx_path, "r") as z:
        for name in z.namelist():
            print(name)
        xml = z.read("xl/worksheets/sheet1.xml")
        root = ET.fromstring(xml)
        print(root.tag)


    # records = load_mji_00602_xlsx(xlsx_path)
    records = load_mji_00602_xlsx_as_zip(xlsx_path)

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
