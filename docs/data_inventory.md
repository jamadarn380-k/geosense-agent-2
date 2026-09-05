\# GeoSense Data Inventory



\## Project Details



\- Project Title: GIS-Based Site Suitability Analysis for Public EV Charging Stations

\- Final Study Area: Pune Municipal Corporation – 41 Wards

\- State: Maharashtra, India

\- Practical Exercise: Exercise 3 – Multi-Source Geospatial Data Acquisition and Organisation

\- Data Acquisition Date: 31-08-2026



\## Data Management Rule



\- Original downloaded data will be stored without modification.

\- Original OSM ZIP data is stored in `data/raw/osm\_download\_zip/`.

\- Extracted OSM shapefiles are stored in `data/shapefiles/osm/`.

\- Original SRTM DEM tiles are stored in `data/raw/elevation/`.

\- All future clipped, merged, buffered, and scored layers will be stored in `data/processed/`.

\- Original data will never be directly edited, clipped, merged, overwritten, or deleted.



\## Dataset Inventory



| Dataset | Main Contents | Purpose in EV Charging Site Suitability Analysis | Source | Download Date | File Format | Destination Folder | QGIS Verification |

|---|---|---|---|---|---|---|---|

| Pune PMC 41 Ward Boundary | Boundary polygons for Pune Municipal Corporation’s 41 wards | Defines the final study area for EV charging-station suitability analysis | Public GIS / PMC ward-boundary source | 31-08-2026 | Shapefile (.shp) | `data/raw/boundaries/pune\_pmc\_41\_wards/` | Loaded and visually verified in QGIS |

| OpenStreetMap Full Extract | Roads, buildings, POIs, traffic, traffic signals, land use, water bodies, waterways, railways, places, natural features, transport, power features, and other OSM layers | Provides road accessibility, demand locations, building density, parking context, water-body buffers, land-use suitability, traffic proxy indicators, and power-infrastructure context | Geofabrik OpenStreetMap | 31-08-2026 | ZIP archive and Shapefile (.shp) | ZIP: `data/raw/osm\_download\_zip/`; extracted layers: `data/shapefiles/osm/` | Loaded and visually verified in QGIS |

| OSM Roads | Roads, streets, highways, and road hierarchy | Used to identify accessible locations and proximity to major roads | Geofabrik OpenStreetMap | 31-08-2026 | Shapefile (.shp) | `data/shapefiles/osm/` | Verified in QGIS |

| OSM Buildings | Building footprints | Used as a built-up density and potential EV-demand proxy | Geofabrik OpenStreetMap | 31-08-2026 | Shapefile (.shp) | `data/shapefiles/osm/` | Verified in QGIS |

| OSM POIs | Markets, malls, hospitals, colleges, offices, parking, petrol pumps, restaurants, hotels, temples, and other facilities | Identifies locations where people and vehicles may stop, park, or require charging | Geofabrik OpenStreetMap | 31-08-2026 | Shapefile (.shp) | `data/shapefiles/osm/` | Verified in QGIS |

| OSM Traffic and Traffic Signals | Traffic-related points and road-control features | Used as a proxy for high-activity junctions and traffic corridors | Geofabrik OpenStreetMap | 31-08-2026 | Shapefile (.shp) | `data/shapefiles/osm/` | Verified in QGIS |

| OSM Land Use | Residential, commercial, industrial, agricultural, green, and other land-use categories | Identifies suitable commercial, mixed-use, public, and built-up locations; helps exclude unsuitable land | Geofabrik OpenStreetMap | 31-08-2026 | Shapefile (.shp) | `data/shapefiles/osm/` | Verified in QGIS |

| OSM Water Bodies | Lakes, ponds, reservoirs, rivers, and other water polygons | Used to exclude water-covered areas and create safety buffers | Geofabrik OpenStreetMap | 31-08-2026 | Shapefile (.shp) | `data/shapefiles/osm/` | Verified in QGIS |

