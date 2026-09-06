<<GEMINIにて生成>>

`mjrengo`（Python版）用の完全な `README.md` です。リポジトリ直下（または `mjrengo` パッケージのルート）にそのまま配置して使用できます。

---

# README.md

```markdown
# mjrengo (Python)

`mjrengo` は、異体字・独自グリフタグ（`{...}`）の正規化（Normalize）および描画（Render）を行うPythonライブラリです。  
データベース（`GLYPH_TABLE`）を参照した属性自動補完・アクティブ判定・エラー全件収集機能と、エスケープ文字（`\\`, `\{`, `\}`）の安全なパース機構を提供します。

---

## パッケージ構成 (Project Structure)

```text
mjrengo/
├── mjrengo/
│   ├── __init__.py          # パッケージ公開API定義
│   ├── glyph_utils.py       # 共通ユーティリティ (エスケープ退避・復元・タグパース・パイプライン)
│   ├── glyph_normalizer.py  # 正規化エンジン (GLYPH_TABLE参照・属性補完・エラー全件収集)
│   └── glyph_renderer.py    # 描画エンジン (コードポイント変換・アンエスケープ処理)
├── tests/
│   └── test_mjrengo.py      # pytest 用単体テスト
├── LICENSE                  # ライセンス情報 (MIT License)
├── README.md                # ドキュメント (本書)
└── pyproject.toml           # パッケージ定義ファイル

```

---

## タグ・エスケープ仕様

### 1. グリフタグの構造

* **標準タグ形式**: `{タグ名 [属性1=値1 属性2=値2 ...]}`
* **補完前（入力）例**: `{GJ000001}`
* **正規化後（補完済み）例**: `{GJ000001 b=U+30F1 v=U+100000}`

### 2. エスケープ仕様

* **対象文字**: `\\`, `\{`, `\}` の3種類
* **動作メカニズム**: パース前に制御文字（SOH: `\u0001`, STX: `\u0002`, ETX: `\u0003`）へ一時退避させることで、正規表現の誤判定を防ぎます。

| エスケープ表記 | 退避文字 (SOH/STX/ETX) | 正規化時 (`normalize`) | 描画時 (`render`) |
| --- | --- | --- | --- |
| `\\` | `\u0001` (SOH) | `\\` (保持) | `\` (アンエスケープ) |
| `\{` | `\u0002` (STX) | `\{` (保持) | `{` (アンエスケープ) |
| `\}` | `\u0003` (ETX) | `\}` (保持) | `}` (アンエスケープ) |

---

## 使い方

### 1. タグの正規化と検証 (`GlyphNormalizer`)

`GLYPH_TABLE` を参照し、属性の自動補完とエラー（未定義、非アクティブ）の全件収集を行います。

```python
from mjrengo import GlyphNormalizer

# 異体字テーブルの準備
GLYPH_TABLE = {
    'GJ000001': {'b': 'U+30F1', 'v': 'U+100000', 'active': True},
    'GJ000002': {'b': None, 'v': 'U+100001', 'active': True},
    'GJ000003': {'b': 'U+5B89', 'v': 'U+1B002', 'active': False}  # 非アクティブ
}

normalizer = GlyphNormalizer(GLYPH_TABLE)

# --- 正常系 ---
text = r"エスケープ: \{GJ000001\} / タグ: {GJ000001} と {GJ000002}"
res = normalizer.normalize(text)

if res["success"]:
    print(res["result"])
    # 出力: エスケープ: \{GJ000001\} / タグ: {GJ000001 b=U+30F1 v=U+100000} と {GJ000002 v=U+100001}

# --- 異常系 (エラー全件収集) ---
err_text = "非アクティブ {GJ000003} と 未定義 {GJ999999}"
err_res = normalizer.normalize(err_text)

if not err_res["success"]:
    print(err_res["errors"])
    # 出力例:
    # [
    #   {'glyph_name': 'GJ000003', 'reason': 'INACTIVE', 'message': "Glyph 'GJ000003' is marked as inactive."},
    #   {'glyph_name': 'GJ999999', 'reason': 'NOT_FOUND', 'message': "Glyph 'GJ999999' is not defined in GLYPH_TABLE."}
    # ]

```

### 2. タグの描画 (`GlyphRenderer`)

正規化済み文字列のコードポイント（`v` 優先、次点で `b`）から Unicode 文字への置換とアンエスケープを行います。

```python
from mjrengo import GlyphRenderer

normalized_text = r"エスケープ: \{GJ000001\} / タグ: {GJ000001 b=U+30F1 v=U+100000}"

# 描画の実行 (Unicode化 & アンエスケープ)
rendered_text = GlyphRenderer.render(normalized_text)

print(rendered_text)
# 出力: エスケープ: {GJ000001} / タグ: 𐀀

```

---

## API リファレンス

### `GlyphNormalizer(glyph_table: Optional[dict] = None)`

* **`normalize(text: str, glyph_table: Optional[dict] = None) -> dict`**
* テキスト内のタグを補完・検証します。
* **戻り値 (dict)**:
* `success` (`bool`): エラーが1つもなければ `True`
* `result` (`str | None`): 成功時は正規化済み文字列、失敗時は `None`
* `errors` (`list[dict]`): エラー情報のリスト (`glyph_name`, `reason`, `message`)





### `GlyphRenderer`

* **`render(text: str) -> str`**
* 正規化済みテキストを受け取り、エスケープの解除（アンエスケープ）とタグの Unicode 文字変換を行って文字列を返します。



---

## 開発・テスト実行

本リポジトリでの単体テスト実行手順です。単体テストには **pytest** を使用します。

### 1. 依存関係のインストール

```bash
pip install pytest

```

### 2. テストの実行

```bash
pytest

```

---

## ライセンス

[MIT License](https://www.google.com/search?q=LICENSE)

```

<ElicitationsGroup message="Python配布環境の作成を進める場合、以下のファイル生成が可能です:">
  <Elicitation label="PyPI・pip インストール用の pyproject.toml を作成する" query="mjrengo 用の pyproject.toml を作成してください。"/>
  <Elicitation label="pytest 用のテストファイル（tests/test_mjrengo.py）を作成する" query="mjrengo 用の pytest テストコードを作成してください。"/>
</ElicitationsGroup>

```