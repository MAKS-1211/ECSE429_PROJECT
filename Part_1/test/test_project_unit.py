import unittest
import json
import requests
import os
import subprocess
import time

# Defining HTTP status codes
NOT_FOUND = 404
BAD_REQUEST = 400
OK = 200
CREATED = 201

class MyTestCase(unittest.TestCase):
    '''
    This method sets up the class and prepares the system to be tested by running the API
    '''
    @classmethod
    def setUpClass(cls):
        cls.current_directory = os.getcwd()
        cls.api_path = cls.current_directory + "/runTodoManagerRestAPI-1.5.22.jar"
        cls.jar_process = subprocess.Popen(['java', '-jar', cls.api_path])
        time.sleep(5)

    '''
    This method closes up the class by shutting down the API
    '''
    @classmethod
    def tearDownClass(cls):
        cls.jar_process.terminate()
        cls.jar_process.wait()

    '''
    This method clears the database before every test so that the system can be in the same state for every test
    '''
    def setUp(self):
        response = requests.get("http://localhost:4567/projects")
        for data_points in response.json()['projects']:
            deleted_id = str(data_points['id'])
            requests.delete("http://localhost:4567/projects/" + deleted_id)

    '''
    This test checks if the API correctly handles malformed JSON input
    '''
    def test_json_malformed(self):
        malformed_json = {
            "attribute1": "does not exist",
            "attribute2": False,
            "attribute3": -1
        }

        response = requests.post("http://localhost:4567/projects", data=json.dumps(malformed_json))
        self.assertEqual(response.status_code, BAD_REQUEST)
        self.assertEqual(response.json()["errorMessages"][0], "Could not find field: attribute1 on Entity project")

    '''
    This test checks if the API correctly handles malformed XML input
    '''
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

        response = requests.post("http://localhost:4567/projects", data=malformed_xml, headers=headers)
        self.assertEqual(response.status_code, BAD_REQUEST)
        self.assertEqual(response.json()["errorMessages"][0], "java.lang.IllegalStateException: Expected BEGIN_OBJECT but was STRING at line 2 column 7 path $")

    '''
    This test checks if the API correctly posts a new project with all fields specified 
    '''
    def test_post_new_project(self):
        new_project = {
            "completed": True,
            "active": False,
            "description": "Exploratory Testing",
            "title": "Project 1"
        }

        response = requests.post("http://localhost:4567/projects", data=json.dumps(new_project))
        self.assertEqual(response.status_code, requests.codes.created)
        self.assertEqual(str(response.json()['completed']).upper(), str(new_project['completed']).upper())
        self.assertEqual(str(response.json()['active']).upper(), str(new_project['active']).upper())
        self.assertEqual(response.json()['description'], new_project['description'])
        self.assertEqual(response.json()['title'], new_project['title'])

    '''
    This test checks if the API correctly posts a new project with only the title specified 
    '''
    def test_post_project_only_title(self):
        new_project = {
            "title": "Project 2"
        }

        response = requests.post("http://localhost:4567/projects", data=json.dumps(new_project))
        self.assertEqual(response.status_code, requests.codes.created)
        self.assertEqual(str(response.json()['completed']).upper(), "FALSE")
        self.assertEqual(str(response.json()['active']).upper(), "FALSE")
        self.assertEqual(response.json()['description'], "")
        self.assertEqual(response.json()['title'], new_project['title'])

    '''
    This test checks if the API correctly posts a new project with only the description specified 
    '''
    def test_post_project_only_description(self):
        new_project = {
            "description": "description of project"
        }

        response = requests.post("http://localhost:4567/projects", data=json.dumps(new_project))
        self.assertEqual(response.status_code, requests.codes.created)
        self.assertEqual(str(response.json()['completed']).upper(), "FALSE")
        self.assertEqual(str(response.json()['active']).upper(), "FALSE")
        self.assertEqual(response.json()['description'], new_project['description'])
        self.assertEqual(response.json()['title'], "")

    '''
    This test checks if the API correctly posts a new project with only the active field specified 
    '''
    def test_post_project_only_active(self):
        new_project = {
            "active": True
        }

        response = requests.post("http://localhost:4567/projects", data=json.dumps(new_project))
        self.assertEqual(response.status_code, requests.codes.created)
        self.assertEqual(str(response.json()['completed']).upper(), "FALSE")
        self.assertEqual(str(response.json()['active']).upper(), str(new_project["active"]).upper())
        self.assertEqual(response.json()['description'], "")
        self.assertEqual(response.json()['title'], "")

    '''
    This test checks if the API correctly posts a new project with only the completed field specified 
    '''
    def test_post_project_only_completed(self):
        new_project = {
            "completed": True
        }

        response = requests.post("http://localhost:4567/projects", data=json.dumps(new_project))
        self.assertEqual(response.status_code, requests.codes.created)
        self.assertEqual(str(response.json()['completed']).upper(), str(new_project["completed"]).upper())
        self.assertEqual(str(response.json()['active']).upper(), "FALSE")
        self.assertEqual(response.json()['description'], "")
        self.assertEqual(response.json()['title'], "")

    '''
    This test checks if the API correctly raises an error when the completed field is mistyped 
    '''
    def test_post_project_completed_int(self):
        new_project = {
            "completed": 2
        }

        response = requests.post("http://localhost:4567/projects", data=json.dumps(new_project))
        self.assertEqual(response.status_code, BAD_REQUEST)
        self.assertEqual(response.json()["errorMessages"][0], "Failed Validation: completed should be BOOLEAN")

    '''
    This test checks if the API correctly raises an error when the active field is mistyped 
    '''
    def test_post_project_active_int(self):
        new_project = {
            "active": 2
        }

        response = requests.post("http://localhost:4567/projects", data=json.dumps(new_project))
        self.assertEqual(response.status_code, BAD_REQUEST)
        self.assertEqual(response.json()["errorMessages"][0], "Failed Validation: active should be BOOLEAN")

    '''
    This test checks if the API correctly raises an error when the active field is null 
    '''
    def test_post_project_active_null(self):
        new_project = {
            "active": None
        }

        response = requests.post("http://localhost:4567/projects", data=json.dumps(new_project))
        self.assertEqual(response.status_code, BAD_REQUEST)
        self.assertEqual(response.json()["errorMessages"][0], "Failed Validation: active should be BOOLEAN")

    '''
    This test checks if the API correctly raises an error when an id is specified
    '''
    def test_post_project_specified_id(self):
        new_project = {
            "id": 20
        }

        response = requests.post("http://localhost:4567/projects", data=json.dumps(new_project))
        self.assertEqual(response.status_code, BAD_REQUEST)
        self.assertEqual(response.json()["errorMessages"][0], "Invalid Creation: Failed Validation: Not allowed to create with id")

    '''
    This test checks if the API correctly gets all projects in the database 
    '''
    def test_get_all_projects(self):
        new_project1 = {
            "active": True,
            "completed": False,
            "description": "Project 2",
            "title": "Project Description 2"
        }

        new_project2 = {
            "active": False,
            "completed": True,
            "description": "Project 2",
            "title": "Project Description 2"
        }

        response1 = requests.post("http://localhost:4567/projects", data=json.dumps(new_project1))
        response2 = requests.post("http://localhost:4567/projects", data=json.dumps(new_project2))
        response_output = requests.get("http://localhost:4567/projects")

        self.assertEqual(response_output.status_code, requests.codes.ok)

        for data_points in response_output.json()['projects']:

            if data_points['id'] == response1.json()['id']:
                self.assertEqual(data_points['active'], response1.json()["active"])
                self.assertEqual(data_points['completed'], response1.json()["completed"])
                self.assertEqual(data_points['description'], response1.json()['description'])
                self.assertEqual(data_points['title'], response1.json()['title'])

            elif data_points['id'] == response2.json()['id']:
                self.assertEqual(data_points['active'], response2.json()["active"])
                self.assertEqual(data_points['completed'], response2.json()["completed"])
                self.assertEqual(data_points['description'], response2.json()['description'])
                self.assertEqual(data_points['title'], response2.json()['title'])

            else:
                self.fail("ID not matching!")

    '''
    This test checks if the API correctly raises an error when the path does not exist 
    '''
    def test_get_all_projects_invalid_path(self):
        response1 = requests.get("http://localhost:4567/project")
        self.assertEqual(response1.status_code, NOT_FOUND)

    '''
    This test checks if the API correctly returns a project at a specified id 
    '''
    def test_get_project_by_id(self):
        new_project = {
            "title": "project 1",
            "description": "project description",
            "active": True,
            "completed": True
        }

        response = requests.post("http://localhost:4567/projects", data=json.dumps(new_project))

        response_output = requests.get("http://localhost:4567/projects/" + response.json()["id"])

        self.assertEqual(response_output.status_code, OK)
        self.assertEqual(str(response_output.json()["projects"][0]['completed']).upper(), str(new_project['completed']).upper())
        self.assertEqual(str(response_output.json()["projects"][0]['active']).upper(), str(new_project['active']).upper())
        self.assertEqual(response_output.json()["projects"][0]['description'], new_project['description'])
        self.assertEqual(response_output.json()["projects"][0]['title'], new_project['title'])

    '''
    This test checks if the API correctly raises an error when there is no project associated to the id 
    '''
    def test_get_project_by_nonexistant_id(self):
        response = requests.get("http://localhost:4567/projects/20")
        self.assertEqual(response.status_code, NOT_FOUND)
        self.assertEqual(response.json()["errorMessages"][0], "Could not find an instance with projects/20")

    '''
    This test checks if the API correctly raises an error when the id is a negative integer
    '''
    def test_get_project_by_negative_id(self):
        response = requests.get("http://localhost:4567/projects/-20")
        self.assertEqual(response.status_code, NOT_FOUND)
        self.assertEqual(response.json()["errorMessages"][0], "Could not find an instance with projects/-20")

    '''
    This test checks if the API correctly amends all fields at once at a specified id using a POST request 
    '''
    def test_post_by_id_full_body(self):
        project1 = {
            "title": "project 1",
            "description": "project description",
            "active": True,
            "completed": True
        }
        response1 = requests.post("http://localhost:4567/projects", data=json.dumps(project1))

        project2 = {
            "title": "project 1",
            "description": "project description",
            "active": False,
            "completed": True
        }
        response2 = requests.post("http://localhost:4567/projects/" + str(response1.json()["id"]), data=json.dumps(project2))

        self.assertEqual(response2.status_code, OK)
        self.assertEqual(str(response2.json()['completed']).upper(), str(project2['completed']).upper())
        self.assertEqual(str(response2.json()['active']).upper(), str(project2['active']).upper())
        self.assertEqual(response2.json()['description'], project2['description'])
        self.assertEqual(response2.json()['title'], project2['title'])

    '''
    This test checks if the API correctly amends the description at a specified id using a POST request 
    '''
    def test_post_by_id_only_description(self):
        project1 = {
            "title": "project 1",
            "description": "project description",
            "active": True,
            "completed": True
        }
        response1 = requests.post("http://localhost:4567/projects", data=json.dumps(project1))

        project2 = {
            "description": "new description",
        }
        response2 = requests.post("http://localhost:4567/projects/" + str(response1.json()["id"]),
                                  data=json.dumps(project2))

        self.assertEqual(response2.status_code, OK)
        self.assertEqual(str(response2.json()['completed']).upper(), str(project1['completed']).upper())
        self.assertEqual(str(response2.json()['active']).upper(), str(project1['active']).upper())
        self.assertEqual(response2.json()['description'], project2['description'])
        self.assertEqual(response2.json()['title'], project1['title'])

    '''
    This test checks if the API correctly amends the title at a specified id using a POST request 
    '''
    def test_post_by_id_only_title(self):
        project1 = {
            "title": "project 1",
            "description": "project description",
            "active": True,
            "completed": True
        }
        response1 = requests.post("http://localhost:4567/projects", data=json.dumps(project1))

        project2 = {
            "title": "new title",
        }
        response2 = requests.post("http://localhost:4567/projects/" + str(response1.json()["id"]),
                                  data=json.dumps(project2))

        self.assertEqual(response2.status_code, OK)
        self.assertEqual(str(response2.json()['completed']).upper(), str(project1['completed']).upper())
        self.assertEqual(str(response2.json()['active']).upper(), str(project1['active']).upper())
        self.assertEqual(response2.json()['description'], project1['description'])
        self.assertEqual(response2.json()['title'], project2['title'])

    '''
    This test checks if the API correctly amends the active field at a specified id using a POST request 
    '''
    def test_post_by_id_only_active(self):
        project1 = {
            "title": "project 1",
            "description": "project description",
            "active": True,
            "completed": True
        }
        response1 = requests.post("http://localhost:4567/projects", data=json.dumps(project1))

        project2 = {
            "active": False,
        }
        response2 = requests.post("http://localhost:4567/projects/" + str(response1.json()["id"]),
                                  data=json.dumps(project2))

        self.assertEqual(response2.status_code, OK)
        self.assertEqual(str(response2.json()['completed']).upper(), str(project1['completed']).upper())
        self.assertEqual(str(response2.json()['active']).upper(), str(project2['active']).upper())
        self.assertEqual(response2.json()['description'], project1['description'])
        self.assertEqual(response2.json()['title'], project1['title'])

    '''
    This test checks if the API correctly amends the completed field at a specified id using a POST request 
    '''
    def test_post_by_id_only_completed(self):
        project1 = {
            "title": "project 1",
            "description": "project description",
            "active": True,
            "completed": True
        }
        response1 = requests.post("http://localhost:4567/projects", data=json.dumps(project1))

        project2 = {
            "completed": False,
        }
        response2 = requests.post("http://localhost:4567/projects/" + str(response1.json()["id"]),
                                  data=json.dumps(project2))

        self.assertEqual(response2.status_code, OK)
        self.assertEqual(str(response2.json()['completed']).upper(), str(project2['completed']).upper())
        self.assertEqual(str(response2.json()['active']).upper(), str(project1['active']).upper())
        self.assertEqual(response2.json()['description'], project1['description'])
        self.assertEqual(response2.json()['title'], project1['title'])

    '''
    This test checks if the API correctly raises an error when the active field is a string in a POST request to an id
    '''
    def test_post_by_id_string_active(self):
        project1 = {
            "title": "project 1",
            "description": "project description",
            "active": True,
            "completed": True
        }
        response1 = requests.post("http://localhost:4567/projects", data=json.dumps(project1))

        project2 = {
            "active": "hello",
        }
        response2 = requests.post("http://localhost:4567/projects/" + str(response1.json()["id"]),
                                  data=json.dumps(project2))

        self.assertEqual(response2.status_code, BAD_REQUEST)
        self.assertEqual(response2.json()["errorMessages"][0], "Failed Validation: active should be BOOLEAN")

    '''
    This test checks if the API correctly raises an error when the completed field is a string in a POST request to an id
    '''
    def test_post_by_id_string_completed(self):
        project1 = {
            "title": "project 1",
            "description": "project description",
            "active": True,
            "completed": True
        }
        response1 = requests.post("http://localhost:4567/projects", data=json.dumps(project1))

        project2 = {
            "completed": "hello",
        }
        response2 = requests.post("http://localhost:4567/projects/" + str(response1.json()["id"]),
                                  data=json.dumps(project2))

        self.assertEqual(response2.status_code, BAD_REQUEST)
        self.assertEqual(response2.json()["errorMessages"][0], "Failed Validation: completed should be BOOLEAN")

    '''
    This test checks that the title will remain unchanged if it is set as null in a POST request to an id
    '''
    def test_post_by_id_null_title(self):
        project1 = {
            "title": "project 1",
            "description": "project description",
            "active": True,
            "completed": True
        }
        response1 = requests.post("http://localhost:4567/projects", data=json.dumps(project1))

        project2 = {
            "title": None,
        }
        response2 = requests.post("http://localhost:4567/projects/" + str(response1.json()["id"]),
                                  data=json.dumps(project2))

        self.assertEqual(response2.status_code, OK)
        self.assertEqual(str(response2.json()['completed']).upper(), str(project1['completed']).upper())
        self.assertEqual(str(response2.json()['active']).upper(), str(project1['active']).upper())
        self.assertEqual(response2.json()['description'], project1['description'])
        self.assertEqual(response2.json()['title'], project1['title'])

    '''
    This test checks that the API raises an error if we try to amend the id in a POST request to an id
    '''
    def test_post_by_id_change_id(self):
        project1 = {
            "title": "project 1",
            "description": "project description",
            "active": True,
            "completed": True
        }
        response1 = requests.post("http://localhost:4567/projects", data=json.dumps(project1))

        project2 = {
            "id": 20,
        }
        response2 = requests.post("http://localhost:4567/projects/" + str(response1.json()["id"]),
                                  data=json.dumps(project2))

        self.assertEqual(response2.status_code, BAD_REQUEST)
        self.assertEqual(response2.json()["errorMessages"][0], "Can not amend id on Entity project from " + str(response1.json()["id"]) + " to 20.0")

    '''
    This test checks that the API will raise an error in a POST request to an id with no project
    '''
    def test_post_by_id_invalid_id(self):
        project = {
            "title": "project",
            "description": "project description",
            "active": True,
            "completed": True
        }
        response = requests.post("http://localhost:4567/projects/20", data=json.dumps(project))

        self.assertEqual(response.status_code, NOT_FOUND)
        self.assertEqual(response.json()["errorMessages"][0], "No such project entity instance with GUID or ID 20 found")

    '''
    This test checks that the API will raise an error if the active and completed fields are Strings in a PUT request to an id
    '''
    def test_put_by_id_string_active_and_completed(self):
        project1 = {
            "title": "project 1",
            "description": "project description",
            "active": True,
            "completed": True
        }
        response1 = requests.post("http://localhost:4567/projects", data=json.dumps(project1))

        project2 = {
            "title": "project 1",
            "description": "project description",
            "active": "False",
            "completed": "True"
        }
        response2 = requests.put("http://localhost:4567/projects/" + str(response1.json()["id"]), data=json.dumps(project2))

        self.assertEqual(response2.status_code, BAD_REQUEST)
        self.assertEqual(response2.json()["errorMessages"][0], "Failed Validation: active should be BOOLEAN, completed should be BOOLEAN")

    '''
    This test checks that the API correctly amends all fields ar once in a PUT request to an id
    '''
    def test_put_by_id_full_body(self):
        project1 = {
            "title": "project 1",
            "description": "project description",
            "active": True,
            "completed": True
        }
        response1 = requests.post("http://localhost:4567/projects", data=json.dumps(project1))

        project2 = {
            "title": "project 1",
            "description": "project description",
            "active": False,
            "completed": True
        }
        response2 = requests.put("http://localhost:4567/projects/" + str(response1.json()["id"]), data=json.dumps(project2))

        self.assertEqual(response2.status_code, OK)
        self.assertEqual(str(response2.json()['completed']).upper(), str(project2['completed']).upper())
        self.assertEqual(str(response2.json()['active']).upper(), str(project2['active']).upper())
        self.assertEqual(response2.json()['description'], project2['description'])
        self.assertEqual(response2.json()['title'], project2['title'])

    '''
    This test checks that the API correctly amends only the description in a PUT request to an id
    '''
    def test_put_by_id_only_description_expected(self):
        project1 = {
            "title": "project 1",
            "description": "project description",
            "active": True,
            "completed": True
        }
        response1 = requests.post("http://localhost:4567/projects", data=json.dumps(project1))

        project2 = {
            "description": "new description",
        }
        response2 = requests.put("http://localhost:4567/projects/" + str(response1.json()["id"]),
                                  data=json.dumps(project2))

        self.assertEqual(response2.status_code, OK)
        self.assertEqual(str(response2.json()['completed']).upper(), str(project1['completed']).upper())
        self.assertEqual(str(response2.json()['active']).upper(), str(project1['active']).upper())
        self.assertEqual(response2.json()['description'], project2['description'])
        self.assertEqual(response2.json()['title'], project1['title'])

    '''
    This test the actual behaviour of the API when trying to amend only the description field in a PUT request to an id
    The API resets all other fields to their default values instead of leaving them unchanged 
    '''
    def test_put_by_id_only_description_actual(self):
        project1 = {
            "title": "project 1",
            "description": "project description",
            "active": True,
            "completed": True
        }
        response1 = requests.post("http://localhost:4567/projects", data=json.dumps(project1))

        project2 = {
            "description": "new description",
        }
        response2 = requests.put("http://localhost:4567/projects/" + str(response1.json()["id"]),
                                  data=json.dumps(project2))

        self.assertEqual(response2.status_code, OK)
        self.assertEqual(str(response2.json()['completed']).upper(), "FALSE")
        self.assertEqual(str(response2.json()['active']).upper(), "FALSE")
        self.assertEqual(response2.json()['description'], project2['description'])
        self.assertEqual(response2.json()['title'], "")

    '''
    This test checks that the API correctly amends only the title in a PUT request to an id
    '''
    def test_put_by_id_only_title_expected(self):
        project1 = {
            "title": "project 1",
            "description": "project description",
            "active": True,
            "completed": True
        }
        response1 = requests.post("http://localhost:4567/projects", data=json.dumps(project1))

        project2 = {
            "title": "new title",
        }
        response2 = requests.put("http://localhost:4567/projects/" + str(response1.json()["id"]),
                                  data=json.dumps(project2))

        self.assertEqual(response2.status_code, OK)
        self.assertEqual(str(response2.json()['completed']).upper(), str(project1['completed']).upper())
        self.assertEqual(str(response2.json()['active']).upper(), str(project1['active']).upper())
        self.assertEqual(response2.json()['description'], project1['description'])
        self.assertEqual(response2.json()['title'], project2['title'])


    '''
    This test the actual behaviour of the API when trying to amend only the title field in a PUT request to an id
    The API resets all other fields to their default values instead of leaving them unchanged 
    '''
    def test_put_by_id_only_title_actual(self):
        project1 = {
            "title": "project 1",
            "description": "project description",
            "active": True,
            "completed": True
        }
        response1 = requests.post("http://localhost:4567/projects", data=json.dumps(project1))

        project2 = {
            "title": "new title",
        }
        response2 = requests.put("http://localhost:4567/projects/" + str(response1.json()["id"]),
                                  data=json.dumps(project2))

        self.assertEqual(response2.status_code, OK)
        self.assertEqual(str(response2.json()['completed']).upper(), "FALSE")
        self.assertEqual(str(response2.json()['active']).upper(), "FALSE")
        self.assertEqual(response2.json()['description'], "")
        self.assertEqual(response2.json()['title'], project2['title'])

    '''
    This test checks that the API correctly amends only the active field in a PUT request to an id
    '''
    def test_put_by_id_only_active_expected(self):
        project1 = {
            "title": "project 1",
            "description": "project description",
            "active": True,
            "completed": True
        }
        response1 = requests.post("http://localhost:4567/projects", data=json.dumps(project1))

        project2 = {
            "active": False,
        }
        response2 = requests.put("http://localhost:4567/projects/" + str(response1.json()["id"]),
                                  data=json.dumps(project2))

        self.assertEqual(response2.status_code, OK)
        self.assertEqual(str(response2.json()['completed']).upper(), str(project1['completed']).upper())
        self.assertEqual(str(response2.json()['active']).upper(), str(project2['active']).upper())
        self.assertEqual(response2.json()['description'], project1['description'])
        self.assertEqual(response2.json()['title'], project1['title'])

    '''
    This test the actual behaviour of the API when trying to amend only the active field in a PUT request to an id
    The API resets all other fields to their default values instead of leaving them unchanged 
    '''
    def test_put_by_id_only_active_actual(self):
        project1 = {
            "title": "project 1",
            "description": "project description",
            "active": True,
            "completed": True
        }
        response1 = requests.post("http://localhost:4567/projects", data=json.dumps(project1))

        project2 = {
            "active": False,
        }
        response2 = requests.put("http://localhost:4567/projects/" + str(response1.json()["id"]),
                                  data=json.dumps(project2))

        self.assertEqual(response2.status_code, OK)
        self.assertEqual(str(response2.json()['completed']).upper(), "FALSE")
        self.assertEqual(str(response2.json()['active']).upper(), str(project2['active']).upper())
        self.assertEqual(response2.json()['description'], "")
        self.assertEqual(response2.json()['title'], "")

    '''
    This test checks that the API correctly amends only the completed field in a PUT request to an id
    '''
    def test_put_by_id_only_completed_expected(self):
        project1 = {
            "title": "project 1",
            "description": "project description",
            "active": True,
            "completed": True
        }
        response1 = requests.post("http://localhost:4567/projects", data=json.dumps(project1))

        project2 = {
            "completed": False,
        }
        response2 = requests.put("http://localhost:4567/projects/" + str(response1.json()["id"]),
                                  data=json.dumps(project2))

        self.assertEqual(response2.status_code, OK)
        self.assertEqual(str(response2.json()['completed']).upper(), str(project2['completed']).upper())
        self.assertEqual(str(response2.json()['active']).upper(), str(project1['active']).upper())
        self.assertEqual(response2.json()['description'], project1['description'])
        self.assertEqual(response2.json()['title'], project1['title'])

    '''
    This test the actual behaviour of the API when trying to amend only the completed field in a PUT request to an id
    The API resets all other fields to their default values instead of leaving them unchanged 
    '''
    def test_put_by_id_only_completed_actual(self):
        project1 = {
            "title": "project 1",
            "description": "project description",
            "active": True,
            "completed": True
        }
        response1 = requests.post("http://localhost:4567/projects", data=json.dumps(project1))

        project2 = {
            "completed": False,
        }
        response2 = requests.put("http://localhost:4567/projects/" + str(response1.json()["id"]),
                                  data=json.dumps(project2))

        self.assertEqual(response2.status_code, OK)
        self.assertEqual(str(response2.json()['completed']).upper(), str(project2['completed']).upper())
        self.assertEqual(str(response2.json()['active']).upper(), "FALSE")
        self.assertEqual(response2.json()['description'], "")
        self.assertEqual(response2.json()['title'], "")

    '''
    This test checks that the API correctly deletes the project at a valid id by deleting it
    and then sending a GET request to the same id to make sure it no longer exists 
    '''
    def test_delete_valid_id(self):
        project1 = {
            "title": "project 1",
            "description": "project description",
            "active": True,
            "completed": True
        }
        response1 = requests.post("http://localhost:4567/projects", data=json.dumps(project1))

        response2 = requests.delete("http://localhost:4567/projects/" + str(response1.json()["id"]))
        self.assertEqual(response2.status_code, OK)

        response3 = requests.get("http://localhost:4567/projects/" + str(response1.json()["id"]))
        self.assertEqual(response3.status_code, NOT_FOUND)

    '''
    This test checks if the API correctly raises an error for a DELETE request at an id with no project
    '''
    def test_delete_invalid_id(self):
        response = requests.delete("http://localhost:4567/projects/90")
        self.assertEqual(response.status_code, NOT_FOUND)
        self.assertEqual(response.json()["errorMessages"][0], "Could not find any instances with projects/90")

    '''
    This test checks if the API correctly raises an error for a DELETE request at an id which is text
    '''
    def test_delete_string_id(self):
        response = requests.delete("http://localhost:4567/projects/eight")
        self.assertEqual(response.status_code, NOT_FOUND)
        self.assertEqual(response.json()["errorMessages"][0], "Could not find any instances with projects/eight")

    '''
    This test checks if the API correctly raises an error for a DELETE request at an id which is a negative integer
    '''
    def test_delete_negative_id(self):
        response = requests.delete("http://localhost:4567/projects/-8")
        self.assertEqual(response.status_code, NOT_FOUND)
        self.assertEqual(response.json()["errorMessages"][0], "Could not find any instances with projects/-8")

if __name__ == '__main__':
    unittest.main()
