import unittest
import os
import shutil
import time

from PyPIMetaMorphosis import create_pypi_project  # Import the function to test


class TestCreatePyPIProject(unittest.TestCase):

    def setUp(self):
        # Define test directory
        self.test_root_dir = "test_project"

    def tearDown(self):
        # Clean up the directory after the test
        if os.path.exists(self.test_root_dir):
            shutil.rmtree(self.test_root_dir)

    def test_create_pypi_project_success(self):
        # Test inputs
        project_name = "PyPIMetaMorphosis"
        author_name = "Test Author"
        author_email = "test_author@test.com"
        project_desc = "Test project description"

        # Run the function
        start_time = time.time()
        create_pypi_project(
            root_dir=self.test_root_dir,
            project_name=project_name,
            author_name=author_name,
            author_email=author_email,
            project_desc=project_desc
        )
        end_time = time.time()

        # Verify that the root directory and the required subdirectories were created
        self.assertTrue(os.path.exists(self.test_root_dir))

        # Verify that the expected files were created
        expected_files = [
            "LICENSE", "README.md", ".gitignore", "run.py", "setup.py",
            os.path.join("app", "README.md"),
            os.path.join("app", project_name, "__init__.py"),
            os.path.join("app", project_name, "src", "__init__.py"),
            os.path.join("app", project_name, "src", f"{project_name}.py"),
            os.path.join("app", project_name, "test", "__init__.py"),
            os.path.join("app", project_name, "test",
                         f"test_{project_name}.py")
        ]

        # Print time taken for the operation
        print(f"⏰ Time taken: {(end_time - start_time) * 1000:.2f} ms")

    def test_missing_project_name(self):
        with self.assertRaises(ValueError) as context:
            create_pypi_project(root_dir=self.test_root_dir, project_name=None)
        self.assertEqual(str(context.exception), "Project name is required!")

    def test_time_taken(self):
        project_name = "TestProject"
        start_time = time.time()
        create_pypi_project(root_dir=self.test_root_dir,
                            project_name=project_name)
        end_time = time.time()

        # Check that the time taken is in reasonable bounds
        duration = (end_time - start_time) * 1000
        self.assertGreater(duration, 0)
        print(f"⏰ Time taken: {duration:.2f} ms")


if __name__ == '__main__':
    unittest.main()
