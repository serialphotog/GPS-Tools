import argparse
import os

from gps_tools.CommandLine import prompt_user_for_yes_or_no
from gps_tools.CSVParser import CSVParser
from gps_tools.CSVTools import process_column_mapping
from gps_tools.CSVWriter import CSVWriter
from gps_tools.GPXParser import GPXParser
from gps_tools.GPXWriter import GPXWriter


def _validate_csv2gpx_args(args) -> bool:
    """
    Validates csv2gpx command line arguments.

    :param args: The command line arguments to validate.

    :returns: True if the arguments are valid, else False.
    """
    if not os.path.isfile(args.csv_path):
        print(f'Could not find the input CSV: {args.csv_path}')
        return False

    if os.path.isfile(args.gpx_path) and not args.force:
        try:
            overwrite = prompt_user_for_yes_or_no(f'Output GPX {args.gpx_path} '
                                                  'already exists. Overwrite it?',
                                                  'no')
        except EOFError:
            print(f'Output file exists. Use --force to overwrite {args.gpx_path}.')
            return False
        if not overwrite:
            print(f'Output file exists. Aborting.')
            return False

    return True


def csv2gpx_main() -> int:
    parser = argparse.ArgumentParser(description="A simple utility to convert CSV files to GPX files.")
    parser.add_argument('--input', '-i', dest="csv_path", required=True, help="Path to the input CSV file.")
    parser.add_argument('--output', '-o', dest="gpx_path", required=True, help="Path to write the resulting GPX file to.")
    parser.add_argument('--format', '-f', dest="column_mapping", help="The column mapping to use when parsing the CSV file.")
    parser.add_argument('--skip', '-s', dest="skip_first", action="store_true", help="Skips the first row of the CSV file.")
    parser.add_argument('--verbose', '-v', dest="verbose", action="store_true", help="Enable verbose output.")
    parser.add_argument('--force', dest="force", action="store_true", help="Overwrite the output file if it already exists.")
    args = parser.parse_args()

    if not _validate_csv2gpx_args(args=args):
        return 1

    if args.column_mapping:
        try:
            column_mapping = process_column_mapping(args.column_mapping)
        except ValueError as e:
            print(e)
            return 1
    else:
        column_mapping = None

    csv_parser = CSVParser(csv_path=args.csv_path,
                           column_mapping=column_mapping,
                           skip_first=args.skip_first,
                           verbose=args.verbose)
    total, errors = csv_parser.parse()
    print(f'Successfully read {total} rows. {errors} rows had errors and were skipped.')

    gpx_writer = GPXWriter(gps_points=csv_parser.get_gps_points(),
                           output_path=args.gpx_path,
                           verbose=args.verbose)
    total_waypoints = gpx_writer.generate()
    print(f'Successfully generated GPX file with {total_waypoints} waypoints.')
    return 0


def _validate_gpx2csv_args(args) -> bool:
    """
    Validates gpx2csv command line arguments.

    :param args: The command line arguments to validate.

    :returns: True if the arguments are valid, else False.
    """
    if not os.path.isfile(args.gpx_path):
        print(f'Could not find the input GPX: {args.gpx_path}')
        return False

    if os.path.isfile(args.csv_path) and not args.force:
        try:
            overwrite = prompt_user_for_yes_or_no(f'Output CSV {args.csv_path} '
                                                  'already exists. Overwrite it?',
                                                  'no')
        except EOFError:
            print(f'Output file exists. Use --force to overwrite {args.csv_path}.')
            return False
        if not overwrite:
            print(f'Output file exists. Aborting.')
            return False

    return True


def gpx2csv_main() -> int:
    parser = argparse.ArgumentParser(description="A simple utility to convert GPX files to CSV files.")
    parser.add_argument('--input', '-i', dest="gpx_path", required=True, help="Path to the input GPX file.")
    parser.add_argument('--output', '-o', dest="csv_path", required=True, help="Path to write the resulting CSV file to.")
    parser.add_argument('--format', '-f', dest="column_mapping", help="The column mapping to use in the resulting CSV file.")
    parser.add_argument('--force', dest="force", action="store_true", help="Overwrite the output file if it already exists.")
    args = parser.parse_args()

    if not _validate_gpx2csv_args(args=args):
        return 1

    if args.column_mapping:
        try:
            column_mapping = process_column_mapping(args.column_mapping)
        except ValueError as e:
            print(e)
            return 1
    else:
        column_mapping = None

    gpx_parser = GPXParser(gpx_path=args.gpx_path)
    total = gpx_parser.parse()
    print(f'Successfully parsed {total} waypoints.')

    csv_writer = CSVWriter(gps_points=gpx_parser.get_gps_points(),
                           output_path=args.csv_path,
                           column_mapping=column_mapping)
    total = csv_writer.generate()
    print(f'Successfully generated CSV file with {total} waypoints.')
    return 0
