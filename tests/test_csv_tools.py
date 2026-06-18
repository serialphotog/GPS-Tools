import unittest

from Lib.CSVTools import process_column_mapping


class ProcessColumnMappingTests(unittest.TestCase):

    def test_processes_valid_mapping(self):
        mapping = process_column_mapping('lat:2,lon:3,name:0,desc:skip')

        self.assertEqual(
            mapping,
            {'lat': 2, 'lon': 3, 'name': 0, 'desc': 'skip'}
        )

    def test_trims_whitespace(self):
        mapping = process_column_mapping(' lat:2, lon:3, name:0, desc:skip ')

        self.assertEqual(mapping['lat'], 2)
        self.assertEqual(mapping['lon'], 3)
        self.assertEqual(mapping['name'], 0)
        self.assertEqual(mapping['desc'], 'skip')

    def test_rejects_duplicate_components(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate entry'):
            process_column_mapping('lat:0,lat:1,name:2,desc:3')

    def test_rejects_duplicate_column_indexes(self):
        with self.assertRaisesRegex(ValueError, 'mapped to both'):
            process_column_mapping('lat:0,lon:0,name:2,desc:3')

    def test_rejects_negative_column_indexes(self):
        with self.assertRaisesRegex(ValueError, 'cannot be negative'):
            process_column_mapping('lat:-1,lon:1,name:2,desc:3')

    def test_rejects_skipped_coordinates(self):
        with self.assertRaisesRegex(ValueError, 'cannot skip'):
            process_column_mapping('lat:skip,lon:1,name:2,desc:3')

    def test_rejects_missing_components(self):
        with self.assertRaisesRegex(ValueError, 'Invalid column mapping format'):
            process_column_mapping('lat:0,lon:1,name:2')


if __name__ == '__main__':
    unittest.main()
