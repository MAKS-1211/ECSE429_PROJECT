import json
from behave import *
import requests


@given(u'I am currently working with a rest API that has no todo entries')
def step_impl(context):
    context.response = requests.get("http://localhost:4567/todos")
    for data_points in context.response.json()['todos']:
        deleted_id = str(data_points['id'])
        requests.delete("http://localhost:4567/todos/" + deleted_id)


@when(u'I send a POST request "/todos" of the todo item with a doneStatus True and Title as \'ECSE 429\'')
def step_impl(context):
    new_todo1 = {
        "doneStatus": True,
        "title": "ECSE 429"
    }
    context.response_output1 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))


@then(u'I get back my todo item with a new todo item ID')
def step_impl(context):
    assert context.response_output1.status_code == requests.codes.created


@then(u'I get back my todo item with the same Title')
def step_impl(context):
    assert str(context.response_output1.json()['title']) == "ECSE 429"


@then(u'I get back my todo item with the doneStatus as True')
def step_impl(context):
    assert str(context.response_output1.json()['doneStatus']).upper() == "True".upper()


@when(u'I send a POST request "/todos" of the todo item with a doneStatus False and Title as \'ECSE 427\'')
def step_impl(context):
    new_todo1 = {
        "doneStatus": False,
        "title": "ECSE 427"
    }
    context.response_output2 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))


@then(u'I get back my todo item with the doneStatus as False')
def step_impl(context):
    assert str(context.response_output2.json()['doneStatus']).upper() == "False".upper()


@when(u'I send a POST request "/todos" of the todo item with a doneStatus True and no title')
def step_impl(context):
    new_todo1 = {
        "doneStatus": True,
    }
    context.response_output1 = requests.post("http://localhost:4567/todos", data=json.dumps(new_todo1))


@then(u'I get back an error message: \'title : field is mandatory\'')
def step_impl(context):
    assert context.response_output1.json()["errorMessages"][0] == "title : field is mandatory"


@then(u'I get back my todo item with the same Title as above')
def step_impl(context):
    assert str(context.response_output2.json()['title']) == "ECSE 427"


@then(u'I get back my todo item with a new todo item ID as above')
def step_impl(context):
    assert context.response_output2.status_code == requests.codes.created
