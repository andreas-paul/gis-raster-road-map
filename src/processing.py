import os
import fiona
import rasterio as rio
from glob import glob
from osgeo import gdal
from shutil import copyfile
from rasterio.mask import mask
from src.config import log, settings
from PIL import Image, ImageEnhance
from osgeo_utils.gdal_pansharpen import gdal_pansharpen

# Remove max image pixels to prevent PIL errors due to file size
Image.MAX_IMAGE_PIXELS = None

work_dir = settings.workdir
out_dir = settings.outdir


def rgb_pansharpening(save_file_path: str = None, image_id: str = None):
    """Merge bands and create pansharpened raster

    This function merges raster bands (2,3 & 4) to create RGB, and subsequently 
    creates a pansharpened image using GDAL and band 8.

    Parameters
    ----------
    bands_stack : list 
        Sorted list containing individual raster bands B2, B3, B4, B8.
    save_file_name : str
        Path with file name of output file (pansharpened image).

    Returns
    -------
    None

    """

    # Collect image files
    bands = os.path.join(work_dir, image_id + "*[2,3,4,8]*.TIF")
    bands_stack = glob(bands)
    bands_stack.sort()

    # Run gdal_pansharpen
    gdal_pansharpen(
        pan_name=bands_stack[3],
        spectral_names=bands_stack[:3], 
        band_nums=[3, 2, 1],
        dst_filename=save_file_path)



def clip_raster(extent_file_path: str, src_raster_path: str, out_raster_path: str):
    """ Clips raster using an extent file

    This function clips an input raster using an extent file and saves the clipped raster to a new file.

    Parameters
    ----------
    extent_file_path: str
        Path to extent file of type Geopackage (.gpkg) or Shapefile (.shp)
    src_raster_path: str
        Path to input raster 
    out_raster_path: str
        Path to output raster

    Returns
    -------
    None

    """

    with fiona.open(extent_file_path, "r") as shape:
        shapes = [feature['geometry'] for feature in shape]

    with rio.open(src_raster_path) as src:
        out_img, out_trans = mask(src, shapes, crop=True)
        out_meta = src.meta
    
    out_meta.update({"driver": "GTiff",
                    "height": out_img.shape[1],
                    "width": out_img.shape[2],
                    "transform": out_trans})

    with rio.open(out_raster_path, "w", **out_meta) as dest:
        dest.write(out_img)


def save_raster_as_jpg(src_file_path: str = None, save_file_path: str = None, scaling='-scale 0 14000'):
    """Converts image to 8 Bit jpg and stretches histogram to make it look nicer
    """

    options_list = ['-ot Byte', '-of JPEG', scaling]    
    options_string = " ".join(options_list)
        
    gdal.Translate(
        save_file_path,
        src_file_path,
        options=options_string
)


def color_correct(src_file_path: str = None, out_file_path: str = None):
    """Color correct image
    """
    out = Image.open(src_file_path)
    out = ImageEnhance.Color(out).enhance(1.5)
    out = ImageEnhance.Contrast(out).enhance(1.2)
    out = ImageEnhance.Sharpness(out).enhance(1.2)
    out = ImageEnhance.Brightness(out).enhance(0.95)
    out.save(out_file_path, dpi=(600,600))

    if os.path.exists(f"{src_file_path}.aux.xml"):
        copyfile(f"{src_file_path}.aux.xml", f"{out_file_path}.aux.xml")
