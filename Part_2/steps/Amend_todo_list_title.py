import json
from behave import *
import requests


@when(u'I send a POST request "/todo/id" with the ID of the todo item and the new title- ECSE 206')
def step_impl(context):
    new_todo3 = {
        "title": "ECSE 206"
    }
    context.response_output1 = requests.post("http://localhost:4567/todos/"
                                             + str(context.response1.json()['id']), data=json.dumps(new_todo3))


@then(u'I get the todo item title as ECSE 206 for that todo item')
def step_impl(context):
    print(context.response_output1.json())
    assert str(context.response_output1.json()['title']) == "ECSE 206"


@then(u'I get the todo item description as it was for that todo item')
def step_impl(context):
    assert str(context.response_output1.json()['description']) == context.response1.json()['description']


@then(u'I get back the todo item status as it was for that todo item')
def step_impl(context):
    assert str(context.response_output1.json()['doneStatus']) == context.response1.json()['doneStatus']


@when(
    u'I send a POST request "/todo/id" with the ID of the todo item, the new title- ECSE 331 and the new description- '
    u'Mid Term 2')
def step_impl(context):
    new_todo3 = {
        "title": "ECSE 331",
        "description": "Mid Term 2"
    }
    context.response_output2 = requests.post("http://localhost:4567/todos/"
                                             + str(context.response2.json()['id']), data=json.dumps(new_todo3))


@then(u'I get the todo item title as ECSE 331 for that todo item')
def step_impl(context):
    assert str(context.response_output2.json()['title']) == "ECSE 331"


@then(u'I get the todo item description as Mid Term 2 for that todo item')
def step_impl(context):
    assert str(context.response_output2.json()['description']) == "Mid Term 2"


@then(u'I get back the todo item status as it was for that todo item initially')
def step_impl(context):
    assert str(context.response_output2.json()['doneStatus']).upper() == str(context.response2.json()['doneStatus']).upper()


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
