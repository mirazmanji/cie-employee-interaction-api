import unittest
from app import app, db

class BasicTests(unittest.TestCase):

        @classmethod
        def setUpClass(cls) -> None:
            pass

        @classmethod
        def tearDown(self) -> None:
            pass

        def setUp(self):
            # Create test client
            self.app = app.test_client()
            #propogate the exceptions to the test client
            self.app.testing = True

        def tearDown(self):
            pass

        def test_employees_status(self):
            # sends HTTP GET request to the application
            # on the specified path
            result = self.app.get('/employees')
            # assert the status code of the response
            self.assertEqual(result.status_code, 200)

        def test_employees_data(self):
            # sends the HTTP GET request to the application
            # on the specified path
            result = self.app.get('/employees')
            # assert the response data
            self.assertEqual(result.data, "Connection Refused")

        def test_employee_salary_status(self):
            # sends HTTP GET request to the application
            # on the specified path
            result = self.app.get('/employees/100010')
            # assert the status code of the response
            self.assertEqual(result.status_code, 200)

        def test_employees_salary_data(self):
            # sends the HTTP GET request to the application
            # on the specified path
            result = self.app.get('/employees/100010')
            # assert the response data
            self.assertEqual(result.data, "Connection Refused")

# TODO: Test cases for valid output from DB, Test Auth Keys, Test null values

# runs the unit tests in the module
if __name__ == '__main__':
    unittest.main()