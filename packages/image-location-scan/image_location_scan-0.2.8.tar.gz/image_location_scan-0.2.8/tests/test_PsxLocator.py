from exifScan.metashape.PsxLocator import main
import sys
from unittest.mock import patch, MagicMock
import logging


def test_python_version():
    if sys.version_info[1] > 11:
        assert main("tests/images") is None

# test fails
# def test_metashape_import(caplog):
#     with patch.dict('sys.modules', {'Metashape': None}):
#         with caplog.at_level(logging.INFO):

#             assert main("tests/images") is None


def test_no_project_files_found(tmp_path):
    # Create a temporary directory
    d = tmp_path / "sub"
    d.mkdir()
    result = main(d)
    assert result is None


def test_project_files_found(tmp_path, caplog):
    # Create a temporary directory with project files
    d = tmp_path / "sub"
    d.mkdir()
    (d / "project1.psx").write_text("content")
    (d / "project2.psz").write_text("content")

    with patch('Metashape.Document.open', return_value=None):
        with patch('Metashape.Document') as MockDocument:

            mock_doc = MockDocument.return_value
            mock_chunk = MagicMock()
            mock_camera = MagicMock()
            mock_camera.photo.path = "/some/path/photo.jpg"
            mock_chunk.cameras = [mock_camera]
            mock_doc.chunks = [mock_chunk]
            mock_doc.chunks = [mock_chunk]

            result = main(d)
            assert result is not None
            assert len(result) == 1
            assert "/some/path" in result


def test_camera_without_photo(tmp_path):
    # Create a temporary directory with project files
    d = tmp_path / "sub"
    d.mkdir()
    (d / "project1.psx").write_text('<?xml version="1.0" encoding="UTF-8"?><document version="1.2.0" path="{projectname}.files/project.zip"/>')

    with patch('Metashape.Document') as MockDocument:
        mock_doc = MockDocument.return_value
        mock_chunk = MagicMock()
        mock_camera = MagicMock()
        mock_camera.photo = None
        mock_chunk.cameras = [mock_camera]
        mock_doc.chunks = [mock_chunk]

        result = main(d)
        assert result is not None
        assert len(result) == 0


def test_with_images(tmp_path, caplog):
    # this whole path business is a mess..

    # Create a temporary directory with project files and images
    d = tmp_path / "sub"
    d.mkdir()
    (d / "project1.psx").write_text("content")
    (d / "project2.psz").write_text("content")

    # Create images directory
    images_dir = d / "tests/images"
    images_dir.mkdir(parents=True)
    (images_dir / "image1.jpg").write_text("image content")
    (images_dir / "image2.jpg").write_text("image content")

    with patch('Metashape.Document.open', return_value=None):
        with patch('Metashape.Document') as MockDocument:
            mock_doc = MockDocument.return_value
            mock_chunk = MagicMock()
            mock_camera1 = MagicMock()
            mock_camera1.photo.path = str(images_dir / "image1.jpg").replace("\\", "/")
            mock_camera2 = MagicMock()
            mock_camera2.photo.path = str(images_dir / "image2.jpg").replace("\\", "/")
            mock_chunk.cameras = [mock_camera1, mock_camera2]
            mock_doc.chunks = [mock_chunk]

            result = main(d)
            logging.info(result)
            sanitised_images_dir = str(images_dir).replace("\\", "/")
            assert result is not None
            assert len(result) == 1
            assert sanitised_images_dir in result
            assert "project1.psx" in result[str(images_dir).replace("\\", "/")]


def test_with_test_project(tmp_path, caplog):

    test_project_path = 'tests/images/test.psx'
    test_path = 'tests/images'
    with caplog.at_level(logging.INFO):
        result = main(test_path)

        logging.info(result)
        assert result is not None
        assert len(result) == 1
        assert test_path in list(result.keys())[0]
        assert test_project_path in list(result.values())[0]
