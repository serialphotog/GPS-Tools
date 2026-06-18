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

    def test_csv2gpx_requires_input_and_output_args(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / 'csv2gpx')],
            capture_output=True,
            text=True,
            cwd=ROOT
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn('required', result.stderr)

    def test_csv2gpx_refuses_existing_output_without_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_csv = tmp_path / 'input.csv'
            output_gpx = tmp_path / 'output.gpx'
            input_csv.write_text('40.1,-105.2,Peak,Trail\n', encoding='utf-8')
            output_gpx.write_text('keep me\n', encoding='utf-8')

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / 'csv2gpx'),
                    '-i',
                    str(input_csv),
                    '-o',
                    str(output_gpx),
                ],
                input='n\n',
                capture_output=True,
                text=True,
                cwd=ROOT
            )

            contents = output_gpx.read_text(encoding='utf-8')

        self.assertEqual(result.returncode, 1)
        self.assertIn('Output file exists. Aborting.', result.stdout)
        self.assertEqual(contents, 'keep me\n')

    def test_csv2gpx_force_overwrites_existing_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_csv = tmp_path / 'input.csv'
            output_gpx = tmp_path / 'output.gpx'
            input_csv.write_text('40.1,-105.2,Peak,Trail\n', encoding='utf-8')
            output_gpx.write_text('replace me\n', encoding='utf-8')

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / 'csv2gpx'),
                    '-i',
                    str(input_csv),
                    '-o',
                    str(output_gpx),
                    '--force',
                ],
                capture_output=True,
                text=True,
                cwd=ROOT
            )

            contents = output_gpx.read_text(encoding='utf-8')

        self.assertEqual(result.returncode, 0)
        self.assertIn('<gpx', contents)
        self.assertNotIn('replace me', contents)

    def test_gpx2csv_refuses_existing_output_without_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_gpx = tmp_path / 'input.gpx'
            output_csv = tmp_path / 'output.csv'
            input_gpx.write_text(
                '<gpx><wpt lat="40.1" lon="-105.2">'
                '<name>Peak</name><desc>Trail</desc>'
                '</wpt></gpx>',
                encoding='utf-8'
            )
            output_csv.write_text('keep me\n', encoding='utf-8')

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / 'gpx2csv'),
                    '-i',
                    str(input_gpx),
                    '-o',
                    str(output_csv),
                ],
                input='n\n',
                capture_output=True,
                text=True,
                cwd=ROOT
            )

            contents = output_csv.read_text(encoding='utf-8')

        self.assertEqual(result.returncode, 1)
        self.assertIn('Output file exists. Aborting.', result.stdout)
        self.assertEqual(contents, 'keep me\n')

    def test_gpx2csv_force_overwrites_existing_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_gpx = tmp_path / 'input.gpx'
            output_csv = tmp_path / 'output.csv'
            input_gpx.write_text(
                '<gpx><wpt lat="40.1" lon="-105.2">'
                '<name>Peak</name><desc>Trail</desc>'
                '</wpt></gpx>',
                encoding='utf-8'
            )
            output_csv.write_text('replace me\n', encoding='utf-8')

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / 'gpx2csv'),
                    '-i',
                    str(input_gpx),
                    '-o',
                    str(output_csv),
                    '--force',
                ],
                capture_output=True,
                text=True,
                cwd=ROOT
            )

            with output_csv.open(newline='', encoding='utf-8') as csv_file:
                rows = list(csv.reader(csv_file))

        self.assertEqual(result.returncode, 0)
        self.assertEqual(rows, [['40.1', '-105.2', 'Peak', 'Trail']])


if __name__ == '__main__':
    unittest.main()
