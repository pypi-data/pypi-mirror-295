import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from exifScan.ExifToolScan import ExifToolScanner, process_output, reader
import os


def test_initialization():
    scanner = ExifToolScanner(FileTypes=['jpg', 'png'], recursive=True, ignoreDirs=['/ignore/this'], ignoreMetashape=True)
    assert scanner.FileTypes == ['jpg', 'png']
    assert scanner.recursive is True
    assert scanner.ignoreDirs == ['/ignore/this']
    assert scanner.ignoreMetashape is True


@patch('exifScan.ExifToolScan.subprocess.Popen')
@patch('exifScan.ExifToolScan.threading.Thread')
def test_run_exiftool(mock_thread, mock_popen):
    mock_process = MagicMock()
    mock_process.wait.return_value = None
    mock_popen.return_value = mock_process

    scanner = ExifToolScanner(FileTypes=['jpg'], recursive=False)
    result = scanner.run_exiftool('/path/to/scan')

    mock_popen.assert_called_once()
    assert result is not None


@patch('exifScan.ExifToolScan.os.path.getsize')
@patch('exifScan.ExifToolScan.pd.read_json')
def test_process_output(mock_read_json, mock_getsize):
    mock_getsize.return_value = 100
    mock_read_json.return_value = pd.DataFrame({'data': [1, 2, 3]})

    result = process_output('/path/to/scan', 'exifOut.json')
    assert not result.empty


@patch('exifScan.ExifToolScan.os.path.getsize')
@patch('exifScan.ExifToolScan.os.remove')
def test_process_output_empty_file(mock_remove, mock_getsize):
    mock_getsize.return_value = 0

    result = process_output('/path/to/scan', 'exifOut.json')
    assert result.empty
    mock_remove.assert_called_once_with('exifOut.json')


def test_reader():
    mock_pipe = MagicMock()
    mock_pipe.readline.side_effect = ['line1\n', 'line2\n', '']
    mock_func = MagicMock()
    stop_event = MagicMock()
    stop_event.is_set.return_value = False

    reader(mock_pipe, mock_func, stop_event)
    assert mock_func.call_count == 2


def test_images_in_folder():
    images_folder = 'tests/images'
    assert os.path.exists(images_folder)
    assert len(os.listdir(images_folder)) > 0  # Ensure there are images in the folder

    scanner = ExifToolScanner(FileTypes=['jpg', 'png'], recursive=True)
    result = scanner.run_exiftool(images_folder)

    # Ensure the result is a DataFrame
    assert isinstance(result, pd.DataFrame)

    # Check the number of rows matches the number of images
    num_images = len([f for f in os.listdir(images_folder) if f.lower().endswith(('jpg', 'png'))])
    assert len(result) == num_images

    # Verify specific columns
    assert 'SourceFile' in result.columns
    assert 'GPSLongitude' in result.columns
    assert 'GPSLatitude' in result.columns
    assert 'GPSAltitude' in result.columns
    assert 'CreateDate' in result.columns
    assert 'ImageSize' in result.columns
    assert 'FileSize' in result.columns
    assert 'Make' in result.columns
    assert 'Model' in result.columns
    # Validate data types
    assert result['SourceFile'].dtype == object
    assert result['GPSLongitude'].dtype == float
    assert result['GPSLatitude'].dtype == float
    assert result['GPSAltitude'].dtype == float
    assert result['CreateDate'].dtype == object
    assert result['ImageSize'].dtype == object
    assert result['FileSize'].dtype == 'int64'
    assert result['Make'].dtype == object
    assert result['Model'].dtype == object

    # Check for non-null values in important columns
    assert result['SourceFile'].notnull().all()
    assert result['GPSLongitude'].notnull().all()
    assert result['GPSLatitude'].notnull().all()
    assert result['GPSAltitude'].notnull().all()
    assert result['CreateDate'].notnull().all()
    assert result['ImageSize'].notnull().all()
    assert result['FileSize'].notnull().all()
    assert result['Make'].notnull().all()
    assert result['Model'].notnull().all()

    # Check that all 'Make' values are 'DJI'
    assert (result['Make'] == 'DJI').all()

    # Check that all 'Model' values are 'FC6310'
    assert (result['Model'] == 'FC6310').all()

    for date in result['CreateDate']:
        assert date.startswith('2024:07:09') or date.startswith('2019:02:21')
        assert len(date) == 19  # Ensure the format is 'YYYY:MM:DD HH:MM:SS'


