from typing import Dict

SKIP_VALUE: str = 'skip'
VALID_COMPONENTS = {'lat', 'lon', 'name', 'desc'}
REQUIRED_COMPONENTS = {'lat', 'lon', 'name', 'desc'}

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
    column_mapping = {}

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
        component = components[0].strip()
        value = components[1].strip()
        if not component in VALID_COMPONENTS:
            raise ValueError(f'Invalid entry found in column mapping: {component}')
        if component in column_mapping:
            raise ValueError(f'Duplicate entry found in column mapping: {component}')
        
        if not value == SKIP_VALUE:
            # Ensure that this component maps to an integer
            try:
                value = int(value)
            except ValueError as e:
                raise ValueError(e)
            if value < 0:
                raise ValueError(f'Column mapping cannot be negative: {component}:{value}')
        else:
            if component == 'lat' or component == 'lon':
                raise ValueError('You cannot skip the lat or lon values')
        
        # Add the parsed mapping to the column mappings
        column_mapping[component] = value

    missing_components = REQUIRED_COMPONENTS - column_mapping.keys()
    if missing_components:
        missing = ', '.join(sorted(missing_components))
        raise ValueError(f'Missing entries in column mapping: {missing}')

    used_columns = {}
    for component, value in column_mapping.items():
        if value == SKIP_VALUE:
            continue
        if value in used_columns:
            raise ValueError(
                f'Column {value} is mapped to both {used_columns[value]} and {component}'
            )
        used_columns[value] = component

    return column_mapping
