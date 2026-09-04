<<<Gemini にて生成>>>

フォルダ構成（Project Structure）を構成要素のトップに組み込んだ、完全版の `README.md` です。このままリポジトリ直下に配置して使用できます。

---

# README.md

```markdown
# mjrengo-js

`mjrengo-js` は、異体字・独自グリフタグ（`{...}`）の正規化（Normalize）および軽量描画（Render）を行うJavaScriptライブラリです。  
サーバー（Python等）での事前正規化と、クライアント（JavaScript）でのDBレス軽量描画を想定した設計になっています。

---

## フォルダ構成 (Project Structure)

本ライブラリは、単一責任の原則に基づきモジュールが分離されています。クライアント側での描画利用時は `glyphRenderer.js` のみを読み込むことで、DBレスな超軽量動作を実現します。

```text
mjrengo-js/
├── src/
│   ├── glyphUtils.js        # 共通ユーティリティ (エスケープ退避・復元・タグパース・パイプライン)
│   ├── glyphNormalizer.js   # 正規化エンジン (GLYPH_TABLE参照・属性補完・エラー全件収集)
│   └── glyphRenderer.js     # 描画エンジン (コードポイント変換・アンエスケープ処理)
├── tests/
│   ├── glyphNormalizer.test.js # 正規化機能の単体テスト
│   └── glyphRenderer.test.js   # 描画機能の単体テスト
├── .gitignore               # Git管理除外ファイル設定
├── LICENSE                  # ライセンス情報 (MIT License)
├── README.md                # ドキュメント (本書)
└── package.json             # パッケージ定義・エクスポート設定

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

## インストール

```bash
npm install mjrengo-js

```

または GitHub から直接インストール:

```bash
npm install github:your-username/mjrengo-js

```

---

## 使い方

### 1. クライアント側での描画 (`GlyphRenderer`)

データベースを参照せず、正規化済み文字列のコードポイント（`v` 優先、次点で `b`）から直接描画を行います。

```javascript
import { GlyphRenderer } from "mjrengo-js";

// サーバーから受け取った正規化済み文字列
const inputText = "エスケープ: \\{GJ000001\\} / タグ: {GJ000001 b=U+30F1 v=U+100000}";

// 描画実行 (アンエスケープ & Unicode変換)
const outputText = GlyphRenderer.render(inputText);

console.log(outputText);
// 出力: "エスケープ: {GJ000001} / タグ: 𐀀"

```

### 2. サーバー/Node.js側での正規化・検証 (`GlyphNormalizer`)

`GLYPH_TABLE` を参照し、属性の自動補完とエラー（未定義、非アクティブ）の全件収集を行います。

```javascript
import { GlyphNormalizer } from "mjrengo-js/normalize";

const GLYPH_TABLE = {
  'GJ000001': { 'b': 'U+30F1', 'v': 'U+100000', 'active': true },
  'GJ000002': { 'b': 'U+5B89', 'v': 'U+1B002', 'active': false } // 非アクティブ
};

const normalizer = new GlyphNormalizer(GLYPH_TABLE);

// 正規化の実行
const response = normalizer.normalize("タグ: {GJ000001} と {GJ000002} と {GJ999999}");

if (!response.success) {
  console.error("エラーが発生しました:", response.errors);
  /*
  response.errors の出力例:
  [
    { glyph_name: "GJ000002", reason: "INACTIVE", message: "Glyph 'GJ000002' is marked as inactive." },
    { glyph_name: "GJ999999", reason: "NOT_FOUND", message: "Glyph 'GJ999999' is not defined in GLYPH_TABLE." }
  ]
  */
} else {
  console.log("正規化結果:", response.result);
}

```

---

## API リファレンス

### `GlyphRenderer.render(text: string): string`

* 正規化済みテキストを受け取り、エスケープの解除（アンエスケープ）とタグの文字描画を行って文字列を返します。

### `GlyphNormalizer.normalize(text: string, [glyphTable]): Object`

* テキスト内のタグを補完・検証します。
* **返却オブジェクト構造**:
* `success` (`boolean`): エラーが1つもなければ `true`
* `result` (`string | null`): 成功時は正規化済み文字列、失敗時は `null`
* `errors` (`Array<Object>`): 検出されたエラーのリスト (`glyph_name`, `reason`, `message`)


## 開発・テスト実行

本リポジトリをクローンしてローカルでテストを実行する手順です。単体テストには **Jest** を使用しています。

### 1. 依存関係のインストール

開発に必要な環境（Jest 等）をインストールします。

```bash
npm install

```

### 2. テストの実行

```bash
npm test

```



## ライセンス

[MIT License](https://www.google.com/search?q=LICENSE)

```

<ElicitationsGroup message="プロジェクト作成をさらに進める場合、以下のファイル生成が可能です:">
  <Elicitation label="mjrengo-js 用の .gitignore と MIT LICENSE ファイルを生成する" query="mjrengo-js 用の .gitignore と MIT LICENSE ファイルのテキストを作成してください。"/>
  <Elicitation label="package.json の最終確定コードを出力する" query="mjrengo-js のフォルダ構成に対応した完全な package.json を作成してください。"/>
</ElicitationsGroup>

```
