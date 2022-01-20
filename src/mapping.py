import geopandas
import rasterio as rio
from rasterio.plot import show
import matplotlib.pyplot as plt


def overlay_road_network(road_network: str, src_file_path: str, out_file_path: str):
    """ Overlay road vectors on-top of raster image

    This function takes both a road network layer, ideally in Geopackage format, and a raster, overlays the road network on-top of the raster, and saves this map to disk. It is not the fastest solution, as it is using matplotlib. A different solution might use skimage or OpenCV, but this was out of the scope of this exercise.
    
    The road network bounds need to be within the bounds of the source file.

    Parameters
    ----------
    road_network : str
        Full path to geospatial file, e.g. a geopackage or shapefile, that contains the road network. 
    scr_file_path : str
        Full path to source raster, to be used as a base map.        
    out_file_path : str
        Full path to output image. 

    Returns
    -------
    None

    """

    roads = geopandas.read_file(road_network, layer='San-Francisco-roads')
    roads = roads.to_crs('epsg:32610')
    src= rio.open(src_file_path)

    fig, ax = plt.subplots()
    plt.figure(dpi=1200)

    extent=[src.bounds[0], src.bounds[2], src.bounds[1], src.bounds[3]]
    ax = rio.plot.show(src, extent=extent, ax=ax)
    roads.plot(ax=ax, color='darkred', linewidth=0.5)
    ax.set_title("Road map of San Francisco City, California, USA")
    ax.set_xlabel("Longitude UTM 10N (m)")
    ax.set_ylabel("Latitude UTM 10N (m)")
    fig.set_size_inches(15,15)
    fig.savefig(out_file_path, dpi=1200)

    
