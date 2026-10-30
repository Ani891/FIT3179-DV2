"""
Reads the Tourism Research Australia (TRA) Domestic Tourism Statistics workbook and writes the CSV
files the charts load. Run from the project folder:

    python3 scripts/prepare_tra_data.py path/to/tra-dots-june-quarter-2026-compared-to-june-quarter-2025.xlsx

Inputs  : TRA workbook, Table 3c (reason of visit, year ending Dec 2025) and Table 1c (state visited, year ending Jun 2026).
Outputs : data/reason_compare.csv, data/state_all_domestic.csv, and the 'Share of all domestic nights' rows in data/state_shares.csv.
"""
import csv, sys
import openpyxl

path = sys.argv[1]
wb = openpyxl.load_workbook(path, data_only=True)

def block(ws, title_start, n_rows, col):
    """Return {label: value} for the n_rows rows under the row whose first cell starts with title_start."""
    rows = list(ws.iter_rows(values_only=True))
    for i, r in enumerate(rows):
        if r[0] and str(r[0]).startswith(title_start):
            return {str(rows[i + k][0]).strip(): rows[i + k][col] for k in range(1, n_rows + 1)}
    raise ValueError(title_start + " not found")

# ---- Table 3c: all domestic overnight trips by reason of visit, year ending December 2025 (column B = index 1)
reasons = block(wb["Table 3c"], "Overnight trips", 5, 1)
total = [v for k, v in reasons.items() if k.startswith("Total")][0]
all_pct = {k: round(100 * reasons[k] / total, 1) for k in ["Holiday", "Visiting friends and relatives", "Business"]}

# Caravan and camping shares, year ending December 2025: TRA "Caravan and camping data" page (S1).
caravan_pct = {"Holiday": 77, "Visiting friends and relatives": 13, "Business": 5}

with open("data/reason_compare.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["reason", "caravan_pct", "all_pct", "source_id"])
    for k in caravan_pct:
        w.writerow([k, caravan_pct[k], all_pct[k], "S1; S5 (calculated)"])

# ---- Table 1c: all domestic visitor nights by state visited, year ending June 2026 (column C = index 2)
nights = block(wb["Table 1c"], "Visitor nights", 8, 2)
states = ["New South Wales", "Queensland", "Victoria", "Western Australia", "South Australia", "Tasmania", "Northern Territory"]
seven = sum(nights[s] for s in states)   # ACT left out so the denominator matches the caravan charts
with open("data/state_all_domestic.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["state", "nights_thousands", "share_of_seven_states_pct", "source_id"])
    for s in states:
        w.writerow([s, round(nights[s], 1), round(100 * nights[s] / seven, 1), "S5 (calculated)"])

# ---- add the benchmark to the heatmap data
rows = [r for r in csv.reader(open("data/state_shares.csv", encoding="utf-8"))]
head, body = rows[0], [r for r in rows[1:] if r[1] != "Share of all domestic nights"]
for s in states:
    body.append([s, "Share of all domestic nights", round(100 * nights[s] / seven, 1), "S5 (calculated)"])
with open("data/state_shares.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows([head] + body)
print("done:", all_pct, {s: round(100 * nights[s] / seven, 1) for s in states})
