# This script is made to be run from
# \\file\Shared\SEESPostGrad\JD\Geospatial database\scripts
# and has ExifScanJSON.py, PsxLocator.py and CreateMetadata.py
# as dependencies. As well as the obvious python dependencies,
# it also needs the Metashape script api installed with a
# functioning license in the folder, license in the host@port format.
# JD 23/01/2020

from datetime import datetime as dt
import os

import geopandas as gpd
import pandas as pd
import subprocess
import pyogrio
import logging
from exifScan.CreateMetadata import MetadataWriter
from exifScan.ExifToolScan import ExifToolScanner
from exifScan.geoDfFromExifDf import GeoDataProcessor
from exifScan.writeKart import KartWriter
from exifScan.generateHTML.createHTML import HTMLWriter

# https://geopandas.org/en/stable/docs/user_guide/io.html
gpd.options.io_engine = "pyogrio"


class ExifScanner:
    # should refactor this with *args,**kwargs patterns now that we have defaults in the __main__ part. Same for all helper classes
    def __init__(self, WorkDirectory=None, MetashapeDirectory=None, KartDirectory=None, KartRemote=None,
                 GeopackageDirectory=None, OutputGeopackage='Photos.gpkg', htmlFolder=None, mapFileName='map.html',
                 otherMapLayers=None, otherMapLayerNames=None, ExifOutputFile="exiftoolOut",
                 readExifFromOutputFile=False, recursive=False, ignoreDirs=[], ignoreMetashape=False,
                 groupByTags=["Make", "Model", "CreateDate"], xyTagNames=['GPSLongitude', 'GPSLatitude'], zTagName='GPSAltitude',
                 imageFileExtensions=['JPG'], metashapeCacheTime=120, KartWriteDelay=120, stats={'Scan Started at': "", }, linzAPIKey=None
                 ):

        self.WorkDirectory = WorkDirectory or os.getcwd()
        self.MetashapeDirectory = MetashapeDirectory
        self.KartDirectory = KartDirectory
        self.KartRemote = KartRemote
        self.KartWriteDelay = KartWriteDelay
        self.GeopackageDirectory = GeopackageDirectory or self.WorkDirectory
        self.OutputGeopackage = OutputGeopackage
        self.htmlFolder = htmlFolder
        self.mapFileName = mapFileName
        self.otherMapLayers = otherMapLayers
        self.otherMapLayerNames = otherMapLayerNames
        self.ExifOutputFile = ExifOutputFile
        self.readExifFromOutputFile = readExifFromOutputFile
        self.recursive = recursive
        self.ignoreDirs = ignoreDirs
        self.ignoreMetashape = ignoreMetashape
        self.groupByTags = groupByTags
        self.xyTagNames = xyTagNames
        self.zTagName = zTagName
        self.imageFileExtensions = [s.upper() for s in imageFileExtensions]
        self.metashapeCacheTime = metashapeCacheTime
        self.splitSize = 100
        self.OutputGeopackagePath = os.path.join(self.GeopackageDirectory, self.OutputGeopackage)
        self.non_geoloacted_path = os.path.join(self.WorkDirectory, 'nongeolocated.csv')
        self.gpkg_layer = 'allGroupedData'
        self.metadata_writer = MetadataWriter(self.WorkDirectory, self.metashapeCacheTime, self.MetashapeDirectory, self.removefromGdf)
        self.exifToolScanner = ExifToolScanner(self.imageFileExtensions, self.recursive, self.ignoreDirs, self.ignoreMetashape)
        self.geoprocessor = GeoDataProcessor(WorkDirectory, xyTagNames, zTagName, self.groupByTags)
        self.linzAPIKey = linzAPIKey
        self.htmlWriter = HTMLWriter(self.OutputGeopackagePath, self.htmlFolder, self.mapFileName, self.otherMapLayers, self.otherMapLayerNames, self.splitSize, self.linzAPIKey)
        self.stats = stats
        self.kart_writer = KartWriter(self.KartDirectory, self.OutputGeopackagePath, self.KartRemote, self.KartWriteDelay)

    def write_HTML(self):
        if self.htmlFolder:
            # set leaflet map and table location
            info = ''
            for feature, value in self.stats.items():
                info = info + f'<span>{feature}: {value}</span><br/>'

            self.htmlWriter.updateHTML(info)

    def scan_for_photos(self, ScanFolder):
        StartTime = dt.now()
        now = StartTime.strftime("%Y%m%d%H%M%S")
        startCtime = StartTime.ctime()

        if not ScanFolder:
            raise Exception("Error: ScanFolder is not defined or is False")
        logging.info(f'Started folder Scan at {startCtime}')

        logging.debug(f'Current working directory is: {self.WorkDirectory}')

        if not self.MetashapeDirectory:
            self.metadata_writer.MetashapeDirectory = ScanFolder
            logging.debug(f'Current Metashape directory is: {ScanFolder}')

        ExifStartTime = dt.now()
        now = ExifStartTime.strftime("%Y%m%d%H%M%S")

        if self.readExifFromOutputFile:
            ExifOutputFileName = self.ExifOutputFile + '.json'
            exifFile = os.path.join(self.WorkDirectory, ExifOutputFileName)
            df = pd.read_json(exifFile)
        else:
            ExifOutputFileName = self.ExifOutputFile + str(now) + '.json'
            exifFile = os.path.join(self.WorkDirectory, ExifOutputFileName)
            df = self.exifToolScanner.run_exiftool(ScanFolder, exifFile)
        if df is None:
            logging.error('Error when running ExifScan')
            return None

        logging.info("Exiftool done processing. %s photos were found and exif data was extracted. The tool process took %s (h:mm:ss).", len(df), dt.now() - ExifStartTime)

        if df.empty:
            if not self.recursive:
                logging.info('Scanned folder has no images, will attempt to remove from database.')
                result = self.removefromGdf(ScanFolder)
                if not result:
                    logging.error('Error when removing from database, aborting script')
                    return
                self.kart_writer.import_to_kart()
                self.write_HTML()
            logging.info('Script ended as no images found')
            return ScanFolder

        logging.info('Processing data using pandas and geopandas.')

        geoDfStartTime = dt.now()
        points, geoDf, nonGeolocated = self.geoprocessor.process(df)

        if len(nonGeolocated):
            logging.warning(f'Found {len(nonGeolocated)} nonGeolocated group(s) in the folder with exention(s) {self.imageFileExtensions}.')

            nonGeolocated = self.metadata_writer.update_metadata(nonGeolocated)

            try:
                with open(self.non_geoloacted_path, 'a') as f:
                    f.write(f'ScanFolder: {ScanFolder} time: {dt.now() - geoDfStartTime}\n')
                nonGeolocated.to_csv(self.non_geoloacted_path, mode='a', index=False)
            except Exception as e:
                logging.exception(f"An unexpected error occurred: {e}. The error type is : {e.__class__.__name__}")

        logging.info("Geopandas done processing. The tool process took %s (h:mm:ss).", dt.now() - geoDfStartTime)

        if points is None or len(points) == 0:
            if not self.recursive:
                logging.info('Scanned folder has no geo-located images, will attempt to remove folder from database.')
                result = self.removefromGdf(ScanFolder)
                if not result:
                    logging.error('Error when removing from database, aborting script')
                    return
                self.kart_writer.import_to_kart()
                self.write_HTML()
            logging.info('Script ended as no geolocated images identified')
            return ScanFolder

        logging.info('Creating geopackages and tables.')

        tost = geoDf.copy()
        tost = tost.to_crs(3857)
        invalidGeometries = tost.geometry.apply(lambda g: not g.is_valid)
        if len(tost[invalidGeometries]):
            logging.warning(f'There are {len(tost[invalidGeometries])} invalid geometries in the geodataframe when projected in "Web Mercator".')
            logging.debug(tost[invalidGeometries])

        geoDf['areaSqkm'] = tost.area / 10**6

        gpkgname = 'Database' + now + '.gpkg'
        gpkgPath = os.path.join(self.WorkDirectory, gpkgname)
        points.to_file(gpkgPath, layer='points', driver="GPKG")

        if len(geoDf):
            geoDf.to_file(gpkgPath, layer=self.gpkg_layer, driver="GPKG")
            logging.debug(f"Archived filtered polygon called: allGroupedData in {gpkgPath}. It has {len(geoDf)} feature(s).")
            self.replaceInGPKG(geoDf, ScanFolder)

        self.kart_writer.import_to_kart()
        self.write_HTML()

        logging.info(f"Created files from the photo data. The whole thing took {dt.now() - StartTime} (h:mm:ss).")
        return ScanFolder

    def replaceInGPKG(self, geoDf, ScanFolder):

        try:
            # Read the existing data from a GeoPackage file
            existing = gpd.read_file(self.OutputGeopackagePath, layer=self.gpkg_layer, fid_as_index=True)

            # Determine the maximum index in the existing dataframe
            max_index = existing.index.max()

            # Set the index of the new GeoDataFrame to start after the largest index in the existing dataframe
            geoDf.index = geoDf.index + max_index + 1

            # Add metadata to the new GeoDataFrame for duplicate checking
            geoDf = self.metadata_writer.update_metadata(geoDf)

            # Concatenate the existing and new GeoDataFrames
            concatDf = pd.concat([existing, geoDf])

            # If not in recursive mode, remove rows that are not in the new GeoDataFrame (indicating modifications)
            if not self.recursive:
                # Filter existing rows to keep only those from the specified folder
                existingFiltered = existing[existing['SourceFileDir'] == ScanFolder.replace('\\', '/')]
                # Keep only relevant columns for comparison
                existingFiltered = existingFiltered.copy()[self.groupByTags + ['SourceFileDir']]
                newValuesFiltered = geoDf.copy()[self.groupByTags + ['SourceFileDir']]
                # Identify rows unique to the existing dataset
                uniqueToExisting = existingFiltered[~existingFiltered.apply(tuple, 1).isin(newValuesFiltered.apply(tuple, 1))]
                # Remove those rows from the concatenated dataframe
                concatDf = concatDf.drop(uniqueToExisting.index)
                if len(uniqueToExisting):
                    logging.info(f'Removed {len(uniqueToExisting)} entries that were no longer present in scanned folder.')

            # Keep the first occurrence of entirely identical rows
            filteredConcatDf = concatDf.copy().drop_duplicates(keep='first')

            # Sort the DataFrame by specified columns
            filteredConcatDf.sort_values(by=[*self.groupByTags, 'SourceFileDir'], inplace=True)

            # Create a dictionary where keys are indices of the first occurrence of each duplicate set
            firstOccurrenceIndices = filteredConcatDf.drop_duplicates([*self.groupByTags, 'SourceFileDir'], keep='first')

            # Get the indices of the first occurrence of each duplicate set
            firstIndices = firstOccurrenceIndices.index

            # Drop duplicates and keep the last occurrence
            filteredConcatDf = filteredConcatDf.drop_duplicates([*self.groupByTags, 'SourceFileDir'], keep='last')

            # Create a new DataFrame with indices of the first occurrence of each duplicate set
            newDf = filteredConcatDf.copy()
            newDf.index = firstIndices
            newDf.index.name = 'fid'

        except pyogrio.errors.DataSourceError as e:
            logging.warning(f"Error: {e}. This is normal is this is the first recursive Scan. A new df will be created.")
            newDf = geoDf
            newDf.index.name = 'fid'
        except pyogrio.errors.DataLayerError:
            logging.warning(f"Layer {self.gpkg_layer} doesn't exist. This is normal is this is the first time creating this layer. A new df will be created.")
            newDf = geoDf
            newDf.index.name = 'fid'

        # update metaData on all rows in df
        # doing this additional update as it is relatively quick if the Metashape values are cached.
        newDf = self.metadata_writer.update_metadata(newDf)

        newDf.to_file(self.OutputGeopackagePath, layer=self.gpkg_layer, driver="GPKG")
        logging.info(f"Replaced or wrote {self.gpkg_layer} dataset to the '{self.gpkg_layer}' layer in {self.OutputGeopackagePath},which now has a total of {len(newDf)} feature(s).")

    def removefromGdf(self, value):
        try:  # check if file exists before continuing
            gpd.read_file(self.OutputGeopackagePath)
        except pyogrio.errors.DataSourceError as e:
            logging.error(f"Error: {e}. Check if the file exists or if the path is correct.")
            return True
        except Exception as e:
            logging.exception(f"An unexpected error occurred: {e}. The error type is : {e.__class__.__name__}")

        layers = pyogrio.list_layers(self.OutputGeopackagePath)

        for layer in layers:
            # layer is in format ['name' 'type']
            layerName = layer[0]
            existing = gpd.read_file(self.OutputGeopackagePath, layer=layerName, fid_as_index=True)
            # keep everything in forward slashes.
            value = value.replace('\\', '/')

            filteredGdf = existing[existing['SourceFileDir'] != value]
            # Debugging statements
            filteredGdf.to_file(self.OutputGeopackagePath, layer=layerName, driver="GPKG")
            removedRows = len(existing) - len(filteredGdf)
            if removedRows:
                logging.warning(f"Removed {removedRows} rows with value :{value} in {self.OutputGeopackagePath}")
        return True
