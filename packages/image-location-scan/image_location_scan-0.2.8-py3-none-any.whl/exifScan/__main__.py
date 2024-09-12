import argparse
import sys
from exifScan import dualLogging, watchDirectory
from exifScan.runExifScan import ExifScanner
import json
import logging

import os


def getArgs():
    parser = argparse.ArgumentParser(
        prog='Watch Directory - PhotoDatabase',
        description='This script runs watchdog on a folder after taking a directory snapshot, and then keeps a geopackage map in sync with changes while the script is active.',
        epilog='I hope this proves useful.')

    parser.add_argument('path', help='The path to scan for Exif data. This argument is required')
    parser.add_argument('--WorkDirectory', default='.', help='The working directory. will default to cwd.')
    parser.add_argument('--MetashapeDirectory', help='The Metashape directory. Will search this directory recursively to find Metashape project files. Will only work with python <3.11. Will default to ScanFolder.')
    parser.add_argument('--KartRemote', help='The Kart remote page. Will push to the remote repo if set')
    parser.add_argument('--KartDirectory', help='The Kart directory. Will write to a kart repo if set')
    parser.add_argument('--GeopackageDirectory', help='The output directory. Will default to WorkDirectory.')
    parser.add_argument('--LogDirectory', default='.', help='The log directory.')
    parser.add_argument('--OutputGeopackage', default='Photos.gpkg', help='The output GeoPackage')
    parser.add_argument('--htmlFolder', help='The HTML folder. Will output a html map and table to this folder if set.')
    parser.add_argument('--mapFileName', default='map.html', help='The map file name. Only works if --htmlFolder is set')
    parser.add_argument('--otherMapLayers', nargs='+', type=str, help='A list of paths representing other layers that will be loaded by geopandas to display in the html Map.')
    parser.add_argument('--otherMapLayerNames', nargs='+', type=str, help='A list of layer names representing other layers that will be loaded by geopandas to display in the html Map.')
    parser.add_argument('--ExifOutputFile', default="outdb", help='The Exif output file name in the WorkDirectory Do not add file extension, will automatically append json extension.')
    parser.add_argument('--readExifFromOutputFile', action='store_true', default=False, help='Whether to read Exif from output file. Uses the --ExifOutputFile to find the file.')
    parser.add_argument('--recursive', action='store_true', default=False, help='Whether to run recursively. Will not attempt to remove files from existing geodf')
    parser.add_argument('--ignoreDirs', nargs='+', default=[], help='Directories that watchdog will not scan after the initial scan.')
    parser.add_argument('--ignoreMetashape', action='store_true', help='ignore file directories that include the string ".files" and "auto-project".')
    parser.add_argument('--persistObserver', action='store_true', default=True, help='Persist the Observer once stopped by saving the a pickle file of the last image.')
    parser.add_argument('--dualLogging', action='store_true', default=False, help='Whether logging should log to console and to files.')
    parser.add_argument("--groupByTags", nargs='+', help="List of tags to group by", default=["Make", "Model", "CreateDate"])
    parser.add_argument("--xyTagNames", nargs='+', help="List of tag names for x and y coordinates", default=['GPSLongitude', 'GPSLatitude'])
    parser.add_argument("--zTagName", type=str, help="Tag name for z coordinate", default='GPSAltitude')
    parser.add_argument("--imageFileExtensions", nargs='+', help="Image file extensions", default=['JPG'])
    parser.add_argument("--metashapeCacheTime", help="Time to keep Metashape data cached (in minutes)", default=120)
    parser.add_argument("--KartWriteDelay", help="Time delay before writing changes to kart", default=120)
    parser.add_argument("--pollingInterval", help="Time (in seconds) between polling intervals. Will revert to default if unset.")
    parser.add_argument("--config", type=str, help="The config file, a path to a json file.")
    parser.add_argument("--watchDirectory", action='store_true', default=False, help='Whether to watch direcotry for changes after initial scan.')
    parser.add_argument('--logLevel', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='INFO', help='Set the logging level')
    parser.add_argument("--timerInterval", help="Time between change events before processing changes", default=30)
    parser.add_argument("--linzAPIKey", help="Time between change events before processing changes", default=None)
    args = parser.parse_args()

    if args.config:
        try:
            with open(args.config, 'r') as f:
                config_args = json.load(f)
            for key, value in vars(args).items():
                defaultValue = parser.get_default(key)
                if value != defaultValue:
                    config_args[key] = value
                else:
                    if key not in config_args:
                        config_args[key] = value

            args = argparse.Namespace(**config_args)
        except Exception as e:
            print(f'An error occurred with the config file: {e}')
            sys.exit()
        delattr(args, 'config')

    return args


def main():

    args = getArgs()
    argsDict = vars(args)
    path = argsDict['path']
    prettyNameSpace = '\n'.join(f'{k}: {v}' for k, v in argsDict.items())
    path = argsDict.pop('path', None)
    enable_dualLogging = argsDict.pop('dualLogging', None)
    logLevel = argsDict.pop('logLevel', None)
    log_directory = argsDict.pop('LogDirectory', '.')

    if enable_dualLogging:

        dualLogging.windows_enable_ansi_terminal_mode()
        logfile = os.path.join(log_directory, 'runExifScan.log')
        dualLogging.set_up_logging(console_log_output="stdout", console_log_level=logLevel, console_log_color=True,
                                   logfile_file=logfile, logfile_log_level="debug", logfile_log_color=False,
                                   warn_file=logfile + "warn.log", warn_log_level="warning", warn_log_color=False,
                                   log_line_template="%(color_on)s[%(asctime)s] [%(threadName)s] [%(levelname)-8s] %(message)s%(color_off)s")
        logging.info(f'Logfile path: {logfile}')

    else:
        logging.basicConfig(format='[%(asctime)s] [%(threadName)s] %(levelname)s:%(message)s', level=getattr(logging, logLevel))

    logging.warning('======================================================================')
    # pretty each arg on a newline
    logging.debug(f"Arguments used for watchDirectory:{prettyNameSpace}")
    watch = argsDict.pop('watchDirectory', None)
    if watch:
        watchDirectory.watchFolder(path, argsDict)
    else:
        scanner = ExifScanner(**argsDict)
        scanner.scan_for_photos(path)


if __name__ == "__main__":
    main()
