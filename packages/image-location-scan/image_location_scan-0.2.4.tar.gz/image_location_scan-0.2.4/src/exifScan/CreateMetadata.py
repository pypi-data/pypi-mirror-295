import pandas as pd
import pickle
import os
from datetime import datetime as dt, timedelta as td
import logging
from exifScan.metashape import PsxLocator


class MetadataWriter:
    def __init__(self, WorkDirectory, metashapeCacheTime, MetashapeDirectory, removefromGdf):
        self.WorkDirectory = WorkDirectory
        self.metashapeCacheTime = metashapeCacheTime
        self.MetashapeDirectory = MetashapeDirectory
        self.metashape_cache_file = os.path.join(self.WorkDirectory, 'metashapeCache.pkl')
        self.removefromGdf = removefromGdf

    def update_metadata(self, gpdDf):
        startTime = dt.now()

        gpdDf = self.locate_and_match_metadata(gpdDf)
        gpdDf = self.associate_metashape_projects(gpdDf)

        logging.info(f"The Metadata was created in {dt.now() - startTime} (h:mm:ss).")
        return gpdDf

    def locate_and_match_metadata(self, gpdDf):
        FileName = "metadata.xlsx"
        not_found = []
        fileNo = 0

        for folder in gpdDf["SourceFileDir"].unique():
            cur_dir = folder
            try:
                while True:
                    file_list = os.listdir(cur_dir)
                    parent_dir = os.path.dirname(cur_dir)
                    if FileName in file_list:
                        fileNo += 1
                        ExcelFile = os.path.join(cur_dir, FileName)
                        logging.debug(f"Metadata file {FileName} for {folder} found in {cur_dir}")
                        break
                    else:
                        ExcelFile = None
                        if cur_dir == parent_dir:
                            logging.warning(f"Metadata file {FileName} not found for {folder}")
                            break
                        else:
                            cur_dir = parent_dir
            except FileNotFoundError as e:
                ExcelFile = None
                logging.error(f"Couldn't find folder {folder}. Error: {e}")
                not_found.append(folder)

            if ExcelFile:
                try:
                    MetadataDfRow = pd.read_excel(ExcelFile, header=0, index_col='Index')
                    ExcelFileDir = ExcelFile.rpartition('\\')[0].replace("\\", "/")
                    for column in ['Metadata File Location']:
                        if column not in gpdDf:
                            gpdDf[column] = ""
                            logging.info(f"Added metadata column {column}")
                    gpdDf.loc[gpdDf['SourceFileDir'] == folder, 'Metadata File Location'] = ExcelFileDir.replace("/", "\\")

                    for column in MetadataDfRow.index:
                        if column not in gpdDf:
                            gpdDf[column] = ""
                            logging.info(f"Added metadata column {column}")
                        gpdDf.loc[gpdDf['SourceFileDir'] == folder, column] = MetadataDfRow.loc[column, 'Values']
                except FileNotFoundError as e:
                    logging.error(f"Couldn't find metadata excel file in {folder}. Error:{e}")

        logging.info(f'Located and matched {fileNo} metadata files.')
        # a short script to remove folders that were missed - this might not be necessary in more recent version of the package
        filteredGdf = gpdDf
        if len(not_found):
            logging.info('Some folders are missing, will attempt to remove from database.')

            for folder in not_found:
                logging.debug(f"Removing following folder from database: {folder}")
                folder = folder.replace('\\', '/')
                filteredGdf = gpdDf[gpdDf['SourceFileDir'] != folder]
                removedRows = len(gpdDf) - len(filteredGdf)
                if removedRows:
                    self.removefromGdf(folder)
                    logging.warning(f"Removed {removedRows} entries with folder value: {folder}")
                else:
                    logging.error(f'Error when removing following folder from database: {folder}')
        return filteredGdf

    def associate_metashape_projects(self, gpdDf):
        now = dt.now()
        if (os.path.exists(self.metashape_cache_file) and dt.fromtimestamp(os.path.getmtime(self.metashape_cache_file)) > now - td(minutes=self.metashapeCacheTime)):
            logging.info(f'Using cached Metashape project matches as time elapsed ({(now - dt.fromtimestamp(os.path.getmtime(self.metashape_cache_file))).total_seconds() / 60}) is less than cacheTime ({self.metashapeCacheTime}).')
            with open(self.metashape_cache_file, 'rb') as f:
                MSDataDict = pickle.load(f)
        else:
            MSDataDict = PsxLocator.main(self.MetashapeDirectory)
            with open(self.metashape_cache_file, 'wb') as f:
                pickle.dump(MSDataDict, f)
                logging.debug(f'Metashape data was saved to: {self.metashape_cache_file}')

        if MSDataDict is None or len(MSDataDict) == 0:
            logging.info("No Metashape project files contain any images from the database.")
            return gpdDf

        logging.info(f"{len(MSDataDict)} Metashape project file(s) contain images from the database.")

        MSDataDict = {k.lower().encode("utf-8"): v for k, v in MSDataDict.items()}
        gpdDf['SourceFileDirLower'] = gpdDf['SourceFileDir'].str.lower().str.encode("utf-8")

        for k in MSDataDict.keys():
            if k in gpdDf.SourceFileDirLower.values:
                logging.debug(f'Photos from folder {k} in current geodataframe')

        gpdDf['Metashape Files'] = gpdDf['SourceFileDirLower'].apply(lambda x: MSDataDict.get(x)).fillna('')
        gpdDf = gpdDf.drop(columns='SourceFileDirLower')

        return gpdDf
