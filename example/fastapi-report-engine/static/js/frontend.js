// フォント切り替え（variant_text のみ）
export function updateVariantFont() {
    const glyphSet = document.getElementById("glyph_set").value;

    const variantInput = document.getElementById("variant_text");
    const jsonArea = document.getElementById("json_result");

    let font = "inherit";

    if (glyphSet === "mj-plus") {
        font = "DWPIMincho";
    } else if (glyphSet === "mj-plusx") {
        font = "DWPIexMincho";
    } else if (glyphSet === "mj" || glyphSet === "mj-onka") {
        font = "IPAmjMincho";
    }

    // variant と json_result のフォントを連動
    variantInput.style.fontFamily = font;
    jsonArea.style.fontFamily = font;
}


// GET /convert/{glyph_set}/{text} を呼び出す
export async function doConvert() {
    const glyphSet = document.getElementById("glyph_set").value;
    const text = document.getElementById("text").value;

    // 改行がない前提なので GET パスで安全
    const encodedText = encodeURIComponent(text);
    const url = `/convert/${glyphSet}/${encodedText}`;

    try {
        const res = await fetch(url);
        const data = await res.json();

        // JSON 全体を表示
        document.getElementById("json_result").value =
            JSON.stringify(data, null, 2);

        // Base / Variant を 1 行 input にセット
        document.getElementById("base_text").value =
            data.text?.rendered?.base || "";

        document.getElementById("variant_text").value =
            data.text?.rendered?.variant || "";

        // フォント更新
        updateVariantFont();

    } catch (err) {
        alert("Error calling /convert: " + err);
    }
}

// 初期化（ページロード時にフォント設定）
export function initConsole() {
    updateVariantFont();
}
