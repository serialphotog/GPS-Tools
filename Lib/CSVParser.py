import csv
import os

from Lib.GPSPoint import GPSPoint
from typing import Dict, Tuple

class CSVParser:

    def __init__(self, 
                 csv_path: str, 
                 column_mapping: Dict = None, 
                 skip_first: bool = False,
                 verbose: bool = False):
        """
        Initializes the CSV parser with the path to the CSV file to parse.

        :param csv_path: The path to the CSV file to parse.
        :param column_mapping: A dictionary defining the mapping of GPS Point
                               fields to a CSV column number. Defaults to None.
        :param skip_first: If True, will skip the first row of the CSV file when
                           parsing.
        :param verbose: If True, verbose output will be enabled.

        :throws: ValueError if the supplied CSV file does not exist.
        """
        if not os.path.isfile(csv_path):
            raise ValueError(f'Could not find {csv_path}')
        
        self.csv_path = csv_path
        self.column_mapping = column_mapping
        self.skip_first_row = skip_first
        self.verbose = verbose
        self.gps_points = []
        
    def parse(self) -> Tuple[int, int]:
        """
        Processes the CSV file, extracting the valid GPS points.

        :returns: A tuple containing the total process rows and the rows
                  containing errors, respectively.
        """
        print(f'Parsing {self.csv_path}')

        with open(self.csv_path, 'r') as csv_file:
            reader = csv.reader(csv_file)

            # Skip the first row, if specified
            if self.skip_first_row:
                if self.verbose:
                    print(f'Skipping the first row of {self.csv_path}')
                next(reader, None)

            total_rows = 0
            errors = 0
            for row in reader:
                # Filter for non-empty rows
                if any(row):
                    total_rows += 1

                    if not self._process_row(row):
                        errors += 1

        return (total_rows, errors)
    
    def _process_row(self, row) -> bool:
        """
        Parses an individual row of the CSV file, adding valid entries to the 
        list of GPS points.

        :param row: The row to parse.

        :returns: True if the row was valid and successfully parsed, else False.
        """
        if not self.column_mapping:
            # Use the default column mapping
            lat_col = 0
            lon_col = 1
            name_col = 2
            desc_col = 3
        else:
            # Use the passed in column mapping
            lat_col = self.column_mapping['lat']
            lon_col = self.column_mapping['lon']
            name_col = self.column_mapping['name']
            desc_col = self.column_mapping['desc']

        # Check the coordinates
        lat = row[lat_col]
        lon = row[lon_col]
        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            if self.verbose:
                print(f'Invalid coordinates encountered: {lat}, {lon}. Skipping entry.')
            return False
        
        # Parse the name and description if they're not skipped
        if not name_col == 'skip':
            name = row[name_col]
        else:
            name = None
        
        if not desc_col == 'skip':
            desc = row[desc_col]
        else:
            desc = None
        
        # Build the GPS Point object
        point = GPSPoint(
            name=name,
            description=desc,
            latitude=lat,
            longitude=lon
        )
        self.gps_points.append(point)

        return True
    
    def get_gps_points(self):
        """
        :returns: The stored GPS points from this parser.
        """
        return self.gps_points