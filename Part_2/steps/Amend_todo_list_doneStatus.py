import json
from behave import *
import requests


@when(u'I send a POST request "/todo/id" with the ID of the todo item and the new done status- True')
def step_impl(context):
    new_todo3 = {
        "doneStatus": True
    }
    context.response_output1 = requests.post("http://localhost:4567/todos/"
                                             + str(context.response1.json()['id']), data=json.dumps(new_todo3))


@then(u'I get the todo item title as it was for that todo item')
def step_impl(context):
    assert str(context.response_output1.json()['title']) == context.response1.json()['title']


@then(u'I get back the todo item status as the updated version - True')
def step_impl(context):
    assert str(context.response_output1.json()['doneStatus']).upper() == "True".upper()


@when(u'I send a POST request "/todo/id" with the ID of the todo item, the new done status- False and the new '
      u'description- Final Exam')
def step_impl(context):
    new_todo3 = {
        "doneStatus": False,
        "description": "Final Exam"
    }
    context.response_output2 = requests.post("http://localhost:4567/todos/"
                                             + str(context.response2.json()['id']), data=json.dumps(new_todo3))


@then(u'I get the todo item title as it was for that todo item initially')
def step_impl(context):
    assert str(context.response_output2.json()['title']) == context.response2.json()['title']


@then(u'I get the todo item description as Final Exam for that todo item')
def step_impl(context):
    assert str(context.response_output2.json()['description']) == "Final Exam"


@then(u'I get back the todo item status as the updated version - False')
def step_impl(context):
    assert str(context.response_output2.json()['doneStatus']).upper() == "False".upper()


@when(u'I send a POST request "/todo/id" with the ID of the todo item and the new done status - InProgress')
def step_impl(context):
    new_todo3 = {
        "doneStatus": "InProgress"
    }
    context.response_output3 = requests.post("http://localhost:4567/todos/"
                                             + str(context.response2.json()['id']), data=json.dumps(new_todo3))


@then(u'I get back an error message - Failed Validation: doneStatus should be BOOLEAN')
def step_impl(context):
    assert context.response_output3.json()["errorMessages"][0] == "Failed Validation: doneStatus should be BOOLEAN"
