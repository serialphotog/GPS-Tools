import tempfile
import unittest
from pathlib import Path

from gps_tools.GPXParser import GPXParser


class GPXParserTests(unittest.TestCase):

    def test_parses_namespaced_waypoints(self):
        gpx = (
            '<gpx xmlns="http://www.topografix.com/GPX/1/1">'
            '<wpt lat="40.1" lon="-105.2">'
            '<name>Peak</name><desc>Trail</desc>'
            '</wpt></gpx>'
        )

        points = self._parse_points(gpx)

        self.assertEqual(len(points), 1)
        self.assertEqual(points[0].latitude, 40.1)
        self.assertEqual(points[0].longitude, -105.2)
        self.assertEqual(points[0].name, 'Peak')
        self.assertEqual(points[0].description, 'Trail')

    def test_parses_non_namespaced_waypoints(self):
        gpx = (
            '<gpx><wpt lat="40.1" lon="-105.2">'
            '<name>Peak</name><desc>Trail</desc>'
            '</wpt></gpx>'
        )

        points = self._parse_points(gpx)

        self.assertEqual(len(points), 1)
        self.assertEqual(points[0].name, 'Peak')

    def test_skips_waypoints_with_missing_coordinates(self):
        gpx = '<gpx><wpt><name>Peak</name></wpt></gpx>'

        with tempfile.TemporaryDirectory() as tmp:
            gpx_path = Path(tmp) / 'points.gpx'
            gpx_path.write_text(gpx, encoding='utf-8')

            parser = GPXParser(str(gpx_path))
            total, errors = parser.parse()

        self.assertEqual(total, 1)
        self.assertEqual(errors, 1)
        self.assertEqual(parser.get_gps_points(), [])

    def test_skips_invalid_waypoints_and_keeps_valid_ones(self):
        gpx = (
            '<gpx>'
            '<wpt lat="north" lon="-105.2"><name>Bad</name></wpt>'
            '<wpt lat="40.1" lon="-105.2"><name>Peak</name></wpt>'
            '</gpx>'
        )

        with tempfile.TemporaryDirectory() as tmp:
            gpx_path = Path(tmp) / 'points.gpx'
            gpx_path.write_text(gpx, encoding='utf-8')

            parser = GPXParser(str(gpx_path))
            total, errors = parser.parse()

        points = parser.get_gps_points()
        self.assertEqual(total, 2)
        self.assertEqual(errors, 1)
        self.assertEqual(len(points), 1)
        self.assertEqual(points[0].name, 'Peak')

    def _parse_points(self, gpx):
        with tempfile.TemporaryDirectory() as tmp:
            gpx_path = Path(tmp) / 'points.gpx'
            gpx_path.write_text(gpx, encoding='utf-8')

            parser = GPXParser(str(gpx_path))
            total, errors = parser.parse()

        self.assertEqual(total, 1)
        self.assertEqual(errors, 0)
        return parser.get_gps_points()


if __name__ == '__main__':
    unittest.main()
