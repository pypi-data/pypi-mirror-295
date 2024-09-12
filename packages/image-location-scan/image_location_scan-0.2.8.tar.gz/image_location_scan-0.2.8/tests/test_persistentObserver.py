import os
import pickle
import threading
import pytest
import tempfile
from watchdog.events import FileCreatedEvent
from watchdog.observers.api import EventQueue
from persistentObserver.persistentObserver import PersistentPollingEmitter, PersistentPollingObserver, ObservedWatch, DirectorySnapshot, EmptyDirectorySnapshot
from persistentObserver.folderUpdateHandler import FolderUpdateHandler
import logging


class MockEventHandler:
    def __init__(self):
        self.recentSnapshot = None
        self.currentSnapshot = None

    def update_snapshot(self, snapshot):
        self.recentSnapshot = self.currentSnapshot
        self.currentSnapshot = snapshot

    def get_snapshot(self):
        return self.currentSnapshot


class MockScanner:

    def scan_for_photos(self, path):
        return path


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def temp_file():
    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        yield tmpfile.name
    os.remove(tmpfile.name)


def test_emitter_initialization(temp_dir, temp_file):
    event_queue = []
    watch = ObservedWatch(temp_dir, recursive=True)
    event_handler = MockEventHandler()

    emitter = PersistentPollingEmitter(event_queue, watch, event_handler, temp_file)
    assert isinstance(emitter._snapshot, EmptyDirectorySnapshot)


def test_emitter_snapshot_handling(temp_dir, temp_file):
    event_queue = []
    watch = ObservedWatch(temp_dir, recursive=True)
    event_handler = MockEventHandler()

    # Create a snapshot file
    snapshot = DirectorySnapshot(temp_dir, recursive=True)
    with open(temp_file, 'wb') as f:
        pickle.dump({temp_dir: snapshot}, f)

    emitter = PersistentPollingEmitter(event_queue, watch, event_handler, temp_file)
    emitter.on_thread_start()

    assert emitter._hasPreviousSnapshot
    assert emitter._snapshot.paths == snapshot.paths
    assert emitter._snapshot.stat_info(temp_dir) == snapshot.stat_info(temp_dir)


def test_emitter_queue_events(temp_dir, temp_file):
    event_queue = EventQueue()
    watch = ObservedWatch(temp_dir, recursive=True)
    event_handler = MockEventHandler()

    emitter = PersistentPollingEmitter(event_queue, watch, event_handler, temp_file)
    emitter.on_thread_start()

    # Create a new file to trigger an event
    new_file_path = os.path.join(temp_dir, 'new_file.txt')
    with open(new_file_path, 'w') as f:
        f.write('test')

    emitter.queue_events(1)
    assert any(isinstance(event[0], FileCreatedEvent) for event in event_queue.queue)


def test_observer_initialization(temp_file):
    observer = PersistentPollingObserver(save_to=temp_file)
    assert observer._filename == temp_file
    assert observer._protocol == 0


def test_observer_schedule(temp_dir, temp_file):
    observer = PersistentPollingObserver(save_to=temp_file)
    event_handler = MockEventHandler()

    watch = observer.schedule(event_handler, temp_dir, recursive=True)
    assert watch.path == temp_dir
    assert watch.is_recursive


def test_emitter_error_handling(temp_dir, temp_file):
    event_queue = EventQueue()
    watch = ObservedWatch(temp_dir, recursive=True)
    event_handler = MockEventHandler()

    # Simulate a permission error by making the directory read-only
    os.chmod(temp_dir, 0o400)
    emitter = PersistentPollingEmitter(event_queue, watch, event_handler, temp_file)
    emitter.on_thread_start()

    try:
        emitter.queue_events(1)
    except OSError:
        assert True  # Expected behavior
    finally:
        os.chmod(temp_dir, 0o700)  # Restore permissions


def test_emitter_concurrency(temp_dir, temp_file):
    event_queue = EventQueue()
    watch = ObservedWatch(temp_dir, recursive=True)
    event_handler = MockEventHandler()

    emitter = PersistentPollingEmitter(event_queue, watch, event_handler, temp_file)
    emitter.on_thread_start()

    def create_file():
        new_file_path = os.path.join(temp_dir, 'concurrent_file.txt')
        with open(new_file_path, 'w') as f:
            f.write('test')

    threads = [threading.Thread(target=create_file) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    emitter.queue_events(1)
    assert len(event_queue.queue) >= 2


def test_observer_persistence(temp_dir, temp_file, caplog):
    with caplog.at_level(logging.DEBUG):
        observer = PersistentPollingObserver(save_to=temp_file)
        event_handler = FolderUpdateHandler([], MockScanner)

        event_snapshot = event_handler.currentSnapshot.path('')

        assert event_snapshot is None

        observer.schedule(event_handler, temp_dir, recursive=True)
        observer.start()
        observer.stop()
        observer.join()
        snapshot = event_handler.currentSnapshot

        assert os.path.exists(temp_file)
        # snapshots = {emitter.watch.path: emitter.get_handler_snapshot() for emitter in observer.emitters}
        # with open('data.pkl', 'wb') as file:
        #     pickle.dump(snapshots, file)

        # Load data from the file
        with open(temp_file, 'rb') as file:
            loaded_data = pickle.load(file)

        assert pickle.dumps(loaded_data[temp_dir]) == pickle.dumps(snapshot)
        # Restart observer and check if it loads the previous snapshot
        new_observer = PersistentPollingObserver(save_to=temp_file)
        new_event_handler = FolderUpdateHandler([], MockScanner)
        new_observer.schedule(new_event_handler, temp_dir, recursive=True)
        new_observer.start()

        new_snapshot = event_handler.currentSnapshot
        assert new_snapshot == snapshot
        paths_list = list(new_event_handler.currentSnapshot.paths)

        # Now you can access the first element
        assert paths_list[0] == temp_dir

        assert new_event_handler.currentSnapshot.path(temp_dir) is None
