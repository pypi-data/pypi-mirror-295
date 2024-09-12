from __future__ import annotations
from watchdog.observers.api import DEFAULT_EMITTER_TIMEOUT, DEFAULT_OBSERVER_TIMEOUT, BaseObserver, EventEmitter, ObservedWatch
from watchdog.events import (
    DirCreatedEvent,
    DirDeletedEvent,
    DirModifiedEvent,
    DirMovedEvent,
    FileCreatedEvent,
    FileDeletedEvent,
    FileModifiedEvent,
    FileMovedEvent,
)

from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff, EmptyDirectorySnapshot
import threading
import pickle
import os
import logging
from datetime import datetime as dt


class PersistentPollingEmitter(EventEmitter):
    """
    Platform-independent emitter that polls a directory to detect file
    system changes.
    """

    def __init__(
        self,
        event_queue,
        watch,
        event_handler,
        previous_snapshot_file,
        on_snapshot=None,
        timeout=DEFAULT_EMITTER_TIMEOUT,
        event_filter=None,
        stat=os.stat,
        listdir=os.scandir,
    ):
        super().__init__(event_queue, watch, timeout, event_filter)
        previous_snapshots = load_pickle_file(previous_snapshot_file)
        if previous_snapshots is None:
            previous_snapshots = dict()
        self._hasPreviousSnapshot = isinstance(previous_snapshots.get(self.watch.path, None), DirectorySnapshot)
        self._snapshot: DirectorySnapshot = previous_snapshots.get(self.watch.path, EmptyDirectorySnapshot())
        self._event_handler = event_handler
        self._lock = threading.Lock()
        self.on_snapshot = on_snapshot
        self._take_snapshot = lambda: DirectorySnapshot(
            self.watch.path, self.watch.is_recursive, stat=stat, listdir=listdir
        )
        self._run_immediately = False

    def on_thread_start(self):

        if not self._hasPreviousSnapshot:
            logging.info('Invalid previous snapshot.')
            self._snapshot = self._take_snapshot()
        else:
            logging.info('Using previous snapshot.')
            self._event_handler.recentSnapshot = self._snapshot
            self._event_handler.currentSnapshot = self._snapshot
            self._run_immediately = True

    def _handle_diff_events(self, events):
        # Files.
        for src_path in events.files_deleted:
            self.queue_event(FileDeletedEvent(src_path))
        for src_path in events.files_modified:
            self.queue_event(FileModifiedEvent(src_path))
        for src_path in events.files_created:
            self.queue_event(FileCreatedEvent(src_path))
        for src_path, dest_path in events.files_moved:
            self.queue_event(FileMovedEvent(src_path, dest_path))

        # Directories.
        for src_path in events.dirs_deleted:
            self.queue_event(DirDeletedEvent(src_path))
        for src_path in events.dirs_modified:
            self.queue_event(DirModifiedEvent(src_path))
        for src_path in events.dirs_created:
            self.queue_event(DirCreatedEvent(src_path))
        for src_path, dest_path in events.dirs_moved:
            self.queue_event(DirMovedEvent(src_path, dest_path))

    def get_handler_snapshot(self):
        return self._event_handler.get_snapshot()

    def queue_events(self, timeout):
        # Skip the timeout if there was a previous snapshot
        if self._run_immediately:
            logging.info('Skipping timeout as a previous snapshot was loaded.')

            self._run_immediately = False
            timeout = 0

        # We don't want to hit the disk continuously.
        # timeout behaves like an interval for polling emitters.
        if self.stopped_event.wait(timeout):
            return

        with self._lock:
            if not self.should_keep_running():
                return
            logging.debug("Starting Diff.")

            # Get event diff between fresh snapshot and previous snapshot.
            # Update snapshot.
            try:
                snapshotStart = dt.now()
                new_snapshot = self._take_snapshot()
                self._event_handler.update_snapshot(new_snapshot)
                if self.on_snapshot:
                    self.on_snapshot(dt.now() - snapshotStart)

            except OSError:
                self.queue_event(DirDeletedEvent(self.watch.path))
                self.stop()
                return

            events = DirectorySnapshotDiff(self._snapshot, new_snapshot)
            self.old_snapshot = self._snapshot
            self._snapshot = new_snapshot

            # Handle the diff events
            self._handle_diff_events(events)


def load_pickle_file(file_path):
    if not os.path.exists(file_path):
        return None

    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
            return data
    except (pickle.UnpicklingError, EOFError, AttributeError, ImportError, IndexError) as e:
        print(f"Error loading pickle file: {e}")
        return None


class PersistentPollingObserver(BaseObserver):
    """
    Platform-independent observer that polls a directory to detect file
    system changes.
    """

    def __init__(self, save_to, on_snapshot=None, protocol=0, timeout=DEFAULT_OBSERVER_TIMEOUT):
        self._filename = save_to
        self.on_snapshot = on_snapshot
        self._protocol = protocol
        self.previous_snapshot_exists = os.path.exists(self._filename)
        super().__init__(emitter_class=PersistentPollingEmitter, timeout=timeout)

    def schedule(self, event_handler, path, recursive=False, event_filter=None):
        with self._lock:
            watch = ObservedWatch(path, recursive, event_filter)
            self._add_handler_for_watch(event_handler, watch)

            # If we don't have an emitter for this watch already, create it.
            if self._emitter_for_watch.get(watch) is None:
                emitter = self._emitter_class(
                    event_queue=self.event_queue,
                    watch=watch,
                    event_handler=event_handler,
                    previous_snapshot_file=self._filename,
                    timeout=self.timeout,
                    event_filter=event_filter,
                    on_snapshot=self.on_snapshot
                )
                if self.is_alive():
                    emitter.start()
                self._add_emitter(emitter)
            self._watches.add(watch)
        return watch

    def stop(self, *args, **kwargs):
        snapshots = {emitter.watch.path: emitter.get_handler_snapshot() for emitter in self.emitters}
        dir_name = os.path.dirname(self._filename)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            logging.warning(f'Created folder {dir_name} to dump DirectorySnapshot.')
        with open(self._filename, 'wb') as f:
            pickle.dump(snapshots, f, self._protocol)
        logging.info(f'Saved pickled DirectorySnapshot at {self._filename}.')
        super().stop(*args, **kwargs)
