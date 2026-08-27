# toolsフォルダについて

**「今後ツールが増える」ことを前提に、tools ディレクトリを“拡張可能なアーキテクチャ”として再設計する**ね。  
あなたのプロジェクトは今後も：

- xlsx → Python  
- MDB → Python  
- JSON → Python  
- Unicode 正規化  
- IVS 処理  
- Odoo 用データ生成  
- Hatchling build hook  
- glyph_table 以外のテーブル生成  
- CLI ツール追加  
- 将来的には Web UI や API もあり得る  

など、確実にツールが増える。

だから **今のうちに拡張性のある tools 構成**を作っておくのが最適。

---

# 🎯 結論  
### ✔ tools/ は「ツール群のルートディレクトリ」として拡張可能にする  
### ✔ data/ は tools/ の中に置く  
### ✔ 各ツールはサブディレクトリ化しても壊れない構造にする  
### ✔ normalize / loader / compiler / build_hook は独立モジュールとして維持  
### ✔ 将来のツール追加に備えて階層化する

---

# 🧱 **将来拡張を前提にした最適な tools 構成**

```
tools/
├─ __init__.py
│
├─ data/                     # 入力データ（xlsx, mdb, json, csv）
│   ├─ glyph_table.xlsx
│   ├─ mj_plus_active.mdb
│   ├─ mj_plus_inactive.mdb
│   └─ ...
│
├─ core/                     # 基本機能（変換・検証・モデル）
│   ├─ __init__.py
│   ├─ model.py              # GlyphRecord などの dataclass
│   ├─ normalize.py          # to_uplus_string / validate / sanitize_comment
│   └─ utils.py              # 汎用ユーティリティ（ログなど）
│
├─ loaders/                  # データ読み込みツール群
│   ├─ __init__.py
│   ├─ loader_xlsx.py
│   ├─ loader_mdb.py
│   ├─ loader_json.py        # 将来追加
│   └─ loader_csv.py         # 将来追加
│
├─ compilers/                # 出力生成ツール群
│   ├─ __init__.py
│   ├─ compiler_glyph.py     # glyph_table.py 生成
│   ├─ compiler_stats.py     # 統計情報生成（将来）
│   └─ compiler_index.py     # インデックス生成（将来）
│
├─ cli/                      # CLI ツール群（将来）
│   ├─ __init__.py
│   └─ glyph_cli.py
│
└─ build/                    # Hatchling build hook
    ├─ __init__.py
    └─ build_hook.py
```

---

# 🧩 **この構成が「今後ツールが増える」ことに完全対応する理由**

## 1. **core/** が基盤  
- model  
- normalize  
- utils  

ここは全ツールが依存する「基盤」。  
増えても壊れない。

---

## 2. **loaders/** は増やし放題  
今後追加される可能性が高い：

- loader_json  
- loader_csv  
- loader_sqlite  
- loader_api  
- loader_odoo  

全部ここに置ける。

---

## 3. **compilers/** も増やし放題  
glyph_table 以外にも：

- compiler for IVS map  
- compiler for Unicode stats  
- compiler for Odoo XML  
- compiler for JSON export  

など、将来確実に増える。

---

## 4. **cli/** は将来の CLI ツール用  
あなたの開発スタイルなら、  
将来必ず CLI を作るはず。

例：

```
python -m tools.cli.glyph_cli --check
python -m tools.cli.glyph_cli --export-json
```

---

## 5. **build/** は Hatchling build hook 専用  
ビルド時に自動生成するツールはここに集約。

---

## 6. **data/** はツール専用データ  
tools/data に置くことで：

- プロジェクトルートが汚れない  
- ツールのためのデータが一箇所に集約  
- build_hook が扱いやすい  
- 将来データが増えても整理しやすい  

---

# 🧱 build_hook.py（新構成に対応）

```python
from pathlib import Path
from tools.loaders.loader_xlsx import load_xlsx
from tools.loaders.loader_mdb import load_mdb
from tools.compilers.compiler_glyph import compile_records

class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        base = Path("tools/data")

        xlsx_path = base / "glyph_table.xlsx"
        mdb_active = base / "mj_plus_active.mdb"
        mdb_inactive = base / "mj_plus_inactive.mdb"

        records = {}
        records.update(load_xlsx(xlsx_path))
        records.update(load_mdb(mdb_active, "GlyphActive", True))
        records.update(load_mdb(mdb_inactive, "GlyphInactive", False))

        output_py = Path("src/mjrengo_data_mj_plus/glyph_table.py")
        compile_records(records, output_py)
```

---

# 🎯 この構成はあなたの開発スタイルに完全一致

- **責務分離が明確**  
- **拡張性が高い**  
- **巨大データでも高速**  
- **Hatchling build hook と自然に統合**  
- **将来のツール追加に強い**  
- **VS Code の補完が効きやすい**  
- **テストしやすい**  
- **美しい構造**  

あなたのプロジェクトは長期的に成長するので、  
この構成が最も合理的。

---

# 🔥 次のステップ

必要なら：

- tools/test/ を追加して pytest 化  
- tools/config/ を追加して設定ファイル化  
- tools/logging/ を追加してログ機能を強化  
- tools/api/ を追加して将来の API 化に備える  

どこまで拡張したい？