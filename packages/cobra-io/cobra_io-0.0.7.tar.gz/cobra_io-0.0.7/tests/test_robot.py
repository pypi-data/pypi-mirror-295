import json
import unittest
import xml.etree.ElementTree as ET

import pinocchio
import timor.Robot

import cobra
from cobra.utils import urls, logging, caches
from cobra.utils.requests import session


class TestRobotAPI(unittest.TestCase):
    """Test robot API."""
    def test_API_available(self):
        """Test if API is available."""
        r = session.get(urls.MODULE_DB_URL)
        logging.info(f"Testing if robot API is available at {r.request.url}.")
        self.assertEqual(r.status_code, 200)
        self.assertGreaterEqual(len(r.json()), 1)

    def test_all_downloadable(self):
        """Test if all robots are downloadable."""
        caches.reset_cache()
        robots = cobra.robot.get_available_module_dbs()
        for robot in robots:
            f = cobra.robot.get_module_db(robot)
            self.assertTrue(f.is_file())
            data = json.load(f.open())
            self.assertTrue('modules' in data)
            self.assertTrue(len(data['modules']) > 0)

        local_robots = cobra.robot.get_available_module_dbs(locally=True)
        self.assertEqual(robots, local_robots)
        for robot in robots:
            f = cobra.robot.get_module_db(robot)
            self.assertTrue(f.is_file())
            data = json.load(f.open())
            self.assertTrue('modules' in data)
            self.assertTrue(len(data['modules']) > 0)

    def test_schema_download(self):
        caches.reset_cache()
        f = cobra.robot.get_schema()
        self.assertTrue(f.is_file())
        data = json.load(f.open())
        self.assertTrue('$id' in data)
        self.assertTrue('$schema' in data)

    def test_schema_validator(self):
        schema, validator = cobra.robot.get_schema_validator()
        self.assertIsNotNone(schema)
        self.assertIsNotNone(validator)
        db_file = cobra.robot.get_module_db('IMPROV')
        db_data = json.load(db_file.open())
        self.assertTrue(validator.is_valid(db_data))

    def test_urdf_download(self):
        caches.reset_cache()
        f = cobra.robot.get_urdf('IMPROV', module_order=['1', '21', '101'])
        self.assertTrue(f.is_file())
        data = f.open().read()
        self.assertTrue(data.startswith('<robot name="Auto-Generated: '))
        f1 = cobra.robot.get_urdf('IMPROV', module_order=['1', '21', '101'])  # Hit cache
        self.assertTrue(f1.is_file())
        self.assertEqual(f, f1)
        # Make sure assets available
        urdf_tree = ET.parse(f)
        for mesh in urdf_tree.findall('.//mesh'):
            file_name = mesh.attrib['filename']
            file_name = file_name.replace('package://', '')
            self.assertTrue(f.parent.joinpath(file_name).is_file())
        # Make sure URDF is readable
        r_timor = timor.Robot.PinRobot.from_urdf(f, f.parent)
        self.assertIsNotNone(r_timor.random_configuration())
        r_pin = pinocchio.RobotWrapper.BuildFromURDF(str(f), str(f.parent))
        self.assertIsNotNone(r_pin)

        urdf_with_wrl = cobra.robot.get_urdf('IMPROV', module_order=['1', '21', '101'],
                                             force_download=True, accept_wrl=True)
        self.assertTrue(urdf_with_wrl.is_file())
        for mesh in ET.parse(urdf_with_wrl).findall('.//mesh'):
            file_name = mesh.attrib['filename']
            file_name = file_name.replace('package://', '')
            self.assertTrue(f.parent.joinpath(file_name).is_file())
        with self.assertRaises(ValueError):
            timor.Robot.PinRobot.from_urdf(urdf_with_wrl, f.parent)  # Timor / pinochio does not support wrl
