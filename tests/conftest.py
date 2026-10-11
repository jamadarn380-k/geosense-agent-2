"""
GeoSense Agent 2.0 - Phase 3
Pytest configuration to add src/phase3_lidar to sys.path.
"""

import os
import sys

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "src", "phase3_lidar")
    ),
)