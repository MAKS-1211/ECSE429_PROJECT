import json
import os
import subprocess
import time
from behave import *
import requests


@given(u'I am currently navigated to the rest API todo list manager')
def step_impl(context):
    context.current_directory = os.getcwd()
    context.api_path = context.current_directory + "/runTodoManagerRestAPI-1.5.22.jar"
    context.jar_process = subprocess.Popen(['java', '-jar', context.api_path])
    time.sleep(5)


@given(u'I know the ID of the pre-existing todo items inside the API')
def step_impl(context):
    context.response = requests.get("http://localhost:4567/todos")
    for data_points in context.response.json()['todos']:
        deleted_id = str(data_points['id'])
        requests.delete("http://localhost:4567/todos/" + deleted_id)

    new_todo1 = {
        "doneStatus": False,
        "description": "Project Part B",
        "title": "ECSE 429"
    }

    new_todo2 = {
        "doneStatus": True,
        "description": "Assignment 2",
        "title": "ECSE 427"
    }

    context.response1 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))
    context.response2 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo2))


@when(u'I send a GET request "/todo/id" with the ID 3 of the todo item I want')
def step_impl(context):
    context.response_output1 = requests.get("http://localhost:4567/todos/" + str(context.response1.json()['id']))


@then(u'I get the todo item title as ECSE 429 for that todo item')
def step_impl(context):
    assert str(context.response_output1.json()['todos'][0]['title']) == "ECSE 429"


@then(u'I get the todo item description as Project Part B for that todo item')
def step_impl(context):
    assert str(context.response_output1.json()['todos'][0]['description']) == "Project Part B"


@then(u'I get back the todo item status as False for that todo item')
def step_impl(context):
    assert str(context.response_output1.json()['todos'][0]['doneStatus']).upper() == "False".upper()


@when(u'I send a GET request "/todo/id" with the ID 4 of the todo item I want')
def step_impl(context):
    context.response_output2 = requests.get("http://localhost:4567/todos/" + str(context.response2.json()['id']))


@then(u'I get the todo item title as ECSE 427 for that todo item')
def step_impl(context):
    assert str(context.response_output2.json()['todos'][0]['title']) == "ECSE 427"


@then(u'I get the todo item description as Assignment 2 for that todo item')
def step_impl(context):
    assert str(context.response_output2.json()['todos'][0]['description']) == "Assignment 2"


@then(u'I get back the todo item status as True for that todo item')
def step_impl(context):
    assert str(context.response_output2.json()['todos'][0]['doneStatus']).upper() == "True".upper()


@when(u'I send a GET request "/todo" for all the items in the todo list')
def step_impl(context):
    context.response_output5 = requests.get("http://localhost:4567/todos")


@then(u'I get back all the todo items')
def step_impl(context):
    assert context.response_output5.status_code == 200


@then(u'I check for the todo item ID 3 I wanted')
def step_impl(context):
    for data_points in context.response_output5.json()['todos']:
        if data_points['id'] == context.response1.json()['id']:
            assert True



@when(u'I send a GET request "/todo/id" with the ID three of the todo item I want')
def step_impl(context):
    context.response_output4 = requests.get("http://localhost:4567/todos/three")


@then(u'I get back an error message Could not find an instance with todos/three')
def step_impl(context):
    assert context.response_output4.json()["errorMessages"][0] == "Could not find an instance with todos/three"


@then(u'I get back an error message Could not find an instance with todos/four')
def step_impl(context):
    assert context.response_output4.json()["errorMessages"][0] == "Could not find an instance with todos/four"


@then(u'I get the todo item title as ECSE 429 for that todo item from the todo list')
def step_impl(context):
    for data_points in context.response_output5.json()['todos']:
        if data_points['id'] == context.response1.json()['id']:
            assert data_points['title'] == "ECSE 429"


@then(u'I get the todo item description as Project Part B for that todo item from the todo list')
def step_impl(context):
    for data_points in context.response_output5.json()['todos']:
        if data_points['id'] == context.response1.json()['id']:
            assert data_points['description'] == "Project Part B"


@then(u'I get back the todo item status as False for that todo item from the todo list')
def step_impl(context):
    for data_points in context.response_output5.json()['todos']:
        if data_points['id'] == context.response1.json()['id']:
            assert str(data_points['doneStatus']).upper() == "False".upper()


@then(u'I check for the todo item ID 4 I wanted')
def step_impl(context):
    for data_points in context.response_output5.json()['todos']:
        if data_points['id'] == context.response2.json()['id']:
            assert True


@then(u'I get the todo item title as ECSE 427 for that todo item from the todo list')
def step_impl(context):
    for data_points in context.response_output5.json()['todos']:
        if data_points['id'] == context.response2.json()['id']:
            assert data_points['title'] == "ECSE 427"


@then(u'I get the todo item description as Assignment 2 for that todo item from the todo list')
def step_impl(context):
    for data_points in context.response_output5.json()['todos']:
        if data_points['id'] == context.response2.json()['id']:
            assert data_points['description'] == "Assignment 2"


@then(u'I get back the todo item status as True for that todo item from the todo list')
def step_impl(context):
    for data_points in context.response_output5.json()['todos']:
        if data_points['id'] == context.response2.json()['id']:
            assert str(data_points['doneStatus']).upper() == "True".upper()

@then(u'I shutdown the rest API todo list manager')
def step_impl(context):
    context.jar_process.terminate()
    context.jar_process.wait()


@when(u'I send a GET request "/todo/id" with the ID four of the todo item I want')
def step_impl(context):
    context.response_output4 = requests.get("http://localhost:4567/todos/four")
