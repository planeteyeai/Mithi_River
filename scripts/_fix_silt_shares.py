import json
import math
from collections import Counter
from pathlib import Path

from PIL import Image

ASSET = Path(r"C:\Users\Kunal.Desale\Desktop\mithiriver\public\asset")
class_defs = [
    {"id": 1, "key": "00FF00", "label": "Low", "color": "#00ff00"},
    {"id": 2, "key": "FFFF00", "label": "Moderate", "color": "#ffff00"},
    {"id": 3, "key": "FFA500", "label": "High", "color": "#ffa500"},
    {"id": 4, "key": "FF0000", "label": "Very High", "color": "#ff0000"},
]
WATER = "1E90FF"


def box_area_ha(box):
    lat_m = (box["north"] - box["south"]) * 111320
    mid = (box["north"] + box["south"]) / 2
    lon_m = (box["east"] - box["west"]) * 111320 * math.cos(math.radians(mid))
    return (lat_m * lon_m) / 10000


def sample(path):
    im = Image.open(path).convert("RGBA")
    counts = Counter()
    water = 0
    for r, g, b, a in im.getdata():
        if a == 0:
            continue
        key = f"{r:02X}{g:02X}{b:02X}"
        if key == WATER:
            water += 1
            continue
        matched = False
        for d in class_defs:
            if key == d["key"]:
                counts[d["id"]] += 1
                matched = True
                break
        if not matched:
            best = None
            bestd = 1e9
            for d in class_defs:
                tr = int(d["key"][0:2], 16)
                tg = int(d["key"][2:4], 16)
                tb = int(d["key"][4:6], 16)
                d2 = (r - tr) ** 2 + (g - tg) ** 2 + (b - tb) ** 2
                if d2 < bestd:
                    bestd = d2
                    best = d["id"]
            if bestd <= 40 * 40:
                counts[best] += 1
    total = sum(counts.values())
    return counts, total, water


p = ASSET / "mula-mutha-silt.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["classes"] = [
    {"class": c["id"], "label": c["label"], "color": c["color"]} for c in class_defs
]
for per in d["periods"]:
    counts, total, water = sample(ASSET / f"mula-mutha-silt-class-{per['month']}.png")
    area = box_area_ha(per["bounds"])
    classes = []
    for c in class_defs:
        px = counts.get(c["id"], 0)
        share = round(100 * px / total, 1) if total else 0
        frac = px / (total + water) if (total + water) else 0
        classes.append(
            {
                **c,
                "class": c["id"],
                "pixels": px,
                "share_pct": share,
                "area_ha": round(area * frac, 1),
            }
        )
    per["classes"] = classes
    per["total_pixels"] = total
    per["water_mask_pixels"] = water
    per["classified_area_ha"] = round(sum(c["area_ha"] for c in classes), 1)
    per["classification"] = {
        "raster": f"/asset/mula-mutha-silt-class-{per['month']}.png"
    }
    print(
        per["month"],
        "classed",
        total,
        "water",
        water,
        [(c["label"], c["share_pct"]) for c in classes],
    )

p.write_text(json.dumps(d, indent=2), encoding="utf-8")
june = next(x for x in d["periods"] if x["id"] == 5)

# Update silt-class legend in layerLegends.js
leg = Path(r"C:\Users\Kunal.Desale\Desktop\mithiriver\src\lib\layerLegends.js")
text = leg.read_text(encoding="utf-8")
import re

silt_new = f"""  'silt-class': {{
    provenance: 'Estimated',
    colors: [
      {{ color: '#00ff00', label: 'Low', value: '{june['classes'][0]['share_pct']}%' }},
      {{ color: '#ffff00', label: 'Moderate', value: '{june['classes'][1]['share_pct']}%' }},
      {{ color: '#ffa500', label: 'High', value: '{june['classes'][2]['share_pct']}%' }},
      {{ color: '#ff0000', label: 'Very high', value: '{june['classes'][3]['share_pct']}%' }},
    ],
  }},"""
text2, n = re.subn(r"  'silt-class': \{[\s\S]*?\n  \},", silt_new, text, count=1)
print("silt legend", n)
leg.write_text(text2, encoding="utf-8")
