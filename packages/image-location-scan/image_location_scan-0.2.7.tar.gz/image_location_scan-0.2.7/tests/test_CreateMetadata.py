import pytest
from unittest.mock import patch
import pandas as pd
from exifScan.CreateMetadata import MetadataWriter
from datetime import datetime as dt, timedelta as td
import os
import logging


@pytest.fixture
def setup_writer():
    WorkDirectory = 'tests/test_folders/metadata'
    metashapeCacheTime = 10
    MetashapeDirectory = '/path/to/metashape'
    os.makedirs(WorkDirectory, exist_ok=True)

    def removeGdf():
        pass

    writer = MetadataWriter(WorkDirectory, metashapeCacheTime, MetashapeDirectory, removeGdf)
    gpdDf = pd.DataFrame({
        'SourceFileDir': ['/path/to/source1', '/path/to/source2']
    })
    return writer, gpdDf


@patch('exifScan.CreateMetadata.os.listdir')
@patch('exifScan.CreateMetadata.pd.read_excel')
def test_locate_and_match_metadata(mock_read_excel, mock_listdir, setup_writer):
    writer, gpdDf = setup_writer
    mock_listdir.return_value = ['metadata.xlsx', '']
    mock_read_excel.return_value = pd.DataFrame({
        'Index': ['col1', 'col2'],
        'Values': ['val1', 'val2']
    }).set_index('Index')

    result = writer.locate_and_match_metadata(gpdDf.copy())
    assert 'Metadata File Location' in result.columns
    print(result)
    assert result.loc[result['SourceFileDir'] == '/path/to/source1', 'Metadata File Location'].values[0] == '\\path\\to\\source1'


@patch('exifScan.CreateMetadata.PsxLocator.main')
@patch('exifScan.CreateMetadata.pickle.load')
@patch('exifScan.CreateMetadata.pickle.dump')
@patch('exifScan.CreateMetadata.os.path.exists')
@patch('exifScan.CreateMetadata.os.path.getmtime')
def test_associate_metashape_projects(mock_getmtime, mock_exists, mock_dump, mock_load, mock_psxlocator, setup_writer, caplog):
    writer, gpdDf = setup_writer
    mock_exists.return_value = False
    mock_psxlocator.return_value = {'/path/to/source1': 'project1'}
    mock_load.return_value = {'/path/to/source1': 'project1'}
    mock_getmtime.return_value = (dt.now() - td(minutes=5)).timestamp()

    with caplog.at_level(logging.INFO):
        result = writer.associate_metashape_projects(gpdDf.copy())
        assert 'Metashape Files' in result.columns
        assert result.loc[result['SourceFileDir'] == '/path/to/source1', 'Metashape Files'].values[0] == 'project1'
        assert 'Using cached Metashape project matches' in caplog.text or 'Metashape data was saved to' in caplog.text or '1 Metashape project file(s) contain images from the database.' in caplog.text
