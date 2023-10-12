import unittest
import json
import requests


class MyTestCase(unittest.TestCase):

    def test_post_new_todo(self):
        new_todo = {
            "doneStatus": False,
            "description": "Writing code",
            "title": "Unit Testing"
        }

        response = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo))
        self.assertEqual(response.status_code, requests.codes.created)

    def test_get_new_todo(self):
        new_todo = {
            "doneStatus": True,
            "description": "Writing code 2",
            "title": "Unit Testing 2"
        }

        response = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo))
        response2 = requests.get("http://localhost:4567/todos/" + str(response.json()['id']))
        self.assertEqual(response2.json()['todos'][0]['doneStatus'], response.json()["doneStatus"])
        self.assertEqual(response2.json()['todos'][0]['description'], response.json()['description'])
        self.assertEqual(response2.json()['todos'][0]['title'], response.json()['title'])

    def test_get_all_todos(self):
        response1 = requests.get("http://localhost:4567/todos")
        self.assertEqual(response1.status_code, requests.codes.ok)


if __name__ == '__main__':
    unittest.main()
