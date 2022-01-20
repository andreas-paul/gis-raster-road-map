import os
import boto3
import zipfile
import urllib.request
from src.config import settings, log
from botocore.exceptions import ClientError

work_dir = settings.workdir
out_dir = settings.outdir

def dl_from_aws(image_id: str, bucket: str, 
                path: str, bands: list):
    """Download Landsat data from AWS Open Data repository

    This function attempts to download landsat imagery from Amazon web
    services S3, using boto3 client. It requires AWS credentials to be present.

    Parameters
    ----------
    image_id : str
        Landsat image id to be used to construct AWS S3 path. Example: 'LC08_L1TP_044034_20210508_20210518_01_T1'  
    bucket :  str
        Landsat S3 bucket. Example: 'landsat-pds'
    path :  str
        Landsat path used on AWS S3. Example: 'c1/L8/044/034/LC08_L1TP_044034_20210508_20210518_01_T1/'
    bands : list
        List of bands to be downloaded. Example: [1,2,3] to download 
        bands 1, 2 and 3

    Returns
    -------
    None

    """

    client = boto3.client('s3')

    for band in bands:   
        src_path = path + image_id + str(band) + '.TIF'
        save_path = f"{work_dir}/{image_id + str(band)}.TIF"
        if not os.path.exists(save_path):
            try:
                client.download_file(bucket, src_path, save_path)
            except ClientError as e:
                raise ClientError("Unable to connect to AWS")
            except Exception as e: 
                raise Exception(str(e))


def dl_from_dropbox(save_file_path: str = None):
    """Download backup Landsat data file from Dropbox repository

    This function downloads a backup zipfile from Dropbox, if AWS S3 downloads
    fails, for whichever reason (mainly if no credentials are present). This file
    contains the 4 bands that are used in this assignment (2, 3, 4 and 8)

    Parameters
    ----------
    save_file_path : str
        Full path to which the dropbox file should be save to.

    Returns
    -------
    None

    """

    urllib.request.urlretrieve(settings.data_file, save_file_path)
    if os.path.exists(save_file_path):
        unzip(save_file_path)


def unzip(file_path: str):    
    """Unzip file ending with .zip

    This function unzips the ZIP file downloaded if AWS S3 download failed.

    Parameters
    ----------
    file_path : str
        Full path to zip file-

    Returns
    -------
    None

    """

    with zipfile.ZipFile(file_path, 'r') as zipped:
        zipped.extractall(work_dir)    
    os.remove(file_path)


def get_landsat_data(image_id: str = None, 
                        bucket: str = None, 
                        path: str = None, 
                        bands: str = None):
    """Wrapper function to check if AWS credentials are present.

    This function acts as a wrapper to check if AWS credentials are present or not.
    If no AWS credentials are found, it will initiate a dropbox download. Otherwise, it will initiate download from AWS S3, of Landsat data

    Parameters
    ----------
    image_id : str
        Landsat image id to be used to construct AWS S3 path. Example: 'LC08_L1TP_044034_20210508_20210518_01_T1'  
    bucket :  str
        Landsat S3 bucket. Example: 'landsat-pds'
    path :  str
        Landsat path used on AWS S3. Example: 'c1/L8/044/034/LC08_L1TP_044034_20210508_20210518_01_T1/'
    bands : list
        List of bands to be downloaded. Example: [1,2,3] to download 
        bands 1, 2 and 3

    Returns
    -------
    None

    """

    if not boto3.Session().get_credentials():
        log.warning("No AWS Credentials found. Switching to download from Dropbox.")
        dl_from_dropbox(f"{work_dir}/landsat.zip")
    else:    
        log.success("AWS Credentials found. Attempting download from AWS.")    
        try:
            dl_from_aws(image_id, bucket, path, bands)
        except Exception:
            dl_from_dropbox(f"{work_dir}/landsat.zip")
