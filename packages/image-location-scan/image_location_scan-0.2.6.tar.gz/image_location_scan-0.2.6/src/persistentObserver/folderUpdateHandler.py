from watchdog.events import FileSystemEventHandler
from watchdog.utils.dirsnapshot import EmptyDirectorySnapshot

from threading import Timer

import logging

import os

from datetime import datetime as dt


class FolderUpdateHandler(FileSystemEventHandler):
    def __init__(self, ignoreDirs, Scanner, timer_interval=30):
        self.directoriesToCheck = []
        self.paused = False
        self.timer = None
        self.ignoreDirs = ignoreDirs
        if len(self.ignoreDirs):
            logging.info(f'Watchdog is ignoring directories that contain: {self.ignoreDirs}')
        # only makes sense to read from json file at startup
        self.Scanner = Scanner
        self.timer_interval = timer_interval
        self.currentSnapshot = EmptyDirectorySnapshot()

    def appendDirectory(self, directory):
        if not directory:
            return

        if directory not in self.directoriesToCheck:
            self.directoriesToCheck.append(directory)
            logging.warning(f'Appended {directory} to directories requiring update.')

        self.restartTimer()

    def restartTimer(self):
        if self.timer:
            self.timer.cancel()
            logging.debug('Restarting timer.')
        self.timer = Timer(self.timer_interval, self.process_event)
        self.timer.start()

    def update_snapshot(self, snapshot):
        self.recentSnapshot = snapshot
        if not self.paused:
            logging.debug('currentSnapshot updated')

            self.currentSnapshot = snapshot

    def get_snapshot(self):
        return self.currentSnapshot

    def process_event(self):
        self.timer = None
        if (self.paused):
            self.restartTimer()
            logging.debug('Handler is paused.')
            return
        self.paused = True
        logging.debug('Pausing Handler.')

        logging.warning(f"Processing all change events. Directories to check: {self.directoriesToCheck}")

        directoriesToCheckCopy = self.directoriesToCheck.copy()
        for path in directoriesToCheckCopy:

            result = self.Scanner.scan_for_photos(path)
            if result != path:
                logging.error(f"An error occurred when scanning the following folder:{path}")
                logging.error("Retrying in 1 hour")
                # set limit for re-tries?
                self.directoriesToCheck.remove(path)
                Timer(3600, self.appendDirectory, [path])
            else:
                self.directoriesToCheck.remove(path)
                logging.info(f'{dt.now()} Successfully scanned the following path for images: {path}')
                logging.info('======================================================================')
        self.currentSnapshot = self.recentSnapshot
        logging.debug('Resuming Handler after updating currentSnapshot')
        logging.warning("Done processing all change events.")
        self.paused = False

    def getDirectory(self, event, path):
        if not event.is_directory:
            directory = os.path.dirname(path)
        elif event.is_directory:
            directory = path
        else:
            return
        for ignore in self.ignoreDirs:
            if ignore in directory:
                return
        return directory.rstrip('/\\')

    def on_any_event(self, event):

        directory = self.getDirectory(event, event.src_path)
        logging.info(f'Event type: {event.event_type}, event source : {event.src_path}')
        self.appendDirectory(directory)

        if (directory):
            if hasattr(event, 'dest_path'):
                directory = self.getDirectory(event, event.dest_path)
                logging.info(f'Event type: {event.event_type}, event source : {event.dest_path}')
                self.appendDirectory(directory)
