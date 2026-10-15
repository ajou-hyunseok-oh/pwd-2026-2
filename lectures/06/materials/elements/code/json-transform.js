// Parse (문자열 → 값)
const obj = JSON.parse(jsonString);

// Stringify (값 → 문자열)
const s = JSON.stringify(obj, null, 2);

// Replacer로 필드 필터/정렬
const s2 = JSON.stringify(obj, ["id", "title"], 2);
