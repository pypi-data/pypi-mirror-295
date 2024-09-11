import subprocess
import pandas as pd
import logging
import threading
import os


class ExifToolScanner:
    def __init__(self, FileTypes, recursive=False, ignoreDirs=[], ignoreMetashape=False):
        self.FileTypes = FileTypes
        self.recursive = recursive
        self.ignoreDirs = ignoreDirs
        self.ignoreMetashape = ignoreMetashape

    def run_exiftool(self, ScanFolder, saveFile="exifOut.json"):
        logging.info(f"Exiftool now scanning for geolocated {' '.join(self.FileTypes)} files in: {ScanFolder}")

        exifCmd = [
            "exiftool",
            "-GPSLongitude", "-GPSLatitude", "-GPSAltitude",
            "-SourceFile", "-CreateDate", "-ImageSize", "-FileSize", "-Make", "-Model",
            "-j", "-c", "%.6f", "-n",
            ScanFolder,
            "-progress"
        ]
        for filetype in self.FileTypes:
            exifCmd.append('-ext')
            exifCmd.append(filetype)

        for directory in self.ignoreDirs:
            exifCmd.append('-i')
            directory = directory.replace('\\', '/')
            exifCmd.append(directory)
        if self.ignoreMetashape:
            exifCmd.append('-if')
            exifCmd.append('$directory !~ /\\.files/')

        if self.recursive:
            exifCmd.append('-r')

        logging.info(f"Command used for Exiftool: {' '.join(exifCmd)}")

        with open(saveFile, "w") as outfile:
            stop_event = threading.Event()
            process = subprocess.Popen(exifCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            stdout_thread = threading.Thread(target=reader, args=[process.stdout, outfile.write, stop_event])
            stderr_thread = threading.Thread(target=reader, args=[process.stderr, lambda x: logging.info(x.strip()), stop_event])

            stdout_thread.start()
            stderr_thread.start()
            try:
                process.wait()

                stdout_thread.join()
                stderr_thread.join()

            except KeyboardInterrupt:
                stop_event.set()
                process.terminate()
                stdout_thread.join()
                stderr_thread.join()
                return None

        return process_output(ScanFolder, saveFile)


def process_output(ScanFolder, saveFile):
    try:
        if os.path.getsize(saveFile) != 0:
            exif_df = pd.read_json(saveFile)
        else:
            logging.info(f"No images were found in {ScanFolder}")
            os.remove(saveFile)
            exif_df = pd.DataFrame()

    except FileNotFoundError:
        logging.error(f"FileNotFoundError: The file {saveFile} does not exist or the path is incorrect.")
        return None
    except ValueError:
        logging.info(f"The file {saveFile} might be empty (no images were found) or not a valid JSON file.")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred when attempting to read {saveFile}: {e}")
        return None

    return exif_df


def reader(pipe, func, stop_event):
    try:
        with pipe:
            for line in iter(pipe.readline, ''):
                if stop_event.is_set():
                    break
                func(line)
    except Exception as e:
        logging.error(f'Error in reader: {str(e)}')
