from behave import *
import json
import requests


@when("The user marks the project as done by deleting it from the database")
def step_impl(context):
    context.response = requests.delete("http://localhost:4567/projects/" + context.id)


@step("The project will no longer be in the database")
def step_impl(context):
    get_response = requests.get("http://localhost:4567/projects/" + context.id)
    assert get_response.status_code == 404


@when("The user marks the project as done by updating the active and completed status using a POST call")
def step_impl(context):
    context.project = {
        "completed": True,
        "active": False
    }

    context.response = requests.post("http://localhost:4567/projects/" + context.id, data=json.dumps(context.project))


@step("The user receives the updated project back in the response")
def step_impl(context):
    assert str(context.response.json()['completed']).upper() == str(context.project['completed']).upper()
    assert str(context.response.json()['active']).upper() == str(context.project['active']).upper()
    assert str(context.response.json()['title']).upper() == str(context.existing_project['title']).upper()
    assert str(context.response.json()['description']).upper() == str(context.existing_project['description']).upper()


@step("The project will have its completed and active status updated in the database")
def step_impl(context):
    get_response = requests.get("http://localhost:4567/projects/" + context.id)
    assert str(get_response.json()["projects"][0]['completed']).upper() == str(context.project['completed']).upper()
    assert str(get_response.json()["projects"][0]['active']).upper() == str(context.project['active']).upper()
    assert str(get_response.json()["projects"][0]['title']).upper() == str(context.existing_project['title']).upper()
    assert str(get_response.json()["projects"][0]['description']).upper() == str(context.existing_project['description']).upper()
