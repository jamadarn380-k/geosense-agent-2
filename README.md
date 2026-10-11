# GeoSense Agent 2.0

Phase 3: LiDAR processing, street-level semantic segmentation, and walkability scoring.

## Phase 3 — LiDAR & Street Semantic Analysis

- LiDAR bbox analysis: building height, canopy cover, impervious surface, slope risk
- Street semantic segmentation: SegFormer (road, sidewalk, building, vegetation, sky, car)
- Walkability scoring: sidewalk/vegetation/car weighted score
- Unified site profile: JSON combining LiDAR + street data
- 10 pytest tests passing

### Example profile

See `outputs/reports/enhanced_site_profile_32.77_-117.15.json`

### Point cloud screenshot

![Point cloud](outputs/point_clouds/study_area_colored.png)