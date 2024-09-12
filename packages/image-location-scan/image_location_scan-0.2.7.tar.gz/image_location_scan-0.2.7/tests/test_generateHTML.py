import geopandas as gpd
import os
import pytest
from exifScan.generateHTML.createHTML import HTMLWriter  # Replace 'exifScan.generateHTML.createHTML' with the actual module name
import tempfile
from shapely.geometry import Point
import logging
from bs4 import BeautifulSoup
import shutil


@pytest.fixture
def setup_test_environment():
    # Create a temporary directory
    test_dir = tempfile.mkdtemp()
    yield test_dir
    # Cleanup after tests
    # shutil.rmtree(test_dir)


def test_html_writer_initialization(setup_test_environment):
    # Test data
    test_dir = setup_test_environment
    OutputGeopackagePath = "path/to/geopackage"
    htmlFolder = test_dir
    mapFileName = "map.html"
    otherMapLayers = ["layer1", "layer2"]
    otherMapLayerNames = ["Layer 1", "Layer 2"]
    splitSize = 10

    # Create an instance of HTMLWriter
    writer = HTMLWriter(OutputGeopackagePath, htmlFolder, mapFileName, otherMapLayers, otherMapLayerNames, splitSize)

    # Assertions
    assert writer.OutputGeopackagePath == OutputGeopackagePath
    assert writer.htmlFolder == htmlFolder
    assert writer.mapFileName == mapFileName
    assert writer.otherMapLayers == otherMapLayers
    assert writer.otherMapLayerNames == otherMapLayerNames
    assert writer.splitSize == splitSize
    assert writer.mapLocation == os.path.join(htmlFolder, mapFileName)
    assert writer.original_color_list == ['#66C5CC', '#F6CF71', '#F89C74', '#DCB0F2', '#87C55F', '#9EB9F3', '#FE88B1', '#C9DB74', '#8BE0A4', '#B497E7', '#D3B484', '#B3B3B3']


@pytest.fixture
def html_writer(setup_test_environment):
    test_dir = setup_test_environment
    layer_1_dir = os.path.join(test_dir, "layer_1.shp")
    layer_2_dir = os.path.join(test_dir, "layer_2.shp")

    return HTMLWriter(
        OutputGeopackagePath=os.path.join(test_dir, "test.gpkg"),
        htmlFolder=test_dir,
        mapFileName="map.html",
        otherMapLayers=[layer_1_dir, layer_2_dir],
        # otherMapLayerNames=["Layer 1", "Layer 2"],
        splitSize=10
    )


