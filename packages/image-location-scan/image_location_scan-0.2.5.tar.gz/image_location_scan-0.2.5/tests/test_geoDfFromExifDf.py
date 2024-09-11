import pytest
import pandas as pd
import numpy as np
from exifScan.geoDfFromExifDf import GeoDataProcessor
import logging


@pytest.fixture
def setup_processor():
    WorkDirectory = '/path/to/workdir'
    xyTagNames = ['GPSLongitude', 'GPSLatitude']
    zTagName = 'GPSAltitude'
    groupByList = ['CameraModel', 'LensModel']
    processor = GeoDataProcessor(WorkDirectory, xyTagNames, zTagName, groupByList)
    exifDf = pd.DataFrame({
        'SourceFile': ['/path/to/source1/file1.jpg', '/path/to/source2/file2.jpg'],
        'GPSLongitude': [174.7633, np.nan],
        'GPSLatitude': [-36.8485, np.nan],
        'GPSAltitude': [10, np.nan],
        'CreateDate': ['2021:01:01', '2021:01:02'],
        'CameraModel': ['Model1', 'Model2'],
        'LensModel': ['Lens1', 'Lens2']
    })
    return processor, exifDf


def test_process_valid_data(setup_processor, caplog):
    processor, exifDf = setup_processor

    with caplog.at_level(logging.INFO):
        pointsDf, polygonsDf, nonGeoDf = processor.process(exifDf.copy())

        assert not pointsDf.empty
        assert not polygonsDf.empty
        assert 'Handling geolocated images' in caplog.text or 'Points created' in caplog.text or 'Grouped points into polygons' in caplog


def test_process_invalid_data(setup_processor, caplog):
    processor, exifDf = setup_processor
    exifDf['GPSLongitude'] = np.nan
    exifDf['GPSLatitude'] = np.nan

    with caplog.at_level(logging.INFO):
        pointsDf, polygonsDf, nonGeoDf = processor.process(exifDf.copy())

        assert pointsDf.empty
        assert polygonsDf.empty
        assert not nonGeoDf.empty
        assert 'Handling non-geolocated images' in caplog.text or 'images are not geolocated' in caplog.text


def test_process_mixed_data(setup_processor, caplog):
    processor, exifDf = setup_processor
    exifDf.loc[1, 'GPSLongitude'] = 174.7633
    exifDf.loc[1, 'GPSLatitude'] = -36.8485

    with caplog.at_level(logging.INFO):
        pointsDf, polygonsDf, nonGeoDf = processor.process(exifDf.copy())

        assert not pointsDf.empty
        assert not polygonsDf.empty
        assert nonGeoDf.empty
        assert 'Handling geolocated images' in caplog.text or 'images are geolocated' in caplog.text
