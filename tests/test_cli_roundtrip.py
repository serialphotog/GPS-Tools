import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CLIRoundTripTests(unittest.TestCase):

    def test_csv_to_gpx_to_csv_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_csv = tmp_path / 'input.csv'
            output_gpx = tmp_path / 'output.gpx'
            output_csv = tmp_path / 'output.csv'
            input_csv.write_text(
                'lat,lon,name,desc\n40.1,-105.2,Peak,Trail\n',
                encoding='utf-8'
            )

            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / 'csv2gpx'),
                    '-i',
                    str(input_csv),
                    '-o',
                    str(output_gpx),
                    '-s',
                ],
                check=True,
                cwd=ROOT
            )
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / 'gpx2csv'),
                    '-i',
                    str(output_gpx),
                    '-o',
                    str(output_csv),
                ],
                check=True,
                cwd=ROOT
            )

            with output_csv.open(newline='', encoding='utf-8') as csv_file:
                rows = list(csv.reader(csv_file))

        self.assertEqual(rows, [['40.1', '-105.2', 'Peak', 'Trail']])


if __name__ == '__main__':
    unittest.main()