| OSM Waterways | Rivers, streams, drains, and waterways | Used to create river, nala, and drainage buffers and support flood-risk assessment | Geofabrik OpenStreetMap | 31-08-2026 | Shapefile (.shp) | `data/shapefiles/osm/` | Verified in QGIS |

| OSM Power Features | Power lines, substations, and related mapped electrical features where available | Gives an initial indication of electrical-infrastructure proximity | Geofabrik OpenStreetMap | 31-08-2026 | Shapefile (.shp) | `data/shapefiles/osm/` | To be checked in QGIS |

| SRTM DEM Tile 1 | Elevation raster tile | Used for elevation, slope, drainage, and terrain-based flood-risk analysis | NASA Earthdata SRTM | 31-08-2026 | HGT / GeoTIFF | `data/raw/elevation/` | Loaded and visually verified in QGIS |

| SRTM DEM Tile 2 | Elevation raster tile | Used with Tile 1 to cover the complete Pune PMC study region | NASA Earthdata SRTM | 31-08-2026 | HGT / GeoTIFF | `data/raw/elevation/` | Loaded and visually verified in QGIS |

| Google Earth Engine Account | Cloud platform access for Sentinel-2 and Landsat imagery | Will be used during Phase 2 to verify land cover, water, vegetation, open spaces, parking, and final candidate sites | Google Earth Engine | Account already available | Cloud platform account | Cloud-based | Account available |

| Population Data | Population density and demographic data | Intended for EV-demand scoring; OSM buildings, residential land use, and POIs will be initial proxy indicators until suitable population data is obtained | Census India / PMC / data.gov.in | Not acquired | CSV / Excel / GIS data | To be added later | Pending |

| Flood Risk Data | Flood-hazard, flood-inundation, or flood-prone location data | Used to exclude high flood-risk areas from EV charging-station candidate locations | NDMA / ISRO Bhuvan / official source | To be acquired | GIS layer / reference data | `data/raw/flood\_risk/` | Pending |



\## QGIS Validation



\- The Pune PMC 41 ward boundary layer was loaded and visually checked in QGIS.

\- OpenStreetMap roads, buildings, POIs, traffic-related features, land use, water bodies, and waterways were loaded and visually checked in QGIS.

\- Both SRTM DEM tiles were loaded successfully in QGIS.

\- DEM elevation variation was visualised using a suitable colour ramp.

\- Screenshots were captured as evidence of successful spatial-data validation.



\## QGIS Project and Screenshots



\- QGIS project file: `qgis/exercise\_3\_data\_validation.qgz`

\- OSM validation screenshot folder: `outputs/screenshots/`

\- DEM validation screenshot folder: `outputs/screenshots/`



\## Final Study-Area Decision



The final study area for this project is the combined spatial extent of the 41 Pune Municipal Corporation wards. All suitability processing, clipping, buffer generation, scoring, and final candidate-site generation will be limited to this study area.



\## Future Processing Plan



1\. Validate the 41 Pune ward polygons and create a combined outer study-area boundary.

2\. Create processed copies of required OSM layers and clip them to the Pune PMC 41-ward boundary.

3\. Merge the two SRTM DEM tiles and clip the merged DEM to the final study area.

4\. Acquire and add existing EV charging-station locations.

5\. Acquire and add flood-risk or flood-inundation data.

6\. Add available population/demand, parking, and power-infrastructure data.

7\. Generate buffers, criterion scores, a weighted suitability map, and final EV charging-station candidate locations.



\## Actual Downloaded File Names



\- Pune PMC 41 Ward Boundary File: `Pune.shp`

\- Original OSM ZIP File: `Write your OSM ZIP file name here`

\- OSM Roads File: `Write your roads shapefile name here`

\- OSM Buildings File: `Write your buildings shapefile name here`

\- OSM POI File: `Write your POI shapefile name here`

\- OSM Land Use File: `Write your land-use shapefile name here`

\- OSM Water Bodies File: `Write your water-body shapefile name here`

\- OSM Waterways File: `Write your waterways shapefile name here`

\- SRTM DEM Tile 1: `Write your first DEM file name here`

\- SRTM DEM Tile 2: `Write your second DEM file name here`

