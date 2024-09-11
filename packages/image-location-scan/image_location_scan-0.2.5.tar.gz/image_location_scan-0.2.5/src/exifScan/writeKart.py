import subprocess
import logging


class KartWriter:
    def __init__(self, kart_directory, output_geopackage_path, kart_remote=None):
        self.KartDirectory = kart_directory
        self.OutputGeopackagePath = output_geopackage_path
        self.KartRemote = kart_remote

    def import_to_kart(self):
        if self.KartDirectory:
            kartCmd = [
                "kart",
                "import",
                self.OutputGeopackagePath,
                "--all-tables",
                "--replace-existing"
            ]
            try:
                result = subprocess.run(kartCmd, cwd=self.KartDirectory)
                if result.returncode == 41:
                    logging.warning("Kart repository has not been initialised. Initialising now...")
                    init_process = subprocess.run(['kart', 'init', '--import', self.OutputGeopackagePath], cwd=self.KartDirectory)

                    if init_process.returncode == 0:
                        logging.info("Kart repository initialised successfully.")
                    else:
                        logging.error(f"Failed to initialise Kart repository. Return code: {init_process.returncode}")
                elif result.returncode == 44:
                    logging.info("Kart repository recorded no changes.")
                elif result.returncode == 0:
                    logging.info("Kart repository imported successfully.")

                    if self.KartRemote:
                        remoteResult = subprocess.run(['kart', 'push'], cwd=self.KartDirectory)

                        if remoteResult.returncode == 128:
                            logging.warning("Kart remote repository has not been set. Setting now...")
                            remoteAddResult = subprocess.run(['kart', 'remote', 'add', 'origin', self.KartRemote], cwd=self.KartDirectory)
                            pushResult = subprocess.run(['kart', 'push', '--set-upstream', 'origin', 'main'], cwd=self.KartDirectory)
                            if remoteAddResult.returncode == 0 and pushResult.returncode == 0:
                                logging.info(f"Kart {self.KartRemote} remote repository set successfully.")
                            else:
                                logging.error(f"Failed to set Kart remote repository.\nRemote add return code: {remoteAddResult.returncode}\n Push result: {pushResult.returncode}")
                        elif remoteResult.returncode == 0:
                            logging.info('Kart repository pushed successfully.')
                        else:
                            logging.error(f'Kart remote failed with error code: {remoteResult.returncode}')
                else:
                    logging.error(f'Kart import failed with error code: {result.returncode}')

            except NotADirectoryError:
                logging.error(f'Kart directory doesn\'t exist: {self.KartDirectory}. Data will not be backed up to a repository.')

# Example usage:
# kart_writer = KartWriter("/path/to/kart_directory", "/path/to/output_geopackage.gpkg", "https://remote.repo.url")
# kart_writer.import_to_kart()
