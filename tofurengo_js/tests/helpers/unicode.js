export function toCodePoints(str) {
  return Array.from(str)
    .map(ch => ch.codePointAt(0).toString(16).toUpperCase())
    .join(" ");
}
