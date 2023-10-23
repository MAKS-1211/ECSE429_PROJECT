import unittest
import json
import requests
import os
import subprocess
import time


class MyTestCase(unittest.TestCase):
    """
    Run before start of Unit Testing for this class
    """

    @classmethod
    def setUpClass(cls):
        cls.current_directory = os.getcwd()
        cls.api_path = cls.current_directory + "/runTodoManagerRestAPI-1.5.22.jar"
        cls.jar_process = subprocess.Popen(['java', '-jar', cls.api_path])
        time.sleep(5)

    """
    Run function at the end of Unit testing for this class
    """

    @classmethod
    def tearDownClass(cls):
        cls.jar_process.terminate()
        cls.jar_process.wait()

    """
    Run before every test function in this class
    """

    def setUp(self):
        response = requests.get("http://localhost:4567/todos")
        for data_points in response.json()['todos']:
            deleted_id = str(data_points['id'])
            requests.delete("http://localhost:4567/todos/" + deleted_id)

    """
    Check for JSON Malformation errors
    """

    def test_json_malformed(self):
        malformed_json = {
            "attribute1": "does not exist",
            "attribute2": False,
            "attribute3": -1
        }

        response = requests.post("http://localhost:4567/todos", data=json.dumps(malformed_json))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["errorMessages"][0], "Could not find field: attribute1 on Entity todo")

    """
    Check for XML Malformation errors
    """

    def test_xml_malformed(self):
        malformed_xml = """
      <root>
        <attribute1>does not exist</attribute1>
        <attribute2>false</attribute2>
        <attribute3>-1</attribute3>
      </root>
      """

        headers = {
            'Content-Type': 'application/xml'
        }

        response = requests.post("http://localhost:4567/todos", data=malformed_xml, headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["errorMessages"][0],
                         "java.lang.IllegalStateException: Expected BEGIN_OBJECT but was STRING at line 2 column 7 path $")

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

    """
    Test for error checking on not posting title for new todo item 
    """

    def test_post_new_todo_no_title(self):  # Invalid
        new_todo = {
            "doneStatus": False,
            "description": "Writing code",
        }

        response = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["errorMessages"][0], "title : field is mandatory")

    """
    Test for checking when no description is posted for new todo item
    """

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

    """
    Test for error check if new todo item is posted with a user generated todo ID
    """

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

    """
    Test for checking when no doneStatus is posted for new todo item
    """

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

    """
    Test for error check when empty string title is posted for new todo item
    """

    def test_post_new_todo_empty_title(self):  # InValid
        new_todo = {
            "description": "Python coding",
            "doneStatus": False,
            "title": ""
        }

        response = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["errorMessages"][0], "Failed Validation: title : can not be empty")

    """
    Test for getting 1 todos from getting all todos
    """

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

    """
       Test for getting multiple todos from getting all todos
    """

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

    """
    Test for updating doneStatus of a pre-existing todo item
    """

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

    """
        Test for updating description of a pre-existing todo item
        """

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

    """
        Test for updating title of a pre-existing todo item
        """

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

    """
    Test for error checking on updating title of a non existing todo item
    """

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

    """
    Test for get a single todo item from ID
    """

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

    """
    Test for error check on getting todo item of a non existent ID
    """

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

    """
        Test for error check on getting todo item of a non existent negative ID
    """

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

    """
        Test for updating all items of a todo list from a single query
    """

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

    """
    Test for updating doneStatus of a pre existent todo item from ID
    """

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

    """
        Test for updating doneStatus of a pre existent todo item from ID
    """

    def test_put_for_amend_done_status_single_todo_completely(self):  # BUG!!
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

        self.assertEqual(response2.status_code, 400)
        self.assertEqual(response2.json()["errorMessages"][0], "title : field is mandatory")


    """
    Test for updating description of a pre existent todo item from ID
    """

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

    """
        Test for updating description of a pre existent todo item from ID
    """
    def test_put_for_amend_description_single_todo_completely(self):  # BUG!!
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

        self.assertEqual(response2.status_code, 400)
        self.assertEqual(response2.json()["errorMessages"][0], "title : field is mandatory")

    """
        Test for updating title of a pre existent todo item from ID
        """
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

    """
        Test for updating title of a pre existent todo item from ID
    """
    def test_put_for_amend_title_single_todo_completely(self):  # BUG!!
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
        self.assertEqual(str(response2.json()['doneStatus']).upper(), "FALSE")
        self.assertEqual(response2.json()['description'], "")
        self.assertEqual(response2.json()['title'], edited_new_todo1['title'])


    """
    Test for deletion of a single todo item through ID
    """
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

    """
        Test for error check on deletion of a non existent single todo item through ID
    """
    def test_delete_non_existent_single_todo(self):
        new_todo1 = {
            "doneStatus": True,
            "description": "Writing code 1",
            "title": "Unit Testing 1"
        }

        response1 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))

        response2 = requests.delete("http://localhost:4567/todos/" + str(int(response1.json()['id']) + 1))

        self.assertEqual(response2.status_code, 404)
        self.assertEqual(response2.json()["errorMessages"][0], "Could not find any instances with todos/"
                         + str(int(response1.json()['id']) + 1))

    """
            Test for error check on deletion of a negative single todo item through ID
    """
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
