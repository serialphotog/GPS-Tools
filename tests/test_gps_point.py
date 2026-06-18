import unittest

from gps_tools.GPSPoint import GPSPoint


class GPSPointTests(unittest.TestCase):

    def test_points_compare_by_value(self):
        self.assertEqual(
            GPSPoint('Peak', 40.1, -105.2, 'Trail'),
            GPSPoint('Peak', 40.1, -105.2, 'Trail')
        )


if __name__ == '__main__':
    unittest.main()
