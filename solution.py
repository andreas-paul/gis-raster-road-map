import os
from src.bbox import create_bounding_box
from src.config import log, settings
from src.download import get_landsat_data
from src.mapping import overlay_road_network
from src.osm import get_osm_street_data
from src.processing import rgb_pansharpening, save_raster_as_jpg, clip_raster, color_correct


def main():

    log.info('Starting solution. This will take a few minutes.')
    
    # Define initial variables
    log.info('Defining initial variables')
    work_dir = settings.workdir
    out_dir = settings.outdir
    rgb_img_id = f"{work_dir}/{settings.image_id}_PAN.TIF"
    bbox_path = f'{work_dir}/San-Francisco-bbox.gpkg'
    road_path = f'{work_dir}/San-Francisco-roads.gpkg'

    # Create directories.
    log.info('Creating directories') 
    for directory in [work_dir, out_dir]:
        if not os.path.exists(directory):
            os.mkdir(directory)

    # Download Landsat data
    log.info('Downloading Landsat data')
    get_landsat_data(image_id=settings.image_id, 
                        bucket = settings.s3_bucket, 
                        path = settings.s3_path, 
                        bands = settings.use_bands)

    # Download OpenStreetMap data
    log.info('Downloading OpenStreetMap road data')
    get_osm_street_data(place="San Francisco, CA, USA", 
                        save_file_path=road_path)

    # Stack and pansharpen Landsat imagery
    log.info('Stacking and pansharpening RGB raster')
    rgb_pansharpening(save_file_path=rgb_img_id,                
                        image_id=settings.image_id)

    # Save pansharpened RGB image as 'tci.jpg'
    log.info('Saving pansharpened RGB image to disk')
    save_raster_as_jpg(src_file_path=rgb_img_id,
                        save_file_path=f'{work_dir}/_tmp_tci.jpg')
    log.success('Success')

    # Color correct RGB image 
    log.info('Applying color corrections')
    color_correct(src_file_path=f'{work_dir}/_tmp_tci.jpg', 
                    out_file_path=f'{out_dir}/tci.jpg')
    
    # Create bounding box to clip raster 
    log.info('Creating bounding box from coordinates')
    create_bounding_box(save_file_path=bbox_path,
                        latitudes=settings.latitudes, 
                        longitudes=settings.longitudes,
                        crs=settings.crs)

    # Clip raster to San Francisco area
    log.info('Clipping raster to San Francisco area')
    clip_raster(extent_file_path=bbox_path,
                src_raster_path=f'{out_dir}/tci.jpg',
                out_raster_path=f'{work_dir}/_tmp_map.tif')

    # Overlay road network
    log.info('Overlaying road network and saving map to disk')
    overlay_road_network(road_network=road_path, 
                            src_file_path=f'{work_dir}/_tmp_map.tif',
                            out_file_path=f'{out_dir}/map.jpg')

    # Final check
    assert os.path.exists(f'{out_dir}/tci.jpg')
    assert os.path.exists(f'{out_dir}/map.jpg')

    log.success('Finished solution. Thank you for your patience.')


if __name__ == "__main__":
    main()
