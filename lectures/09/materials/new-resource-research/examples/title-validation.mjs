// Teaching candidate for 4.8, 5.5, 7.5 and 7.10; not a model execution trace.
// Input contract: string. Examples use ASCII and precomposed Korean syllables.
// String.length counts UTF-16 code units, not visible Unicode graphemes.
export function isValidTitle(input) {
  const title = input.trim();
  return title.length >= 1 && title.length <= 20;
}

// Deliberate bug for the repair example: ignores outer whitespace.
export function isValidTitleBeforeRepair(input) {
  return input.length >= 1 && input.length <= 20;
}
