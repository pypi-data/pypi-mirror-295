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
from unittest import TestCase, skip
import json
import shapely
from shapely import Polygon, Point, Geometry, wkt
from shapely.ops import transform as sh_transform
from pyproj import Transformer
import os
from os import walk

import footprint_facility
from footprint_facility import AlreadyReworkedPolygon, to_geojson


#############################################################################
# Private Utilities to manipulate input test Footprint file
# - load
# - retrieve longitude/Latitude list according to the input
# - build shapely geometry
#############################################################################
def _load_samples():
    path = os.path.join(os.path.dirname(__file__),
                        'samples', 'footprints_basic.json')
    with open(path) as f:
        return json.load(f)['footprint']


def _split(txt, seps):
    """
    Split with list of separators
    """
    default_sep = seps[0]
    # we skip seps[0] because that's the default separator
    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)
    return [i.strip() for i in txt.split(default_sep)]


def get_odd_values(fp):
    # [1::2] odd indexes
    return [float(x) for x in _split(fp['coords'], (' ', ','))[1::2]]


def get_even_values(fp):
    # [::2] even indexes
    return [float(x) for x in _split(fp['coords'], (' ', ','))[::2]]


def get_longitudes(fp):
    func = get_even_values
    if fp.get('coord_order') is not None:
        if fp['coord_order'].split()[1][:3:] == 'lon':
            func = get_odd_values
    return func(fp)


# Extract latitude coord list
def get_latitudes(fp):
    func = get_odd_values
    if fp.get('coord_order') is not None:
        if fp['coord_order'].split()[0][:3:] == 'lat':
            func = get_even_values
    return func(fp)


def fp_to_geometry(footprint) -> Geometry:
    lon = get_longitudes(footprint)
    lat = get_latitudes(footprint)
    return Polygon([Point(xy) for xy in zip(lon, lat)])


def disk_on_globe(lon, lat, radius, func=None):
    """Generate a shapely.Polygon object representing a disk on the
    surface of the Earth, containing all points within RADIUS meters
    of latitude/longitude LAT/LON."""

    # Use local azimuth projection to manage distances in meter
    # then convert to lat/lon degrees
    local_azimuthal_projection = \
        "+proj=aeqd +R=6371000 +units=m +lat_0={} +lon_0={}".format(lat, lon)
    lat_lon_projection = "+proj=longlat +datum=WGS84 +no_defs"

    wgs84_to_aeqd = Transformer.from_crs(lat_lon_projection,
                                         local_azimuthal_projection)
    aeqd_to_wgs84 = Transformer.from_crs(local_azimuthal_projection,
                                         lat_lon_projection)

    center = Point(float(lon), float(lat))
    point_transformed = sh_transform(wgs84_to_aeqd.transform, center)
    buffer = point_transformed.buffer(radius)
    disk = sh_transform(aeqd_to_wgs84.transform, buffer)
    if func is None:
        return disk
    else:
        return func(disk)


