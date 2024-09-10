import os
import time
import zipfile
from dnalib.log import log
from .utils import Utils

class LandingZoneUtils:

    @staticmethod
    def load_files_dataframe(landing_path):
        file_path = Utils.landingzone_path(landing_path)        
        try:            
            files_dataframe = (
                Utils.spark_instance().createDataFrame(Utils.dbutils().fs.ls(file_path))
                .filter("(name <> 'processados/')") 
                .select('path', 'name', 'modificationTime')
                .orderBy("modificationTime", ascending=False)
                .select('path','name')
                .first()["path"]
            )
        except Exception as e:
            log(__name__).error(f"Unable to load files for path {file_path}: {e}")            
            raise Exception(f"Unable to load files for path {file_path}")

        return files_dataframe