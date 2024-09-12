import pytest

from girder.plugin import loadedPlugins


@pytest.mark.plugin('girder_zip_extractor')
def test_import(server):
    assert 'girder_zip_extractor' in loadedPlugins()
