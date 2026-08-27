from pathlib import Path

p = Path(r"C:\Users\Kunal.Desale\Desktop\mithiriver\src\components\Dashboard.jsx")
text = p.read_text(encoding="utf-8")
start = text.index("    geology: [")
end = text.index("  }), [", start)
new = """    geology: [
      {
        id: 'lithology',
        label: 'Spectral lithology',
        hint: 'Provisional surface-material classes',
        checked: showLithologyLayer,
        onToggle: setShowLithologyLayer,
      },
      {
        id: 'erosion',
        label: 'Bank erosion hotspots',
        hint: '2016–2026 classified overlay',
        checked: showErosionLayer,
        onToggle: setShowErosionLayer,
      },
      {
        id: 'tributaries',
        label: 'Joining streams',
        hint: 'OSM drainage on the Mithi reach',
        checked: showTributaryLayer,
        onToggle: setShowTributaryLayer,
      },
      {
        id: 'mainstem',
        label: 'Main stem',
        hint: 'Mithi River OSM ways',
        checked: showMainStemLayer,
        onToggle: setShowMainStemLayer,
      },
    ],
    salinity: [
      {
        id: 'ndsi-salinity',
        label: 'Relative salinity',
        hint: 'Water-pixel salinity classes',
        checked: showNdsiSalinityLayer,
        onToggle: setShowNdsiSalinityLayer,
      },
    ],
    pollution: [
      {
        id: 'garbage',
        label: 'Garbage locations',
        hint: '213 detected solid-waste sites',
        checked: showGarbageLayer,
        onToggle: setShowGarbageLayer,
      },
    ],
    waterquality: [],
    landuse: [
      {
        id: 'silt-class',
        label: 'Silt classification',
        hint: 'Monthly classed raster · Jan–Jul 2026',
        checked: showSiltClassLayer,
        onToggle: setShowSiltClassLayer,
      },
    ],
    biodiversity: [],
    climate: [
      {
        id: 'flood-heat',
        label: 'Flood heatmap',
        hint: 'Classed flood points by image pair',
        checked: showClimateFloodHeat,
        onToggle: setShowClimateFloodHeat,
      },
      {
        id: 'water-heat',
        label: 'Surface-water heatmap',
        hint: 'Classed water points by image pair',
        checked: showClimateWaterHeat,
        onToggle: setShowClimateWaterHeat,
      },
    ],
    flood: [],
"""
text = text[:start] + new + text[end:]
text = text.replace(
    "uploadedKML?.displayName === 'Mula-Mutha River'",
    "uploadedKML?.displayName === 'Mula-Mutha River-DISABLED'",
)
text = text.replace("...(isMulaMuthaRiver ? [chainageLayer] : []),", "")
p.write_text(text, encoding="utf-8")
print("ok")
