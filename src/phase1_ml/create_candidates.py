from pathlib import Path

import geopandas as gpd
import numpy as np
from shapely.geometry import Point


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PUNE_BOUNDARY_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "boundaries"
    / "pune_pmc_15_zones"
    / "Pune.shp"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "candidate_locations.shp"
)

UTM_CRS = "EPSG:32643"
GRID_SPACING_METRES = 500


def create_candidate_grid():
    """Create candidate points at 500-metre spacing inside Pune's 15 zones."""

    if not PUNE_BOUNDARY_FILE.exists():
        raise FileNotFoundError(
            f"Pune boundary file was not found:\n{PUNE_BOUNDARY_FILE}"
        )

    pune_zones = gpd.read_file(PUNE_BOUNDARY_FILE)

    if pune_zones.crs is None:
        raise ValueError(
            "Pune.shp has no CRS information. Check whether Pune.prj is present."
        )

    print(f"Pune zone polygons found: {len(pune_zones)}")

    pune_zones_utm = pune_zones.to_crs(UTM_CRS)

    study_area = pune_zones_utm.geometry.unary_union

    min_x, min_y, max_x, max_y = study_area.bounds

    x_coordinates = np.arange(min_x, max_x, GRID_SPACING_METRES)
    y_coordinates = np.arange(min_y, max_y, GRID_SPACING_METRES)

    points = [
        Point(x, y)
        for x in x_coordinates
        for y in y_coordinates
    ]

    grid = gpd.GeoDataFrame(
        {"geometry": points},
        crs=UTM_CRS
    )

    candidates = grid[grid.geometry.within(study_area)].copy()

    candidates["location_id"] = range(1, len(candidates) + 1)

    candidates_wgs84 = candidates.to_crs(epsg=4326)

    candidates_wgs84["longitude"] = candidates_wgs84.geometry.x
    candidates_wgs84["latitude"] = candidates_wgs84.geometry.y

    return candidates_wgs84


def main():
    """Generate and save candidate EV charging-station locations."""

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    candidates = create_candidate_grid()

    candidates.to_file(OUTPUT_FILE)

    print(f"\nCreated {len(candidates)} candidate locations.")
    print(f"Saved candidate grid to:\n{OUTPUT_FILE}")


if __name__ == "__main__":
    main()