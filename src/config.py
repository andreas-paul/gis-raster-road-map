from pydantic import BaseSettings
from loguru import logger

log = logger

class Settings(BaseSettings):

    # Local directories
    workdir = 'app/tmp'
    outdir = 'app/out'

    # Settings for: osmnx
    osmnx_use_cache: bool = False
    osmnx_log_console: bool = False

    # Landsat data
    use_bands: list = [2, 3, 4, 8]
    image_id: str = 'LC08_L1TP_044034_20210508_20210518_01_T1'  
    s3_path: str = 'c1/L8/044/034/LC08_L1TP_044034_20210508_20210518_01_T1/'
    s3_image_id_part: str = 'LC08_L1TP_044034_20210508_20210518_01_T1_B'
    s3_bucket: str = 'landsat-pds'

    # Backup data repository on Dropbox
    data_file: str = ""

    # Coordinate reference system (CRS)
    crs: str = '32610'

    # Bounding box (extent)
    latitudes: list = [4172770.092375004, 4187911.262887822, 4187911.262887822, 4172770.092375004]
    longitudes: list = [541115.984246796, 541115.984246796, 558190.0701442292, 558190.0701442292]


settings = Settings()