"""Rebuild Mithi lithology class table from the official KMZ legend colours."""
import json
import math
import re
from collections import Counter
from pathlib import Path

from PIL import Image

ASSET = Path(r"C:\Users\Kunal.Desale\Desktop\mithiriver\public\asset")

# Official order from mula-mutha-spectral-lithology-legend.png
OFFICIAL = [
    {"id": 0, "key": "655940", "label": "Silty / Sandy Channel Sediment", "color": "#655940"},
    {"id": 1, "key": "8B0000", "label": "Basaltic / Fresh Basalt Spectral Zone", "color": "#8b0000"},
    {"id": 2, "key": "FFD700", "label": "Weathered Basalt", "color": "#ffd700"},
    {"id": 3, "key": "FF0000", "label": "Lateritic / Ferruginous Zone", "color": "#ff0000"},
    {"id": 4, "key": "9370DB", "label": "Clay-Rich / Altered Zone", "color": "#9370db"},
    {"id": 5, "key": "F4A460", "label": "Alluvial / Sandy-Clayey Sediment", "color": "#f4a460"},
    {"id": 6, "key": "00A6A6", "label": "Estuarine / Clayey-Silt Sediment", "color": "#00a6a6"},
    {"id": 7, "key": "808080", "label": "Mixed Weathered Geological Material", "color": "#808080"},
    {"id": 8, "key": "FF69B4", "label": "Exposed / Bright Mineral Surface", "color": "#ff69b4"},
]


def box_area_ha(box):
    lat_m = (box["north"] - box["south"]) * 111320
    mid = (box["north"] + box["south"]) / 2
    lon_m = (box["east"] - box["west"]) * 111320 * math.cos(math.radians(mid))
    return (lat_m * lon_m) / 10000


targets = []
for d in OFFICIAL:
    key = d["key"]
    targets.append((d["id"], int(key[0:2], 16), int(key[2:4], 16), int(key[4:6], 16)))

png = ASSET / "mula-mutha-spectral-lithology.png"
im = Image.open(png).convert("RGBA")
w, h = im.size
buckets = Counter()
total = 0
max_d2 = 55 * 55
for r, g, b, a in im.getdata():
    if a < 200:
        continue
    total += 1
    best_id, best_d2 = None, max_d2 + 1
    for cid, tr, tg, tb in targets:
        d2 = (r - tr) ** 2 + (g - tg) ** 2 + (b - tb) ** 2
        if d2 < best_d2:
            best_d2 = d2
            best_id = cid
    if best_id is not None and best_d2 <= max_d2:
        buckets[best_id] += 1

meta_path = ASSET / "mula-mutha-spectral-lithology.json"
meta = json.loads(meta_path.read_text(encoding="utf-8"))
area = box_area_ha(meta["bounds"])
classes = []
for d in OFFICIAL:
    px = buckets.get(d["id"], 0)
    share = round(100.0 * px / total, 1) if total else 0.0
    classes.append(
        {
            **d,
            "class": d["id"],
            "pixels": px,
            "share_pct": share,
            "area_ha": round(area * (share / 100.0), 1),
        }
    )
    print(d["id"], d["label"], share, "%", px)

meta["classes"] = classes
meta["total_pixels"] = total
meta["classified_pixels"] = sum(buckets.values())
meta["total_area_ha"] = round(area, 1)
meta["width"] = w
meta["height"] = h
meta["note"] = (
    "Provisional spectral lithology from Mithi_River_Lithology_Interpretation_Map.tif. "
    "Class labels and colours match the KMZ legend (field validation required)."
)
meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

# Update layerLegends.js
leg = Path(r"C:\Users\Kunal.Desale\Desktop\mithiriver\src\lib\layerLegends.js")
text = leg.read_text(encoding="utf-8")
rows = ",\n".join(
    f"      {{ color: '{c['color']}', label: '{c['label']}', value: '{c['share_pct']}%' }}"
    for c in classes
)
lith_new = f"""  lithology: {{
    provenance: 'Estimated',
    colors: [
{rows},
    ],
  }},"""
text2, n = re.subn(r"  lithology: \{[\s\S]*?\n  \},", lith_new, text, count=1)
print("legend replace", n)
leg.write_text(text2, encoding="utf-8")
