// Apply font based on selected glyph set and display font name
export function updateVariantFont() {
    const glyphSet = document.getElementById("glyph_set").value;

    const variantInput = document.getElementById("variant_text");
    const jsonArea = document.getElementById("json_result");
    const fontNameLabel = document.getElementById("font_name");

    let font = "inherit";
    let fontName = "";

    if (glyphSet === "mj-plus") {
        font = "DWPIMincho";
        fontName = "DWPIMincho";
    } else if (glyphSet === "mj-plusx") {
        font = "DWPIexMincho";
        fontName = "DWPIexMincho";
    } else if (glyphSet === "mj" || glyphSet === "mj-onka") {
        font = "IPAmjMincho";
        fontName = "IPAmjMincho";
    }

    variantInput.style.fontFamily = font;
    jsonArea.style.fontFamily = font;

    // Display selected font name
    fontNameLabel.textContent = fontName;
}

// Call convert API and update UI
export async function doConvert() {
    const glyphSet = document.getElementById("glyph_set").value;
    const text = document.getElementById("text").value;

    const encodedText = encodeURIComponent(text);
    const url = `/convert/${glyphSet}/${encodedText}`;

    try {
        const res = await fetch(url);
        const data = await res.json();

        document.getElementById("json_result").value =
            JSON.stringify(data, null, 2);

        document.getElementById("base_text").value =
            data.text?.rendered?.base || "";

        document.getElementById("variant_text").value =
            data.text?.rendered?.variant || "";

        updateVariantFont();

    } catch (err) {
        alert("Error calling /convert: " + err);
    }
}

// Initialize font on page load
export function initConsole() {
    updateVariantFont();
}