def test_empty_directory():
    empty_folder = 'tests/test_folders/empty_images'
    os.makedirs(empty_folder, exist_ok=True)
    assert os.path.exists(empty_folder)
    assert len(os.listdir(empty_folder)) == 0  # Ensure the directory is empty

    scanner = ExifToolScanner(FileTypes=['jpg', 'png'], recursive=True)
    result = scanner.run_exiftool(empty_folder)
    assert result.empty  # Expect an empty DataFrame


def test_unsupported_file_types():
    unsupported_folder = 'tests/test_folders/unsupported_images'
    os.makedirs(unsupported_folder, exist_ok=True)
    with open(os.path.join(unsupported_folder, 'test.txt'), 'w') as f:
        f.write('This is a test file.')
    assert os.path.exists(unsupported_folder)
    assert len(os.listdir(unsupported_folder)) > 0  # Ensure there is at least one file

    scanner = ExifToolScanner(FileTypes=['jpg', 'png'], recursive=True)
    result = scanner.run_exiftool(unsupported_folder)
    assert result.empty  # Expect an empty DataFrame since no supported files are present


def test_corrupted_files():
    corrupted_folder = 'tests/test_folders/corrupted_images'
    os.makedirs(corrupted_folder, exist_ok=True)
    with open(os.path.join(corrupted_folder, 'corrupted.jpg'), 'wb') as f:
        f.write(b'\x00\x01\x02\x03\x04\x05')  # Write some invalid binary data
    assert os.path.exists(corrupted_folder)
    assert len(os.listdir(corrupted_folder)) > 0  # Ensure there is at least one file

    scanner = ExifToolScanner(FileTypes=['jpg', 'png'], recursive=True)
    result = scanner.run_exiftool(corrupted_folder)
    assert not result.empty  # Expect a non-empty DataFrame
    assert 'GPSLongitude' not in result.columns or result['GPSLongitude'].isnull().all()
    assert 'GPSLatitude' not in result.columns or result['GPSLatitude'].isnull().all()


def test_large_files():
    large_folder = 'tests/large_images'
    # Assuming you have a large image file for testing
    large_image_path = os.path.join(large_folder, 'CROWN_2853_B_3_cropped.tif')
    assert os.path.exists(large_image_path)

    scanner = ExifToolScanner(FileTypes=['tif', 'png'], recursive=True)
    result = scanner.run_exiftool(large_folder)
    assert not result.empty  # Expect a non-empty DataFrame


# def test_invalid_file_types():
#     invalid_folder = 'tests/test_folders/invalid_images'
#     os.makedirs(invalid_folder, exist_ok=True)
#     with open(os.path.join(invalid_folder, 'test.invalid'), 'w') as f:
#         f.write('This is a test file.')
#     assert os.path.exists(invalid_folder)
#     assert len(os.listdir(invalid_folder)) > 0  # Ensure there is at least one file

#     scanner = ExifToolScanner(FileTypes=['jpg', 'png'], recursive=True)
#     with pytest.raises(ValueError, match="Unsupported file type"):
#         scanner.run_exiftool(invalid_folder)


def test_non_existent_directory():
    non_existent_folder = 'tests/test_folders/non_existent_images'
    scanner = ExifToolScanner(FileTypes=['jpg', 'png'], recursive=True)
    result = scanner.run_exiftool(non_existent_folder)
    assert isinstance(result, pd.DataFrame)
    assert result.empty  # Expect a non-empty DataFrame


def test_invalid_json_format():
    invalid_json_folder = 'tests/test_folders/invalid_json'
    os.makedirs(invalid_json_folder, exist_ok=True)
    path = os.path.join(invalid_json_folder, 'invalid.json')
    with open(path, 'w') as f:
        f.write('{"invalid": "json"}')  # Write invalid JSON data
    assert os.path.exists(invalid_json_folder)
    assert len(os.listdir(invalid_json_folder)) > 0  # Ensure there is at least one file

    result = process_output(invalid_json_folder, path)
    assert result is None


def test_missing_required_parameters():
    with pytest.raises(TypeError, match="missing 1 required positional argument"):
        ExifToolScanner()  # Missing required parameters
