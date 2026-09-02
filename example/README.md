# Convert Console

Convert Console は、MJ テキスト変換 API を手軽に試すための Web UI です。  
1 行のテキストを入力し、グリフセットを選択すると、Base 文字・Variant 文字・JSON レスポンスを確認できます。

---

## 特長

- 1 行テキスト入力  
- グリフセット選択（`mj-plus`, `mj-plusx`, `mj`, `mj-onka`）  
- Base レンダリング結果の表示  
- Variant レンダリング結果の表示（フォント自動切替）  
- JSON レスポンスの整形表示  
- Swagger UI へのリンク付き

---

## 必要環境

- Python 3.10+
- FastAPI
- Uvicorn
- `/static` 配下で CSS / JS / フォントを提供できる構成

---

## サーバー起動

FastAPI サーバーを起動します。

```bash
cd code/example
python main.py
```

UI は以下でアクセスできます。

```
https://localhost/console
```

API ドキュメント（Swagger UI）は以下です。

```
https://localhost/docs
```


## UI の使い方

### 1. グリフセットを選択
Variant 表示に使用するグリフセットを選びます。  
選択に応じて UI のフォントが自動で切り替わります。

### 2. テキスト入力
1 行のテキストを入力します。  
API には以下の形式で送信されます。

```
GET /convert/{glyph_set}/{text}
```

### 3. Convert ボタンを押す
API を呼び出し、結果が UI に反映されます。

### 4. 出力フィールド
- **Base Rendered Text**  
  Base グリフのレンダリング結果。

- **Variant Rendered Text**  
  Variant グリフのレンダリング結果（フォント自動切替）。

- **Result JSON**  
  API レスポンス全体を整形して表示。


## UI が利用する API

UI は以下のエンドポイントを呼び出します。

```
GET /convert/{glyph_set}/{text}
```

例：

```
/convert/mj-plus/あ
```

レスポンス形式：

```json
{
  "text": {
    "rendered": {
      "base": "...",
      "variant": "..."
    }
  }
}
```


## ディレクトリ構成

```
static/
  css/
    style.css
    fonts.css
  js/
    frontend.js
index.html
main.py
```


## 補足

- `/console` は API スキーマから除外されており、`/docs` には表示されません。
- Variant と JSON のフォントはグリフセットに応じて自動で切り替わります。
- UI の入力欄はすべて 1 行で統一されています（JSON は除く）。


## License

MIT
