import folium
import geopandas as gpd
import pandas.api.types as pdapi
import pandas as pd
from exifScan.creditosfolium.creditosfolium import Creditos
import logging
import pyogrio.errors as pe
import os
from exifScan.generateHTML import generateHTMLSnippets
from bs4 import BeautifulSoup
import shutil


class HTMLWriter:

    def __init__(self, OutputGeopackagePath, htmlFolder, mapFileName, otherMapLayers=[], otherMapLayerNames=None, splitSize=100, linzAPIKey=None):
        self.OutputGeopackagePath = OutputGeopackagePath
        self.htmlFolder = htmlFolder
        self.mapFileName = mapFileName
        self.otherMapLayers = otherMapLayers
        self.otherMapLayerNames = otherMapLayerNames
        self.splitSize = splitSize
        self.mapLocation = os.path.join(htmlFolder, mapFileName) if htmlFolder else None
        self.original_color_list = ['#66C5CC', '#F6CF71', '#F89C74', '#DCB0F2', '#87C55F', '#9EB9F3', '#FE88B1', '#C9DB74', '#8BE0A4', '#B497E7', '#D3B484', '#B3B3B3']
        self.dataCategories = ['Historical Aerial Imagery']
        self.linzAPIKey = linzAPIKey
        if self.htmlFolder:
            module_dir = os.path.dirname(os.path.abspath(__file__))
            # List of files to copy
            files_to_copy = ['styles.css', 'info.jpg', 'nouislider.min.css', 'nouislider.min.js']

            # Iterate over the array of files and copy each one
            for file_name in files_to_copy:
                src_path = os.path.join(module_dir, file_name)
                dest_path = os.path.join(self.htmlFolder, file_name)
                shutil.copyfile(src_path, dest_path)
                logging.debug(f'Saved {file_name} at {dest_path}')

    def updateHTML(self, info):

        mapGdf = gpd.read_file(self.OutputGeopackagePath, layer='allGroupedData')

        # Clean and organise mapGdf into categories

        mapGdf = mapGdf.drop('fid', axis=1, errors='ignore')
        # convert back to forward slash to make it easy to copy paste
        mapGdf['SourceFileDir'] = mapGdf['SourceFileDir'].str.replace('/', '\\')
        if 'Metashape Files' in mapGdf:
            mapGdf['Metashape Files'] = mapGdf['Metashape Files'].str.replace('/', '\\')

        # split data into categories
        categorisedGdfs = {}
        # ensure Geotagged photos is at the top of the list.
        categorisedGdfs['Geotagged photos'] = mapGdf
        if 'Type' in mapGdf.columns:
            for category in self.dataCategories:
                # Filter the GeoDataFrame for the current category
                categoryGdf = mapGdf[mapGdf['Type'] == category]

                # Remove the filtered rows from the original GeoDataFrame
                mapGdf = mapGdf[mapGdf['Type'] != category].copy()
                if len(categoryGdf):
                    categorisedGdfs[category] = categoryGdf

        # remove oversized
        oversized = mapGdf[mapGdf['areaSqkm'] > self.splitSize]
        mapGdf = mapGdf.copy()[mapGdf['areaSqkm'] < self.splitSize]
        if len(mapGdf):
            categorisedGdfs['Geotagged photos'] = mapGdf
        else:
            del categorisedGdfs['Geotagged photos']

        for _, row in oversized.iterrows():
            folder = row['SourceFileDir']
            size = row['areaSqkm']
            logging.warning(f'Folder {folder} is oversized : {size} km2. Please check the folder for unrelated data.')

        # a dict containing the elements to be added to the map
        mapElements = {}
        copyButtonString = ''

        if self.mapLocation:

            # Create a map centered at the centroid of your geodata - centroid not currently used..

            # Calculate the centroid of all geometries
            # centroid = mapGdf.unary_union.centroid
            # logging.debug(f'centroid location: {centroid.y}, {centroid.x}')

            m = folium.Map(location=[-43.58911567661342, 170.00244140625003], zoom_start=7)

            # add Linz basemaps
            if self.linzAPIKey:
                mapTypes = ['aerial']
                for i, mapType in enumerate(mapTypes):
                    urlTemplate = f'https://basemaps.linz.govt.nz/v1/tiles/{mapType}/WebMercatorQuad/{{z}}/{{x}}/{{y}}.webp?api={self.linzAPIKey}'
                    folium.TileLayer(
                        tiles=urlTemplate,
                        attr='Basemap attribution: Sourced from LINZ. CC BY 4.0',
                        name=f'LINZ Data Service - {mapType}',
                        max_zoom=20,
                    ).add_to(m)

            # add Creditos at bottom right.

            content = '<br/> Use the range slider to filter data by Date.<br/>If several features are overlapping, try right-clicking on the feature.'
            if info:
                content = info + content
            Creditos(
                imageurl="info.jpg",
                imagealt="Information Icon",
                tooltip="Information",
                width="36px",
                height="36px",
                expandcontent=content,
            ).add_to(m)

            # add map data.
            # a copy button to copy the file path in the table.
            copyButtonString = generateHTMLSnippets.copyButton()
            dfs = list(categorisedGdfs.values())

            # Find the earliest year
            earliest_year = find_earliest_year(dfs)
            for k, v in categorisedGdfs.items():
                category_id = k.replace(' ', '_')

                addExifLayerToMap(v, k, m, category_id, mapElements)
                copyButtonString += f'makeCellsCopyable("table{category_id}", "SourceFileDir");'

            if self.otherMapLayers:
                for i, layerPath in enumerate(self.otherMapLayers):

                    try:
                        if self.otherMapLayerNames and self.otherMapLayerNames[i]:
                            otherGdf = gpd.read_file(layerPath, layer=self.otherMapLayerNames[i])
                        else:
                            otherGdf = gpd.read_file(layerPath)

                        otherGdf = sanitiseTableGdf(otherGdf)
                        otherGdf = otherGdf.to_crs(epsg=4326)

                        layername = self.otherMapLayerNames[i] if self.otherMapLayerNames else f'Layer {i + 1}'

                        tableDataOther = otherGdf.drop('geometry', axis=1)
                        mapElements[layername] = {}

                        mapElements[layername]['table'] = tableDataOther

                        popupOther = folium.GeoJsonPopup(fields=tableDataOther.columns.tolist(), labels=True, class_name="mystyle", max_width="860px")

                        # shim for sfmData gdb
                        def style_function(feature):
                            year = feature['properties'].get('Photographed_On', None)
                            if year:
                                className = f"year-{year.split('-')[0]} animateVisibility {layername}"
                            else:
                                className = f"animateVisibility {layername}"

                            return {
                                'className': className,
                                'fillOpacity': 0.1
                            }

                        otherGeojson = folium.GeoJson(data=otherGdf, show=False, popup=popupOther, class_name='animateVisibility ' + layername, name=layername, style_function=style_function, highlight_function=lambda feature: {'fillOpacity': 0.5})
                        otherGeojson.add_to(m)
                        mapElements[layername]['geojson'] = otherGeojson

                    except pe.DataSourceError:
                        logging.exception(f'{layerPath} does not exist in the file system, and is not recognized as a supported dataset name.')
                    except Exception as e:
                        logging.exception(f'Unexpected error: {e}')

            folium.LayerControl().add_to(m)

            # add geojson css styling to file.
            geojson_styling = '<style>'
            color_list = self.original_color_list.copy()
            for name, value in mapElements.items():
                if 'geojson' in value:
                    geojson_styling += generateHTMLSnippets.cssColors_for_geojson(name, color_list, mapElements)
            geojson_styling += '</style>'
            m.get_root().header.add_child(folium.Element(geojson_styling))

            rightclickJS = generateHTMLSnippets.rightClick(mapElements)
            m.get_root().html.add_child(folium.Element(rightclickJS))

            m.get_root().html.add_child(folium.JavascriptLink('nouislider.min.js'))
            # Link your CSS file to the map
            m.get_root().header.add_child(folium.CssLink('styles.css'))
            m.get_root().header.add_child(folium.CssLink('nouislider.min.css'))

            m.add_css_link(
                "bootstrap_css",
                'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.3.0/css/bootstrap.min.css'
            )
            m.add_js_link(
                "bootstrap_js",
                'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.3.0/js/bootstrap.bundle.min.js'
            )

            # Create the HTML for the button
            bottom_left_ui = '''
            <div class="container custom-container">
                <div class="row align-items-center">
                    <div class="col-2">
                        <button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasScrolling" aria-controls="offcanvasBottom">Show Table</button>
                    </div>
                    <div class="col-6">
                        <div id="sliderContainer">
                        </div>
                    </div>
                </div>
            </div>
            '''

            # Create a Folium element with the HTML
            element = folium.Element(bottom_left_ui)

            # Add the element to the map
            m.get_root().html.add_child(element)

            m.save(self.mapLocation)

            # Save it to an HTML file

            logging.info(f'Saved new map at {self.mapLocation}')

            # Open the HTML file and parse it
            with open(self.mapLocation, 'r') as f:
                soup = BeautifulSoup(f, 'html.parser')

            new_title = soup.new_tag('title')
            new_title.string = "Map"

            # Add the <title> tag to the <head> section
            soup.head.append(new_title)
            # Add a link to a CSS file in the header
            head = soup.head
            link2 = soup.new_tag('link', rel='stylesheet', href='https://cdn.datatables.net/2.0.2/css/dataTables.bootstrap5.css')
            script3 = soup.new_tag('script', src='https://cdn.datatables.net/2.0.2/js/dataTables.js')
            script4 = soup.new_tag('script', src='https://cdn.datatables.net/2.0.2/js/dataTables.bootstrap5.js')
            head.append(link2)
            head.append(script3)
            head.append(script4)

            body = soup.body

            # Add some HTML content in the body

            # Create navlink, tab and js for the geotagged images table

            navlinks = []
            tabsContent = []
            jsContent = [generateHTMLSnippets.year_filter_slider(earliest_year)]

            # Create navlink, tab and js for other tables

            for key, value in mapElements.items():
                name = key
                el_id = key.replace(' ', '_')

                if 'geojson' in value:
                    geojson_element = value['geojson']
                    head.append(generateHTMLSnippets.zoomOnEl(soup, m.get_name(), f'table{el_id}', geojson_element.get_name()))
                if 'table' in value:
                    table_element = value['table']

                    navlinks.append(generateHTMLSnippets.navLink(el_id, name, name == 'Geotagged photos'))
                    tabsContent.append(generateHTMLSnippets.tabDivs(el_id, name, table_element, name == 'Geotagged photos'))
                    jsContent.append(generateHTMLSnippets.tableJs(el_id))

            # concatenate all the html as strings

            html = generateHTMLSnippets.HTMLTail(navlinks, tabsContent, jsContent, copyButtonString)
            body.append(BeautifulSoup(html, 'html.parser'))
            # Write the changes back to the HTML file
            with open(self.mapLocation, 'w') as f:
                f.write(str(soup))

            logging.debug(f'Added table at {self.mapLocation}')


