import csv
import tempfile
import unittest
from pathlib import Path

from Lib.CSVParser import CSVParser
from Lib.CSVWriter import CSVWriter
from Lib.GPSPoint import GPSPoint


class CSVParserTests(unittest.TestCase):

    def test_parses_default_mapping_and_skips_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / 'points.csv'
            csv_path.write_text(
                'lat,lon,name,desc\n40.1,-105.2,Peak,Trail\n',
                encoding='utf-8'
            )

            parser = CSVParser(str(csv_path), skip_first=True)
            total, errors = parser.parse()

        points = parser.get_gps_points()
        self.assertEqual(total, 1)
        self.assertEqual(errors, 0)
        self.assertEqual(len(points), 1)
        self.assertEqual(points[0].latitude, 40.1)
        self.assertEqual(points[0].longitude, -105.2)
        self.assertEqual(points[0].name, 'Peak')
        self.assertEqual(points[0].description, 'Trail')

    def test_counts_short_rows_as_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / 'points.csv'
            csv_path.write_text('40.1,-105.2\n', encoding='utf-8')

            parser = CSVParser(str(csv_path))
            total, errors = parser.parse()

        self.assertEqual(total, 1)
        self.assertEqual(errors, 1)
        self.assertEqual(parser.get_gps_points(), [])

    def test_supports_custom_mapping_with_skipped_description(self):
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / 'points.csv'
            csv_path.write_text('Peak,40.1,-105.2\n', encoding='utf-8')
            mapping = {'lat': 1, 'lon': 2, 'name': 0, 'desc': 'skip'}

            parser = CSVParser(str(csv_path), column_mapping=mapping)
            total, errors = parser.parse()

        points = parser.get_gps_points()
        self.assertEqual(total, 1)
        self.assertEqual(errors, 0)
        self.assertEqual(points[0].description, None)


class CSVWriterTests(unittest.TestCase):

    def test_writes_default_mapping(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / 'points.csv'
            writer = CSVWriter(
                [GPSPoint('Peak', 40.1, -105.2, 'Trail')],
                str(output_path)
            )

            total = writer.generate()

            with output_path.open(newline='', encoding='utf-8') as csv_file:
                rows = list(csv.reader(csv_file))

        self.assertEqual(total, 1)
        self.assertEqual(rows, [['40.1', '-105.2', 'Peak', 'Trail']])

    def test_writes_sparse_row_when_description_is_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / 'points.csv'
            mapping = {'lat': 2, 'lon': 3, 'name': 0, 'desc': 'skip'}
            writer = CSVWriter(
                [GPSPoint('Peak', 40.1, -105.2, 'Trail')],
                str(output_path),
                column_mapping=mapping
            )

            total = writer.generate()

            with output_path.open(newline='', encoding='utf-8') as csv_file:
                rows = list(csv.reader(csv_file))

        self.assertEqual(total, 1)
        self.assertEqual(rows, [['Peak', '', '40.1', '-105.2']])


if __name__ == '__main__':
    unittest.main()
