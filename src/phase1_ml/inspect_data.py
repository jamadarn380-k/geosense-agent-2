from pathlib import Path

import geopandas as gpd

from db_connection import get_engine


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PUNE_BOUNDARY_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "boundaries"
    / "pune_pmc_15_zones"
    / "Pune.shp"
)


def inspect_pune_boundary():
    """Show columns and sample records from Pune boundary data."""

    print("\n" + "=" * 60)
    print("PUNE BOUNDARY DATA")
    print("=" * 60)

    pune_zones = gpd.read_file(PUNE_BOUNDARY_FILE)

    print("\nBoundary columns:")
    print(pune_zones.columns.tolist())

    print("\nFirst five boundary records:")
    print(pune_zones.drop(columns="geometry").head().to_string(index=False))


def inspect_osm_poi():
    """Show columns and POI categories from the PostGIS osm_poi table."""

    print("\n" + "=" * 60)
    print("OSM POI DATA")
    print("=" * 60)

    engine = get_engine()

    poi = gpd.read_postgis(
        "SELECT * FROM osm_poi;",
        engine,
        geom_col="geometry"
    )

    print("\nOSM POI columns:")
    print(poi.columns.tolist())

    print("\nNumber of Pune POI features:")
    print(len(poi))

    print("\nFirst five POI records:")
    print(poi.drop(columns="geometry").head().to_string(index=False))

    if "fclass" in poi.columns:
        print("\nPOI categories available in fclass:")

        categories = sorted(
            poi["fclass"]
            .dropna()
            .astype(str)
            .unique()
        )

        print(categories)

    else:
        print("\nNo fclass column found in osm_poi.")


def inspect_osm_poi_areas():
    """Show categories available in the OSM POI area table."""

    print("\n" + "=" * 60)
    print("OSM POI AREA DATA")
    print("=" * 60)

    engine = get_engine()

    poi_areas = gpd.read_postgis(
        "SELECT * FROM osm_poi_areas;",
        engine,
        geom_col="geometry"
    )

    print("\nOSM POI area columns:")
    print(poi_areas.columns.tolist())

    print("\nNumber of Pune POI area features:")
    print(len(poi_areas))

    print("\nFirst five POI area records:")
    print(poi_areas.drop(columns="geometry").head().to_string(index=False))

    if "fclass" in poi_areas.columns:
        print("\nPOI area categories available in fclass:")

        categories = sorted(
            poi_areas["fclass"]
            .dropna()
            .astype(str)
            .unique()
        )

        print(categories)

    else:
        print("\nNo fclass column found in osm_poi_areas.")


def main():
    """Run all data-inspection functions."""

    inspect_pune_boundary()
    inspect_osm_poi()
    inspect_osm_poi_areas()


if __name__ == "__main__":
    main()