import os
import shutil
import tempfile
import unittest
from unittest.mock import patch
import json
import logging
from app.utils import get_params, prepare_logging, log, zip_and_delete_logs


class TestGetParams(unittest.TestCase):
    def setUp(self):
        self.test_file = os.path.join(tempfile.gettempdir(), "config.json")
        self.test_data = {
            "DIRS_TO_SEARCH": ["/test/dir1", "test/dir2"],
            "MAX_DAYS_THRESHOLD": 7,
        }
        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump(self.test_data, f)

    def tearDown(self):
        os.remove(self.test_file)

    def test_get_params(self):
        dirs_to_search, max_days_threshold = get_params(self.test_file)
        self.assertEqual(dirs_to_search, self.test_data["DIRS_TO_SEARCH"])
        self.assertEqual(max_days_threshold, int(self.test_data["MAX_DAYS_THRESHOLD"]))


class TestPrepareLogging(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        logger = logging.getLogger()
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

        shutil.rmtree(self.test_dir)

    def test_prepare_logging(self):
        log_file = os.path.join(self.test_dir, "logs.log")
        prepare_logging(self.test_dir)
        self.assertTrue(os.path.exists(log_file))


class TestLog(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.test_dir, "logs.log")
        prepare_logging(self.test_dir)

    def tearDown(self):
        logger = logging.getLogger()
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)
        shutil.rmtree(self.test_dir)

    def test_log(self):
        message = "Test message"
        log(message)

        with open(self.log_file, "r", encoding="utf-8") as f:
            self.assertIn(message, f.read())


class TestZipAndDeleteLogs(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def create_test_files(self, filenames):
        for filename in filenames:
            file_path = os.path.join(self.test_dir, filename)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("test content")

    @patch("os.path.getmtime")
    def test_zip_and_delete_logs_old_files(self, mock_getmtime):
        mock_getmtime.return_value = 0  # Simulate old files

        test_files = ["file1.log", "file2.txt", "file3.py"]
        self.create_test_files(test_files)

        zip_and_delete_logs(self.test_dir, file_age_limit=1)

        for filename in test_files[:2]:
            zip_path = os.path.join(self.test_dir, f"{filename}.zip")
            self.assertTrue(os.path.exists(zip_path))

            file_path = os.path.join(self.test_dir, filename)
            self.assertFalse(os.path.exists(file_path))

        file_path = os.path.join(self.test_dir, test_files[2])
        self.assertTrue(os.path.exists(file_path))

    @patch("os.path.getmtime")
    def test_zip_and_delete_logs_new_files(self, mock_getmtime):
        mock_getmtime.return_value = 1  # Simulate new files

        test_files = ["file1.log", "file2.txt", "file3.py"]
        self.create_test_files(test_files)
        zip_and_delete_logs(self.test_dir, file_age_limit=1)

        for filename in test_files:
            file_path = os.path.join(self.test_dir, filename)
            self.assertTrue(os.path.exists(file_path))
            zip_path = os.path.join(self.test_dir, f"{filename}.zip")
            self.assertFalse(os.path.exists(zip_path))


if __name__ == "__main__":
    unittest.main()
