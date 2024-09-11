import pytest

from girder.plugin import loadedPlugins


@pytest.mark.plugin('zip_extractor')
def test_import(server):
    assert 'zip_extractor' in loadedPlugins()
