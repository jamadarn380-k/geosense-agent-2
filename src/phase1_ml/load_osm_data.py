from pathlib import Path

import geopandas as gpd

from db_connection import get_engine


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OSM_DATA_DIR = PROJECT_ROOT / "data" / "shapefiles" / "osm"

PUNE_BOUNDARY_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "boundaries"
    / "pune_pmc_15_zones"
    / "Pune.shp"
)

LAYERS_TO_LOAD = [
    ("gis_osm_roads_free_1.shp", "osm_roads"),
    ("gis_osm_buildings_a_free_1.shp", "osm_buildings"),
    ("gis_osm_landuse_a_free_1.shp", "osm_landuse"),
    ("gis_osm_pois_free_1.shp", "osm_poi"),
    ("gis_osm_pois_a_free_1.shp", "osm_poi_areas"),
    ("gis_osm_water_a_free_1.shp", "osm_water"),
    ("gis_osm_waterways_free_1.shp", "osm_waterways"),
    ("gis_osm_traffic_free_1.shp", "osm_traffic"),
    ("gis_osm_traffic_a_free_1.shp", "osm_traffic_areas"),
    ("gis_osm_transport_free_1.shp", "osm_transport"),
    ("gis_osm_protected_areas_a_free_1.shp", "osm_protected_areas"),
]


def get_pune_study_area():
    """Read Pune zone polygons and create one combined study-area geometry."""

    if not PUNE_BOUNDARY_FILE.exists():
        raise FileNotFoundError(
            f"Pune boundary file was not found:\n{PUNE_BOUNDARY_FILE}"
        )

    pune_zones = gpd.read_file(PUNE_BOUNDARY_FILE)

    if pune_zones.crs is None:
        raise ValueError(
            "Pune.shp has no CRS information. Check whether Pune.prj is present."
        )

    pune_zones = pune_zones.to_crs(epsg=4326)

    study_area = pune_zones.dissolve()

    print(f"Pune zone polygons found: {len(pune_zones)}")

    return pune_zones, study_area


def load_boundary_to_postgis(pune_zones, engine):
    """Load Pune zone boundary polygons into PostGIS."""

    print("\nLoading Pune zone boundary into PostGIS...")

    pune_zones.to_postgis(
        name="pune_zones",
        con=engine,
        if_exists="replace",
        index=False
    )

    print("Successfully loaded Pune boundary table: pune_zones")


def load_osm_layer(filename, table_name, study_area, engine):
    """Read an OSM layer, keep Pune-only features, and load data into PostGIS."""

    filepath = OSM_DATA_DIR / filename

    if not filepath.exists():
        print(f"\nSkipped because file was not found: {filename}")
        return

    print(f"\nProcessing layer: {filename}")

    study_bounds = study_area.total_bounds

    try:
        layer = gpd.read_file(filepath, bbox=study_bounds)
    except Exception:
        print("Bounding-box read was unavailable. Reading complete layer...")
        layer = gpd.read_file(filepath)

    if layer.empty:
        print(f"No features found near Pune for: {filename}")
        return

    if layer.crs is None:
        print(f"Skipped because CRS information is missing: {filename}")
        return

    layer = layer.to_crs(epsg=4326)

    print(f"Features near Pune before clipping: {len(layer)}")

    pune_layer = gpd.clip(layer, study_area)

    print(f"Features inside Pune study area: {len(pune_layer)}")

    if pune_layer.empty:
        print(f"No features remained after clipping: {filename}")
        return

    pune_layer.to_postgis(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False
    )

    print(f"Successfully loaded PostGIS table: {table_name}")


def main():
    """Load Pune zones and selected OSM layers into PostGIS."""

    engine = get_engine()

    pune_zones, study_area = get_pune_study_area()

    load_boundary_to_postgis(pune_zones, engine)

    for filename, table_name in LAYERS_TO_LOAD:
        load_osm_layer(filename, table_name, study_area, engine)

    print("\nAll available Pune OSM layers were loaded into PostGIS successfully.")


if __name__ == "__main__":
    main()