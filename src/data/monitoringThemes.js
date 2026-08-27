/** Shared monitoring themes — landing page and signed-in hub.
 *
 *  Mithi River Eye: only themes with shipped datasets are deep-linked.
 */

export const MONITORING_THEMES = [
  {
    name: 'Hydrology',
    desc: 'River outline, rainfall and air-quality context on the live map',
    to: '/dashboard?view=flood',
    datasets: [],
  },
  {
    name: 'Geology',
    desc: 'Spectral lithology, bank erosion hotspots, and joining drainage',
    to: '/dashboard?view=geology',
    datasets: ['lithology', 'erosion', 'tributaries'],
  },
  {
    name: 'Biodiversity',
    desc: 'Vegetation type and health — awaiting Mithi biodiversity overlays',
    to: '/dashboard',
    datasets: [],
  },
  {
    name: 'Soil & land use',
    desc: 'Monthly river silt classification · Jan–Jul 2026',
    to: '/dashboard?view=landuse',
    datasets: ['silt'],
  },
  {
    name: 'Salinity intrusion',
    desc: 'Relative salinity classes along the tidal Mithi reach',
    to: '/dashboard?view=salinity',
    datasets: ['ndsi-salinity'],
  },
  {
    name: 'Water quality',
    desc: 'TSS / NDCI / BOD–COD overlays — awaiting Mithi water-quality pack',
    to: '/dashboard',
    datasets: [],
  },
  {
    name: 'Pollution',
    desc: 'Detected garbage / solid-waste dumping sites along the reach',
    to: '/dashboard?view=pollution',
    datasets: ['garbage'],
  },
  {
    name: 'Climate impact',
    desc: 'Flood and surface-water heatmap from 2026 image pairs',
    to: '/dashboard?view=climate',
    datasets: ['floodwater'],
  },
  {
    name: 'Socio-economic',
    desc: 'Night-lights, fishing activity, tourism footprint, sand mining',
    to: '/dashboard',
    datasets: [],
  },
]
