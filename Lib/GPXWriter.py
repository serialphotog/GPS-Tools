import xml.etree.ElementTree as ET

from typing import Dict

# Various constant values for generating GPX files
GPX_ROOT_ELEM: str = 'gpx'
GPX_HEADER_VALUES: Dict[str, str] = {
    'xmlns': 'http://www.topografix.com/GPX/1/1',
    'xmlns:gpxx': 'http://www.garmin.com/xmlschemas/GpxExtensions/v3',
    'CREATOR': 'AdamThompsonPhoto.com',
}
GPX_WAYPOINT: str = 'wpt'
GPX_WAYPOINT_NAME: str = "name"
GPX_WAYPOINT_DESC: str = "desc"

class GPXWriter:

    def __init__(self, 
                 gps_points,
                 output_path: str,
                 verbose: bool = False):
        """
        Initializes the GPX writer.

        :param gps_points: The list of GPS points to add to the generated GPX
                           file.
        :param output_path: The output path for the generated GPX file.
        :param verbose: If True, enables verbose output.
        """
        self.gps_points = gps_points
        self.output_path = output_path
        self.verbose = verbose

    def generate(self) -> int:
        """
        Generates an output GPX file.

        :returns: The total number of waypoints added to the output GPX file.
        """
        print(f'Generating {self.output_path}')

        # Build the GPX file header
        gpx_head = ET.Element(GPX_ROOT_ELEM)
        for key, value in GPX_HEADER_VALUES.items():
            gpx_head.set(key, value)

        # Generate each waypoint entry
        total = 0
        for point in self.gps_points:
            total += 1
            self._build_waypoint(gpx_head, point)

        # Write the GPX file to disk
        xml = ET.tostring(gpx_head)
        with open(self.output_path, 'wb') as f:
            f.write(xml)

        return total
    
    def _build_waypoint(self, parent, point):
        """
        Builds the waypoint element for an individual GPS point.

        :param parent: The parent XML element to add the waypoint to.
        :param point: The GPS point to build the waypoint entry for.
        """
        waypoint_elem = ET.SubElement(parent, GPX_WAYPOINT)
        waypoint_elem.set('lat', str(point.latitude))
        waypoint_elem.set('lon', str(point.longitude))

        # Add the name
        if point.name:
            name_elem = ET.SubElement(waypoint_elem, GPX_WAYPOINT_NAME)
            name_elem.text = point.name

        # Add the description
        if point.description:
            desc_elem = ET.SubElement(waypoint_elem, GPX_WAYPOINT_DESC)
            desc_elem.text = point.description