#############################################################################
# Test Class
#############################################################################
class Test(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.footprints = _load_samples()
        footprint_facility.check_time(enable=True,
                                      incremental=False,
                                      summary_time=True)

    @classmethod
    def tearDownClass(cls):
        footprint_facility.show_summary()

    def setUp(self):
        pass

    def test_check_contains_pole_north(self):
        geom = disk_on_globe(-160, 90, 500 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))

    def test_check_contains_pole_south(self):
        geom = disk_on_globe(-160, -90, 500 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))

    def test_check_no_pole_antimeridian(self):
        geom = disk_on_globe(-179, 0, 500 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))

    def test_check_no_pole_no_antimeridian(self):
        geom = disk_on_globe(0, 0, 500*1000)
        self.assertFalse(footprint_facility.check_cross_antimeridian(geom))

    def test_check_samples(self):
        """
        Pass through all the entries of the sample file that are marked as
        testable, then ensure they can be managed and reworked without failure.
        """
        for footprint in self.footprints:
            if footprint.get('testable', True):
                geom = fp_to_geometry(footprint)
                result = footprint_facility.check_cross_antimeridian(geom)
                self.assertEqual(result, footprint['antimeridian'],
                                 f"longitude singularity not properly "
                                 f"detected({footprint['name']}).")

    def test_rework_with_north_pole(self):
        """This footprint contains antimeridian and North Pole.
        """
        geom = disk_on_globe(-160, 90, 500 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.Polygon)
        self.assertAlmostEqual(int(rwkd.area), 1600, delta=100)

    def test_rework_with_south_pole(self):
        """This footprint contains antimeridian and South Pole.
        """
        geom = disk_on_globe(0, -90, 500 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.Polygon)
        self.assertAlmostEqual(int(rwkd.area), 1600, delta=100)

    def test_rework_close_to_north_pole(self):
        """This footprint contains antimeridian and no pole, very close to
          the North Pole.
          Footprint crossing antimeridian and outside polar area:
          Result should be a multipolygon not anymore crossing antimeridian.
        """
        geom = disk_on_globe(-178, 81, 300 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.MultiPolygon)
        self.assertAlmostEqual(int(rwkd.area), 150, delta=10)

    def test_rework_close_to_south_pole(self):
        """This footprint contains antimeridian and no pole, very close to
          the South Pole.
          Footprint crossing antimeridian and outside polar area:
          Result should be a multipolygon not anymore crossing antimeridian.
        """
        geom = disk_on_globe(-178, -81, 300 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.MultiPolygon)
        self.assertAlmostEqual(int(rwkd.area), 150, delta=10)

    def test_rework_no_pole(self):
        """This footprint contains antimeridian and no pole.
          Footprint crossing antimeridian and outside polar area:
          Result should be a multipolygon not anymore crossing antimeridian.
        """
        geom = disk_on_globe(-178, 0, 500 * 1000)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.MultiPolygon)
        self.assertAlmostEqual(int(rwkd.area), 70, delta=10)

    def test_rework_no_pole_no_antimeridian(self):
        """This footprint none of antimeridian and pole.
          No change of the footprint is required here.
        """
        geom = disk_on_globe(0, 0, 500 * 1000)
        self.assertFalse(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertFalse(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertEqual(geom, rwkd)
        self.assertTrue(shapely.equals(geom, rwkd),
                        "Generated footprint is not equivalents to input.")
        self.assertAlmostEqual(int(rwkd.area), 70, delta=10)
        print(footprint_facility.to_geojson(rwkd))

    def test_rework_cdse_product_no_pole_no_antimeridian(self):
        """
        Index 15 is a S3B SLSTR footprint located over Atlantic sea.
        It does not intersect antimeridian nor pole.

        Product available in CDSE as:
        S3B_OL_2_LRR____20240311T111059_20240311T115453_20240311T134014_2634_090_308______PS2_O_NR_002
        product id: 247c85f8-a78c-4abf-9005-2171ad6d8455
        """
        index = 15
        geom = fp_to_geometry(self.footprints[index])
        self.assertFalse(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertFalse(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertTrue(shapely.equals(geom, rwkd),
                        "Generated footprints are not equivalents")
        self.assertAlmostEqual(int(rwkd.area), 3000, delta=50)
        print(footprint_facility.to_geojson(rwkd))

    def test_rework_cdse_product_no_pole_cross_antimeridian(self):
        """
        Index 17 is a S3B OLCI Level 1 ERR footprint located over Pacific sea.
        It intersects antimeridian but does not pass over the pole.

        Product available in CDSE as:
        S3B_OL_1_ERR____20240224T213352_20240224T221740_20240225T090115_2628_090_086______PS2_O_NT_003
        product id: 07a3fa27-787f-479c-9bb3-d267249ffad3
        """
        index = 17
        geom = fp_to_geometry(self.footprints[index])
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.MultiPolygon)
        self.assertAlmostEqual(int(rwkd.area), 3000, delta=50)
        print(footprint_facility.to_geojson(rwkd))

    def test_rework_cdse_product_south_pole_antimeridian_overlapping(self):
        """
        Index 18 is a very long S3A SLSTR WST footprint.
        It intersects antimeridian and passes over the South Pole.
        At the South Pole location the footprint overlaps.

        Product available in CDSE as:
        S3A_SL_2_WST____20240224T211727_20240224T225826_20240226T033733_6059_109_228______MAR_O_NT_003
        product id: 67a2b237-50dc-4967-98ce-bad0fbc04ad3
        """
        index = 18
        geom = fp_to_geometry(self.footprints[index])
        print(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.Polygon,
                      footprint_facility.to_geojson(rwkd))
        self.assertAlmostEqual(int(rwkd.area), 10850, delta=50)
        print(footprint_facility.to_geojson(rwkd))

    @skip("Overlapping both north and south pole is still not supported")
    def test_rework_product_north_pole_antimeridian_overlapping(self):
        """
         Footprint with overlapping on the North Pole.It also passes other
         both North and South Pole.

         The fact the footprint cross both north and south pole fails with de
         manipulation and display.

         This product is an old historical product and this use case has not
         been retrieved in CDSE.
        """
        index = 10
        geom = fp_to_geometry(self.footprints[index])
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.MultiPolygon,
                      footprint_facility.to_geojson(rwkd))
        self.assertAlmostEqual(int(rwkd.area), 52430, delta=50)
        print(footprint_facility.to_geojson(rwkd))

    def test_rework_cdse_product_line_no_pole_antimeridian(self):
        """Thin line footprint products shall be managed by product type first.
           No need to wast resources to recognize and handle thin polygons.
           index 16 footprint is S3A product type SR_2_LAN_LI from CDSE
           S3A_SR_2_LAN_LI_20240302T235923_20240303T001845_20240304T182116_1161_109_330______PS1_O_ST_005
        """
        index = 16
        geom = fp_to_geometry(self.footprints[index])
        print(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_linestring_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.MultiLineString)
        self.assertAlmostEqual(int(rwkd.length), 180, delta=5)
        print(footprint_facility.to_geojson(rwkd))

    def test_rework_cdse_product_line_no_pole_no_antimeridian(self):
        """Thin line footprint products shall be managed by product type first.
           No need to wast resources to recognize and handle thin polygons.

           index 21 footprint is S3A product type SR_2_WAT from CDSE
           S3A_SR_2_WAT____20240312T172025_20240312T180447_20240314T075541_2661_110_083______MAR_O_ST_005
           cdse product id: f4b8547b-45ff-430c-839d-50a9be9c6105
        """
        index = 21
        geom = fp_to_geometry(self.footprints[index])
        self.assertFalse(footprint_facility.check_cross_antimeridian(geom))
        rwkd = footprint_facility.rework_to_linestring_geometry(geom)
        self.assertFalse(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertIs(type(rwkd), shapely.geometry.LineString)
        self.assertAlmostEqual(int(rwkd.length), 220, delta=5)
        print(footprint_facility.to_geojson(rwkd))

    def test_rework_south_hemisphere_no_pole_antimeridian(self):
        """
        Footprint index 2 is a small simple footprint crossing antimeridan
        """
        footprint = self.footprints[2]
        geom = fp_to_geometry(footprint)
        self.assertEqual(footprint_facility.check_cross_antimeridian(geom),
                         footprint['antimeridian'])
        rwkd = footprint_facility.rework_to_polygon_geometry(geom)
        self.assertTrue(footprint_facility.check_cross_antimeridian(rwkd))
        self.assertAlmostEqual(int(rwkd.area), 18, delta=1)
        print(footprint_facility.to_geojson(rwkd))

    def testSimplifySimple(self):
        """
        Ensure an already simple polygon is not affected by the algorithm
        """
        index = 0
        geom = fp_to_geometry(self.footprints[index])

        origin_area = getattr(geom, 'area', 0)
        points_number = len(shapely.get_coordinates(geom))

        rwkd = footprint_facility.simplify(geom, tolerance=.1)

        self.assertFalse(shapely.is_empty(rwkd) or shapely.is_missing(rwkd),
                         "Geometry is empty.")
        self.assertEqual(rwkd.area, origin_area, "Surface Area changed")
        self.assertEqual(len(shapely.get_coordinates(rwkd)), points_number)
        self.assertTrue(shapely.equals(geom, rwkd),
                        "Generated footprints are not equivalents")

    def testSimplifyAntimeridian(self):
        """
        Ensure an already simple polygon , crossing antimeridian
        is not affected by the algorithm
        """
        index = 3
        geom = footprint_facility.rework_to_polygon_geometry(
            fp_to_geometry(self.footprints[index]))

        origin_area = getattr(geom, 'area', 0)
        points_number = len(shapely.get_coordinates(geom))

        rwkd = footprint_facility.simplify(geom, tolerance=.1)
        print(rwkd)

        self.assertEqual(type(rwkd), shapely.geometry.MultiPolygon)
        self.assertFalse(shapely.is_empty(rwkd) or shapely.is_missing(rwkd),
                         "Geometry is empty.")
        self.assertEqual(rwkd.area, origin_area, "Surface Area changed")
        self.assertEqual(len(shapely.get_coordinates(rwkd)), points_number)
        self.assertTrue(shapely.equals(geom, rwkd),
                        "Generated footprints are not equivalents")

    def test_best_tolerance_for_single_geom(self):
        index = 15
        geom = footprint_facility.rework_to_polygon_geometry(
            fp_to_geometry(self.footprints[index]))

        # Surface change is limiting to 0.5% vs 100% of points could disappear
        percentage_area_change = .5
        percentage_less_points = 100
        best_tolerance = (
            footprint_facility.find_best_tolerance_for(
                geom,
                percentage_area_change,
                percentage_less_points))

        stats = self.simplify_bench(geom, best_tolerance)
        self.assertLessEqual(stats['Area']['variation'],
                             percentage_area_change / 100)
        self.assertLessEqual(stats['Points']['variation'],
                             percentage_less_points / 100)
        print(stats)
        self.assertAlmostEqual(best_tolerance, 0.27, delta=0.01)

        # Point reduction 50% is controlling the surface (See document: 50%
        # is quickly reached)
        percentage_area_change = 1
        percentage_less_points = 50
        best_tolerance = (
            footprint_facility.find_best_tolerance_for(
                geom,
                percentage_area_change,
                percentage_less_points))

        stats = self.simplify_bench(geom, best_tolerance)
        self.assertLessEqual(stats['Area']['variation'],
                             percentage_area_change / 100)
        self.assertLessEqual(stats['Points']['variation'],
                             percentage_less_points / 100)
        print(stats)
        self.assertAlmostEqual(best_tolerance, 0.028, delta=0.001)

    def test_best_tolerance_for_synergy(self):
        index = 22
        geom = footprint_facility.rework_to_polygon_geometry(
            fp_to_geometry(self.footprints[index]))

        # Synergy does not require tolerance: area surface never change,
        # and points are reduced from 292 to 5 with tolerance 0
        # The following parameter can not be reached  by the algorithm:
        #   This use cas is the most time-consuming
        percentage_area_change = .5
        percentage_less_points = 100
        best_tolerance = (
            footprint_facility.find_best_tolerance_for(
                geom,
                percentage_area_change,
                percentage_less_points))

        stats = self.simplify_bench(geom, best_tolerance)
        self.assertLessEqual(stats['Area']['variation'],
                             percentage_area_change / 100)
        self.assertLessEqual(stats['Points']['variation'],
                             percentage_less_points / 100)
        print(stats)
        self.assertEqual(best_tolerance, 0)

        # No area change for synergy
        percentage_area_change = 0
        percentage_less_points = 50
        best_tolerance = (
            footprint_facility.find_best_tolerance_for(
                geom,
                percentage_area_change,
                percentage_less_points))
        print(best_tolerance)
        stats = self.simplify_bench(geom, best_tolerance)
        self.assertLessEqual(stats['Area']['variation'],
                             percentage_area_change / 100)
        self.assertLessEqual(stats['Points']['variation'],
                             percentage_less_points / 100)
        print(stats)
        self.assertEqual(best_tolerance, 0)

    def testLongNoAntimeridian(self):
        """
        Use Long polygon not located on the antimeridian.
        Simplification shall reduce the number of coordinates
        :return: simplified polygon
        """
        index = 15
        geom = footprint_facility.rework_to_polygon_geometry(
            fp_to_geometry(self.footprints[index]))

        origin_area = getattr(geom, 'area', 0)
        points_number = len(shapely.get_coordinates(geom))

        self.assertEqual(points_number, 211)
        self.assertAlmostEqual(origin_area, 2976.02, delta=0.01)

        # No change expected
        stats = self.simplify_bench(geom, tolerance=0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 2976.02, delta=0.01)
        self.assertEqual(stats['Points']['new'], 211)

        # small choice
        stats = self.simplify_bench(geom, tolerance=.05)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 2977.53, delta=0.01)
        self.assertEqual(stats['Points']['new'], 87)

        # Best choice for 1% area change
        stats = self.simplify_bench(geom, tolerance=.45)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 3005.78, delta=0.01)
        self.assertEqual(stats['Points']['new'], 26)

        # greater choice
        stats = self.simplify_bench(geom, tolerance=1.0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 3015.72, delta=0.01)
        self.assertEqual(stats['Points']['new'], 21)

        # greater choice
        stats = self.simplify_bench(geom, tolerance=2.0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 3036.00, delta=0.01)
        self.assertEqual(stats['Points']['new'], 13)

    def testLongWithAntimeridian(self):
        """
        Use Long polygon not located on the antimeridian.
        Simplification shall reduce the number of coordinates
        :return: simplified polygon
        """
        index = 17
        geom = footprint_facility.rework_to_polygon_geometry(
            fp_to_geometry(self.footprints[index]))

        origin_area = getattr(geom, 'area', 0)
        points_number = len(shapely.get_coordinates(geom))

        self.assertEqual(points_number, 216)
        self.assertAlmostEqual(origin_area, 2961.08, delta=0.01)

        # No change expected
        stats = self.simplify_bench(geom, tolerance=0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 2961.08, delta=0.01)
        self.assertEqual(stats['Points']['new'], 216)

        # small choice
        stats = self.simplify_bench(geom, tolerance=.05)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 2963.40, delta=0.01)
        self.assertEqual(stats['Points']['new'], 87)

        # Best choice for 1% area change
        stats = self.simplify_bench(geom, tolerance=.45)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 2982.90, delta=0.01)
        self.assertEqual(stats['Points']['new'], 33)

        # greater choice
        stats = self.simplify_bench(geom, tolerance=1.0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 2993.12, delta=0.01)
        self.assertEqual(stats['Points']['new'], 24)

        # greater choice
        stats = self.simplify_bench(geom, tolerance=2.0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 3049.02, delta=0.01)
        self.assertEqual(stats['Points']['new'], 18)

    def testLongWithAntimeridianAndPole(self):
        """
        Use Long polygon not located on the antimeridian.
        Simplification shall reduce the number of coordinates
        :return: simplified polygon
        """
        index = 18
        geom = footprint_facility.rework_to_polygon_geometry(
            fp_to_geometry(self.footprints[index]))
        print(footprint_facility.to_geojson(geom))

        origin_area = getattr(geom, 'area', 0)
        points_number = len(shapely.get_coordinates(geom))

        self.assertEqual(points_number, 272)
        self.assertAlmostEqual(origin_area, 10857.59, delta=0.01)

        # No change expected
        stats = self.simplify_bench(geom, tolerance=0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 10857.59, delta=0.01)
        self.assertEqual(stats['Points']['new'], 272)

        # small choice
        stats = self.simplify_bench(geom, tolerance=.05)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 10862.31, delta=0.01)
        self.assertEqual(stats['Points']['new'], 166)

        # Best choice for 1% area change
        stats = self.simplify_bench(geom, tolerance=.45)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 10951.32, delta=0.01)
        self.assertEqual(stats['Points']['new'], 70)

        # greater choice
        stats = self.simplify_bench(geom, tolerance=1.0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 10964.73, delta=0.01)
        self.assertEqual(stats['Points']['new'], 55)

        # greater choice
        stats = self.simplify_bench(geom, tolerance=2.0)
        print(stats)
        self.assertAlmostEqual(stats['Area']['new'], 11229.99, delta=0.01)
        self.assertEqual(stats['Points']['new'], 39)

    def iter_among_simplify_tolerance(self, geometry, min: float, max: float,
                                      step: float):
        for tolerance in (map(lambda x: x/10000.0,
                              range(int(min*10000),
                                    int(max*10000),
                                    int(step*10000)))):
            print(self.simplify_bench(geometry, tolerance))

    @staticmethod
    def simplify_bench(geometry, tolerance=.1):
        origin_area = getattr(geometry, 'area', 0)
        origin_points_number = len(shapely.get_coordinates(geometry))

        reworked = footprint_facility.simplify(geometry, tolerance=tolerance)
        new_area = reworked.area
        variation_area = (new_area - origin_area)/origin_area
        new_points_number = len(shapely.get_coordinates(reworked))
        variation_point = ((new_points_number - origin_points_number) /
                           origin_points_number)
        return dict(value=tolerance,
                    Points=dict(
                        origin=origin_points_number,
                        new=new_points_number,
                        variation=variation_point),
                    Area=dict(
                        origin=origin_area,
                        new=new_area,
                        variation=variation_area))

    def testSimplifySynergyEurope(self):
        """
        Europe Syngery footprint has 297 point to be simplified
        :return:
        """
        index = 22
        geom = fp_to_geometry(self.footprints[index])
        self.assertTrue("EUROPE" in self.footprints[index]['name'],
                        f"Wrong name {self.footprints[index]['name']}")
        self.assertEqual(len(shapely.get_coordinates(geom)), 297)
        self.assertTrue(shapely.is_valid(geom))

        rwkd = footprint_facility.simplify(geom, 0, True)
        self.assertEqual(len(shapely.get_coordinates(rwkd)), 5)
        self.assertTrue(shapely.equals(geom, rwkd),
                        "Generated footprints are not equivalents")

    def testSimplifySynergyAustralia(self):
        """
        Australia Syngery footprint has 295 point to be simplified
        :return:
        """
        index = 23
        geom = fp_to_geometry(self.footprints[index])
        self.assertTrue("AUSTRALASIA" in self.footprints[index]['name'],
                        f"Wrong name {self.footprints[index]['name']}")
        self.assertEqual(len(shapely.get_coordinates(geom)), 295)
        self.assertTrue(shapely.is_valid(geom))

        rwkd = footprint_facility.simplify(geom, 0, True)
        self.assertEqual(len(shapely.get_coordinates(rwkd)), 5)
        self.assertTrue(shapely.equals(geom, rwkd),
                        "Generated footprints are not equivalents")
        print(footprint_facility.to_geojson(rwkd))

    def test_print_geojson_all(self):
        for index, footprint in enumerate(self.footprints):
            method = footprint.get('method', None)
            if footprint.get('testable', True) and method:
                geom = fp_to_geometry(footprint)
                reworked = None
                try:
                    if method.lower() == 'polygon':
                        reworked = (footprint_facility.
                                    rework_to_polygon_geometry(geom))
                    elif method.lower() == 'linestring':
                        reworked = (footprint_facility.
                                    rework_to_linestring_geometry(geom))
                    print(
                        f"{index}-{footprint['name']}: "
                        f"{footprint_facility.to_geojson(reworked)}")
                except Exception as exception:
                    print(f"WARN: {index}-{footprint['name']} "
                          f"raised an exception ({repr(exception)})")

    def test_print_wkt_all(self):
        for index, footprint in enumerate(self.footprints):
            method = footprint.get('method', None)
            if footprint.get('testable', True) and method:
                geom = fp_to_geometry(footprint)
                reworked = None
                try:
                    if method.lower() == 'polygon':
                        reworked = (footprint_facility.
                                    rework_to_polygon_geometry(geom))
                    elif method.lower() == 'linestring':
                        reworked = (footprint_facility.
                                    rework_to_linestring_geometry(geom))
                    print(
                        f"{index}-{footprint['name']}: "
                        f"{footprint_facility.to_wkt(reworked)}")
                except Exception as exception:
                    print(f"WARN: {index}-{footprint['name']} "
                          f"raised an exception ({repr(exception)})")

    def test_S1A_WV_SLC__1SSV_no_antimeridian(self):
        """
        Manage imagette of Sentinel-1 wave mode.
        This Test use real manifest.safe file of S1A WV data.
        convex hull algortihm generates a polygon reducing points number
        from 470 to 53.
        """
        filename = ('S1A_WV_SLC__1SSV_20240408T072206_20240408T074451_053339_'
                    '0677B9_0282.manifest.safe')
        path = os.path.join(os.path.dirname(__file__), 'samples', filename)

        # Extract data from manifest
        import xml.etree.ElementTree as ET
        tree = ET.parse(path)
        root = tree.getroot()

        ns_safe = "{http://www.esa.int/safe/sentinel-1.0}"
        ns_gml = "{http://www.opengis.net/gml}"
        xpath = (f".//metadataObject[@ID='measurementFrameSet']/metadataWrap/"
                 f"xmlData/{ns_safe}frameSet/{ns_safe}frame/"
                 f"{ns_safe}footPrint/{ns_gml}coordinates")
        coordinates = root.findall(xpath)

        # build the python geometry
        polygons = []
        for coord in coordinates:
            footprint = dict(coord_order="lat lon", coords=coord.text)
            polygons.append(
                footprint_facility.
                rework_to_polygon_geometry(fp_to_geometry(footprint)))

        geometry = shapely.MultiPolygon(polygons)
        self.assertEqual(
            len(shapely.get_coordinates(geometry)), 470)
        self.assertEqual(len(
            shapely.get_coordinates(geometry.convex_hull)), 53)

    def test_S1A_WV_SLC__1SSV_crossing_antimeridian(self):
        """
        Manage imagette of Sentinel-1 wave mode.
        This Test use real manifest.safe file of S1A WV data. This data crosses
        the antimridian.
        Convex hull algortihm generates a polygon reducing points number
        from 470 to 53. But This algorithm does not support antimeridian
        singularity, it shall be split into 2 polygons before execution.
        :return:
        """
        filename = ('S1A_WV_SLC__1SSV_20240405T060850_20240405T062741_053294_'
                    '0675E8_157E.manifest.safe')
        path = os.path.join(os.path.dirname(__file__), 'samples', filename)

        # Extract data from manifest
        import xml.etree.ElementTree as ET
        tree = ET.parse(path)
        root = tree.getroot()

        ns_safe = "{http://www.esa.int/safe/sentinel-1.0}"
        ns_gml = "{http://www.opengis.net/gml}"
        xpath = (f".//metadataObject[@ID='measurementFrameSet']/metadataWrap/"
                 f"xmlData/{ns_safe}frameSet/{ns_safe}frame/"
                 f"{ns_safe}footPrint/{ns_gml}coordinates")
        coordinates = root.findall(xpath)

        # build the python geometry
        polygons = []
        for coord in coordinates:
            footprint = dict(coord_order="lat lon", coords=coord.text)
            polygons.append(
                footprint_facility.
                rework_to_polygon_geometry(fp_to_geometry(footprint)))
        geometry = shapely.MultiPolygon(polygons)

        east_geometry = geometry.intersection(shapely.box(-180, -90, 0, 90))
        west_geometry = geometry.intersection(shapely.box(0, -90, 180, 90))

        self.assertEqual(len(shapely.get_coordinates(geometry)), 390)
        self.assertEqual(
            len(shapely.get_coordinates(east_geometry.convex_hull)) +
            len(shapely.get_coordinates(west_geometry.convex_hull)), 49)

    def test_jan_07_06_2024_S1(self):
        """
        Issue reported by 07/06/2024,
        regarding product reported from https://datahub.creodias.eu/odata/v1
        "S1A_EW_OCN__2SDH_20240602T183043_20240602T183154_054148_0695B3_"
        "DC42.SAFE"

        Command line used:
        <code>
        #Sentinel-6
        product="S1A_EW_OCN__2SDH_20240602T183043_20240602T183154_054148_"
                "0695B3_DC42.SAFE"
        wget -qO - 'https://datahub.creodias.eu/odata/v1/Products?'
                                '$filter=((Name%20eq%20%27'$product'%27))' |
            jq '.value[] | .Footprint' |
            tr -d '"' |
            tr -d "'" |
            cut -f 2 -d ';' |
            xargs -I {} python3 -c '
              from footprint_facility import to_wkt,rework_to_polygon_geometry;
              from shapely import wkt;
              print(to_wkt(rework_to_polygon_geometry(wkt.loads("{}"))));'
        </code>
        """

        product = ("MULTIPOLYGON (((-174.036011 66.098473, -170.292542 "
                   "70.167793, -180 71.02345651890965, "
                   "-180 66.64955743876074, -174.036011 66.098473)), "
                   "((180 66.64955743876074, 180 71.02345651890965, "
                   "178.781082 71.130898, 176.806686 66.944626, "
                   "180 66.64955743876074)))")
        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_jan_07_06_2024_S2(self):
        """
        Issue reported 07/06/2024,
        regarding product reported from https://datahub.creodias.eu/odata/v1
        "S2B_MSIL1C_20240111T183749_N0510_R141_T01CDN_20240112T201221.SAFE"

        Command line used:
        <code>
        #Sentinel-6
        product="S2B_MSIL1C_20240111T183749_N0510_R141_T01CDN_"
                "20240112T201221.SAFE"
        wget -qO - 'https://datahub.creodias.eu/odata/v1/Products?'
                              '$filter=((Name%20eq%20%27'$product'%27))' |
           jq '.value[] | .Footprint' |
           tr -d '"' |
           tr -d "'" |
           cut -f 2 -d ';' |
           xargs -I {} python3 -c '
              from footprint_facility import to_wkt,rework_to_polygon_geometry;
              from shapely import wkt;
              print(to_wkt(rework_to_polygon_geometry(wkt.loads("{}"))));'
        </code>
        """
        product = ("POLYGON ((-179.508117526313 -79.16127199879642, -180 "
                   "-79.01692999138557, -180 -79.19944296655834, "
                   "-180 -79.19959581716972, -180 -79.19972960600606, "
                   "-180 -79.19988578232916, -180 -79.20007346017209, "
                   "-180 -79.20013436682478, -180 -79.20024126342099, "
                   "-180 -79.20029258993124, -180 -79.20049921536173, "
                   "-180 -79.20054631332516, -180 -79.20066396817484, "
                   "-180 -79.20077375877023, -180 -79.2008843839914, "
                   "-180 -79.21714918681978, -180 -79.21715630792468, "
                   "-180 -79.2175551235766, -180 -79.21773293229286, "
                   "-180 -79.21778003784787, -180 -79.2177900670303, "
                   "-180 -79.21779114542757, -180 -79.21779351757006, "
                   "-180 -79.21780296489362, -180 -79.21780421542903, "
                   "-180 -79.21780998189048, -180 -79.21827514353097, "
                   "-180 -79.21830910412172, -180 -79.33237518158053, "
                   "-178.9375581912928 -79.33974790172739, "
                   "-179.5490821971551 -79.1659353807717, -179.5463891574934 "
                   "-79.16562951391516, -179.5464126641663 "
                   "-79.16562282940411, -179.508117526313 "
                   "-79.16127199879642))")
        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_jan_07_06_2024_S3(self):
        """
        Issue reported 07/06/2024,
        regarding product reported from https://datahub.creodias.eu/odata/v1
        "S3A_SL_2_LST____20240601T075148_20240601T075448_20240601T102247_0180_
            113_078_1080_PS1_O_NR_004.SEN3"

        Command line used:
        <code>
        #Sentinel-6
        product="S3A_SL_2_LST____20240601T075148_20240601T075448_"
                "20240601T102247_0180_113_078_1080_PS1_O_NR_004.SEN3"
        wget -qO - 'https://datahub.creodias.eu/odata/v1/Products?'
                   '$filter=((Name%20eq%20%27'$product'%27))' |
           jq '.value[] | .Footprint' |
           tr -d '"' |
           tr -d "'" |
           cut -f 2 -d ';' |
           xargs -I {} python3 -c '
              from footprint_facility import to_wkt,rework_to_polygon_geometry;
              from shapely import wkt;
              print(to_wkt(rework_to_polygon_geometry(wkt.loads("{}"))));'
        </code>
        """
        product = ("MULTIPOLYGON (((180 65.68414879114478, 179.764 65.842, "
                   "175.686 68.0499, 170.896 70.1128, 171.256 70.2301, "
                   "172.291 70.5293, 173.355 70.8266, 174.424 71.108, "
                   "175.533 71.393, 176.703 71.6691, 177.869 71.9409, "
                   "179.088 72.1986, 180 72.38208313539192, "
                   "180 65.68414879114478)), ((-180 72.38208313539192, "
                   "-179.649 72.4527, -178.36 72.6974, -177.039 72.9329, "
                   "-175.694 73.1682, -174.288 73.3878, -172.854 73.5962, "
                   "-171.396 73.7949, -169.91 73.9844, -168.382 74.1639, "
                   "-166.798 74.3324, -165.214 74.4841, -163.563 74.6311, "
                   "-161.917 74.7626, -160.247 74.8843, -158.545 74.996, "
                   "-156.815 75.0909, -155.079 75.1715, -153.303 75.2416, "
                   "-151.49 75.2841, -149.712 75.3291, -147.895 75.3655, "
                   "-146.1 75.3717, -145.923 72.801, -145.686 70.1856, "
                   "-145.411 67.5691, -145.11 64.9601, -145.109 64.9514, "
                   "-146.171 64.9259, -147.266 64.8952, -148.33 64.8479, "
                   "-149.397 64.7954, -150.451 64.7395, -151.517 64.6709, "
                   "-152.57 64.5974, -153.604 64.5188, -154.67 64.4338, "
                   "-155.683 64.3383, -156.721 64.2411, -157.73 64.1281, "
                   "-158.74 64.0097, -159.743 63.8851, -160.753 63.7556, "
                   "-161.729 63.6187, -162.7 63.475, -163.671 63.3246, "
                   "-164.625 63.169, -165.557 62.9984, -166.489 62.8312, "
                   "-167.416 62.6562, -168.325 62.4771, -169.236 62.2889, "
                   "-170.112 62.094, -170.979 61.896, -171.853 61.6965, "
                   "-172.713 61.4854, -173.554 61.2618, -173.86 61.1864, "
                   "-173.885 61.1901, -176.803 63.5458, "
                   "-180 65.68414879114478, -180 72.38208313539192)))")
        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_jan_07_06_2024_S5P(self):
        """
        Issue reported 07/06/2024,
        regarding product reported from https://datahub.creodias.eu/odata/v1
        "S5P_OFFL_L1B_RA_BD8_20240601T002118_20240601T020248_34371_03_020100_"
        "20240601T035317.nc"

        Command line used:
        <code>
        #Sentinel-6
        product="S5P_OFFL_L1B_RA_BD8_20240601T002118_20240601T020248_34371_"
                "03_020100_20240601T035317.nc"
        wget -qO - 'https://datahub.creodias.eu/odata/v1/Products?'
                   '$filter=((Name%20eq%20%27'$product'%27))' |
           jq '.value[] | .Footprint' |
           tr -d '"' |
           tr -d "'" |
           cut -f 2 -d ';' |
           xargs -I {} python3 -c '
              from footprint_facility import to_wkt,rework_to_polygon_geometry;
              from shapely import wkt;
              print(to_wkt(rework_to_polygon_geometry(wkt.loads("{}"))));'
        </code>
        """
        product = ("MULTIPOLYGON (((-180 90, 0 90, 180 90, 180 "
                   "-41.86733642322825, 179.9763 -41.531116, 179.86395 "
                   "-40.08868, 179.74141 -38.645264, 179.60912 -37.200897, "
                   "179.46786 -35.75559, 179.31769 -34.30946, 179.15906 "
                   "-32.862434, 178.99269 -31.414688, 178.81853 -29.966076, "
                   "178.63658 -28.516865, 178.44719 -27.067, 178.25061 "
                   "-25.61658, 178.04707 -24.165606, 177.8364 -22.714108, "
                   "177.61887 -21.262264, 177.39426 -19.81008, 177.1631 "
                   "-18.357447, 176.925 -16.904694, 176.68001 -15.451712, "
                   "176.42805 -13.998643, 176.16916 -12.545524, 175.90312 "
                   "-11.092463, 175.63004 -9.639457, 175.3496 -8.186663, "
                   "175.06177 -6.734143, 174.76614 -5.281979, 174.46315 "
                   "-3.8302007, 174.15176 -2.378978, 173.8324 -0.9284125, "
                   "173.50458 0.5215158, 173.16786 1.9705427, 172.82219 "
                   "3.4187272, 172.46709 4.8658676, 172.10217 6.3118157, "
                   "171.7273 7.756614, 171.34175 9.199921, 170.94524 "
                   "10.641779, 170.53746 12.082073, 170.11725 13.520405, "
                   "169.68442 14.956774, 169.2385 16.391098, 168.77852 "
                   "17.823135, 168.3039 19.252695, 167.81377 20.679672, "
                   "167.30734 22.103739, 166.78372 23.524765, 166.24197 "
                   "24.942528, 165.68028 26.356531, 165.09837 27.766888, "
                   "164.4945 29.173054, 163.86742 30.57479, 163.21565 "
                   "31.971884, 162.53703 33.36365, 161.83011 34.749847, "
                   "161.09294 36.13012, 160.32303 37.503757, 159.51851 "
                   "38.87066, 158.67624 40.229736, 157.79373 41.58067, "
                   "156.86758 42.922604, 155.89424 44.254745, 154.87033 "
                   "45.576374, 153.79134 46.886234, 152.65265 48.1834, "
                   "151.44977 49.466858, 150.1766 50.734867, 148.82782 "
                   "51.986423, 147.3959 53.21909, 145.87462 54.431526, "
                   "144.25616 55.6216, 142.53186 56.786644, 140.6929 "
                   "57.92401, 138.73013 59.03079, 136.63399 60.103626, "
                   "134.3939 61.13849, 132.00021 62.131363, 129.44383 "
                   "63.077717, 126.71549 63.972107, 123.80851 64.80932, "
                   "120.71825 65.58352, 117.4435 66.28858, 113.9866 "
                   "66.91782, 110.35588 67.46508, 106.56541 67.92443, "
                   "102.63593 68.29027, 98.59393 68.55761, 94.47231 "
                   "68.723015, 90.30819 68.78379, 86.14067 68.73939, "
                   "82.00989 68.59008, 77.953156 68.338196, 74.004 67.98733, "
                   "70.19006 67.54217, 66.53354 67.00781, 63.048588 "
                   "66.390724, 59.74498 65.69689, 56.62577 64.93289, "
                   "53.69056 64.10463, 50.934845 63.218437, 48.35202 "
                   "62.279533, 45.933685 61.293293, 43.670315 60.264317, "
                   "41.552414 59.196846, 39.569862 58.094654, 37.71257 "
                   "56.961403, 35.971294 55.800068, 34.337177 54.613335, "
                   "32.801754 53.40378, 31.356928 52.17355, 29.996086 "
                   "50.924458, 28.712265 49.658478, 27.499353 48.377003, "
                   "26.351748 47.081535, 25.264315 45.773205, 23.509417 "
                   "46.187706, 22.387592 46.436874, 19.424397 47.043514, "
                   "18.469027 47.22568, 16.448671 47.595142, 15.751153 "
                   "47.719036, 13.117875 48.17936, 12.130072 48.35204, "
                   "9.9415 48.740776, 9.136205 48.886753, 7.1947713 "
                   "49.245853, 6.4209137 49.39178, 4.406008 49.77871, "
                   "3.5373578 49.94825, 1.0665072 50.43534, -0.1086481 "
                   "50.66653, -2.2045333 51.070694, -3.02813 51.2248, "
                   "-5.5050035 51.66518, -6.7307587 51.867783, -9.840376 "
                   "52.32859, -10.816945 52.456486, -11.346613 52.522366, "
                   "-11.343067 52.666473, -11.319423 54.106884, -11.315634 "
                   "55.54611, -11.333933 56.984184, -11.37619 58.420925, "
                   "-11.446254 59.856216, -11.548398 61.290066, -11.686891 "
                   "62.722286, -11.867555 64.152725, -12.096516 65.58102, "
                   "-12.384995 67.007065, -12.7416525 68.4305, -13.182033 "
                   "69.850876, -13.724232 71.26764, -14.393544 72.67994, "
                   "-15.221556 74.08696, -16.253458 75.48708, -17.554081 "
                   "76.87837, -19.21444 78.25778, -21.374022 79.62078, "
                   "-24.246838 80.96009, -28.17806 82.26377, -33.747017 "
                   "83.51025, -41.931393 84.65964, -54.259308 85.634834, "
                   "-72.295746 86.2957, -94.80977 86.46186, -115.950935 "
                   "86.07003, -131.49446 85.25663, -141.87256 84.19631, "
                   "-148.8116 83.00032, -153.60501 81.72725, -157.0416 "
                   "80.407684, -159.58424 79.058525, -161.51413 77.6892, "
                   "-163.01147 76.30584, -164.1911 74.91215, -165.13258 "
                   "73.51075, -165.89003 72.103264, -166.50316 70.69103, "
                   "-167.00111 69.27482, -167.40501 67.85531, -167.73248 "
                   "66.43314, -167.99614 65.00868, -168.20502 63.582, "
                   "-168.36803 62.153614, -168.49158 60.72353, -168.58104 "
                   "59.291912, -168.6403 57.859013, -168.6735 56.42478, "
                   "-168.6834 54.989403, -168.67216 53.55279, -168.64241 "
                   "52.11524, -168.59605 50.676617, -168.53398 49.23707, "
                   "-168.458 47.7965, -168.36926 46.35513, -168.26866 "
                   "44.912914, -168.15657 43.469837, -168.03493 42.02598, "
                   "-167.90309 40.58142, -167.76227 39.136147, -167.61287 "
                   "37.69012, -167.45518 36.243496, -167.28972 34.796215, "
                   "-167.11655 33.34833, -166.93604 31.899948, -166.7488 "
                   "30.450903, -166.55434 29.001495, -166.35318 27.551653, "
                   "-166.14563 26.10141, -165.93146 24.65076, -165.71072 "
                   "23.199873, -165.48364 21.748617, -165.25038 20.297253, "
                   "-165.01054 18.84571, -164.7642 17.394058, -164.51172 "
                   "15.942321, -164.25249 14.490606, -163.98685 13.039, "
                   "-163.71452 11.58754, -163.4353 10.136244, -163.1493 "
                   "8.685246, -162.85625 7.23458, -162.55586 5.7843776, "
                   "-162.24821 4.334724, -161.93277 2.885562, -161.60968 "
                   "1.4371812, -161.27832 -0.010504091, -160.93875 "
                   "-1.4573016, -160.59015 -2.9031165, -160.2327 -4.3478966, "
                   "-159.86583 -5.791431, -159.4894 -7.233785, -159.10248 "
                   "-8.674613, -158.70517 -10.113982, -158.29645 -11.551577, "
                   "-157.87637 -12.98747, -157.444 -14.421311, -156.99876 "
                   "-15.85309, -156.54001 -17.282581, -156.06744 -18.709654, "
                   "-155.57948 -20.13405, -155.07596 -21.555643, -154.5558 "
                   "-22.974205, -154.01758 -24.389427, -153.46085 "
                   "-25.801155, -152.8842 -27.209108, -152.28654 -28.612999, "
                   "-151.66628 -30.012564, -151.02205 -31.407356, -150.35246 "
                   "-32.79723, -149.65543 -34.181614, -148.9292 -35.56014, "
                   "-148.17175 -36.932407, -147.38063 -38.29769, -146.55342 "
                   "-39.6557, -145.68736 -41.00566, -144.7798 -42.347084, "
                   "-143.8269 -43.67897, -142.82521 -45.00064, -141.77133 "
                   "-46.31118, -140.66045 -47.60957, -139.4877 -48.894478, "
                   "-138.24828 -50.16494, -136.93637 -51.41941, -135.5458 "
                   "-52.656303, -134.0697 -53.87377, -132.5008 -55.069862, "
                   "-130.8311 -56.242336, -129.05223 -57.388638, -127.15525 "
                   "-58.506126, -125.13072 -59.59139, -122.968834 "
                   "-60.641064, -120.659386 -61.651016, -118.19338 "
                   "-62.61717, -115.5613 -63.534576, -112.755646 -64.39802, "
                   "-109.7707 -65.20218, -106.60273 -65.9407, -108.59956 "
                   "-66.93513, -109.949425 -67.55315, -113.80929 -69.11937, "
                   "-115.14966 -69.60426, -118.14668 -70.59907, -119.23415 "
                   "-70.933334, -123.59422 -72.15644, -125.33779 -72.600525, "
                   "-129.42595 -73.55694, -131.01332 -73.89894, -135.04094 "
                   "-74.698845, -136.73071 -75.00694, -141.37552 -75.7759, "
                   "-143.49399 -76.090675, -149.93294 -76.91839, -153.21971 "
                   "-77.26976, -159.44414 -77.81199, -162.01192 -77.991165, "
                   "-170.08966 -78.39724, -174.24023 -78.5178, "
                   "-180 -78.54299733461647, -180 -60.43489669869457, "
                   "-179.96748 -60.16659, -179.83322 -58.742584, -179.73184 "
                   "-57.316566, -179.65977 -55.888824, -179.6136 -54.45934, "
                   "-179.59041 -53.028225, -179.58913 -51.595722, -179.60602 "
                   "-50.161697, -179.64015 -48.726337, -179.69008 -47.2897, "
                   "-179.75443 -45.851803, -179.83203 -44.412685, -179.9221 "
                   "-42.972466, -180 -41.86733642322825, -180 90)), "
                   "((180 -78.54299733461647, 175.04135 -78.56469, 171.68889 "
                   "-78.500534, 169.88521 -78.44987, 170.11551 -78.31641, "
                   "172.13577 -76.97113, 173.73349 -75.609184, 175.0151 "
                   "-74.23472, 176.05489 -72.85067, 176.90472 -71.4589, "
                   "177.60373 -70.061005, 178.18103 -68.65796, 178.65848 "
                   "-67.25062, 179.05312 -65.83957, 179.37799 -64.42529, "
                   "179.6447 -63.00817, 179.86017 -61.588566, "
                   "180 -60.43489669869457, 180 -78.54299733461647)))")
        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_jan_07_06_2024_S6(self):
        """
        Issue reported 07/06/2024,
        regarding product reported from https://datahub.creodias.eu/odata/v1
        "S6A_P4_2__LR______20240601T141934_20240601T151547_20240602T094057_"
        "3373_131_075_037_EUM__OPE_ST_F09.SEN6"

        Command line used:
        <code>
        #Sentinel-6
        product="S6A_P4_2__LR______20240601T141934_20240601T151547_"
                "20240602T094057_3373_131_075_037_EUM__OPE_ST_F09.SEN6"
        wget -qO - 'https://datahub.creodias.eu/odata/v1/Products?'
                   '$filter=((Name%20eq%20%27'$product'%27))' |
           jq '.value[] | .Footprint' |
           tr -d '"' |
           tr -d "'" |
           cut -f 2 -d ';' |
           xargs -I {} python3 -c '
              from footprint_facility import to_wkt,rework_to_polygon_geometry;
              from shapely import wkt;
              print(to_wkt(rework_to_polygon_geometry(wkt.loads("{}"))));'
        </code>
        """
        product = ("MULTIPOLYGON (((180 60.22980148474507, 168.417758 "
                   "56.243085, 155.691259 46.750119, 147.366563 36.111285, "
                   "141.341637 24.872868, 136.505741 13.306639, 132.205885 "
                   "1.583584, 127.965756 -10.173274, 123.326157 -21.849296, "
                   "116.541992 -35.271951, 108.459264 -46.166451, 96.228309 "
                   "-56.013986, 76.619961 -63.592298, 48.281191 -66.644914, "
                   "48.174683 -65.650602, 76.260516 -62.659132, 95.601983 "
                   "-55.234425, 107.656475 -45.570188, 115.649571 "
                   "-34.820747, 122.396845 -21.480001, 127.025064 -9.834011, "
                   "131.267059 1.927975, 135.583207 13.692556, 140.460574 "
                   "25.345868, 146.579813 36.728557, 155.094546 47.552574, "
                   "168.092904 57.188849, 180 61.27018968706418, "
                   "180 60.22980148474507)), ((-180 61.27018968706418, "
                   "-171.164341 64.298748, -145.987795 66.645419, "
                   "-145.894989 65.649735, -171.071535 63.303063, "
                   "-180 60.22980148474507, -180 61.27018968706418)))")

        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_marcin_10_06_2024_01(self):
        """
        Issue reported 10/06/2024,
        regarding product footprint reported from
        https://datahub.creodias.eu/odata/v1
        "S2A_MSIL1C_20240409T224801_N0510_R058_T01RBN_20240410T013411.SAFE"

        """
        product = ("POLYGON ((-179.9876881381423 29.0291685491302, -180 "
                   "29.03155659510362, -180 28.98285094292218, "
                   "-180 28.98271563385081, -180 28.98267749312967, "
                   "-180 28.9826301658557, -180 28.98231907003779, "
                   "-180 28.98207088113581, -180 28.98199564557697, "
                   "-180 28.9818874012062, -180 28.98168445373044, "
                   "-180 28.98134004587741, -180 28.97287167365954, "
                   "-180 28.9724800982187, -180 28.97201308859933, "
                   "-180 28.92366753988982, -180 28.92345535520249, "
                   "-180 28.92154911321751, -180 28.92142927714886, "
                   "-180 28.92138566174452, -180 28.92124143543171, "
                   "-180 28.92122367544565, -180 28.92117129124892, "
                   "-180 28.92110801483784, -180 28.92107004450444, "
                   "-180 28.91396984852497, -180 28.91131882845719, "
                   "-180 28.91121448540229, -180 28.80581804559539, "
                   "-179.0350228270187 28.82378643806586, -179.1700409251341 "
                   "28.8545636014009, -179.2582015439308 28.87464057048835, "
                   "-179.258196659197 28.8746585624768, -179.2583009156745 "
                   "28.87468232757705, -179.2578661104106 28.87628285923174, "
                   "-179.2580148638191 28.87631698966688, -179.2579161794961 "
                   "28.87668033508817, -179.2579401870867 28.87668584831188, "
                   "-179.2579084557888 28.87680270425759, -179.2579329974328 "
                   "28.87680834562038, -179.2576853439967 28.87771959163993, "
                   "-179.5077117875585 28.93318662235096, -179.5083485813891 "
                   "28.93082221299412, -179.5105432199461 28.93128541800726, "
                   "-179.5106967946305 28.9307145946074, -179.7347382855255 "
                   "28.97795276579205, -179.7339339236061 28.98096695785088, "
                   "-179.9842953306247 29.03133422840303, -179.984597481629 "
                   "29.03019291548934, -179.9847308126944 29.03021870182818, "
                   "-179.9849148753883 29.02952269078926, -179.9850016555684 "
                   "29.02953951185671, -179.9851816359575 29.02885949683142, "
                   "-179.9876433795116 29.02933773510185, -179.9876881381423 "
                   "29.0291685491302))")

        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_marcin_10_06_2024_02(self):
        """
        Issue reported 10/06/2024,
        regarding product footprint reported from
        https://datahub.creodias.eu/odata/v1
        "S2A_MSIL1C_20240521T030521_N0510_R075_T51VUC_20240521T064313.SAFE"

        """
        product = ("POLYGON ((119.797421348587 55.93819621688083, "
                   "119.807765253249 55.81589134146334, 121.5593013138845 "
                   "55.8488879777783, 121.5216424730097 56.83505986087058, "
                   "120.235983877957 56.81056346974395, 120.2024267920502 "
                   "56.74457214191219, 120.1305599624232 56.5994713836992, "
                   "120.0573029598348 56.45474361754042, 119.9844055829299 "
                   "56.30992972532578, 119.9114330022377 56.16513333356001, "
                   "119.8380448819553 56.02044430591336, 119.797421348587 "
                   "55.93819621688083))")

        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_marcin_10_06_2024_03(self):
        """
        Issue reported 10/06/2024,
        regarding product footprint reported from
        https://datahub.creodias.eu/odata/v1
        "S2B_MSIL1C_20240513T193859_N0510_R042_T15XVJ_20240513T214054.SAFE"
        """
        product = ("POLYGON ((-96.97673033238847 79.15042075633988, "
                   "-92.53422260052758 79.18123126796907, -92.49706194741519 "
                   "79.97506966116111, -92.58789246863891 79.96030467308965, "
                   "-93.2083285328792 79.85763391842576, -93.81362408192648 "
                   "79.75308071559806, -94.40926223137284 79.64796950837108, "
                   "-94.98949597744156 79.54095981795254, -95.55965621122536 "
                   "79.43332129931305, -96.1178586950274 79.324625086183, "
                   "-96.66449811670545 79.21488698029992, -96.97673033238847 "
                   "79.15042075633988))")

        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_marcin_10_06_2024_04(self):
        """
        Issue reported 10/06/2024,
        regarding product footprint reported from
        https://datahub.creodias.eu/odata/v1
        "S2B_MSIL1C_20231227T210529_N0510_R071_T60DWG_20231227T215209.SAFE"
        """
        product = ("POLYGON ((176.9994652359355 -70.41607942052394, "
                   "176.9994413608334 -71.29052981531568, 179.572179881629 "
                   "-71.26959996377886, 179.6721740780138 "
                   "-71.19803855312027, 179.8599573008396 "
                   "-71.06164728850977, 180 -70.95851167153866, "
                   "180 -70.92556822281612, 179.3942277030721 "
                   "-70.82312532219207, 179.4065959993365 "
                   "-70.81423576046868, 178.7525658093475 "
                   "-70.70538682886387, 178.7478324461233 "
                   "-70.70871718019387, 178.747493319118 -70.70865970914443, "
                   "178.7466712566637 -70.70923776863077, 178.7465004516869 "
                   "-70.70920879475975, 178.7447941071134 "
                   "-70.71040875515017, 178.7446136307058 "
                   "-70.71037810545408, 178.7440344859275 "
                   "-70.71078525996892, 178.7439023131008 "
                   "-70.71076277629899, 178.7430910034338 "
                   "-70.71133296014627, 178.7427845577315 "
                   "-70.71128077984781, 178.7417806732775 "
                   "-70.71198628518216, 178.7416517931338 "
                   "-70.71196431792183, 178.7400909685969 "
                   "-70.71306235743884, 178.739977349168 -70.71304295238998, "
                   "178.7393022707546 -70.71351730865861, 178.739129461579 "
                   "-70.71348776470606, 178.7382493908013 "
                   "-70.71410575542254, 178.170783554921 -70.61698669068961, "
                   "178.1828204293513 -70.60869796010728, 177.5542359158372 "
                   "-70.50195289083793, 177.5472162020975 "
                   "-70.50669177750456, 177.5469060049969 "
                   "-70.50663830899008, 177.5456972851142 "
                   "-70.50745367297019, 177.545666713415 -70.50744839713443, "
                   "177.5440119349725 -70.5085657739295, 177.5433628801525 "
                   "-70.50845362202493, 177.5428597657197 "
                   "-70.50879341424859, 177.5428557244273 "
                   "-70.50879271644239, 177.5421181273214 "
                   "-70.50929034494347, 177.5420059497903 "
                   "-70.50927096526664, 177.5413168288432 "
                   "-70.50973549338948, 176.9994652359355 "
                   "-70.41607942052394))")

        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_marcin_10_06_2024_05(self):
        """
        Issue reported 10/06/2024,
        regarding product footprint reported from
        https://datahub.creodias.eu/odata/v1
        "S2B_MSIL1C_20240111T183749_N0510_R141_T01CDN_20240112T201221.SAFE"
        """
        product = ("POLYGON ((-179.508117526313 -79.16127199879642, -180 "
                   "-79.01692999138557, -180 -79.19944296655834, "
                   "-180 -79.19959581716972, -180 -79.19972960600606, "
                   "-180 -79.19988578232916, -180 -79.20007346017209, "
                   "-180 -79.20013436682478, -180 -79.20024126342099, "
                   "-180 -79.20029258993124, -180 -79.20049921536173, "
                   "-180 -79.20054631332516, -180 -79.20066396817484, "
                   "-180 -79.20077375877023, -180 -79.2008843839914, "
                   "-180 -79.21714918681978, -180 -79.21715630792468, "
                   "-180 -79.2175551235766, -180 -79.21773293229286, "
                   "-180 -79.21778003784787, -180 -79.2177900670303, "
                   "-180 -79.21779114542757, -180 -79.21779351757006, "
                   "-180 -79.21780296489362, -180 -79.21780421542903, "
                   "-180 -79.21780998189048, -180 -79.21827514353097, "
                   "-180 -79.21830910412172, -180 -79.33237518158053, "
                   "-178.9375581912928 -79.33974790172739, "
                   "-179.5490821971551 -79.1659353807717, -179.5463891574934 "
                   "-79.16562951391516, -179.5464126641663 "
                   "-79.16562282940411, -179.508117526313 "
                   "-79.16127199879642))")

        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_marcin_10_06_2024_06(self):
        """
        Issue reported 10/06/2024,
        regarding product footprint reported from
        https://datahub.creodias.eu/odata/v1
        "S2B_MSIL1C_20240326T210529_N0510_R071_T60DWG_20240326T233250.SAFE"
        """
        product = ("POLYGON ((176.9994651544594 -70.41906356609854, "
                   "176.9994413608334 -71.29052981531568, 179.5827002480463 "
                   "-71.26951437804776, 179.6779330353536 "
                   "-71.20164541504658, 179.8660471915699 "
                   "-71.06541455826518, 180 -70.96702620900645, "
                   "180 -70.92851075764088, 179.399173113056 "
                   "-70.8269190325428, 179.4118052503909 -70.81786127781933, "
                   "178.7583023614406 -70.70911422211499, 178.753397288728 "
                   "-70.71254820043357, 178.7529355395073 "
                   "-70.71246995820101, 178.7521208760483 "
                   "-70.71304130653343, 178.7520537809051 "
                   "-70.71302992651998, 178.7503158259021 "
                   "-70.71424701992557, 178.7499498520174 "
                   "-70.71418487616172, 178.749350023558 -70.71460490928753, "
                   "178.7489397011358 -70.71453511892662, 178.7481155498963 "
                   "-70.7151126523084, 178.7480502042567 -70.71510152684793, "
                   "178.7461968290528 -70.71639954174172, 178.7460486272359 "
                   "-70.7163742596462, 178.7452945166694 -70.71690180963448, "
                   "178.7447921469283 -70.71681602157507, 178.7440933445718 "
                   "-70.71730500907283, 178.7438949980914 "
                   "-70.71727110341526, 178.7430226810598 "
                   "-70.71788223813657, 178.1753788459815 -70.6207447884229, "
                   "178.1876847818419 -70.6122901476094, 177.5596526106852 "
                   "-70.50565079699012, 177.5524359693655 "
                   "-70.51050296081975, 177.5517761838235 "
                   "-70.51038924711861, 177.5488326974667 -70.5123663560824, "
                   "177.5482939024504 -70.51227326695077, 177.547791959252 "
                   "-70.5126104218932, 177.5474041860378 -70.51254347329198, "
                   "177.5466434074202 -70.51305453487579, 177.5464329171782 "
                   "-70.5130181746587, 177.5457517781493 -70.51347629162153, "
                   "176.9994651544594 -70.41906356609854))")

        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_marcin_10_06_2024_07(self):
        """
        Issue reported 10/06/2024,
        regarding product footprint reported from
        https://datahub.creodias.eu/odata/v1
        "S2B_MSIL1C_20240121T183749_N0510_R141_T60CWT_20240121T212726.SAFE"
        """
        product = ("POLYGON ((-179.3389758084033 -79.14242545505675, -180 "
                   "-78.9493443207847, -180 -79.20060232223966, "
                   "-180 -79.20070247954938, -180 -79.2007670522849, "
                   "-180 -79.20090023310787, -180 -79.20112235414808, "
                   "-180 -79.2011867192771, -180 -79.20126215418246, "
                   "-180 -79.20128995185189, -180 -79.20148337743043, "
                   "-180 -79.20159443848705, -180 -79.20162579974793, "
                   "-180 -79.2017268386863, -180 -79.20187103282393, "
                   "-180 -79.21844315586061, -180 -79.21847170744411, "
                   "-180 -79.21866164111945, -180 -79.21874225983464, "
                   "-180 -79.21879659217447, -180 -79.21882990235626, "
                   "-180 -79.21894420996992, -180 -79.2189473244755, "
                   "-180 -79.21895573254695, -180 -79.21896107649158, "
                   "-180 -79.21904024752864, -180 -79.21946330316014, "
                   "-180 -79.21956056932171, -180 -79.33150649003348, "
                   "-178.7662167742809 -79.3210939569312, -179.3807034712833 "
                   "-79.14724286926662, -179.3779715745694 "
                   "-79.14692878413946, -179.3780146197653 "
                   "-79.14691659976745, -179.3389758084033 "
                   "-79.14242545505675))")

        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_marcin_10_06_2024_08(self):
        """
        Issue reported 10/06/2024,
        regarding product footprint reported from
        https://datahub.creodias.eu/odata/v1
        "S2B_MSIL1C_20240220T183749_N0510_R141_T01CDN_20240220T210409.SAFE"
        """
        product = ("POLYGON ((-179.472327088384 -79.16489209680499, -180 "
                   "-79.01033649528226, -180 -79.20654449983061, "
                   "-180 -79.20669504227244, -180 -79.20693310677962, "
                   "-180 -79.20718312069948, -180 -79.2073122331582, "
                   "-180 -79.2073313990563, -180 -79.20743070381685, "
                   "-180 -79.20754999893539, -180 -79.20778768373577, "
                   "-180 -79.20794579617595, -180 -79.20802562547372, "
                   "-180 -79.20810912784819, -180 -79.20823965873238, "
                   "-180 -79.2251377184389, -180 -79.22522241611811, "
                   "-180 -79.22542394599088, -180 -79.22546978496251, "
                   "-180 -79.2255205128762, -180 -79.22552750405887, "
                   "-180 -79.22566046972585, -180 -79.22567891628702, "
                   "-180 -79.22574971160533, -180 -79.22578693311603, "
                   "-180 -79.22586581935971, -180 -79.2261620322246, "
                   "-180 -79.22636934723057, -180 -79.33237518158053, "
                   "-178.9119796167795 -79.33992540196326, "
                   "-179.5126923714637 -79.16950069337689, -179.472327088384 "
                   "-79.16489209680499))")

        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_marcin_10_06_2024_09(self):
        """
        Issue reported 10/06/2024,
        regarding product footprint reported from
        https://datahub.creodias.eu/odata/v1
        "S2B_MSIL1C_20240305T224759_N0510_R058_T01RBN_20240305T235933.SAFE"
        """
        product = ("POLYGON ((-179.9726084221875 29.02774848883664, -180 "
                   "29.03305602630523, -180 28.92405745940028, "
                   "-180 28.92365348425323, -180 28.92328471061849, "
                   "-180 28.92315587836184, -180 28.92314589214138, "
                   "-180 28.92292509977204, -180 28.92273860727704, "
                   "-180 28.92243478502562, -180 28.92237840518189, "
                   "-180 28.92220714165031, -180 28.92186336567974, "
                   "-180 28.92169255434653, -180 28.92085916576632, "
                   "-180 28.86398419969101, -180 28.86376235439207, "
                   "-180 28.8625135403597, -180 28.86182198296167, "
                   "-180 28.86177263800117, -180 28.86175922384905, "
                   "-180 28.86165239704172, -180 28.86149088447868, "
                   "-180 28.86135465610515, -180 28.86133582415095, "
                   "-180 28.86118049530125, -180 28.86037359613003, "
                   "-180 28.85994914523384, -180 28.80581804559539, "
                   "-179.0254117042065 28.82396540232699, -179.2435796149245 "
                   "28.87359710319079, -179.2430548092013 28.87553905809875, "
                   "-179.2431117461943 28.87555210696329, -179.2431042081035 "
                   "28.87558000214502, -179.2432616114054 28.87561598611941, "
                   "-179.2429118700997 28.87690997130177, -179.4757171569616 "
                   "28.92847840039094, -179.4947763392047 28.93268856785107, "
                   "-179.4953826090487 28.93042364036135, -179.495640129408 "
                   "28.93047785137913, -179.4958976032855 28.92951710251109, "
                   "-179.7197759107133 28.97665152957523, -179.7189008661309 "
                   "28.9799434948634, -179.9711246134191 29.03057401142689, "
                   "-179.9714021451395 29.02951950260552, -179.9716112261731 "
                   "29.02955986208121, -179.9717934808075 29.02886735888065, "
                   "-179.9718527488075 29.0288788126164, -179.9720421969321 "
                   "29.0281585335533, -179.9723587419275 29.02821982865962, "
                   "-179.9723720061434 29.02816940680941, -179.9724134730059 "
                   "29.0281774310333, -179.9724833152255 29.02791186877477, "
                   "-179.9725614487616 29.02792699987426, -179.9726084221875 "
                   "29.02774848883664))")

        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_marcin_10_06_2024_10(self):
        """
        Issue reported 10/06/2024,
        regarding product footprint reported from
        https://datahub.creodias.eu/odata/v1
        "S2B_MSIL1C_20240101T183749_N0510_R141_T01CDN_20240101T195545.SAFE"
        """
        product = ("POLYGON ((-179.4659439421087 -79.16266030819288, -180 "
                   "-79.00627513455187, -180 -79.20560704191595, "
                   "-180 -79.20577500811633, -180 -79.2058573211517, "
                   "-180 -79.20601309051693, -180 -79.20619753454719, "
                   "-180 -79.20627015670875, -180 -79.20636618450428, "
                   "-180 -79.20638553333532, -180 -79.20661872315614, "
                   "-180 -79.20666765230693, -180 -79.20674674351788, "
                   "-180 -79.20688163422483, -180 -79.20695561042487, "
                   "-180 -79.22381700866191, -180 -79.223885625627, "
                   "-180 -79.22397372241886, -180 -79.22398771828203, "
                   "-180 -79.22409385588804, -180 -79.22414307640015, "
                   "-180 -79.22424054310756, -180 -79.22426808766679, "
                   "-180 -79.2243423088464, -180 -79.22435942662918, "
                   "-180 -79.22440118374973, -180 -79.2248432559935, "
                   "-180 -79.22490396784302, -180 -79.33237518158053, "
                   "-178.8989106382028 -79.34001609297415, "
                   "-179.5073846646551 -79.16744079084668, "
                   "-179.5046365996067 -79.16712591214419, "
                   "-179.5047238949631 -79.16710114155836, "
                   "-179.4659439421087 -79.16266030819288))")

        print(
            footprint_facility.to_wkt(
                footprint_facility.rework_to_polygon_geometry(
                    wkt.loads(product))))

    def test_24_07_2024_Linestring_two_coords(self):
        # Case Sentinel-1 WV_RAW_0A, WV_RAW_0C, WV_RAW_0N, WV_RAW_0S
        # -> The Linestring crosses the antimeridian returns a multilistring,
        # otherwise it returns same polygon
        count = 0
        for (dirpath, dirnames, filenames) in walk(
                'samples/jan-24.07.2024/SENTINEL-1'):
            for file in filenames:
                with open(os.path.join(dirpath, file), "r") as f:
                    _wkt = f.readline()
                count += 1

                geometry = wkt.loads(_wkt)
                rwrk = footprint_facility.rework_to_polygon_geometry(geometry)
                if not footprint_facility.check_cross_antimeridian(geometry):
                    self.assertEqual(rwrk, geometry)
                else:
                    self.assertIsInstance(rwrk,
                                          shapely.geometry.MultiLineString)
        print(f"Successfully checked {count} samples")

    def test_24_07_2024_Linestring_simplify(self):
        # Case Sentinel-1 contains only 2 points
        # The simplify call shall return same geometry.
        _wkt = "LINESTRING (-178.3024 -43.489, 172.2148 -62.4779)"
        rwrk = footprint_facility.rework_to_polygon_geometry(wkt.loads(_wkt))
        # Also here test set_precision over linestring
        self.assertEqual(footprint_facility.simplify(rwrk), rwrk)

    def test_24_07_2024_Linestring_two_coords_cross_antimeridian(self):
        # Case Sentinel-1 WV_RAW_0A, WV_RAW_0C, WV_RAW_0N, WV_RAW_0S
        # -> The Linestring crosses the antimeridian shall return
        # multilinestring.
        _wkt = "LINESTRING (-178.3024 -43.489, 172.2148 -62.4779)"
        rwrk = footprint_facility.rework_to_polygon_geometry(wkt.loads(_wkt))
        print(footprint_facility.to_wkt(rwrk))
        expected = ("MULTILINESTRING ((-180 -46.89999999999998, "
                    "-178.3 -43.5), (172.2 -62.5, 180 -46.89999999999998))")
        # Also here test set_precision over linestring
        self.assertEqual(footprint_facility.to_wkt(rwrk), expected)

    def test_24_07_2024_Linestring_two_coords_use_precision(self):
        # Case Sentinel-1 WV_RAW_0A, WV_RAW_0C, WV_RAW_0N, WV_RAW_0S
        # -> The Linestring crosses the antimeridian shall return
        # multilinestring.
        _wkt = "LINESTRING (-178.3024 -43.489, 172.2148 -62.4779)"
        rwrk = footprint_facility.rework_to_polygon_geometry(wkt.loads(_wkt))
        print(footprint_facility.to_wkt(rwrk))
        expected = ("MULTILINESTRING ("
                    "(-180 -46.9, -178.3 -43.5), "
                    "(172.2 -62.5, 180 -46.9))")
        # Also here test set_precision over linestring
        self.assertEqual(footprint_facility.to_wkt(
            shapely.set_precision(rwrk, 0.01)), expected)

    def test_24_07_2024_sentinel_2(self):
        # These S2 sample products has footprint exactly aligned on the
        # antimeridian that generate problem to compute intersection with it...
        # This issue shall be analysed.
        count = 0
        total = 0
        for (dirpath, dirnames, filenames) in walk(
                'samples/jan-24.07.2024/SENTINEL-2'):
            for file in filenames:
                path = os.path.join(dirpath, file)
                with open(path, "r") as f:
                    _wkt = f.readline()
                total += 1

                geometry = wkt.loads(_wkt)
                try:
                    rwrk = footprint_facility.rework_to_polygon_geometry(
                        geometry)
                except AlreadyReworkedPolygon as e:
                    print(f"{str(e)}: already rwrkd {path}")
                    continue
                except Exception as e:
                    print(f"{str(e)}: something wrong {path}")
                    continue

                count += 1

                if not footprint_facility.check_cross_antimeridian(geometry):
                    self.assertEqual(rwrk, geometry)
                else:
                    self.assertIsInstance(rwrk, shapely.geometry.MultiPolygon)
        print(f"Successfully checked {count}/{total} samples")

    def test_24_07_2024_sentinel_3(self):
        # These S3 seems to be already reworked.
        # An issue regarding the crossing antimeridian shall be fixed.
        count = 0
        total = 0
        for (dirpath, dirnames, filenames) in walk(
                'samples/jan-24.07.2024/SENTINEL-3'):
            for file in filenames:
                path = os.path.join(dirpath, file)
                with open(path, "r") as f:
                    try:
                        _wkt = f.readline()
                    except Exception as e:
                        print(f"{str(e)}: cannot read footprint file({path}).")
                        continue
                total += 1

                geometry = wkt.loads(_wkt)
                try:
                    rwrk = footprint_facility.rework_to_polygon_geometry(
                        geometry)
                except Exception as e:
                    '''
                    they are up to 77000 samples in error
                    print(f"`{str(e)}`: Problem handling footprint of {path}")
                    '''
                    continue
                count += 1
                if not footprint_facility.check_cross_antimeridian(geometry):
                    self.assertEqual(rwrk, geometry)
                else:
                    self.assertIsInstance(rwrk,
                                          shapely.geometry.MultiPolygon)
        print(f"Successfully checked {count}/{total} samples")

    def test_24_07_2024_sentinel_3_already_reworked_north_pole(self):
        _wkt = ("POLYGON ((-128.226 83.7901, -122.55 83.7642, -116.892"
                " 83.6781, -111.514 83.5353, -106.359 83.3365, -101.582"
                " 83.0902, -97.1308 82.7976, -93.044 82.4659, -89.3377"
                " 82.1005, -85.9486 81.7028, -82.8501 81.2809, -80.097"
                " 80.8392, -77.5688 80.3765, -75.2979 79.8955, -73.2257"
                " 79.4019, -71.3502 78.8948, -69.6196 78.3792, -68.0404"
                " 77.853, -66.5831 77.3153, -65.2563 76.7739, -51.4913"
                " 77.9735, -35.7645 78.3998, -35.7546 79.0266, -35.7509"
                " 79.6414, -35.7469 80.2601, -35.7536 80.8774, -35.7301"
                " 81.494, -35.7218 82.1125, -35.6982 82.7319, -35.7033 83.35,"
                " -35.6837 83.9708, -35.7015 84.5908, -35.6797 85.2102,"
                " -35.6513 85.8276, -35.633 86.4479, -35.5921 87.0638,"
                " -35.5279 87.6838, -35.4154 88.3056, -35.175 88.9212, -34.284"
                " 89.5393, 139.081 89.8402, 180 89.8023747, 180 90, -180 90,"
                " -180 89.8023747, -129.234 86.8954, -128.226 83.7901)))")
        with self.assertRaises(AlreadyReworkedPolygon):
            rwrk = footprint_facility.rework_to_polygon_geometry(
                wkt.loads(_wkt))
            print(rwrk)

    def test_24_07_2024_sentinel_6(self):
        # These S6 seems to be already reworked.
        # Issue regarding the computation of the intersection with antimeridian
        count = 0
        total = 0
        for (dirpath, dirnames, filenames) in walk(
                'samples/jan-24.07.2024/SENTINEL-6'):
            for file in filenames:
                with open(os.path.join(dirpath, file), "r") as f:
                    _wkt = f.readline()
                    total += 1

                    geometry = wkt.loads(_wkt)
                    try:
                        rwrk = footprint_facility.rework_to_polygon_geometry(
                            geometry)
                    except Exception as e:
                        continue
                    count += 1
                    if not footprint_facility.check_cross_antimeridian(
                            geometry):
                        self.assertEqual(rwrk, geometry)
                    else:
                        self.assertIsInstance(rwrk,
                                              shapely.geometry.MultiPolygon)
        print(f"Successfully checked {count}/{total} samples")

    def test__24_07_2024_sentinel_6_thin_malfocrossing(self):
        _wkt = ("POLYGON ((-140.176 29.9923, -144.644 20.4233, -148.486 "
                "10.7008, -152.037 0.906387, -155.565 -8.89357, -159.331 "
                "-18.6338, -163.652 -28.237, -168.977 -37.5936, -176.028 "
                "-46.5229, 173.982 -54.6891, 159.162 -61.4295, 137.886 "
                "-65.5398, 112.839 -65.6531, 91.2392 -61.7212, 76.1072 "
                "-55.0823, 65.9181 -46.9691, 58.7492 -38.0683, 53.354 "
                "-28.7273, 48.9931 -19.1323, 45.2061 -9.39557, 41.6723 "
                "0.404495, 38.1278 10.2023, 34.3064 19.9317, 29.8792 29.5123,"
                "24.3688 38.8276, 17.003 47.682, 6.47951 55.7076, -9.16948 "
                "62.1774, -31.2825 65.8134, -56.2909 65.3326, -56.2898 "
                "65.3308, -31.2815 65.8117, -9.17018 62.1757, 6.47782 55.7061,"
                "17.001 47.6808, 24.3669 38.8266, 29.8774 29.5115, 34.3046 "
                "19.931, 38.1261 10.2016, 41.6706 0.403881, 45.2044 -9.39617, "
                "48.9913 -19.1329, 53.3521 -28.7279, 58.7471 -38.069, 65.9158 "
                "-46.97, 76.1046 -55.0833, 91.2365 -61.7224, 112.836 -65.6546,"
                "137.885 -65.5416, 159.163 -61.4312, 173.984 -54.6906, "
                "-176.026 -46.5241, -168.976 -37.5946, -163.65 -28.2379, "
                "-159.329 -18.6346, -155.563 -8.89422, -152.036 0.905776, "
                "-148.485 10.7002, -144.642 20.4227, -140.174 29.9917, "
                "-140.176 29.9923))")
        geometry = wkt.loads(_wkt)
        rwrk = footprint_facility.rework_to_polygon_geometry(wkt.loads(_wkt))
        print(footprint_facility.to_geojson(rwrk))

    def test_24_07_2024_sentinel_6_crossing_antimeridian(self):
        _wkt = ("MULTIPOLYGON (((-180 86.263647169221, -149.52 85.52, -130.65"
                " 83.87, -120.25 81.86, -113.95 79.7, -109.76 77.47, -106.74"
                " 75.2, -104.45 72.9, -102.62 70.58, -101.11 68.26, -99.83"
                " 65.92, -98.72 63.58, -97.74 61.23, -96.85 58.88, -96.04"
                " 56.53, -95.3 54.17, -94.6 51.81, -93.94 49.45, -93.31 47.09,"
                " -92.71 44.72, -92.14 42.35, -91.58 39.98, -91.04 37.61,"
                " -90.51 35.23, -90 32.86, -89.49 30.48, -88.99 28.1, -88.49"
                " 25.73, -88 23.35, -87.51 20.96, -87.02 18.58, -86.53 16.2,"
                " -86.04 13.82, -85.55 11.44, -85.05 9.05, -84.55 6.67, -84.05"
                " 4.29, -83.54 1.91, -83.02 -0.47, -82.5 -2.85, -81.96 -5.23,"
                " -81.41 -7.61, -80.86 -9.98, -80.28 -12.36, -79.69 -14.73,"
                " -79.09 -17.1, -78.46 -19.46, -77.81 -21.83, -77.14 -24.19,"
                " -76.43 -26.54, -75.7 -28.89, -74.93 -31.24, -74.12 -33.58,"
                " -73.26 -35.91, -72.36 -38.24, -71.39 -40.56, -70.36 -42.87,"
                " -69.25 -45.16, -68.04 -47.45, -66.74 -49.72, -65.3 -51.98,"
                " -63.73 -54.22, -61.97 -56.44, -60.01 -58.63, -57.8 -60.78,"
                " -55.27 -62.9, -52.37 -64.96, -49.01 -66.97, -45.06 -68.89,"
                " -40.4 -70.7, -34.86 -72.38, -28.28 -73.88, -20.52 -75.14,"
                " -11.55 -76.11, -1.55 -76.71, 9.05 -76.89, 19.6 -76.65, 29.48"
                " -75.99, 38.29 -74.98, 45.88 -73.68, 51.56 -72.36, 52.04"
                " -72.23, 82.23 -77.8, 78.47 -79.75, 72.15 -81.89, 61.73"
                " -83.89, 42.86 -85.53, 10.86 -86.3, -22.61 -85.71, -43.14"
                " -84.15, -54.4 -82.18, -61.13 -80.05, -65.57 -77.83, -68.72"
                " -75.58, -71.11 -73.29, -72.99 -70.99, -74.54 -68.67, -75.85"
                " -66.35, -76.99 -64.02, -77.99 -61.69, -78.89 -59.35, -79.71"
                " -57, -80.47 -54.65, -81.17 -52.3, -81.84 -49.95, -82.47"
                " -47.59, -83.07 -45.24, -83.65 -42.87, -84.21 -40.51, -84.75"
                " -38.15, -85.28 -35.78, -85.8 -33.41, -86.31 -31.04, -86.81"
                " -28.67, -87.31 -26.29, -87.8 -23.92, -88.29 -21.54, -88.78"
                " -19.17, -89.27 -16.79, -89.76 -14.41, -90.25 -12.03, -90.74"
                " -9.65, -91.24 -7.27, -91.74 -4.88, -92.25 -2.5, -92.77"
                " -0.12, -93.29 2.26, -93.82 4.64, -94.37 7.02, -94.92 9.4,"
                " -95.49 11.77, -96.08 14.15, -96.68 16.52, -97.3 18.89,"
                " -97.95 21.26, -98.62 23.62, -99.31 25.98, -100.04 28.34,"
                " -100.8 30.69, -101.61 33.04, -102.45 35.38, -103.35 37.72,"
                " -104.3 40.04, -105.32 42.36, -106.42 44.67, -107.61 46.97,"
                " -108.89 49.25, -110.3 51.52, -111.86 53.77, -113.58 56,"
                " -115.5 58.21, -117.67 60.38, -120.14 62.51, -122.98 64.6,"
                " -126.27 66.62, -130.12 68.57, -134.67 70.41, -140.08 72.12,"
                " -146.51 73.66, -154.11 74.97, -162.94 75.98, -172.86 76.64,"
                " -180 76.809034090909, -180 86.263647169221)), "
                "((180 76.809034090909, 176.58 76.89, 178.51 86.3,"
                " 180 86.263647169221, 180 76.809034090909)))")
        rwrk = footprint_facility.rework_to_polygon_geometry(wkt.loads(_wkt))
        print(footprint_facility.to_wkt(rwrk))

        # Also here test set_precision over linestring
        self.assertEqual(footprint_facility.to_wkt(rwrk), _wkt)

    def test_24_07_2024_smos_crossing_antimeridian(self,):
        _wkt = ("MULTIPOLYGON (((-180 39.091237574483, -174.883 30.781,"
                " -170.343 21.2287, -166.461 11.5148, -162.896 1.72291,"
                " -159.375 -8.07972, -155.639 -17.8282, -151.378 -27.4468,"
                " -146.157 -36.8296, -139.285 -45.8041, -129.602 -54.0525,"
                " -115.264 -60.9482, -94.5159 -65.3338, -69.5194 -65.8074,"
                " -47.426 -62.1691, -31.7898 -55.7011, -21.2723 -47.6791,"
                " -13.9088 -38.8286, -8.3994 -29.517, -3.97256 -19.9395,"
                " -0.151216 -10.2125, 3.39329 -0.416293, 6.92709 9.38308,"
                " 10.714 19.1201, 15.0749 28.7161, 15.0768 28.7154, 10.7158"
                " 19.1194, 6.92881 9.38248, 3.39497 -0.416908, -0.149515"
                " -10.2132, -3.97081 -19.9403, -8.39757 -29.5178, -13.9069"
                " -38.8296, -21.2703 -47.6804, -31.7881 -55.7027, -47.4253"
                " -62.1708, -69.5205 -65.8091, -94.5183 -65.3353, -115.267"
                " -60.9494, -129.604 -54.0535, -139.288 -45.805, -146.159"
                " -36.8303, -151.38 -27.4475, -155.641 -17.8289, -159.377"
                " -8.08033, -162.897 1.72229, -166.463 11.5141, -170.345"
                " 21.228, -174.885 30.7802, -180 39.08701019979, -180"
                " 39.091237574483)), ((180 39.08701019979, 179.409 40.0468,"
                " 171.709 48.8162, 160.624 56.6854, 144.132 62.8604, 121.27"
                " 66.0003, 96.462 64.9398, 76.5963 60.1221, 63.0174 52.9838,"
                " 53.8089 44.6051, 53.8068 44.606, 63.0149 52.9847, 76.5936"
                " 60.1232, 96.4594 64.9412, 121.269 66.002, 144.132 62.8622,"
                " 160.625 56.6869, 171.711 48.8174, 179.411 40.0478, 180"
                " 39.091237574483, 180 39.08701019979)))")

        print(_wkt)
        rwrk = footprint_facility.rework_to_polygon_geometry(wkt.loads(_wkt))
        print(footprint_facility.to_wkt(rwrk))

        # Also here test set_precision over linestring
        self.assertEqual(footprint_facility.to_wkt(rwrk), _wkt)

    def test_handle_rework_exceptions(self):
        _wkt = ("POLYGON ((34.8393 42, 180 43, 180 90, -180 90, "
                "-180 43, -178.089 41, 34.8393 42))")
        geometry = wkt.loads(_wkt)
        import logging
        logging.basicConfig(level=logging.INFO)

        footprint_facility.check_time(True, True, True)
        with self.assertRaises(AlreadyReworkedPolygon):
            rwrk = footprint_facility.rework_to_polygon_geometry(geometry)

        footprint_facility.set_raise_exception(False)
        rwrk = footprint_facility.rework_to_polygon_geometry(geometry)
        print(footprint_facility.to_geojson(rwrk))
        footprint_facility.set_raise_exception(True)

        footprint_facility.show_summary()
