import unittest
import requests


class ResourcesTest(unittest.TestCase):
    def test_department(self):
        URL = 'http://localhost:5000/departments/'

        with self.subTest():
            r = requests.post(URL, json={'name': 'test_dept'})
            self.assertEqual(201, r.status_code)

        with self.subTest():
            r = requests.get(URL + 'test_dept')
            self.assertEqual(r.json(), {'name': 'test_dept', 'avg_salary': None, "employees": 0})

        with self.subTest():
            r = requests.put(URL + 'test_dept', json={'name': 'test_dept_edited'})
            self.assertEqual(requests.get(URL + 'test_dept_edited').json(),
                             {'name': 'test_dept_edited', 'avg_salary': None, "employees": 0})

        with self.subTest():
            r = requests.delete(URL + 'test_dept_edited')
            self.assertEqual(r.status_code, 204)

        with self.subTest():
            r = requests.get(URL)
            self.assertEqual(
                r.json(),
                [{"avg_salary": 2167, "employees": 3, "name": "IT"},
                 {"avg_salary": 3370, "employees": 2, "name": "PR"},
                 {"avg_salary": 1433, "employees": 3, "name": "Research"},
                 {"avg_salary": 1000, "employees": 1, "name": "Sales"}]
            )

        with self.subTest():
            r = requests.get(URL + 'test_dept')
            self.assertEqual(r.json(), {'name': None, 'avg_salary': None, "employees": 0})

    def test_user(self):
        URL = 'http://localhost:5000/employees/'
        id = None

        with self.subTest():
            r = requests.post(URL, json={'first_name': 'Test',
                                         'last_name': 'Test',
                                         'birth_date': '1995-05-05'})
            id = r.text.strip()
            self.assertEqual(201, r.status_code)

        with self.subTest():
            r = requests.get(URL + id)
            self.assertEqual(r.json()['first_name'], 'Test')

        with self.subTest():
            r = requests.put(URL + id, json={'first_name': 'Edited'})
            self.assertEqual(requests.get(URL + id).json()['first_name'], 'Edited')

        with self.subTest():
            r = requests.delete(URL + id)
            self.assertEqual(r.status_code, 204)

        with self.subTest():
            r = requests.get(URL + id)
            self.assertEqual(r.status_code, 500)


if __name__ == '__main__':
    unittest.main()
