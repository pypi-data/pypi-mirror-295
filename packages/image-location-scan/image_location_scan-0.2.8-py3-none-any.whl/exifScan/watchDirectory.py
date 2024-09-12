import time
import os
from datetime import datetime as dt
import logging
import sys
import copy
from exifScan.runExifScan import ExifScanner
from persistentObserver.persistentObserver import PersistentPollingObserver
from persistentObserver.folderUpdateHandler import FolderUpdateHandler
import threading

startCtime = dt.now().ctime()
stats = {'Scan Started at': startCtime}


def watchFolder(path, argsDict, stop_event=threading.Event()):
    # check for a config file - will only set if not the default value. Unfortunately- this overwrites the command line if it is set to default

    pollingInterval = argsDict.pop('pollingInterval', None)
    persistObserver = argsDict.pop('persistObserver', None)
    timerInterval = argsDict.pop('timerInterval', None)
    on_snapshot = argsDict.pop('on_snapshot', None)

    ExifStartTime = dt.now()
    # deep copy the args so we can set differing args for the initial scan
    initialArgs = copy.deepcopy(argsDict)
    # pop so it isn't an argument in any of the future scans
    ignoreMetashape = argsDict.pop('ignoreMetashape', False)
    ignoreDirs = argsDict.get('ignoreDirs', [])
    if ignoreMetashape:
        ignoreDirs.append('.files')
        ignoreDirs.append('auto-project')

    # pop the exifOutputFiles from the argsDict,
    # as they are only useful in the initial scan
    readFromFile = argsDict.pop('readExifFromOutputFile', None)
    argsDict.pop('ExifOutputFile', None)
    argsDict['stats'] = stats
    logging.warning(f'Watchdog starting new process. Watching: {path}')
    # set handler and start polling.
    Scanner = ExifScanner(**argsDict)
    event_handler = FolderUpdateHandler(ignoreDirs, Scanner, timer_interval=timerInterval)
    pollingKeywords = {}
    if pollingInterval:
        pollingKeywords['timeout'] = pollingInterval

    if persistObserver:
        pollingKeywords['save_to'] = os.path.join(argsDict['WorkDirectory'], 'PersistentObserver\\image.pkl')

    def on_snapshot_callback(time):
        now = dt.now().ctime()
        logging.info(f"Snapshot took {time}(h:mm:ss).")
        if not event_handler.paused:
            stats.pop('Currently updating. Update started', None)
            stats['Last updated'] = now
            Scanner.write_HTML()
        else:
            stats.pop('Last updated', None)
            stats['Currently updating. Update started'] = now
            Scanner.write_HTML()

    if on_snapshot:
        pollingKeywords['on_snapshot'] = on_snapshot_callback

    observer = PersistentPollingObserver(**pollingKeywords)

    # warning that might save a lot of time.
    gpdir = argsDict['GeopackageDirectory'] or argsDict['WorkDirectory']

    OutputGeopackagePath = os.path.join(gpdir, argsDict.get('OutputGeopackage', None))
    if not observer.previous_snapshot_exists or readFromFile:
        if not readFromFile:
            logging.warning('No previous snapshot, will create a full initial recursive scan with Exiftool')
        else:
            logging.warning('Will use previous ExifScan output file.')

        if os.path.exists(OutputGeopackagePath):
            logging.error(f'{OutputGeopackagePath} already exists, and a full scan has been initiated. Please confirm this is intentional.')
            while True:
                confirmation = input("Are you sure you want to proceed? (y/n): ")
                if confirmation.lower() == 'y':
                    break
                elif confirmation.lower() == 'n':
                    logging.warning("Aborting script.")
                    sys.exit()
                else:
                    logging.error("Invalid input. Please enter 'y' or 'n'.")
    elif observer.previous_snapshot_exists:
        logging.warning('Re-using previous snapshot.')
        if readFromFile:
            logging.error('Ignoring previous ExifFile, previous snapshot file exists!')

    observer.schedule(event_handler, path=path, recursive=True)
    logging.debug('Starting Handler.')

    # check if previous snapshot exists, if not scan recursively.
    if not observer.previous_snapshot_exists:
        initialArgs['recursive'] = True
        initialScanner = ExifScanner(**initialArgs)
        result = initialScanner.scan_for_photos(path)

        if result != path:
            logging.error(f'Error while performing initial scan in folder {path}')
        else:
            observer.start()
            logging.info(f"First Folder Poll done . The first poll took {dt.now() - ExifStartTime}(h:mm:ss).")

            logging.info(f"Successfully scanned the following path for images: {path}")
            logging.info('======================================================================')
            try:
                while not stop_event.is_set():
                    time.sleep(1)
            except KeyboardInterrupt:
                logging.info("KeyboardInterrupt")
                observer.stop()
                observer.join()

    else:
        observer.start()
        logging.info(f"First Folder Poll done . The first poll took {dt.now() - ExifStartTime}(h:mm:ss).")

        try:
            while not stop_event.is_set():
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("KeyboardInterrupt")
            observer.stop()
            observer.join()

    logging.info('Script ended')
