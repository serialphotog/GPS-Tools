import csv

from pathlib import Path
from typing import Dict

# The size the pre-populated CSV row needs to be
CSV_ROW_SIZE: int = 4

class CSVWriter:

    def __init__(self, 
                 gps_points: Dict, 
                 output_path: str,
                 column_mapping: Dict = None):
        """
        Initializes the CSV writer.

        :param gps_points: The list of GPS points to add to the generated CSV
                           files.
        :param output_path: The output path for the generated CSV file.
        :param column_mapping: The mapping of GPS Point items to CSV column
                               numbers.
        """
        self.gps_points = gps_points
        self.output_path = output_path
        self.column_mapping = column_mapping

    def generate(self) -> int:
        """
        Generates an output CSV file.

        :returns: The total number of waypoints added to the CSV file.
        """
        out_path = Path(self.output_path)

        with out_path.open("w", newline="", encoding="utf-8") as csv_file:
            csvwriter = csv.writer(csv_file)
            total = 0
            for point in self.gps_points:
                # Build the row to write in the correct order
                row = self._build_csv_row(point=point)

                csvwriter.writerow(row)
                total += 1

        return total
    
    def _build_csv_row(self, point):
        """
        BUilds the CSV row element with each GPS waypoint element in the
        correct order.

        :param point: The GPS point to use to populate the row
        """
        if not self.column_mapping:
            lat_col = 0
            lon_col = 1
            name_col = 2
            desc_col = 3
        else:
            lat_col = self.column_mapping['lat']
            lon_col = self.column_mapping['lon']
            name_col = self.column_mapping['name']
            desc_col = self.column_mapping['desc']

        # Determine how many elements the row will have
        row_size = CSV_ROW_SIZE
        if name_col == 'skip':
            row_size -= 1
        if desc_col == 'skip':
            row_size -= 1
        row = [None] * row_size

        row[lat_col] = point.latitude
        row[lon_col] = point.longitude

        if not name_col == 'skip':
            row[name_col] = point.name

        if not desc_col == 'skip':
            row[desc_col] = point.description

        return row