def sanitiseTableGdf(gdf):
    for col in gdf.columns:
        # If the column is of datetime type
        if pd.api.types.is_datetime64_any_dtype(gdf[col]):
            # Convert the column to string
            gdf[col] = gdf[col].astype(str)
    gdf['index'] = gdf.index

    return gdf


def addExifLayerToMap(gdf, name, m, layer_id, mapElementsDict):
    # Create a DataFrame with the feature data
    data = gdf.drop('geometry', axis=1)
    gdf = gdf.to_crs(epsg=4326)

    # Extract the year and find the earliest year

    categoryTableData = sanitiseTableGdf(data)
    mapElementsDict[name] = {}
    mapElementsDict[name]['table'] = categoryTableData

    # make the SourceFileDir copyable. See rightClick.js for other part of applicable code
    gdf['SourceFileDir'] = gdf['SourceFileDir'] + '<div class="copyText"></div>'

    # make the Metashape Files copyable. See rightClick.js for other part of applicable code
    if 'Metashape Files' in gdf.columns:
        gdf['Metashape Files'] = gdf['Metashape Files'].str.replace('.psx,\n', '.psx<div class="copyText"></div></span><span>')
        gdf['Metashape Files'] = gdf['Metashape Files'].apply(
            lambda x: f'<span>{x}<div class="copyText"></div></span>' if x else x
        )

    # Create a GeoJsonPopup
    popup = folium.GeoJsonPopup(fields=data.columns.tolist(), labels=True, class_name="mystyle", max_width="860px",)

    # Create a GeoJson object with the popup
    mapCopy = gdf.copy()
    mapCopy['index'] = mapCopy.index
    # only show geotagged images layer on load.
    show = (name == 'Geotagged photos')

    def style_function(feature):
        year = feature['properties']['CreateDate'].split('-')[0]
        return {
            'className': f"year-{year} animateVisibility {layer_id}",
            'fillOpacity': 0.1
        }
    geojson = folium.GeoJson(data=mapCopy, name=name, show=show, popup=popup, popup_keep_highlighted=True, style_function=style_function, highlight_function=lambda feature: {'fillOpacity': 0.8})

    mapElementsDict[name]['geojson'] = geojson

    # Add the GeoJson object to the map
    m.add_child(geojson)
    logging.debug(f"{name} added to the map. It has {len(gdf)} features.")

# Function to find the earliest year across multiple DataFrames


def find_earliest_year(dfs):
    earliest_year = float('inf')  # Initialize with a very large number
    for df in dfs:
        temp_dates = pd.to_datetime(df['CreateDate'])
        min_year = temp_dates.dt.year.min()
        if min_year < earliest_year:
            earliest_year = min_year
    return earliest_year


# Example event code- poorly documented so leaving it here.
# from folium.utilities import JsCode
# from folium.elements import EventHandler

# highlight = JsCode(
#     """
#    function highlight(e) {
#        console.log(e)
#    }
# """
# )

# reset = JsCode(
#     """
#    function reset(e) {
#       e.target.setStyle({ color: e.target.original_color });
#    }
# """
# )

# geojson.add_child(EventHandler("load", highlight))
# geojson.add_child(EventHandler("mouseout", reset))
