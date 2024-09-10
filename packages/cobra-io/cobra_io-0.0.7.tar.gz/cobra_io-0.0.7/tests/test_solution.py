from contextlib import redirect_stdout
import io
import json
import logging
import os
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch
import uuid

from timor.task import Solution, Task
import unittest

import cobra.solution
from cobra.utils import caches
from cobra.utils.requests import session


class TestSolutionAPI(unittest.TestCase):
    """Test solution API."""
    def test_solution_retrieval(self):
        with self.assertRaises(KeyError):
            cobra.solution.find_solutions(task_id='simple/PTP_1', version="some-not-existing-version")
        solution_uuids, solution_details = cobra.solution.find_solutions(task_id='simple/PTP_1')
        self.assertGreater(len(solution_uuids), 0)
        for solution_uuid, solution in zip(solution_uuids, solution_details):
            self.assertIsNotNone(solution['id'])
            self.assertIsNotNone(solution['costFunction'])
            self.assertIsNotNone(solution['cost'])
            self.assertEqual(session.get(solution['json']).status_code, 200)

            # Check details same:
            detail = cobra.solution.get_solution_details(solution_uuid)
            for k in detail.keys():
                if k in {'json', 'png', 'html'}:
                    continue  # Might change due to storage bucket creating new access tokens
                self.assertEqual(detail[k], solution[k])

    def test_solution_file_retrieval(self):
        solution_uuids, _ = cobra.solution.find_solutions(task_id='simple/PTP_1')
        first = cobra.solution.get_solution(solution_uuids[0])
        # test cache
        cached = cobra.solution.get_solution(solution_uuids[0])
        for solution_file, task_file in [first, cached]:
            self.assertTrue(solution_file.is_file())
            self.assertTrue(task_file.is_file())
            self.assertIsNotNone(json.load(solution_file.open()))
            self.assertIsNotNone(json.load(task_file.open()))
            timor_task = Task.Task.from_json_file(task_file)
            self.assertIsNotNone(timor_task)
            timor_solution = Solution.SolutionTrajectory.from_json_file(solution_file, {timor_task.id: timor_task})
            self.assertIsNotNone(timor_solution)
            self.assertIsNotNone(timor_solution.cost)

    def test_solution_retrieval_errors(self):
        with self.assertRaises(ValueError):
            cobra.solution.find_solutions()
        with self.assertRaises(KeyError):
            cobra.solution.find_solutions(task_id='non-existing-task-id')
        with self.assertRaises(ValueError):
            cobra.solution.find_solutions(task_uuid="non-existing-task-uuid")
        with self.assertRaises(ValueError):
            cobra.solution.get_solution_details(solution_uuid="non-existing-solution-uuid")

    def test_solution_upload(self,
                             test_user=os.environ.get("TEST_USER", 'cobra@cps.cit.tum.de'),
                             test_password=os.environ.get("TEST_USER_PASSWORD", '!2345678')):
        """
        Run test of solution upload / removal.

        :param test_user: User to use for testing. Is set via hidden variable in CI.
        :param test_password: Password to use for testing. Is set via hidden variable in CI.
        """
        caches.reset_cache()
        logging.info(f"Running test with user {test_user}")
        solution_uuids, solutions_data = cobra.solution.find_solutions(task_id='simple/PTP_1')
        solution_file, task_file = cobra.solution.get_solution(solution_uuids[0])
        solution_data = json.load(solution_file.open())
        # Alter such that registered as new solution
        solution_data['author'].append('CoBRA I/O Test Case ' + str(uuid.uuid1()))
        if test_user in solution_data['email']:
            solution_data['email'].remove(test_user)
        with tempfile.NamedTemporaryFile("w") as tmp_file:
            json.dump(solution_data, tmp_file)
            tmp_file.flush()
            with self.assertRaises(ValueError):  # User not in solution file
                cobra.solution.submit_solution(Path(tmp_file.name), test_user, test_password)
        with tempfile.NamedTemporaryFile("w") as tmp_file:
            solution_data['email'].append(test_user)
            json.dump(solution_data, tmp_file)
            tmp_file.flush()
            status, solution_uuid = cobra.solution.submit_solution(Path(tmp_file.name), test_user, test_password)
            self.assertTrue(status)
        retrieved_solution, _ = cobra.solution.get_solution(solution_uuid=solution_uuid)
        self.assertEqual(solution_data, json.load(retrieved_solution.open()))
        self.assertTrue(cobra.solution.delete_solution(solution_uuid, test_user, test_password))
        with self.assertRaises(ValueError):
            cobra.solution.get_solution(solution_uuid=solution_uuid, force_download=False)
        with self.assertRaises(ValueError):
            cobra.solution.get_solution(solution_uuid=solution_uuid, force_download=True)

    def test_schema_download(self):
        caches.reset_cache()
        f = cobra.solution.get_schema()
        self.assertTrue(f.is_file())
        data = json.load(f.open())
        self.assertTrue('$id' in data)
        self.assertTrue('$schema' in data)
        # Check that cached version is used
        f = cobra.solution.get_schema()
        self.assertTrue(f.is_file())
        data = json.load(f.open())
        self.assertTrue('$id' in data)
        self.assertTrue('$schema' in data)

    def test_main(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            with patch.object(sys, 'argv', ["solution.py", "--task_id", "simple/PTP_1"]):
                cobra.solution.main()
        self.assertTrue("solutions for task simple/PTP_1 in version" in stdout.getvalue())
        solution_uuids, _ = cobra.solution.find_solutions(task_id='simple/PTP_1')
        with redirect_stdout(stdout):
            with patch.object(sys, 'argv', ["solution.py", "--solution_uuid", solution_uuids[0]]):
                cobra.solution.main()
        self.assertTrue("Solution file: " in stdout.getvalue())
        self.assertTrue(", Task file: " in stdout.getvalue())

    def test_neg_solution(self):
        files = cobra.solution.get_negative_solutions(force_download=True)
        self.assertTrue(len(files) > 0)
        for file in files:
            self.assertTrue(file.is_file())
            self.assertTrue(file.name.endswith('.json'))
            data = json.load(file.open())
            self.assertIn('failure', data)
            self.assertIn('taskID', data)
