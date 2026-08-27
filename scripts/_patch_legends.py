from pathlib import Path

# Update layerLegends.js key sections for Mithi
p = Path(r"C:\Users\Kunal.Desale\Desktop\mithiriver\src\lib\layerLegends.js")
text = p.read_text(encoding="utf-8")

replacements = {
    """  erosion: {
    provenance: 'Estimated',
    colors: [
      { color: '#90ee90', label: 'No erosion', value: '83.1%' },
      { color: '#ffff00', label: 'Low erosion', value: '15.5%' },
      { color: '#ffa500', label: 'Moderate erosion', value: '1.4%' },
      { color: '#ff0000', label: 'High erosion', value: '0%' },
      { color: '#800000', label: 'Very high erosion', value: '0%' },
    ],
  },""": """  erosion: {
    provenance: 'Estimated',
    colors: [
      { color: '#ffffff', label: 'No / very low erosion', value: '88.4%' },
      { color: '#ffff00', label: 'Low erosion', value: '10.6%' },
      { color: '#ffa500', label: 'Moderate erosion', value: '0.9%' },
      { color: '#ff0000', label: 'High erosion', value: '0%' },
      { color: '#800000', label: 'Very high erosion', value: '0%' },
    ],
  },""",
    """  tributaries: {
    provenance: 'Estimated',
    colors: [
      { color: '#12b5a8', label: 'Named streams', value: '7' },
      { color: '#5ad2f4', label: 'Joining feeders', value: '31' },
      { color: '#f4a261', label: 'Drains / nullahs', value: '4' },
      { color: '#3d8bfd', label: 'Canals', value: '7' },
      { color: '#8d99ae', label: 'Ditches', value: '7' },
    ],
  },
  mainstem: {
    provenance: 'Estimated',
    colors: [{ color: '#1d4e89', label: 'Main stem (Mula / Mutha)', value: '4' }],
  },""": """  tributaries: {
    provenance: 'Estimated',
    colors: [
      { color: '#12b5a8', label: 'Named streams', value: '6' },
      { color: '#5ad2f4', label: 'Joining feeders', value: '10' },
      { color: '#f4a261', label: 'Drains / nullahs', value: '34' },
      { color: '#3d8bfd', label: 'Canals', value: '0' },
      { color: '#8d99ae', label: 'Ditches', value: '0' },
    ],
  },
  mainstem: {
    provenance: 'Estimated',
    colors: [{ color: '#1d4e89', label: 'Main stem (Mithi)', value: '6' }],
  },""",
    """  'ndsi-salinity': {
    provenance: 'Estimated',
    colors: [
      { color: '#0000FF', label: 'Very low', value: '-1.00 to -0.60' },
      { color: '#00BFFF', label: 'Low', value: '-0.60 to -0.20' },
      { color: '#00FF00', label: 'Moderate', value: '-0.20 to 0.20' },
      { color: '#FFFF00', label: 'High', value: '0.20 to 0.60' },
      { color: '#FF0000', label: 'Very high', value: '0.60 to 1.00' },
    ],
  },""": """  'ndsi-salinity': {
    provenance: 'Estimated',
    colors: [
      { color: '#3182bd', label: 'Low', value: '0.1%' },
      { color: '#74c476', label: 'Moderately low', value: '63.5%' },
      { color: '#ffed6f', label: 'Moderate', value: '24.0%' },
      { color: '#fd8d3c', label: 'High', value: '10.7%' },
      { color: '#a50f15', label: 'Moderately high', value: '1.7%' },
    ],
  },""",
    """  garbage: {
    provenance: 'Estimated',
    colors: [{ color: '#c45c26', label: 'Detected garbage site', value: '67' }],
  },""": """  garbage: {
    provenance: 'Estimated',
    colors: [{ color: '#c45c26', label: 'Detected garbage site', value: '213' }],
  },""",
}

for old, new in replacements.items():
    if old not in text:
        print("MISSING block")
        print(old[:80])
    else:
        text = text.replace(old, new)
        print("replaced ok")

# Replace lithology block by finding markers
import re
lith_new = """  lithology: {
    provenance: 'Estimated',
    colors: [
      { color: '#f4a460', label: 'Silty / Sandy Channel Sediment', value: '11.3%' },
      { color: '#655940', label: 'Estuarine / Clayey-Silt Sediment', value: '55.5%' },
      { color: '#ff69b4', label: 'Exposed / Bright Mineral Surface', value: '9.1%' },
      { color: '#808080', label: 'Silica-rich', value: '7.2%' },
      { color: '#ff0101', label: 'Ferruginous / iron-rich', value: '4.7%' },
      { color: '#8b0101', label: 'Basaltic / mafic', value: '5.3%' },
      { color: '#9370db', label: 'Clay-rich', value: '4.0%' },
      { color: '#ffd701', label: 'Alluvial / sedimentary', value: '2.3%' },
      { color: '#01a6a6', label: 'Weathered / mixed mineral', value: '0.3%' },
    ],
  },"""
text2, n = re.subn(r"  lithology: \{[\s\S]*?\n  \},", lith_new, text, count=1)
print("lithology", n)
p.write_text(text2, encoding="utf-8")
