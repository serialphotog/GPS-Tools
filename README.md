# GPX Tools

A collection of various tools for working with GPX (and related) files.

## csv2gpx

`csv2gpx` is a simple command line utility that allows you to take a CSV file containing GPS data and convert it into a GPX file.

### Command Line Options

- `--input`, `-i`: **Required**. The path to the input CSV file.
- `--output`, `-o`: **Required**. The path to the output GPX file that will be created.
- `--format`, `-f`: Allows you to specify a custom column mapping to use when parsing the CSV file. See the *CSV Column Mapping* section for more information.
- `--skip`, `-s`: Tells the software to ignore the first line of the CSV file. This is useful for ignoring a header row that may be present in the CSV file.
- `--verbose`, `-v`: Enables verbose output for the program.

## gpx2csv

`gpx2csv` is a simple command line utility that allows you to take a GPX file containing GPS waypoints and convert it into a CSV file containing the GPS data.

### Command Line Options

- `--input`, `-i`: **Required**. The path to the input GPX file.
- `--output`, `-o`: **Required**. The path to the output CSV file.
- `--format`, `-f`: Allows you to specify a custom column mapping to use when generating the CSV file. See the *CSV Column Mapping* section for mor information.

## CSV Column Mapping

By default, `csv2gpx` will use the following column mapping:

- Column 1: Latitude
- Column 2: Longitude
- Column 3: Name
- Column 4: Description

Obviously, it wouldn't be very flexible if to require your CSV file to be in this format. For this reason, you can specify your own column mapping using the `--format` (or `-f`) option. 

For this example, let's say you want to convert a CSV file that has the following output:

- Column 1: Name
- Column 2: Description
- Column 3: Latitude
- Column 4: Longitude

You would achieve this by appending the following to your command:

```
-f lat:2,lon:3,name:0,desc:1
```

**NOTE:** The order you specify these in does not matter, but you must specify the mappings for each of *lat*, *lon*, *name*, and *desc*.

It's also worth mentioning that you can ignore either the *name* or *description* entries if you either don't want to include them in your output or if your CSV file does not contain entries for them. For example, I could skip the description entry in my CSV file with the following:

```
-f lat:2,lon:3,name:0,desc:skip
```