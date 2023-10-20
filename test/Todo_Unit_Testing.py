import unittest
import json
import requests
import os
import subprocess
import time


class MyTestCase(unittest.TestCase):
    """def setUp2(self):
        self.current_directory = os.getcwd()
        self.api_path = self.current_directory + "/runTodoManagerRestAPI-1.5.22.jar"
        print(self.api_path)
        self.jar_process = subprocess.Popen(['java', '-jar', self.api_path])
        time.sleep(5)
        response1 = requests.delete("http://localhost:4567/todos/1")
        response2 = requests.delete("http://localhost:4567/todos/2")"""

    '''def tearDown(self):
        self.jar_process.terminate()
        self.jar_process.wait()'''

    @classmethod
    def setUpClass(cls):
        cls.current_directory = os.getcwd()
        cls.api_path = cls.current_directory + "/runTodoManagerRestAPI-1.5.22.jar"
        cls.jar_process = subprocess.Popen(['java', '-jar', cls.api_path])
        time.sleep(5)

    @classmethod
    def tearDownClass(cls):
        cls.jar_process.terminate()
        cls.jar_process.wait()

    def setUp(self):
        response = requests.get("http://localhost:4567/todos")
        for data_points in response.json()['todos']:
            deleted_id = str(data_points['id'])
            requests.delete("http://localhost:4567/todos/" + deleted_id)

    """
    Post request of new todo object with all valid attributes
    """

    def test_post_new_todo(self):  # Valid
        new_todo = {
            "doneStatus": False,
            "description": "Writing code",
            "title": "Unit Testing"
        }

        response = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo))
        self.assertEqual(response.status_code, requests.codes.created)
        self.assertEqual(str(response.json()['doneStatus']).upper(), str(new_todo['doneStatus']).upper())
        self.assertEqual(response.json()['description'], new_todo['description'])
        self.assertEqual(response.json()['title'], new_todo['title'])

    """
    Post request of new todo object with non-boolean attribute for doneStatus
    """

    def test_post_new_todo_done_status_non_boolean(self):  # Invalid
        new_todo = {
            "doneStatus": str("False"),
            "description": "Writing code",
            "title": "Unit Testing"
        }

        response = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["errorMessages"][0], "Failed Validation: doneStatus should be BOOLEAN")

    def test_post_new_todo_no_title(self):  # Invalid
        new_todo = {
            "doneStatus": False,
            "description": "Writing code",
        }

        response = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["errorMessages"][0], "title : field is mandatory")

    def test_post_new_todo_no_description(self):  # Valid
        new_todo = {
            "doneStatus": False,
            "title": "Exploratory Testing"
        }

        response = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo))
        self.assertEqual(response.status_code, requests.codes.created)
        self.assertEqual(str(response.json()['doneStatus']).upper(), str(new_todo['doneStatus']).upper())
        self.assertEqual(response.json()['description'], "")
        self.assertEqual(response.json()['title'], new_todo['title'])

    def test_post_new_todo_with_new_id(self):  # Invalid
        new_todo = {
            "id": 20,
            "description": "Python coding",
            "doneStatus": False,
            "title": "Exploratory Testing"
        }

        response = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["errorMessages"][0], "Invalid Creation: Failed Validation: Not allowed to "
                                                              "create with id")

    def test_post_new_todo_without_doneStatus(self):  # Valid
        new_todo = {
            "description": "Python coding",
            "title": "Exploratory Testing"
        }

        response = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo))
        self.assertEqual(response.status_code, requests.codes.created)
        self.assertEqual(str(response.json()['doneStatus']).upper(), "FALSE")
        self.assertEqual(response.json()['description'], new_todo['description'])
        self.assertEqual(response.json()['title'], new_todo['title'])

    def test_post_new_todo_empty_title(self):  # InValid
        new_todo = {
            "description": "Python coding",
            "doneStatus": False,
            "title": ""
        }

        response = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["errorMessages"][0], "Failed Validation: title : can not be empty")

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
        self.assertEqual(response2.status_code, requests.codes.ok)

    def test_get_all_todos(self):
        new_todo1 = {
            "doneStatus": True,
            "description": "Writing code 1",
            "title": "Unit Testing 1"
        }

        new_todo2 = {
            "doneStatus": False,
            "description": "Writing code 2",
            "title": "Unit Testing 2"
        }

        new_todo3 = {
            "description": "Writing code 3",
            "title": "Unit Testing 3"
        }

        new_todo4 = {
            "doneStatus": True,
            "title": "Unit Testing 4"
        }

        response1 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))
        response2 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo2))
        response3 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo3))
        response4 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo4))
        response_output = requests.get("http://localhost:4567/todos")

        self.assertEqual(response_output.status_code, requests.codes.ok)
        self.assertEqual(len(response_output.json()['todos'][0]), 4)

        for data_points in response_output.json()['todos']:

            if data_points['id'] == response1.json()['id']:
                self.assertEqual(data_points['doneStatus'], response1.json()["doneStatus"])
                self.assertEqual(data_points['description'], response1.json()['description'])
                self.assertEqual(data_points['title'], response1.json()['title'])

            elif data_points['id'] == response2.json()['id']:
                self.assertEqual(data_points['doneStatus'], response2.json()["doneStatus"])
                self.assertEqual(data_points['description'], response2.json()['description'])
                self.assertEqual(data_points['title'], response2.json()['title'])

            elif data_points['id'] == response3.json()['id']:
                self.assertEqual(data_points['doneStatus'], response3.json()["doneStatus"])
                self.assertEqual(data_points['description'], response3.json()['description'])
                self.assertEqual(data_points['title'], response3.json()['title'])

            elif data_points['id'] == response4.json()['id']:
                self.assertEqual(data_points['doneStatus'], response4.json()["doneStatus"])
                self.assertEqual(data_points['description'], response4.json()['description'])
                self.assertEqual(data_points['title'], response4.json()['title'])

            else:
                self.fail("ID not matching!")

    def test_post_for_amend_done_status_single_todo(self):

        new_todo1 = {
            "doneStatus": True,
            "description": "Writing code 1",
            "title": "Unit Testing 1"
        }

        response1 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))

        edited_new_todo1 = {
            "doneStatus": False,
        }

        response2 = requests.post("http://localhost:4567/todos/" + str(response1.json()["id"]),
                                  data=json.dumps(edited_new_todo1))

        self.assertEqual(response2.json()['id'], response1.json()['id'])
        self.assertEqual(str(response2.json()['doneStatus']).upper(), str(edited_new_todo1['doneStatus']).upper())
        self.assertEqual(response2.json()['description'], new_todo1['description'])
        self.assertEqual(response2.json()['title'], new_todo1['title'])
        self.assertEqual(response2.status_code, 200)

    def test_post_for_amend_description_single_todo(self):

        new_todo1 = {
            "doneStatus": True,
            "description": "Writing code 1",
            "title": "Unit Testing 1"
        }

        response1 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))

        edited_new_todo1 = {
            "description": "Writing code better",
        }

        response2 = requests.post("http://localhost:4567/todos/" + str(response1.json()["id"]),
                                  data=json.dumps(edited_new_todo1))

        self.assertEqual(response2.json()['id'], response1.json()['id'])
        self.assertEqual(str(response2.json()['doneStatus']).upper(), str(new_todo1['doneStatus']).upper())
        self.assertEqual(response2.json()['description'], edited_new_todo1['description'])
        self.assertEqual(response2.json()['title'], new_todo1['title'])
        self.assertEqual(response2.status_code, 200)

    def test_post_for_amend_title_single_todo(self):

        new_todo1 = {
            "doneStatus": True,
            "description": "Writing code 1",
            "title": "Unit Testing 1"
        }

        response1 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))

        edited_new_todo1 = {
            "title": "Better Unit Testing!",
        }

        response2 = requests.post("http://localhost:4567/todos/" + str(response1.json()["id"]),
                                  data=json.dumps(edited_new_todo1))

        self.assertEqual(response2.json()['id'], response1.json()['id'])
        self.assertEqual(str(response2.json()['doneStatus']).upper(), str(new_todo1['doneStatus']).upper())
        self.assertEqual(response2.json()['title'], edited_new_todo1['title'])
        self.assertEqual(response2.json()['description'], new_todo1['description'])
        self.assertEqual(response2.status_code, 200)

    def test_post_for_amend_non_existent_single_todo(self):  # Invalid

        new_todo1 = {
            "doneStatus": True,
            "description": "Writing code 1",
            "title": "Unit Testing 1"
        }

        response1 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))

        edited_new_todo1 = {
            "title": "Better Unit Testing!",
        }

        response2 = requests.post("http://localhost:4567/todos/" + str(int(response1.json()["id"]) + 1),
                                  data=json.dumps(edited_new_todo1))

        self.assertEqual(response2.status_code, 404)
        self.assertEqual(response2.json()["errorMessages"][0], "No such todo entity instance with GUID or ID "
                         + str(int(response1.json()["id"]) + 1) + " found")

    def test_get_single_todo(self):

        new_todo1 = {
            "doneStatus": True,
            "description": "Writing code 1",
            "title": "Unit Testing 1"
        }

        response1 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))

        response2 = requests.get("http://localhost:4567/todos/" + str(response1.json()['id']))

        self.assertEqual(response2.json()['todos'][0]['id'], response1.json()['id'])
        self.assertEqual(str(response2.json()['todos'][0]['doneStatus']).upper(), str(new_todo1['doneStatus']).upper())
        self.assertEqual(response2.json()['todos'][0]['title'], new_todo1['title'])
        self.assertEqual(response2.json()['todos'][0]['description'], new_todo1['description'])
        self.assertEqual(response2.status_code, 200)

    def test_get_positive_non_existent_single_todo(self):

        new_todo1 = {
            "doneStatus": True,
            "description": "Writing code 1",
            "title": "Unit Testing 1"
        }

        response1 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))

        response2 = requests.get("http://localhost:4567/todos/" + str(int(response1.json()['id']) + 1))

        self.assertEqual(response2.status_code, 404)
        self.assertEqual(response2.json()["errorMessages"][0], "Could not find an instance with todos/"
                         + str(int(response1.json()["id"]) + 1))

    def test_get_negative_non_existent_single_todo(self):

        new_todo1 = {
            "doneStatus": True,
            "description": "Writing code 1",
            "title": "Unit Testing 1"
        }

        response1 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))

        response2 = requests.get("http://localhost:4567/todos/" + str(-100))

        self.assertEqual(response2.status_code, 404)
        self.assertEqual(response2.json()["errorMessages"][0], "Could not find an instance with todos/"
                         + str(-100))

    def test_put_for_amend_all_single_todo(self):
        new_todo1 = {
            "doneStatus": True,
            "description": "Writing code 1",
            "title": "Unit Testing 1"
        }

        response1 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))

        edited_new_todo1 = {
            "doneStatus": False,
            "description": "Writing code for ECSE",
            "title": "Unit Testing for ECSE"
        }

        response2 = requests.put("http://localhost:4567/todos/" + str(response1.json()["id"]),
                                 data=json.dumps(edited_new_todo1))

        self.assertEqual(response2.json()['id'], response1.json()['id'])
        self.assertEqual(str(response2.json()['doneStatus']).upper(), str(edited_new_todo1['doneStatus']).upper())
        self.assertEqual(response2.json()['description'], edited_new_todo1['description'])
        self.assertEqual(response2.json()['title'], edited_new_todo1['title'])
        self.assertEqual(response2.status_code, 200)

    def test_put_for_amend_done_status_single_todo(self):  # BUG!!
        new_todo1 = {
            "doneStatus": True,
            "description": "Writing code 1",
            "title": "Unit Testing 1"
        }

        response1 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))

        edited_new_todo1 = {
            "doneStatus": False
        }

        response2 = requests.put("http://localhost:4567/todos/" + str(response1.json()["id"]),
                                 data=json.dumps(edited_new_todo1))

        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.json()['id'], response1.json()['id'])
        self.assertEqual(str(response2.json()['doneStatus']).upper(), str(edited_new_todo1['doneStatus']).upper())
        self.assertEqual(response2.json()['description'], new_todo1['description'])
        self.assertEqual(response2.json()['title'], new_todo1['title'])

    def test_put_for_amend_description_single_todo(self):  # BUG!!
        new_todo1 = {
            "doneStatus": True,
            "description": "Writing code 1",
            "title": "Unit Testing 1"
        }

        response1 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))

        edited_new_todo1 = {
            "description": "Writing code for ECSE"
        }

        response2 = requests.put("http://localhost:4567/todos/" + str(response1.json()["id"]),
                                 data=json.dumps(edited_new_todo1))

        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.json()['id'], response1.json()['id'])
        self.assertEqual(str(response2.json()['doneStatus']).upper(), str(new_todo1['doneStatus']).upper())
        self.assertEqual(response2.json()['description'], edited_new_todo1['description'])
        self.assertEqual(response2.json()['title'], new_todo1['title'])

    def test_put_for_amend_title_single_todo(self):  # BUG!!
        new_todo1 = {
            "doneStatus": True,
            "description": "Writing code 1",
            "title": "Unit Testing 1"
        }

        response1 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))

        edited_new_todo1 = {
            "title": "Unit Testing for ECSE"
        }

        response2 = requests.put("http://localhost:4567/todos/" + str(response1.json()["id"]),
                                 data=json.dumps(edited_new_todo1))

        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.json()['id'], response1.json()['id'])
        self.assertEqual(str(response2.json()['doneStatus']).upper(), str(new_todo1['doneStatus']).upper())
        self.assertEqual(response2.json()['description'], new_todo1['description'])
        self.assertEqual(response2.json()['title'], edited_new_todo1['title'])

    def test_delete_single_todo(self):
        new_todo1 = {
            "doneStatus": True,
            "description": "Writing code 1",
            "title": "Unit Testing 1"
        }

        response1 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))

        response2 = requests.delete("http://localhost:4567/todos/" + str(response1.json()['id']))

        self.assertEqual(response2.status_code, 200)

        response3 = requests.get("http://localhost:4567/todos/" + str(response1.json()['id']))

        self.assertEqual(response3.status_code, 404)
        self.assertEqual(response3.json()["errorMessages"][0], "Could not find an instance with todos/"
                         + str(response1.json()['id']))

    def test_delete_non_existent_single_todo(self):
        new_todo1 = {
            "doneStatus": True,
            "description": "Writing code 1",
            "title": "Unit Testing 1"
        }

        response1 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))

        response2 = requests.delete("http://localhost:4567/todos/" + str(int(response1.json()['id'])+1))

        self.assertEqual(response2.status_code, 404)
        self.assertEqual(response2.json()["errorMessages"][0], "Could not find any instances with todos/"
                         + str(int(response1.json()['id'])+1))

    def test_delete_negative_id_single_todo(self):
        new_todo1 = {
            "doneStatus": True,
            "description": "Writing code 1",
            "title": "Unit Testing 1"
        }

        response1 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))

        response2 = requests.delete("http://localhost:4567/todos/" + str(-100))

        self.assertEqual(response2.status_code, 404)
        self.assertEqual(response2.json()["errorMessages"][0], "Could not find any instances with todos/"
                         + str(-100))


if __name__ == '__main__':
    unittest.main()
