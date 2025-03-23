from typing import Dict

def process_column_mapping(column_mapping_string) -> Dict:
    """
    Processes the column mapping format string supplied as a command line 
    argument.

    :param column_mapping_string: The column mapping to use when parsing the
                                  CSV file.

    :returns: A dictionary containing the mapping of GPS point components to
              column numbers.

    :throws: ValueError if an invalid format string is encountered.
    """
    # Storage for the final mapping
    column_mapping = {}

    # Valid mapping components
    valid_components = ['lat', 'lon', 'name', 'desc']

    # Parse each part of the format string
    format_parts = column_mapping_string.split(',')

    # Ensure that we have the expected number of entries in the mapping
    if not len(format_parts) == 4:
        raise ValueError('Invalid column mapping format string encountered.')

    for part in format_parts:
        components = part.split(':')

        # Each component should consist of a 1:1 mapping
        if len(components) != 2:
            raise ValueError('Invalid column mapping provided.')
        
        # Ensure that we have a valid mapping
        component = components[0]
        value = components[1]
        if not component in valid_components:
            raise ValueError(f'Invalid entry found in column mapping: {component}')
        
        if not value == 'skip':
            # Ensure that this component maps to an integer
            try:
                value = int(value)
            except ValueError as e:
                raise ValueError(e)
        else:
            if component == 'lat' or component == 'lon':
                raise ValueError('You cannot skp the lat or lon values')
        
        # Add the parsed mapping to the column mappings
        column_mapping[component] = value

    return column_mapping