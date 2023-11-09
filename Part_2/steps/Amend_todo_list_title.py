import json
from behave import *
import requests


@when(u'I send a POST request "/todo/id" with the ID of the todo item and the new title- ECSE 429')
def step_impl(context):
    new_todo3 = {
        "title": "ECSE 429"
    }
    context.response_output1 = requests.post("http://localhost:4567/todos/"
                                             + str(context.response1.json()['id']), data=json.dumps(new_todo3))


@when(u'I send a POST request "/todo/id" with the ID of the todo item and the new title- ECSE 427')
def step_impl(context):
    new_todo3 = {
        "title": "ECSE 427"
    }
    context.response_output1 = requests.post("http://localhost:4567/todos/"
                                             + str(context.response1.json()['id']), data=json.dumps(new_todo3))


@then(u'I get the todo item title as ECSE 429 for that todo item itself.')
def step_impl(context):
    assert str(context.response_output1.json()['title']) == context.response1.json()['title']


@then(u'I get the todo item title as ECSE 427 for that todo item itself.')
def step_impl(context):
    assert str(context.response_output1.json()['title']) == context.response2.json()['title']


@then(u'I get the todo item description Project Part B, as it was for that todo item')
def step_impl(context):
    assert str(context.response_output1.json()['description']) == context.response1.json()['description']


@then(u'I get the todo item description Assignment 2, as it was for that todo item')
def step_impl(context):
    assert str(context.response_output1.json()['description']) == context.response1.json()['description']


@then(u'I get back the todo item status True as it was for that todo item')
def step_impl(context):
    assert str(context.response_output1.json()['doneStatus']) == context.response1.json()['doneStatus']


@then(u'I get back the todo item status False as it was for that todo item')
def step_impl(context):
    assert str(context.response_output1.json()['doneStatus']) == context.response1.json()['doneStatus']


@when(
    u'I send a POST request "/todo/id" with the ID of the todo item, the new title- ECSE 429 and the new description- '
    u'Project Part B')
def step_impl(context):
    new_todo3 = {
        "title": "ECSE 429",
        "description": "Project Part B"
    }
    context.response_output2 = requests.post("http://localhost:4567/todos/"
                                             + str(context.response2.json()['id']), data=json.dumps(new_todo3))


@when(
    u'I send a POST request "/todo/id" with the ID of the todo item, the new title- ECSE 427 and the new description- '
    u'Assignment 2')
def step_impl(context):
    new_todo3 = {
        "title": "ECSE 427",
        "description": "Assignment 2"
    }
    context.response_output2 = requests.post("http://localhost:4567/todos/"
                                             + str(context.response2.json()['id']), data=json.dumps(new_todo3))


@then(u'I get the todo item title as ECSE 429 for that todo item.')
def step_impl(context):
    assert str(context.response_output2.json()['title']) == "ECSE 429"


@then(u'I get the todo item title as ECSE 427 for that todo item.')
def step_impl(context):
    assert str(context.response_output2.json()['title']) == "ECSE 427"


@then(u'I get the todo item description as Project Part B for that todo item.')
def step_impl(context):
    assert str(context.response_output2.json()['description']) == "Project Part B"


@then(u'I get the todo item description as Assignment 2 for that todo item.')
def step_impl(context):
    assert str(context.response_output2.json()['description']) == "Assignment 2"




@then(u'I get back the todo item status True as it was for that todo item initially')
def step_impl(context):
    assert str(context.response_output2.json()['doneStatus']).upper() == str(
        context.response2.json()['doneStatus']).upper()


@then(u'I get back the todo item status False as it was for that todo item initially')
def step_impl(context):
    assert str(context.response_output2.json()['doneStatus']).upper() == str(
        context.response2.json()['doneStatus']).upper()


@when(
    u'I send a POST request "/todo/id" with the ID of the todo item and the new title as blank')
def step_impl(context):
    new_todo3 = {
        "title": "",
    }
    context.response_output3 = requests.post("http://localhost:4567/todos/"
                                             + str(context.response1.json()['id']), data=json.dumps(new_todo3))


@then(u'I get back an error message - Failed Validation: title : can not be empty')
def step_impl(context):
    assert context.response_output3.json()["errorMessages"][0] == "Failed Validation: title : can not be empty"
