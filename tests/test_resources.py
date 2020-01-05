import unittest
from service.webservice import app


class ResourcesTest(unittest.TestCase):
    app.testing = True

    def test_department(self):
        client = app.test_client()
        URL = '/departments/'

        with self.subTest('creating department'):
            r = client.post(URL, json={'name': 'test_dept'})
            self.assertEqual(201, r.status_code)

        with self.subTest('reading department'):
            r = client.get(URL + 'test_dept')
            self.assertEqual(r.get_json(), {'name': 'test_dept', 'avg_salary': None, "employees": 0})

        with self.subTest('editing department'):
            r = client.put(URL + 'test_dept', json={'name': 'test_dept_edited'})
            self.assertEqual(client.get(URL + 'test_dept_edited').get_json(),
                             {'name': 'test_dept_edited', 'avg_salary': None, "employees": 0})

        with self.subTest('removing department'):
            r = client.delete(URL + 'test_dept_edited')
            self.assertEqual(r.status_code, 204)

        with self.subTest('reading all departments'):
            r = client.get(URL)
            self.assertEqual(
                r.get_json(),
                [{"avg_salary": 2167, "employees": 3, "name": "IT"},
                 {"avg_salary": 3370, "employees": 2, "name": "PR"},
                 {"avg_salary": 1433, "employees": 3, "name": "Research"},
                 {"avg_salary": 1000, "employees": 1, "name": "Sales"}]
            )

        with self.subTest('reading nonexistent department'):
            r = client.get(URL + 'test_dept')
            self.assertEqual(r.status_code, 404)

    def test_user(self):
        client = app.test_client()
        URL = '/employees/'
        id = None

        with self.subTest('creating employee'):
            r = client.post(URL, json={'first_name': 'Test',
                                       'last_name': 'Test',
                                       'birth_date': '1995-05-05'})
            id = r.get_data().decode().strip()
            self.assertEqual(201, r.status_code)

        with self.subTest('reading employee'):
            r = client.get(URL + id)
            self.assertEqual(r.get_json()['first_name'], 'Test')

        with self.subTest('editing employee'):
            r = client.put(URL + id, json={'first_name': 'Edited'})
            self.assertEqual(client.get(URL + id).get_json()['first_name'], 'Edited')

        with self.subTest('removing employee'):
            r = client.delete(URL + id)
            self.assertEqual(r.status_code, 204)

        with self.subTest('reaing nonexistent employee'):
            r = client.get(URL + id)
            self.assertEqual(r.status_code, 404)
