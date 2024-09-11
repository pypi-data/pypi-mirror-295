import pandas as pd
import numpy as np
import logging
import geopandas as gpd
from datetime import datetime as dt
import os


class GeoDataProcessor:
    def __init__(self, WorkDirectory, xyTagNames, zTagName, groupByList):
        self.WorkDirectory = WorkDirectory
        self.xyTagNames = xyTagNames
        self.zTagName = zTagName
        self.groupByList = groupByList
        self.duplicateColumns = [*groupByList, 'SourceFileName', 'CreateDateTime', 'FileSize']

    def process(self, exifDf):
        x_coords = self.xyTagNames[0]
        y_coords = self.xyTagNames[1]

        if not isinstance(exifDf, pd.DataFrame):
            logging.error("The provided argument is not a DataFrame.")
            # return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

        if all(item in exifDf.columns for item in self.xyTagNames):
            for tag in self.xyTagNames:
                exifDf[tag] = pd.to_numeric(exifDf[tag], errors='coerce')
                exifDf[tag] = exifDf[tag].where(exifDf[tag] != 0, np.nan)

            valid_df = exifDf.copy().dropna(subset=self.xyTagNames)
            invalid_df = exifDf.copy()[exifDf[self.xyTagNames].isnull().any(axis=1)]
        else:
            invalid_df = exifDf.copy()
            valid_df = pd.DataFrame(columns=exifDf.columns)

        if len(invalid_df):
            logging.warning(f"{len(invalid_df)} images are not geolocated.")
        logging.info(f"{len(valid_df)} images are geolocated.")

        if not valid_df.empty:
            logging.debug('Handling geolocated images')
            if self.zTagName not in valid_df.columns:
                valid_df[self.zTagName] = 0
                logging.warning(f"Added {self.zTagName} column with default value 0")

            valid_df[self.zTagName] = pd.to_numeric(valid_df[self.zTagName], errors='coerce')
            valid_df[self.zTagName] = valid_df[self.zTagName].fillna(0)

            logging.info("Cleaning up table. Changed altitude NA values to 0")

            applyBounds = True

            if applyBounds:
                ymin, ymax, xmin, xmax = -180, 180, -90, 90

                if ymin > ymax:
                    dataBounded1 = valid_df[valid_df[x_coords] > ymin]
                    dataBounded2 = valid_df[valid_df[x_coords] < ymax]
                    valid_df = pd.concat([dataBounded1, dataBounded2], ignore_index=True)
                else:
                    valid_df = valid_df[(valid_df[x_coords] > ymin) & (valid_df[x_coords] < ymax)]
                    valid_df = valid_df[(valid_df[y_coords] > xmin) & (valid_df[y_coords] < xmax)]

                merged = valid_df.merge(valid_df, how='outer', indicator=True)
                outOfBounds = merged[merged['_merge'] == 'right_only']
                logging.info(f"Removed {len(outOfBounds)} rows that were out of bounds.")

                logging.info(f"Cleaning up table. Data bounded by {ymin} and {ymax} Longitude and by {xmin} and {xmax} Latitude.")

                if valid_df.empty:
                    logging.info('All data was filtered out. Either no NZ locations are included, or the exif data were not valid values.')
            else:
                logging.info('Unbounded data.')

            setDfColumns(valid_df)
            self.getDuplicates(valid_df)

            logging.info("Creating point GeoDataFrame")
            pointsDf = gpd.GeoDataFrame(data=valid_df, geometry=gpd.points_from_xy(valid_df[x_coords], valid_df[y_coords], valid_df[self.zTagName]), crs="EPSG:4326")
            logging.info(f"Points created. It has {len(pointsDf)} features.")

            groupByListGL = [*self.groupByList, 'SourceFileDir']
            groupByListGL = [col for col in groupByListGL if col in pointsDf.columns]

            aggfuncs = {
                'SourceFileName': 'count',
            }

            polygonsDf = pointsDf.dissolve(by=groupByListGL, aggfunc=aggfuncs, as_index=False)
            polygonsDf.rename(columns={'SourceFileName': 'Image Count'}, inplace=True)
            polygonsDf = polygonsDf[[*groupByListGL, 'Image Count', 'geometry']]
            polygonsDf['geometry'] = polygonsDf.convex_hull
            logging.info(f'Grouped points into polygons by {", ".join(groupByListGL)}. It has {len(polygonsDf)} features.')
        else:
            pointsDf = polygonsDf = gpd.GeoDataFrame()

        if not invalid_df.empty:
            logging.debug('Handling non-geolocated images')
            setDfColumns(invalid_df)
            existing_columns = [col for col in self.groupByList if col in invalid_df.columns]
            self.getDuplicates(invalid_df)
            groupByListNGL = [*existing_columns, 'SourceFileDir']
            try:
                nonGeoDf = invalid_df.groupby(groupByListNGL).agg({
                    'SourceFileName': list,
                }).reset_index()
                nonGeoDf['Image Count'] = nonGeoDf['SourceFileName'].str.len()
            except Exception as e:
                logging.error(f"Error while aggregating data : {e}")
                nonGeoDf = pd.DataFrame()
        else:
            nonGeoDf = pd.DataFrame()

        return pointsDf, polygonsDf, nonGeoDf

    def getDuplicates(self, df):

        # get duplicates
        existing_columns = [col for col in self.duplicateColumns if col in df.columns]

        duplicateRows = df.copy()[df.duplicated(existing_columns, keep=False)]

        if (hasattr(df, '_geometry_column_name')):
            identicalGeometryDf = gpd.GeoDataFrame()
            for _, geom in enumerate(duplicateRows.geometry):
                # Get rows where geometry is identical to the current row
                identicalRows = duplicateRows[duplicateRows.geometry.apply(lambda x: x.equals(geom))]

                # Append identical rows to the result DataFrame
                identicalGeometryDf = identicalGeometryDf.append(identicalRows)
            duplicateRows = identicalGeometryDf

        if not duplicateRows.empty:

            logging.warning(f'Found {len(duplicateRows)} duplicate rows (~ {int(df["FileSize"].sum() / 1073741824)} GB).')

            if 'CreateDateTime' in duplicateRows:
                # Convert to datetime with a specified format
                duplicateRows['CreateDateTime'] = pd.to_datetime(duplicateRows['CreateDateTime'], format='%Y:%m:%d %H:%M:%S', errors='coerce')
                # Sort the DataFrame
                duplicateRows = duplicateRows.sort_values(by='CreateDateTime')

            timestamp = dt.now().strftime('%Y%m%d%H%M%S')

            # Create a unique filename using the timestamp
            filename = f'duplicates_{timestamp}.csv'
            filepath = os.path.join(self.WorkDirectory, filename)
            # Write the DataFrame to a CSV file with the unique filename
            try:
                duplicateRows.to_csv(filepath, index=False)
                logging.debug(f'Duplicate rows written to : {filepath} .')

            except Exception as e:
                logging.error(f'Error when writing to {filename} :{e}')


def setDfColumns(df):
    # set up fileName and directory columns
    df['SourceFileDir'] = df['SourceFile'].str.rpartition('/')[0]
    df['SourceFileName'] = df['SourceFile'].str.rpartition('/')[2]
    if 'CreateDate' in df.columns:
        # Strip everything after the seconds value
        df['CreateDate'] = df['CreateDate'].str.slice(0, 10)
        try:
            df['CreateDate'] = pd.to_datetime(df['CreateDate'], format='%Y:%m:%d').dt.date
        except ValueError as e:
            logging.error(f'Unable to parse datetime, will coerce values. Please check source of error: {e}')
            df['CreateDate'] = pd.to_datetime(df['CreateDate'], format='%Y:%m:%d', errors='coerce').dt.date
