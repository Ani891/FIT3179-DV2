# Why Australia Still Hits the Road
FIT3179 Data Visualisation 2. Built with Vega-Lite.

```
index.html     page text and layout (commented section by section)
css/style.css  all styling
scripts/       prepare_tra_data.py reads the TRA Excel workbook and writes data/reason_compare.csv and data/state_all_domestic.csv
js/main.js     draws each chart from its spec
specs/*.json   one Vega-Lite spec per chart or map
data/*.csv     the numbers behind each chart; source_id points to Sources in index.html
```

To view locally, run `python3 -m http.server` in this folder and open http://localhost:8000.
The page needs an internet connection for fonts and the Vega libraries.

Map files:
- `data/state_stats.csv` is included (2024 state figures from the State of Industry 2025 report).
- `data/states.json` you must add: state boundaries as a plain GeoJSON file whose features have a `name` property
  (for example "New South Wales"). Natural Earth's Admin 1 file has this. The two boundary maps read it as `properties.name`.
- The tile-grid map works without `states.json`.
