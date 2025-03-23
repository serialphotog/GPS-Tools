import os
import xml.etree.ElementTree as ET

from Lib.GPSPoint import GPSPoint
from typing import Dict

# The GPX namespace value
NAMESPACE: str = 'http://www.topografix.com/GPX/1/1'
GPX_NAMESPACE: Dict[str, str] = {
    "gpx": NAMESPACE
}

# Used for GPX child matching
CHILD_MATCHER: str = "{" + NAMESPACE + "}"

# Various GPX values
GPX_WAYPOINT_LAT: str = "lat"
GPX_WAYPOINT_LON: str = "lon"
GPX_WAYPOINT_DESC: str = "desc"
GPX_WAYPOINT_NAME: str = "name"
GPX_WAYPOINT: str = "gpx:wpt"

class GPXParser:

    def __init__(self, 
                 gpx_path: str):
        """
        Initializes the GPX parser with the path to the GPX file to parse.

        :param gpx_path: The path to the GPX file to parse.

        :throws: ValueError if the supplied CSV file does not exist.
        """
        if not os.path.isfile(gpx_path):
            raise ValueError(f'Could not find {gpx_path}')
        
        self.gpx_path = gpx_path
        self.gps_points = []

    def parse(self) -> int:
        """
        Processes the GPX file, extracting the valid GPS points.

        :returns: The total number of GPS points loaded from the GPX file.
        """
        print(f'Parsing {self.gpx_path}')

        # Start parsing the GPX file
        gpx_tree = ET.parse(self.gpx_path)
        root_elem = gpx_tree.getroot()

        # Iterate over all of the waypoints
        total = 0
        for waypoint in root_elem.findall(GPX_WAYPOINT, GPX_NAMESPACE):
            total += 1
            self._parse_waypoint(waypoint)

        return total
    
    def _parse_waypoint(self, waypoint):
        """
        Parses a single waypoint from the GPX file and builds the associated 
        GPS Point, appending it to the internal list of GPS points.

        :param waypoint: The waypoint to parse.
        """
        # Extract the coordinates from the waypoint
        latitude = waypoint.attrib[GPX_WAYPOINT_LAT]
        longitude = waypoint.attrib[GPX_WAYPOINT_LON]

        # Parse the children
        name = None
        description = None
        for child in waypoint:
            if child.tag == f'{CHILD_MATCHER}{GPX_WAYPOINT_NAME}':
                name = child.text
            if child.tag == f'{CHILD_MATCHER}{GPX_WAYPOINT_DESC}':
                description = child.text
        
        gps_point = GPSPoint(
            name=name,
            description=description,
            latitude=latitude,
            longitude=longitude
        )
        self.gps_points.append(gps_point)

    def get_gps_points(self):
        """
        :returns: The stored GPS points from this parser
        """
        return self.gps_points