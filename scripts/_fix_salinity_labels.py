import json
import re
from pathlib import Path

ordered = [
    ("#3182bd", "Low"),
    ("#74c476", "Moderately low"),
    ("#ffed6f", "Moderate"),
    ("#fd8d3c", "Moderately high"),
    ("#a50f15", "High"),
]
asset = Path(r"C:\Users\Kunal.Desale\Desktop\mithiriver\public\asset")
for name in ["mithi-salinity.json", "mula-mutha-ndsi-salinity.json"]:
    p = asset / name
    d = json.loads(p.read_text(encoding="utf-8"))
    by_color = {c["color"].lower(): c for c in d["classes"]}
    new = []
    for i, (col, lab) in enumerate(ordered, 1):
        c = by_color.get(col)
        if not c:
            continue
        c = dict(c)
        c["id"] = i
        c["class"] = i
        c["label"] = lab
        c["color"] = col
        new.append(c)
    d["classes"] = new
    p.write_text(json.dumps(d, indent=2), encoding="utf-8")
    print(name, [(c["label"], c["share_pct"]) for c in new])

leg = Path(r"C:\Users\Kunal.Desale\Desktop\mithiriver\src\lib\layerLegends.js")
text = leg.read_text(encoding="utf-8")
new = """  'ndsi-salinity': {
    provenance: 'Estimated',
    colors: [
      { color: '#3182bd', label: 'Low', value: '0.1%' },
      { color: '#74c476', label: 'Moderately low', value: '63.5%' },
      { color: '#ffed6f', label: 'Moderate', value: '24.0%' },
      { color: '#fd8d3c', label: 'Moderately high', value: '10.7%' },
      { color: '#a50f15', label: 'High', value: '1.7%' },
    ],
  },"""
text2, n = re.subn(r"  'ndsi-salinity': \{[\s\S]*?\n  \},", new, text, count=1)
print("legend", n)
leg.write_text(text2, encoding="utf-8")
