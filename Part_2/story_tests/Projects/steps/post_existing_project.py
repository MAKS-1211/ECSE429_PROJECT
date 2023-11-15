from behave import *
import json
import requests

@given(
    "An already existing project with a title {tit}, a description {desc}, an active status {act} and a completed status {comp}")
def step_impl(context, tit, desc, act, comp):
    context.existing_project = {
        "title": tit,
        "description": desc,
        "active": bool(act),
        "completed": bool(comp)
    }
    context.existing_response = requests.post("http://localhost:4567/projects", data=json.dumps(context.existing_project))
    assert context.existing_response.status_code == 201
    context.id = context.existing_response.json()["id"]

@when(
    "The user tries to amend the project with a new title {newtit}, a new description {newdesc}, a new active status {newact} and a new completed status {newcomp} using POST")
def step_impl(context, newtit, newdesc, newact, newcomp):
    context.project = {
        "title": newtit,
        "description": newdesc,
        "active": bool(newact),
        "completed": bool(newcomp)
    }
    context.response = requests.post("http://localhost:4567/projects/" + context.id, data=json.dumps(context.project))

@then("The user receives an OK HTTP status code (200)")
def step_impl(context):
    assert context.response.status_code == 200


@step("The project will have its fields updated in the database")
def step_impl(context):
    get_response = requests.get("http://localhost:4567/projects/" + context.id)

    assert get_response.status_code == 200

    assert str(get_response.json()["projects"][0]['completed']).upper() == str(context.project['completed']).upper()
    assert str(get_response.json()["projects"][0]['active']).upper() == str(context.project['active']).upper()
    assert str(get_response.json()["projects"][0]['description']).upper() == str(context.project['description']).upper()
    assert str(get_response.json()["projects"][0]['title']).upper() == str(context.project['title']).upper()


@when("The user tries to amend the project with no fields declared using POST")
def step_impl(context):
    context.project = {}
    context.response = requests.post("http://localhost:4567/projects/" + context.id, data=json.dumps(context.project))



@step("The user receives the existing project back in the response unchanged")
def step_impl(context):
    assert str(context.response.json()['completed']).upper() == str(context.existing_project['completed']).upper()
    assert str(context.response.json()['active']).upper() == str(context.existing_project['active']).upper()
    assert str(context.response.json()['title']).upper() == str(context.existing_project['title']).upper()
    assert str(context.response.json()['description']).upper() == str(context.existing_project['description']).upper()


@step("The project will have its fields unchanged in the database")
def step_impl(context):
    get_response = requests.get("http://localhost:4567/projects/" + context.id)

    assert get_response.status_code == 200

    assert str(get_response.json()["projects"][0]['completed']).upper() == str(context.existing_project['completed']).upper()
    assert str(get_response.json()["projects"][0]['active']).upper() == str(context.existing_project['active']).upper()
    assert str(get_response.json()["projects"][0]['description']).upper() == str(context.existing_project['description']).upper()
    assert str(get_response.json()["projects"][0]['title']).upper() == str(context.existing_project['title']).upper()


@when("The user tries to amend the project's id to {id} using POST")
def step_impl(context, id):
    context.project = {
        "id": id
    }
    context.response = requests.post("http://localhost:4567/projects/" + context.id, data=json.dumps(context.project))