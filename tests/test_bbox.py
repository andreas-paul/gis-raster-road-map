import os
import fiona
import pytest
from shapely.geometry import shape
from fiona.collection import Collection
from src.bbox import create_bounding_box


@pytest.fixture
def data() -> dict:
    return {'data_dir': "tests/test_data", 
            'save_file': 'test_bbox.gpkg',
            'full_file_path': f"tests/test_data/test-bbox.gpkg",     
            'lats': [51.057804,51.057804, 51.366129, 51.366129],
            'lons': [3.007117, 3.446569, 3.446569, 3.007117],
            'crs': '4326'}


def test_file(data):  
    if not os.path.exists(data['data_dir']):
        os.mkdir(data['data_dir'])
    create_bounding_box(data['full_file_path'], data['lats'], data['lons'], data['crs'])
    assert os.path.exists(data['full_file_path'])


def test_type(data):
    f = fiona.open(data['full_file_path'])    
    assert type(f) == Collection


def test_bounds(data):    
    f = fiona.open(data['full_file_path'])
    poly = next(iter(f))
    assert shape(poly['geometry']).bounds == (3.007117, 51.057804, 3.446569, 51.366129)


def test_cleanup(data):
    if os.path.exists(data['full_file_path']):
        os.remove(data['full_file_path'])
