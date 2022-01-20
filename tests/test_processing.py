import os
import pytest
import rasterio as rio
from rasterio.crs import CRS
from src.processing import clip_raster, save_raster_as_jpg


@pytest.fixture
def data() -> dict:
    return {"src_file_path": "tests/test_data/rgb8.tif",
            "save_file_path": "tests/test_data/rgb8.jpg",
            "scaling": "-scale"}


@pytest.fixture
def data_clip() -> dict:
    return {"extent_file_path": "tests/test_data/test-extents.gpkg",
            "src_raster_path": "tests/test_data/rgb8.tif",
            "out_raster_path": "tests/test_data/test-clipped.tif"}


def test_save_jpg(data):
    save_raster_as_jpg(**data)
    assert os.path.exists(data['save_file_path'])


def test_save_cleanup(data):
    if os.path.exists(data['save_file_path']):
        os.remove(data['save_file_path'])


def test_clip_raster(data_clip):
    clip_raster(**data_clip)
    assert os.path.exists(data_clip['out_raster_path'])
    with rio.open(data_clip['out_raster_path']) as f:
        assert f.meta['width'] == 124
        assert f.meta['height'] == 102
        assert f.meta['crs'] == CRS.from_epsg(32620)


def test_clip_cleanup(data_clip):
    if os.path.exists(data_clip['out_raster_path']):
        os.remove(data_clip['out_raster_path'])
