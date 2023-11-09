import json
from behave import *
import requests


@when(u'I send a POST request "/todos" of the todo item with a description Project Part B, doneStatus True and '
      u'Title as ECSE 429')
def step_impl(context):
    new_todo1 = {
        "description": "Project Part B",
        "doneStatus": True,
        "title": "ECSE 429"
    }
    context.response_output1 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))


@when(u'I send a POST request "/todos" of the todo item with a description Assignment 2, doneStatus False and '
      u'Title as ECSE 427')
def step_impl(context):
    new_todo1 = {
        "description": "Assignment 2",
        "doneStatus": False,
        "title": "ECSE 427"
    }
    context.response_output1 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))


@then(u'I get back my todo item with the same description as Project Part B')
def step_impl(context):
    assert str(context.response_output1.json()['description']) == "Project Part B"


@then(u'I get back my todo item with the same description as Assignment 2')
def step_impl(context):
    assert str(context.response_output1.json()['description']) == "Assignment 2"


@then(u'I get back my todo item with the doneStatus as True.')
def step_impl(context):
    assert str(context.response_output1.json()['doneStatus']).upper() == "True".upper()


@then(u'I get back my todo item with the doneStatus as False.')
def step_impl(context):
    assert str(context.response_output1.json()['doneStatus']).upper() == "False".upper()


@when(u'I send a POST request "/todos" of the todo item with a description Assignment 2 and Title as ECSE 427')
def step_impl(context):
    new_todo1 = {
        "description": "Assignment 2",
        "title": "ECSE 427"
    }
    context.response_output2 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))


@when(u'I send a POST request "/todos" of the todo item with a description Project Part B and Title as ECSE 429')
def step_impl(context):
    new_todo1 = {
        "description": "Project Part B",
        "title": "ECSE 429"
    }
    context.response_output2 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))


@then(u'I get back my todo item with the same description Assignment 2')
def step_impl(context):
    assert str(context.response_output2.json()['description']) == "Assignment 2"


@then(u'I get back my todo item with the same description Project Part B')
def step_impl(context):
    assert str(context.response_output2.json()['description']) == "Project Part B"


@when(u'I send a POST request "/todos" of the todo item with a description Project Part B')
def step_impl(context):
    new_todo1 = {
        "description": "Project Part B",
    }
    context.response_output3 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))


@when(u'I send a POST request "/todos" of the todo item with a description Assignment 2')
def step_impl(context):
    new_todo1 = {
        "description": "Assignment 2",
    }
    context.response_output3 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))


@then(u'I get back my todo item with the same Title ECSE 429')
def step_impl(context):
    assert str(context.response_output2.json()['title']) == "ECSE 429"


@then(u'I get back my todo item with the same Title ECSE 427')
def step_impl(context):
    assert str(context.response_output2.json()['title']) == "ECSE 427"
