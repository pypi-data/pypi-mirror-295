import pytest
from unittest.mock import patch, MagicMock
import os
import glob
from exifScan.runExifScan import ExifScanner
import tempfile
import shutil
import geopandas as gpd
import pandas as pd
import pyogrio
from shapely.geometry import Point, Polygon
gpd.options.io_engine = "pyogrio"


@pytest.fixture
def setup_test_environment():
    # Create a temporary directory
    test_dir = tempfile.mkdtemp()
    yield test_dir
    # Cleanup after tests
    shutil.rmtree(test_dir)


def test_initialization(setup_test_environment):
    test_dir = setup_test_environment
    scanner = ExifScanner(WorkDirectory=test_dir)

    assert scanner.WorkDirectory == test_dir
    assert scanner.OutputGeopackage == 'Photos.gpkg'
    assert scanner.imageFileExtensions == ['JPG']


def test_scan_for_photos_no_folder(setup_test_environment):
    test_dir = setup_test_environment
    scanner = ExifScanner(WorkDirectory=test_dir)

    with pytest.raises(Exception) as excinfo:
        scanner.scan_for_photos(None)
    assert "Error: ScanFolder is not defined or is False" in str(excinfo.value)


def test_scan_for_photos_empty_folder(setup_test_environment):
    test_dir = setup_test_environment
    empty_folder = os.path.join(test_dir, 'empty_folder')
    os.makedirs(empty_folder)

    scanner = ExifScanner(WorkDirectory=test_dir)
    result = scanner.scan_for_photos(empty_folder)

    assert result == empty_folder


@patch('subprocess.run')
def test_update_data_kart_not_initialized(mock_subprocess_run, setup_test_environment):
    test_dir = setup_test_environment
    scanner = ExifScanner(WorkDirectory=test_dir, KartDirectory=test_dir)

    # Mock subprocess.run to simulate Kart not initialized
    mock_subprocess_run.side_effect = [
        MagicMock(returncode=41),  # First call to kart import
        MagicMock(returncode=0)    # Second call to kart init
    ]

    scanner.kart_writer.import_to_kart()
    scanner.write_HTML()

    # Check that subprocess.run was called with the expected commands
    mock_subprocess_run.assert_any_call(
        ["kart", "import", scanner.OutputGeopackagePath, "--all-tables", "--replace-existing"],
        cwd=test_dir
    )
    mock_subprocess_run.assert_any_call(
        ['kart', 'init', '--import', scanner.OutputGeopackagePath],
        cwd=test_dir
    )


@patch('subprocess.run')
def test_update_data_kart_import_success(mock_subprocess_run, setup_test_environment):
    test_dir = setup_test_environment
    scanner = ExifScanner(WorkDirectory=test_dir, KartDirectory=test_dir)

    # Mock subprocess.run to simulate successful Kart import
    mock_subprocess_run.return_value = MagicMock(returncode=0)

    scanner.kart_writer.import_to_kart()
    scanner.write_HTML()
    # Check that subprocess.run was called with the expected command
    mock_subprocess_run.assert_called_with(
        ["kart", "import", scanner.OutputGeopackagePath, "--all-tables", "--replace-existing"],
        cwd=test_dir
    )


@patch('subprocess.run')
def test_update_data_kart_remote_not_set(mock_subprocess_run, setup_test_environment):
    test_dir = setup_test_environment
    scanner = ExifScanner(WorkDirectory=test_dir, KartDirectory=test_dir, KartRemote='remote_repo')

    # Mock subprocess.run to simulate Kart remote not set
    mock_subprocess_run.side_effect = [
        MagicMock(returncode=0),    # First call to kart import
        MagicMock(returncode=128),  # Second call to kart push
        MagicMock(returncode=0),    # Third call to kart remote add
        MagicMock(returncode=0)     # Fourth call to kart push --set-upstream
    ]

    scanner.kart_writer.import_to_kart()
    scanner.write_HTML()
    # Check that subprocess.run was called with the expected commands
    mock_subprocess_run.assert_any_call(
        ["kart", "import", scanner.OutputGeopackagePath, "--all-tables", "--replace-existing"],
        cwd=test_dir
    )
    mock_subprocess_run.assert_any_call(
        ['kart', 'push'],
        cwd=test_dir
    )
    mock_subprocess_run.assert_any_call(
        ['kart', 'remote', 'add', 'origin', 'remote_repo'],
        cwd=test_dir
    )
    mock_subprocess_run.assert_any_call(
        ['kart', 'push', '--set-upstream', 'origin', 'main'],
        cwd=test_dir
    )


@patch('geopandas.read_file')
@patch('pyogrio.list_layers')
@patch('geopandas.GeoDataFrame.to_file')
def test_removefromGdf(mock_to_file, mock_list_layers, mock_read_file, setup_test_environment):
    test_dir = setup_test_environment
    scanner = ExifScanner(WorkDirectory=test_dir)

    # Create a mock GeoDataFrame for existing data
    existing_data = {
        'SourceFileDir': ['dir1', 'dir2', 'dir3'],
        'Make': ['Canon', 'Nikon', 'Sony'],
        'Model': ['EOS', 'D850', 'A7']
    }

    # Add a geometry column with Point geometries
    geometry = [Point(1, 2), Point(2, 3), Point(3, 4)]
    existing_data['geometry'] = geometry
    existing_gdf = gpd.GeoDataFrame(existing_data, index=[1, 2, 3])
    mock_read_file.return_value = existing_gdf

    # Mock the list of layers
    mock_list_layers.return_value = [('layer1', 'type')]

    # Call the removefromGdf method
    result = scanner.removefromGdf('dir2')

    # Check that read_file was called with the correct arguments
    mock_read_file.assert_called_with(scanner.OutputGeopackagePath, layer='layer1', fid_as_index=True)
    mock_to_file.assert_called_with(scanner.OutputGeopackagePath, layer='layer1', driver="GPKG")
    # Check that the method returns True
    assert result is True


