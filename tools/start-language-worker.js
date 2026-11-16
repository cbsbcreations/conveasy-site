// Conveasy start language: Cloudflare Worker "conveasy-start-language" (account of cbsbcreations, zone conveasy.ai).
// Routes: conveasy.ai/ and conveasy.ai/geo (failure mode: fail open, so the site keeps working if the Worker cannot run).
//
// conveasy.ai/     Visitors in Belgium go to conveasy.be: French in Wallonia and Brussels, Dutch in Flanders.
//                  Visitors in Switzerland get German, French or Italian by canton (in the bilingual cantons Fribourg,
//                  Valais, Bern and Graubünden the browser's language decides between them).
//                  Everyone else goes on to the site. Before this Worker runs, the Cloudflare redirect rules of conveasy.ai
//                  already send visitors in DE/AT, NL, FR/LU, ES, PT and IT to their language.
// conveasy.ai/geo  Answers the root page of conveasy.be (which is not behind Cloudflare): {"lang": "fr"} or {"lang": "nl"}.
//
// Cloudflare gives Workers the visitor's region on every plan (request.cf.regionCode / region). Redirect rules only get it
// on the Business plan, which is why this is a Worker. Source of truth: this file in the conveasy-site repo; paste it into
// the Worker's editor in the Cloudflare dashboard after a change.

const BE_FR_CODES = ["WAL", "BRU", "WBR", "WHT", "WLG", "WLX", "WNA"];  // Wallonia, Brussels and the Walloon provinces
const BE_FR_NAMES = /wallo|brussel|bruxelles|hainaut|henegouwen|li[eè]ge|luik|namur|namen|luxemb/;
const CH_FR_CODES = ["GE", "VD", "NE", "JU", "FR", "VS"];
const CH_FR_NAMES = /gen[eè]v|genf|vaud|waadt|neuch|jura|fribourg|freiburg|valais|wallis/;
const CH_IT_NAMES = /ticino|tessin/;
const CH_BILINGUAL = ["FR", "VS", "BE", "GR"];

function regionCode(cf) { return String(cf.regionCode || "").toUpperCase().replace(/^[A-Z]{2}-/, ""); }
function regionName(cf) { return String(cf.region || "").toLowerCase(); }
function browserLang(request) { return String(request.headers.get("Accept-Language") || "").trim().slice(0, 2).toLowerCase(); }

export function chLang(cf, br) {
  const c = regionCode(cf), n = regionName(cf);
  if (CH_BILINGUAL.includes(c) && ["de", "fr", "it"].includes(br)) return br;
  if (CH_FR_CODES.includes(c) || CH_FR_NAMES.test(n)) return "fr";
  if (c === "TI" || CH_IT_NAMES.test(n)) return "it";
  if (c || n) return "de";
  return ["fr", "it"].includes(br) ? br : "de";
}

// The start language of conveasy.be: Dutch or French.
export function beLang(cf, br) {
  if (cf.country === "BE") {
    const c = regionCode(cf), n = regionName(cf);
    if (BE_FR_CODES.includes(c) || BE_FR_NAMES.test(n)) return "fr";
    if (c || n) return "nl";
  } else if (["FR", "LU", "MC"].includes(cf.country) || (cf.country === "CH" && chLang(cf, br) === "fr")) {
    return "fr";
  }
  return br === "fr" ? "fr" : "nl";   // region unknown: the browser's language
}

function go(to) {
  return new Response(null, { status: 302, headers: { location: to, "cache-control": "no-store" } });
}

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const cf = request.cf || {};
    const br = browserLang(request);
    if (url.pathname === "/geo") {
      const origin = request.headers.get("Origin") || "";
      const headers = { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", "vary": "Origin" };
      if (/^https:\/\/(www\.)?conveasy\.be$/.test(origin)) headers["access-control-allow-origin"] = origin;
      return new Response(JSON.stringify({ lang: beLang(cf, br) }), { headers });
    }
    if (url.pathname === "/") {
      if (cf.country === "BE") return go("https://conveasy.be/" + beLang(cf, br) + "/" + url.search);
      if (cf.country === "CH") return go("https://conveasy.ai/" + chLang(cf, br) + "/" + url.search);
    }
    return fetch(request);
  },
};
