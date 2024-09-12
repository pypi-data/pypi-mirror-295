import pytest
from unittest.mock import patch
from exifScan.watchDirectory import watchFolder
import time
import tempfile
import os
import logging


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def temp_file():
    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        yield tmpfile.name
    os.remove(tmpfile.name)


@pytest.fixture
def args_dict(temp_dir):
    return {
        'ignoreMetashape': True,
        'ignoreDirs': [],
        'readExifFromOutputFile': None,
        'pollingInterval': 10,
        'persistObserver': True,
        'WorkDirectory': temp_dir,
        'GeopackageDirectory': temp_dir,
        'OutputGeopackage': 'output.gpkg',
        'timerInterval': 0.5
    }


@patch('exifScan.watchDirectory.ExifScanner')
def test_watch_folder_initial_scan(mock_scanner, args_dict, temp_dir, temp_file):

    # Start the watch process in a separate thread
    import threading
    watch_thread = threading.Thread(target=watchFolder, args=(temp_dir, args_dict))
    watch_thread.start()
    watch_thread.join()
    mock_scanner.assert_called_with(**{'ignoreMetashape': True, 'ignoreDirs': [], 'readExifFromOutputFile': None, 'WorkDirectory': temp_dir, 'GeopackageDirectory': temp_dir, 'OutputGeopackage': 'output.gpkg', 'recursive': True})


@patch('exifScan.watchDirectory.ExifScanner')
def test_watch_folder_reuse_snapshot(mock_scanner, args_dict, temp_dir):

    watchFolder(temp_dir, args_dict)

    mock_scanner.assert_called_with(**{'ignoreMetashape': True, 'ignoreDirs': [], 'readExifFromOutputFile': None, 'WorkDirectory': temp_dir, 'GeopackageDirectory': temp_dir, 'OutputGeopackage': 'output.gpkg', 'recursive': True})
    mock_scanner.return_value.scan_for_photos.assert_called_with(temp_dir)


@patch('exifScan.watchDirectory.os.path.exists')
@patch('exifScan.watchDirectory.ExifScanner')
@patch('exifScan.watchDirectory.FolderUpdateHandler')
@patch('exifScan.watchDirectory.PersistentPollingObserver')
def test_watch_folder_output_geopackage_exists(mock_observer, mock_handler, mock_scanner, mock_exists, args_dict, temp_dir):
    mock_scanner.return_value.scan_for_photos.return_value = temp_dir
    mock_exists.return_value = True
    mock_observer_instance = mock_observer.return_value
    mock_observer_instance.previous_snapshot_exists = False

    with patch('builtins.input', return_value='y'):
        import threading
        stop_event = threading.Event()
        watch_thread = threading.Thread(target=watchFolder, args=(temp_dir, args_dict, stop_event))
        watch_thread.start()
        stop_event.set()
    mock_scanner.assert_called_with(**{'ignoreMetashape': True, 'ignoreDirs': [], 'readExifFromOutputFile': None, 'WorkDirectory': temp_dir, 'GeopackageDirectory': temp_dir, 'OutputGeopackage': 'output.gpkg', 'recursive': True})
    mock_handler.assert_called_with(['.files', 'auto-project'], mock_scanner.return_value, timer_interval=0.5)
    mock_observer_instance.schedule.assert_called_once()
    mock_observer_instance.start.assert_called_once()


@patch('exifScan.watchDirectory.ExifScanner')
def test_watch_folder_file_modification(mock_scanner, args_dict, temp_dir, temp_file, caplog):
    mock_scanner.return_value.scan_for_photos.return_value = temp_dir
    with caplog.at_level(logging.DEBUG):
        # Start the watch process in a separate thread
        import threading
        stop_event = threading.Event()
        watch_thread = threading.Thread(target=watchFolder, args=(temp_dir, args_dict, stop_event))
        watch_thread.start()

        # Give the observer some time to start
        time.sleep(2)

        # Simulate a file modification
        test_file_path = os.path.join(temp_dir, 'test_file.txt')
        with open(test_file_path, 'w') as f:
            f.write('Test content')
        # Give the observer some time to detect the change
        time.sleep(10)

        # Assert that the event handler's methods were called

        # Clean up
        stop_event.set()
        watch_thread.join()
        os.remove(test_file_path)

        mock_scanner.return_value.scan_for_photos.assert_called_with(temp_dir)
        assert mock_scanner.return_value.scan_for_photos.call_count == 2