@patch('geopandas.read_file')
def test_removefromGdf_file_not_exist(mock_read_file, setup_test_environment):
    test_dir = setup_test_environment
    scanner = ExifScanner(WorkDirectory=test_dir)

    # Mock read_file to raise DataSourceError
    mock_read_file.side_effect = pyogrio.errors.DataSourceError("File not found")

    # Call the removefromGdf method
    result = scanner.removefromGdf('dir2')

    # Check that the method returns True
    assert result is True


def test_scan_for_photos_with_images(setup_test_environment):
    test_dir = setup_test_environment
    images_folder = os.path.join(test_dir, 'images')
    os.makedirs(images_folder)

    # Copy test images to the temporary directory
    src_images_folder = 'tests/images'
    for file_name in os.listdir(src_images_folder):
        full_file_name = os.path.join(src_images_folder, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, images_folder)

    scanner = ExifScanner(WorkDirectory=test_dir, htmlFolder=test_dir)
    result = scanner.scan_for_photos(images_folder)
    # Check if the output files are created
    exif_output_pattern = os.path.join(test_dir, scanner.ExifOutputFile + '*.json')
    database_output_pattern = os.path.join(test_dir, 'Database*.gpkg')
    matching_exif_files = glob.glob(exif_output_pattern)
    matching_database_files = glob.glob(database_output_pattern)
    assert len(matching_exif_files) == 1  # Ensure exactly one matching file exists
    assert len(matching_database_files) == 1  # Ensure exactly one matching file exists
    assert result == images_folder
    assert os.path.exists(scanner.htmlWriter.mapLocation)
    assert os.path.exists(scanner.metadata_writer.metashape_cache_file)
    assert os.path.exists(scanner.OutputGeopackagePath)
    output = gpd.read_file(scanner.OutputGeopackagePath)
    # Define the 3D polygon coordinates
    coords1 = [
        (172.676957944444, -43.6096788333333, -201.204),
        (172.677330055556, -43.6089029444444, -204.459),
        (172.677897861111, -43.6084271944444, -209.174),
        (172.677254277778, -43.60940975, -201.059),
        (172.676957944444, -43.6096788333333, -201.204)
    ]
    coords2 = [
        (172.759785861111, -43.5664325833333, 6.14),
        (172.759792388889, -43.5664220555556, 4.94),
        (172.759900777778, -43.5664180833333, 8.34),
        (172.759785861111, -43.5664325833333, 6.14)
    ]

    # Create the 3D polygon
    polygon1 = Polygon(coords1)
    polygon2 = Polygon(coords2)
    data = {
        'Make': ['DJI', 'DJI'], 
        'Model': ['FC6310', 'FC6310'], 
        'SourceFileDir': [images_folder.replace("\\", "/"), images_folder.replace("\\", "/")], 
        'Image Count': [3, 4], 
        'CreateDate': ['2019-02-21', '2024-07-09'], 
        'areaSqkm': [9.53602682174712e-06, 0.003264685668783136],
        'geometry': [polygon2,polygon1]}
    
    for key in output.keys():
        assert output[key].tolist() == data[key]
    # repeat to check if duplication is avoided
    result = scanner.scan_for_photos(images_folder)
    output = gpd.read_file(scanner.OutputGeopackagePath)
    for key in output.keys():
        assert output[key].tolist() == data[key]

    new_row = {
        'Make': 'Canon', 'Model': 'EOS 5D Mark IV', 'SourceFileDir': 'non_existant_folder', 'Image Count': 1, 'CreateDate': '2024-08-01', 'areaSqkm': 0.001, 'geometry': polygon1
    }
    new_data = pd.DataFrame([new_row])
    new_gdf = gpd.GeoDataFrame(new_data, geometry='geometry')
    new_gdf.to_file(scanner.OutputGeopackagePath, layer=scanner.gpkg_layer, driver='GPKG', mode='a')

    assert any(new_gdf['Make'] == 'Canon')
    assert any(new_gdf['Model'] == 'EOS 5D Mark IV')
    assert any(new_gdf['CreateDate'] == '2024-08-01')

    # Run the scan again
    result = scanner.scan_for_photos(images_folder)
    output = gpd.read_file(scanner.OutputGeopackagePath)

    # Check if the new row is still present after the scan
    assert any(output['Make'] != 'Canon')
    assert any(output['Model'] != 'EOS 5D Mark IV')
    assert any(output['CreateDate'] != '2024-08-01')

    result = scanner.removefromGdf(images_folder)

    # Check that to_file was called with the filtered GeoDataFrame
    filtered_data = {
        'Make': [], 'Model': [], 'SourceFileDir': [], 'Image Count': [], 'CreateDate': [], 'areaSqkm': [], 'geometry': []
    }
    filtered_output = gpd.read_file(scanner.OutputGeopackagePath)
    for key in filtered_output.keys():
        assert filtered_output[key].tolist() == filtered_data[key]
