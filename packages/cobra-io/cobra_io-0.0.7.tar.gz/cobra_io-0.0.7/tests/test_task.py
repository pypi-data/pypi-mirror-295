from contextlib import redirect_stdout
import io
import json
import logging
from pathlib import Path
import sys
from unittest.mock import patch

from timor.task import Task
import unittest

import cobra.task
from cobra.utils import caches, urls
from cobra.utils.configurations import COBRA_VERSION
from cobra.utils.requests import session


class TestTaskAPI(unittest.TestCase):
    """Test task API."""
    def test_API_available(self):
        """Test if API is available."""
        r = session.get(urls.TASK_URL + '?page=1&page_size=2')
        logging.info(f"Testing if API is available at {r.request.url}.")
        self.assertEqual(r.status_code, 200)
        self.assertGreaterEqual(len(r.json()['results']), 1)

        r = session.get(urls.TASK_URL + '?scenario_id=simple/PTP_1&version=2022')
        logging.info(f"Testing if API is available at {r.request.url}.")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()['results']), 1)

    def test_task_retrieval(self):
        caches.reset_cache()
        task_file = cobra.task.get_task(id='simple/PTP_1')
        self.assertTrue(task_file.is_file())
        self.assertIsNotNone(json.load(task_file.open()))
        task = Task.Task.from_json_file(task_file)
        self.assertIsNotNone(task)
        with self.assertRaises(ValueError):
            cobra.task.get_task(version='some-not-existing-version')

    def test_find_tasks(self):
        caches.reset_cache()
        candidates, details = cobra.task.find_tasks(id='simple/PTP_1')
        self.assertEqual(len(candidates), 1)
        # Check details
        self.assertEqual(len(details), 1)
        self.assertEqual(details[0]['scenario_id'], 'simple/PTP_1')
        self.assertEqual(details[0]['version'], COBRA_VERSION)
        self.assertEqual(session.get(details[0]['html']).status_code, 200)
        self.assertEqual(session.get(details[0]['json']).status_code, 200)
        self.assertEqual(details[0]['metadata']['goal_count'], 2)
        task_file = cobra.task.get_task(uuid=details[0]['id'])
        self.assertTrue(task_file.is_file())
        self.assertIsNotNone(json.load(task_file.open()))
        task = Task.Task.from_json_file(task_file)
        self.assertIsNotNone(task)
        # Check details same:
        detail = cobra.task.get_task_details(candidates[0])
        for k in detail.keys():
            if k in {'json', 'png', 'html'}:
                continue  # Might change due to storage bucket creating new access tokens
            self.assertEqual(detail[k], details[0][k])
        # Check wrong version
        candidates, details = cobra.task.find_tasks(id='simple/PTP_1', version='some-not-existing-version')
        self.assertEqual(len(candidates), 0)
        # Check wrong id
        candidates, details = cobra.task.find_tasks(id='some-not-existing-id')
        self.assertEqual(len(candidates), 0)

    def test_task_with_asset(self):
        caches.reset_cache()
        task_file = cobra.task.get_task(id='simple/PTP_2', fetch_assets=False)
        with self.assertRaises(FileNotFoundError):
            Task.Task.from_json_file(task_file)
        task_file = cobra.task.get_task(id='simple/PTP_2', fetch_assets=True)
        task = Task.Task.from_json_file(task_file)
        self.assertIsNotNone(task)

    def test_non_exising_task(self):
        with self.assertRaises(KeyError):
            cobra.task.get_task(uuid='some-not-existing-uuid')
        with self.assertRaises(ValueError):
            cobra.task.get_task_details(task_uuid='some-not-existing-uuid')
        with self.assertRaises(KeyError):
            cobra.task.get_task(id='some-not-existing-id')

    def test_schema_download(self):
        caches.reset_cache()
        f = cobra.task.get_schema()
        self.assertTrue(f.is_file())
        data = json.load(f.open())
        self.assertTrue('$id' in data)
        self.assertTrue('$schema' in data)
        # Check that cached version is used
        f = cobra.task.get_schema()
        self.assertTrue(f.is_file())
        data = json.load(f.open())
        self.assertTrue('$id' in data)
        self.assertTrue('$schema' in data)

    def test_schema_validator(self):
        schema, validator = cobra.task.get_schema_validator()
        self.assertIsNotNone(schema)
        self.assertIsNotNone(validator)
        task_file = cobra.task.get_task(id='simple/PTP_2', fetch_assets=False)
        task_data = json.load(task_file.open())
        self.assertTrue(validator.is_valid(task_data))

    def test_main(self):
        caches.reset_cache()
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            with patch.object(sys, 'argv', ["solution.py", "simple/PTP_1"]):
                cobra.task.main()
        task_file = Path(stdout.getvalue().strip())
        self.assertTrue(task_file.is_file())
        task = Task.Task.from_json_file(task_file)
        self.assertIsNotNone(task)
