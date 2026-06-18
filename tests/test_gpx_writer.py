import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from gps_tools.GPSPoint import GPSPoint
from gps_tools.GPXWriter import GPXWriter


class GPXWriterTests(unittest.TestCase):

    def test_writes_standard_gpx_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / 'points.gpx'
            writer = GPXWriter(
                [GPSPoint('Peak', 40.1, -105.2, 'Trail')],
                str(output_path)
            )

            total = writer.generate()
            contents = output_path.read_text(encoding='utf-8')
            root = ET.parse(output_path).getroot()

        self.assertEqual(total, 1)
        self.assertTrue(contents.startswith('<?xml'))
        self.assertEqual(root.attrib['version'], '1.1')
        self.assertEqual(root.attrib['creator'], 'AdamThompsonPhoto.com')
        self.assertNotIn('CREATOR', root.attrib)

    def test_generated_gpx_can_be_parsed_as_namespaced_waypoint(self):
        namespace = {'gpx': 'http://www.topografix.com/GPX/1/1'}

        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / 'points.gpx'
            writer = GPXWriter(
                [GPSPoint('Peak', 40.1, -105.2, 'Trail')],
                str(output_path)
            )

            writer.generate()
            root = ET.parse(output_path).getroot()
            waypoint = root.find('gpx:wpt', namespace)

        self.assertIsNotNone(waypoint)
        self.assertEqual(waypoint.attrib['lat'], '40.1')
        self.assertEqual(waypoint.attrib['lon'], '-105.2')
        self.assertEqual(waypoint.find('gpx:name', namespace).text, 'Peak')
        self.assertEqual(waypoint.find('gpx:desc', namespace).text, 'Trail')


if __name__ == '__main__':
    unittest.main()
