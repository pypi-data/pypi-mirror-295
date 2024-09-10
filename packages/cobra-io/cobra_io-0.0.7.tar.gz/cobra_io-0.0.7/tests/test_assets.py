import unittest

from timor.Geometry import Mesh

from cobra.asset.asset import get_asset
from cobra.utils import caches


class TestAssetsAPI(unittest.TestCase):
    """Test robot API."""
    def test_asset_download(self):
        caches.reset_cache()
        file = get_asset('assets/DMU_125P.stl')
        mesh = Mesh({'file': file})
        self.assertIsNotNone(mesh)
        self.assertGreater(mesh.measure_volume, 0)

    def test_asset_fail(self):
        with self.assertRaises(FileNotFoundError):
            get_asset('some-really-non-existent-file')
