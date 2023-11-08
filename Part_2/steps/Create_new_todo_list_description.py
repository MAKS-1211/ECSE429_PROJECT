import json
from behave import *
import requests


@when(u'I send a POST request "/todos" of the todo item with a description \'Project Part B\', doneStatus True and '
      u'Title as \'ECSE 429\'')
def step_impl(context):
    new_todo1 = {
        "description": "Project Part B",
        "doneStatus": True,
        "title": "ECSE 429"
    }
    context.response_output1 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))


@then(u'I get back my todo item with the same description')
def step_impl(context):
    assert str(context.response_output1.json()['description']) == "Project Part B"


@when(u'I send a POST request "/todos" of the todo item with a description \'Assignment 2\' and Title as \'ECSE 427\'')
def step_impl(context):
    new_todo1 = {
        "description": "Assignment 2",
        "title": "ECSE 427"
    }
    context.response_output2 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))


@then(u'I get back my todo item with the same description as above')
def step_impl(context):
    assert str(context.response_output2.json()['description']) == "Assignment 2"


@when(u'I send a POST request "/todos" of the todo item with a description \'McGill ECSE\'')
def step_impl(context):
    new_todo1 = {
        "description": "McGill ECSE",
    }
    context.response_output1 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))
