import os
import pytest
import geopandas as gpd
from src.osm import get_osm_street_data


@pytest.fixture
def data() -> dict:
    return {'save_file_path': "tests/test_data/test-osm.gkpg",
            'place': 'Meuselwitz, Germany',
            'network_type': 'drive'}


def test_retrieve_save(data):
    get_osm_street_data(**data)
    assert os.path.exists(data['save_file_path'])


def test_fields(data):
    f = gpd.read_file(data['save_file_path'])
    assert len(f.columns) == 15


def test_content(data):
    f = gpd.read_file(data['save_file_path'])
    assert 'Am Lehrbetrieb' in list(f['name'])
    assert 'Zeitzer Straße' in list(f['name'])


def test_cleanup(data):
    if os.path.exists(data['save_file_path']):
        os.remove(data['save_file_path'])