def test_updateHTML(html_writer, setup_test_environment, caplog):
    test_dir = setup_test_environment
    # Create a mock GeoDataFrame for existing data
    test_data = {
        'SourceFileDir': ['dir1', 'dir2', 'dir3'],
        'Make': ['Canon', 'Nikon', 'Sony'],
        'Model': ['EOS', 'D850', 'A7'],
        'areaSqkm': [1, 2, 3],
        'CreateDate': ['1990-03-03', '1991-06-27', '1992-12-12']
    }

    # Add a geometry column with Point geometries
    geometry = [Point(1, 2), Point(2, 3), Point(3, 4)]
    test_gdf = gpd.GeoDataFrame(test_data, index=[1, 2, 3], crs="EPSG:4326", geometry=geometry)
    test_gdf.to_file(os.path.join(test_dir, "test.gpkg"), layer='allGroupedData', driver="GPKG")
    test_gdf.to_file(html_writer.otherMapLayers[0], driver="ESRI Shapefile")
    test_gdf.to_file(html_writer.otherMapLayers[1], driver="ESRI Shapefile")
    with caplog.at_level(logging.INFO):
        html_writer.updateHTML(None)

    assert os.path.exists(os.path.join(test_dir, "map.html"))
    with open(os.path.join(test_dir, "map.html"), 'r') as file:
        map_html_content = file.read()
    assert "<html>" in map_html_content  # Basic check to see if it's an HTML file
    assert map_html_content.count("<html>") == 1, "There should be exactly one occurrence of '<html>'"
    assert map_html_content.count("</html>") == 1, "There should be exactly one occurrence of '</html>'"
    assert "Layer 1" in map_html_content  # Check if the layer name is included
    soup = BeautifulSoup(map_html_content, 'html.parser')
    # Example assertions
    assert soup.title.string == "Map"
    # Check for the folium map div
    folium_map = soup.find('div', class_='folium-map')
    assert folium_map is not None

    # Check for the offcanvas div
    offcanvas = soup.find('div', id='offcanvasScrolling')
    assert offcanvas is not None
    assert offcanvas['aria-labelledby'] == 'offcanvasScrollingLabel'
    assert offcanvas['class'] == ['offcanvas', 'offcanvas-bottom']
    assert offcanvas['data-bs-backdrop'] == 'false'
    assert offcanvas['data-bs-scroll'] == 'true'
    assert offcanvas['tabindex'] == '-1'

    # Check for the offcanvas header
    offcanvas_header = offcanvas.find('div', class_='offcanvas-header')
    assert offcanvas_header is not None

    # Check for the offcanvas body
    offcanvas_body = offcanvas.find('div', class_='offcanvas-body')
    assert offcanvas_body is not None

    # Check for the nav tabs
    nav_tabs = offcanvas_body.find('div', class_='nav nav-tabs')
    assert nav_tabs is not None

    # Check for the tab content
    tab_content = offcanvas_body.find('div', class_='tab-content')
    assert tab_content is not None

    # Check for the table
    table = tab_content.find('table', id='tableGeotagged_photos')
    assert table is not None
    assert table['class'] == ['dataframe', 'table', 'table-striped', 'responsive']

    # Check for table headers
    headers = table.find_all('th')
    assert len(headers) == 10
    assert headers[1].string == 'SourceFileDir'
    assert headers[2].string == 'Make'
    assert headers[3].string == 'Model'
    assert headers[4].string == 'areaSqkm'
    assert headers[5].string == 'CreateDate'
    assert headers[6].string == 'index'
    # Each row had a th for some reason?
    assert headers[7].string == '0'
    assert headers[8].string == '1'
    assert headers[9].string == '2'

    # Check for table rows
    rows = table.find_all('tr')
    assert len(rows) == 4  # Including header row
    assert rows[1].find_all('td')[0].string == 'dir1'
    assert rows[1].find_all('td')[1].string == 'Canon'
    assert rows[1].find_all('td')[2].string == 'EOS'
    assert rows[1].find_all('td')[3].string == '1'
    assert rows[1].find_all('td')[4].string == '1990-03-03'
    assert rows[1].find_all('td')[5].string == '0'
    assert rows[2].find_all('td')[0].string == 'dir2'
    assert rows[2].find_all('td')[1].string == 'Nikon'
    assert rows[2].find_all('td')[2].string == 'D850'
    assert rows[2].find_all('td')[3].string == '2'
    assert rows[2].find_all('td')[4].string == '1991-06-27'
    assert rows[2].find_all('td')[5].string == '1'
    assert rows[3].find_all('td')[0].string == 'dir3'
    assert rows[3].find_all('td')[1].string == 'Sony'
    assert rows[3].find_all('td')[2].string == 'A7'
    assert rows[3].find_all('td')[3].string == '3'
    assert rows[3].find_all('td')[4].string == '1992-12-12'
    assert rows[3].find_all('td')[5].string == '2'

    # Check Scripts
    # Extract the script content
    script_content_1 = soup.findAll('script')[9].string
    # Check if the script content contains the expected values
    assert "const table = document.getElementById( 'tableGeotagged_photos' );" in script_content_1
    # Extract the script content
    script_content_2 = soup.findAll('script')[10].string
    # Check if the script content contains the expected values
    assert "const table = document.getElementById( 'tableLayer_1' );" in script_content_2
    script_content_3 = soup.findAll('script')[11].string
    # Check if the script content contains the expected values
    assert "const table = document.getElementById( 'tableLayer_2' );" in script_content_3
    # Check if the script content contains the expected values
    script_content_4 = soup.findAll('script')[12].string
    assert 'Geotagged photos": "#8BE0A4"' in script_content_4
    assert '"Layer 1": "#F6CF71"' in script_content_4
    assert '"Layer 2": "#C9DB74"' in script_content_4
    script_content_5 = soup.findAll('script')[14].string
    assert "('#tableGeotagged_photos').DataTable({responsive:true});" in script_content_5
    assert "('#tableLayer_1').DataTable({responsive:true});" in script_content_5
    assert "('#tableLayer_2').DataTable({responsive:true});" in script_content_5
    script_content_6 = soup.findAll('script')[15].string
    assert 'makeCellsCopyable("tableGeotagged_photos", "SourceFileDir");' in script_content_6

    test_gdf['areaSqkm'] = [1, 2, 30]
    test_gdf.to_file(os.path.join(test_dir, "test.gpkg"), layer='allGroupedData')
    with caplog.at_level(logging.INFO):
        html_writer.updateHTML(None)
    with open(os.path.join(test_dir, "map.html"), 'r') as file:
        map_html_content = file.read()
    soup = BeautifulSoup(map_html_content, 'html.parser')
    offcanvas = soup.find('div', id='offcanvasScrolling')
    # Check for the offcanvas div
    offcanvas = soup.find('div', id='offcanvasScrolling')
    assert offcanvas is not None
    assert offcanvas['aria-labelledby'] == 'offcanvasScrollingLabel'
    assert offcanvas['class'] == ['offcanvas', 'offcanvas-bottom']
    assert offcanvas['data-bs-backdrop'] == 'false'
    assert offcanvas['data-bs-scroll'] == 'true'
    assert offcanvas['tabindex'] == '-1'

    # Check for the offcanvas header
    offcanvas_header = offcanvas.find('div', class_='offcanvas-header')
    assert offcanvas_header is not None

    # Check for the offcanvas body
    offcanvas_body = offcanvas.find('div', class_='offcanvas-body')
    assert offcanvas_body is not None

    # Check for the nav tabs
    nav_tabs = offcanvas_body.find('div', class_='nav nav-tabs')
    assert nav_tabs is not None

    # Check for the tab content
    tab_content = offcanvas_body.find('div', class_='tab-content')
    assert tab_content is not None

    # Check for the table
    table = tab_content.find('table', id='tableGeotagged_photos')
    assert table is not None
    assert table['class'] == ['dataframe', 'table', 'table-striped', 'responsive']

    # Check for table headers
    headers = table.find_all('th')

    assert len(headers) == 9
    assert headers[1].string == 'SourceFileDir'
    assert headers[2].string == 'Make'
    assert headers[3].string == 'Model'
    assert headers[4].string == 'areaSqkm'
    assert headers[5].string == 'CreateDate'
    assert headers[6].string == 'index'
    # Each row had a th for some reason?
    assert headers[7].string == '0'
    assert headers[8].string == '1'

    # Check for table rows
    rows = table.find_all('tr')
    assert len(rows) == 3  # Including header row
    assert rows[1].find_all('td')[0].string == 'dir1'
    assert rows[1].find_all('td')[1].string == 'Canon'
    assert rows[1].find_all('td')[2].string == 'EOS'
    assert rows[1].find_all('td')[3].string == '1'
    assert rows[1].find_all('td')[4].string == '1990-03-03'
    assert rows[1].find_all('td')[5].string == '0'
    assert rows[2].find_all('td')[0].string == 'dir2'
    assert rows[2].find_all('td')[1].string == 'Nikon'
    assert rows[2].find_all('td')[2].string == 'D850'
    assert rows[2].find_all('td')[3].string == '2'
    assert rows[2].find_all('td')[4].string == '1991-06-27'
    assert rows[2].find_all('td')[5].string == '1'

    test_gdf['Type'] = [None, None, 'Historical Aerial Imagery']
    test_gdf.to_file(os.path.join(test_dir, "test.gpkg"), layer='allGroupedData')
    with caplog.at_level(logging.DEBUG):
        html_writer.updateHTML(None)
    with open(os.path.join(test_dir, "map.html"), 'r') as file:
        map_html_content = file.read()
    soup = BeautifulSoup(map_html_content, 'html.parser')
    offcanvas = soup.find('div', id='offcanvasScrolling')
    # Check for the offcanvas div
    offcanvas = soup.find('div', id='offcanvasScrolling')
    assert offcanvas is not None
    assert offcanvas['aria-labelledby'] == 'offcanvasScrollingLabel'
    assert offcanvas['class'] == ['offcanvas', 'offcanvas-bottom']
    assert offcanvas['data-bs-backdrop'] == 'false'
    assert offcanvas['data-bs-scroll'] == 'true'
    assert offcanvas['tabindex'] == '-1'

    # Check for the offcanvas header
    offcanvas_header = offcanvas.find('div', class_='offcanvas-header')
    assert offcanvas_header is not None

    # Check for the offcanvas body
    offcanvas_body = offcanvas.find('div', class_='offcanvas-body')
    assert offcanvas_body is not None

    # Check for the nav tabs
    nav_tabs = offcanvas_body.find('div', class_='nav nav-tabs')
    assert nav_tabs is not None

    # Check for the tab content
    tab_content = offcanvas_body.find('div', class_='tab-content')
    assert tab_content is not None

    # Check for the table
    table = tab_content.find('table', id='tableGeotagged_photos')
    assert table is not None
    assert table['class'] == ['dataframe', 'table', 'table-striped', 'responsive']

    # Check for table headers
    headers = table.find_all('th')

    assert len(headers) == 10
    assert headers[1].string == 'SourceFileDir'
    assert headers[2].string == 'Make'
    assert headers[3].string == 'Model'
    assert headers[4].string == 'areaSqkm'
    assert headers[5].string == 'CreateDate'
    assert headers[6].string == 'Type'
    assert headers[7].string == 'index'
    # Each row had a th for some reason?
    assert headers[8].string == '0'
    assert headers[9].string == '1'

    # Check for table rows
    rows = table.find_all('tr')
    assert len(rows) == 3  # Including header row
    assert rows[1].find_all('td')[0].string == 'dir1'
    assert rows[1].find_all('td')[1].string == 'Canon'
    assert rows[1].find_all('td')[2].string == 'EOS'
    assert rows[1].find_all('td')[3].string == '1'
    assert rows[1].find_all('td')[4].string == '1990-03-03'
    assert rows[1].find_all('td')[5].string == 'None'
    assert rows[1].find_all('td')[6].string == '0'
    assert rows[2].find_all('td')[0].string == 'dir2'
    assert rows[2].find_all('td')[1].string == 'Nikon'
    assert rows[2].find_all('td')[2].string == 'D850'
    assert rows[2].find_all('td')[3].string == '2'
    assert rows[2].find_all('td')[4].string == '1991-06-27'
    assert rows[2].find_all('td')[5].string == 'None'
    assert rows[2].find_all('td')[6].string == '1'

    # Check for the table
    table = tab_content.find('table', id='tableHistorical_Aerial_Imagery')
    assert table is not None
    assert table['class'] == ['dataframe', 'table', 'table-striped', 'responsive']

    # Check for table headers
    headers = table.find_all('th')

    assert len(headers) == 9
    assert headers[1].string == 'SourceFileDir'
    assert headers[2].string == 'Make'
    assert headers[3].string == 'Model'
    assert headers[4].string == 'areaSqkm'
    assert headers[5].string == 'CreateDate'
    assert headers[6].string == 'Type'
    # Each row had a th for some reason?
    assert headers[7].string == 'index'
    assert headers[8].string == '2'

    # Check for table rows
    rows = table.find_all('tr')
    assert len(rows) == 2  # Including header row
    assert rows[1].find_all('td')[0].string == 'dir3'
    assert rows[1].find_all('td')[1].string == 'Sony'
    assert rows[1].find_all('td')[2].string == 'A7'
    assert rows[1].find_all('td')[3].string == '30'
    assert rows[1].find_all('td')[4].string == '1992-12-12'
    assert rows[1].find_all('td')[5].string == 'Historical Aerial Imagery'
    assert rows[1].find_all('td')[6].string == '2'
    # assert not updated_gdf.empty
    # assert 'geometry' in updated_gdf.columns
    # Assuming updateHTML splits data into multiple files if it exceeds splitSize
    # Check if multiple files are created or if the data is split correctly
    # Check Scripts
    # Extract the script content
    script_content_1 = soup.findAll('script')[9].string
    # Check if the script content contains the expected values
    assert "const table = document.getElementById( 'tableGeotagged_photos' );" in script_content_1
    # Extract the script content
    script_content_1a = soup.findAll('script')[10].string
    # Check if the script content contains the expected values
    assert "const table = document.getElementById( 'tableHistorical_Aerial_Imagery' );" in script_content_1a
    script_content_2 = soup.findAll('script')[11].string
    # Check if the script content contains the expected values
    assert "const table = document.getElementById( 'tableLayer_1' );" in script_content_2
    script_content_3 = soup.findAll('script')[12].string
    # Check if the script content contains the expected values
    assert "const table = document.getElementById( 'tableLayer_2' );" in script_content_3
    # Check if the script content contains the expected values
    script_content_4 = soup.findAll('script')[13].string
    assert 'Geotagged photos": "#8BE0A4"' in script_content_4
    assert '"Historical Aerial Imagery": "#B497E7"' in script_content_4
    assert '"Layer 1": "#B3B3B3"' in script_content_4
    assert '"Layer 2": "#C9DB74"' in script_content_4
    script_content_5 = soup.findAll('script')[15].string
    assert "('#tableGeotagged_photos').DataTable({responsive:true});" in script_content_5
    assert "('#tableHistorical_Aerial_Imagery').DataTable({responsive:true});" in script_content_5
    assert "('#tableLayer_1').DataTable({responsive:true});" in script_content_5
    assert "('#tableLayer_2').DataTable({responsive:true});" in script_content_5
    script_content_6 = soup.findAll('script')[16].string
    assert 'makeCellsCopyable("tableGeotagged_photos", "SourceFileDir");' in script_content_6
    # read number of rows in data.
    try:
        html_writer.updateHTML(None)
    except Exception as e:
        assert False, f"updateHTML raised an exception: {e}"
