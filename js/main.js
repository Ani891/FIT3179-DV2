// js/main.js
// Draws every chart on the page. index.html holds an empty <div id="vis-...">
// for each chart; this file finds it by id and draws the Vega-Lite spec from specs/.
// Loaded last in index.html, so the <div>s already exist when it runs.

// 1. Shared look for every chart (fonts and colours).
const CONFIG = {
  font: "Bitter",
  axis: { labelFont: "Bitter", titleFont: "Oswald", labelColor: "#3b2a1d",
          titleColor: "#3b2a1d", grid: false, domain: false, ticks: false },
  view: { stroke: null }
};

// 2. Chart list: id of the <div> in index.html -> its spec file.
const CHARTS = {
  "vis-regional":   "specs/regional_waffle.json",
  "vis-commercial": "specs/commercial_stacked.json",
  "vis-age":        "specs/age_lollipop.json",
  "vis-party":      "specs/party_butterfly.json",
  "vis-length":     "specs/length_waffle.json",
  "vis-reason":     "specs/reason_dumbbell.json",
  "vis-regions":    "specs/regions_lollipop.json",
  "vis-heatmap":    "specs/state_heatmap.json",
  "vis-choropleth": "specs/map_choropleth.json",
  "vis-symbols":    "specs/map_symbols.json",
  "vis-bivariate":  "specs/map_bivariate.json"
};

if (typeof vegaEmbed === "undefined") {
  document.querySelectorAll(".chart").forEach(el => el.innerHTML = '<p class="missing">The chart libraries did not load. Check your internet connection.</p>');
}

// 3. Load each spec, add the shared settings, draw it.
function draw(id, file) {
  const el = document.getElementById(id);
  if (!el) return;
  fetch(file)
    .then(r => { if (!r.ok) throw new Error(file + " not found (HTTP " + r.status + ")"); return r.json(); })
    .then(spec => vegaEmbed(el, { width: "container", background: null, config: CONFIG, ...spec }, { actions: false }))
    .catch(err => {
      console.error(file, err);
      const hint = location.protocol === "file:"
        ? "Open this page through a web server (for example python3 -m http.server), not by double-clicking the file."
        : "Check the browser console (F12) for details. A map also needs data/states.json.";
      el.innerHTML = '<p class="missing">Chart could not load: ' + file + '<br>' + (err && err.message ? err.message + '<br>' : '') + hint + '</p>';
    });
}
Object.entries(CHARTS).forEach(([id, file]) => draw(id, file));
