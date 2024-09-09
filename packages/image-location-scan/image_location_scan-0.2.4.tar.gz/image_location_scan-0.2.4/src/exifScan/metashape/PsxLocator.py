import os
import sys
import logging
not_supported = False
if (sys.version_info[1] > 11):
    logging.error(f'Metashape not supported in python 3.11 or greater. This system appears to be running Python {sys.version_info[0]}.{sys.version_info[1]}')
    not_supported = True

try:
    import Metashape
except ImportError:
    logging.error("Metashape is not installed. Please install the package to proceed.")
    not_supported = True


def main(Directory):

    if not_supported:
        return

    ScannedDir = Directory
    ProjectPathList = []
    logging.info("Searching for Metashape project(.psx and .psz) files.")
    for root, _, files in os.walk(ScannedDir):
        for file in files:
            if file.endswith((".psx", ".psz")):
                FilePath = (os.path.join(root, file))
                ProjectPathList.append(FilePath)
                logging.debug(f'Added Project :{FilePath}')
    projectNo = len(ProjectPathList)
    logging.info(f"Located {projectNo} psx and psz files.")

    if (projectNo == 0):
        return None

    Doc = Metashape.Document()
    CameraDirDict = {}
    for ProjectPath in ProjectPathList:
        try:
            # read-only to ensure that no data is mutated.
            Doc.open(ProjectPath, read_only=True)
            logging.debug(f'Read {ProjectPath}')
            Chunks = Doc.chunks
            for Chunk in Chunks:
                CameraList = Chunk.cameras
                for Camera in CameraList:
                    if Camera.photo is not None:
                        try:
                            # get photo directory, and add directory to list if it isn't there.
                            CameraPath = Camera.photo.path
                            
                            CameraDir = CameraPath.rpartition('/')[0]
                            
                            if CameraDir not in CameraDirDict:
                                CameraDirDict[CameraDir] = []
                            # replace backslash with forwardslash to make paths consistent.
                            sanitised = ProjectPath.replace("\\", "/")
                            if sanitised not in CameraDirDict[CameraDir]:
                                CameraDirDict[CameraDir].append(sanitised)
                                logging.debug(f'Added ProjectPath {sanitised} to {CameraDir.encode("utf-8")}')
                        except Exception as e:
                            logging.error(f"Unable to read {Camera} in project {ProjectPath} . Error: {e}")
                    else:
                        logging.debug(f'Project:{ProjectPath}: Camera {Camera}has no attribute "path"')
        except Exception as e:
            logging.error(f"Problem with project: {ProjectPath}. Error: {e}")
    logging.info(f"Discovered {len(CameraDirDict)} Metashape project files that contained images from the database.")

    # list are object dtypes, so converted to strings when saving in pyogrio. Converting here to control how it is joined.
    # Maybe use a supported dtype in the future?
    for key in CameraDirDict:
        CameraDirDict[key] = ",\n".join(CameraDirDict[key])

    return CameraDirDict
