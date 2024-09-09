## Image Location Scan

**Image Location Scan** is a powerful tool designed to extract Exif metadata from images, monitor a specified directory for changes, and maintain a synchronized [geopackage file](https://www.geopackage.org/). This script is ideal for users who need to keep track of photo metadata and visualize it on a map, especially in dynamic environments where files are frequently added, removed, or modified. Requires [exiftool](https://exiftool.org/) to be installed and callable by subprocess. Optionally scans and matches Metashape psx and psz files.

### Features

- **Directory Monitoring**: Utilizes `watchdog` to monitor a specified directory for changes and keeps a GeoPackage map updated in real-time.
- **Exif Metadata Extraction**: Extracts Exif metadata from images using `ExifTool`, including GPS coordinates, camera make and model, and more.
- **GeoPackage Synchronization**: Maintains a GeoPackage file that is updated with the latest metadata from the monitored directory.
- **HTML Map Generation**: Generates an HTML map and table to visualize the metadata, with options to include additional map layers.
- **Configurable Logging**: Supports dual logging to both console and file, with customizable log levels.
- **Persistent Observer**: Optionally persists the observer state to resume monitoring after interruptions.
- **Integration with Kart**: Supports integration with Kart for version control and remote repository synchronization.
- **Additonal Metadata**: Manually add key/value metadata by saving `metadata.xlsx` files in the directory structure.

### Installation

To install the package, use the following command:

```bash
pip install image-location-scan
```

### Usage

The script can be run from the command line with various options to customize its behavior. Below is an example of how to use it:

```bash
py -m exifScan '\\file\Shared\SEESPhotoDatabase' --config .\config.json --watchDirectory
```

### Command Line Arguments

- `path`: The path to scan for Exif data (required).
- `--WorkDirectory`: The working directory (defaults to current working directory).
- `--MetashapeDirectory`: Directory to search for Metashape project files.
- `--KartRemote`: Kart remote repository URL for pushing updates.
- `--KartDirectory`: Directory for the Kart repository.
- `--GeopackageDirectory`: Directory to save the GeoPackage file (defaults to WorkDirectory).
- `--LogDirectory`: Directory to save log files (defaults to current directory).
- `--OutputGeopackage`: Name of the output GeoPackage file (defaults to `Photos.gpkg`).
- `--htmlFolder`: Directory to save the HTML map and table.
- `--mapFileName`: Name of the HTML map file (defaults to `map.html`).
- `--otherMapLayers`: List of paths to additional map layers.
- `--otherMapLayerNames`: List of names for additional map layers.
- `--ExifOutputFile`: Name of the Exif output file (defaults to `outdb`).
- `--readExifFromOutputFile`: Read Exif data from the output file instead of scanning.
- `--recursive`: Scan directories recursively.
- `--ignoreDirs`: List of directories to ignore during scanning.
- `--ignoreMetashape`: Ignore directories containing `.files` and `auto-project`.
- `--persistObserver`: Persist the observer state to resume monitoring after interruptions.
- `--dualLogging`: Enable logging to both console and file.
- `--groupByTags`: List of tags to group by. Always groups by folder, but can also split into the groups specified by this flag (defaults to `["Make", "Model"]`).
- `--xyTagNames`: List of tag names for x and y coordinates (defaults to `['GPSLongitude', 'GPSLatitude']`).
- `--zTagName`: Tag name for z coordinate (defaults to `GPSAltitude`).
- `--imageFileExtensions`: List of image file extensions to scan (defaults to `['JPG']`).
- `--metashapeCacheTime`: Time to keep Metashape data cached (in minutes, defaults to 120).
- `--pollingInterval`: Time (in seconds) between polling intervals.
- `--config`: Path to a JSON config file.
- `--watchDirectory`: Watch directory for changes after initial scan.
- `--logLevel`: Set the logging level (choices: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`). Only if dualLogging is disabled.

### Dependencies

- `argparse`
- `sys`
- `json`
- `logging`
- `os`
- `time`
- `datetime`
- `copy`
- `threading`
- `subprocess`
- `folium`
- `pandas`
- `geopandas`
- `ExifTool`
- `watchdog`

### Acknowledgments

Thanks to Phil Harvey and his excellent exiftool software.
