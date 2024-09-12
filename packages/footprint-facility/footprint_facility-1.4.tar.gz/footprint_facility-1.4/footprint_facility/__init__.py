"""
   Copyright 2024 - Gael Systems

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from .footprint_facility import (rework_to_polygon_geometry,
                                 rework_to_linestring_geometry,
                                 check_cross_antimeridian,
                                 simplify, find_best_tolerance_for,
                                 check_time, show_summary, set_raise_exception,
                                 to_wkt, to_geojson, AlreadyReworkedPolygon)
from ._version import get_versions

__version__ = get_versions()['version']
del get_versions

__all__ = ['rework_to_polygon_geometry', 'rework_to_linestring_geometry',
           'check_cross_antimeridian', 'simplify', 'find_best_tolerance_for',
           'check_time', 'show_summary', 'set_raise_exception',
           'to_geojson', 'to_wkt', 'AlreadyReworkedPolygon']
