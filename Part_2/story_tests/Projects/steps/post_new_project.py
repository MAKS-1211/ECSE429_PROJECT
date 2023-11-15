from behave import *
import os
import time
import json
import requests
import subprocess


@given('The API is running')
def step_impl(context):
    context.current_directory = os.getcwd()
    context.api_path = context.current_directory + "/runTodoManagerRestAPI-1.5.22.jar"
    context.jar_process = subprocess.Popen(['java', '-jar', context.api_path])
    time.sleep(5)

@step("the API has no project entries")
def step_impl(context):
    response = requests.get("http://localhost:4567/projects")
    for data_points in response.json()['projects']:
        deleted_id = str(data_points['id'])
        requests.delete("http://localhost:4567/projects/" + deleted_id)

@given('A project with a title {tit}, a description {desc}, an active status {act} and a completed status {comp}')
def step_impl(context, tit, desc, act, comp):
    context.project = {
            "completed": bool(comp),
            "active": bool(act),
            "description": desc,
            "title": tit
        }

@given("A project with no title, no description, no active status and no completed status")
def step_impl(context):
    context.project = {}


@given("A project with a title {tit}, a description {desc}, an active status {act}, a completed status {comp} and an id {id}")
def step_impl(context, tit, desc, act, comp, id):
    context.project = {
        "completed": bool(comp),
        "active": bool(act),
        "description": desc,
        "title": tit,
        "id": id
    }

@when('The user posts the project')
def step_impl(context):
    context.response = requests.post("http://localhost:4567/projects", data=json.dumps(context.project))

@then('The user receives a CREATED HTTP status code (201)')
def step_impl(context):
    assert context.response.status_code == 201

@then('The user receives the project back in the response')
def step_impl(context):
    assert str(context.response.json()['completed']).upper() == str(context.project['completed']).upper()
    assert str(context.response.json()['active']).upper() == str(context.project['active']).upper()
    assert str(context.response.json()['title']).upper() == str(context.project['title']).upper()
    assert str(context.response.json()['description']).upper() == str(context.project['description']).upper()


@step('The user receives a default project back in the response with title = "", description = "", completed = False, active = False')
def step_impl(context):
    assert str(context.response.json()['completed']).upper() == "FALSE"
    assert str(context.response.json()['active']).upper() == "FALSE"
    assert str(context.response.json()['title']).upper() == ""
    assert str(context.response.json()['description']).upper() == ""


@step("The project will be in the database")
def step_impl(context):
    get_response = requests.get("http://localhost:4567/projects/" + context.response.json()["id"])

    assert get_response.status_code == 200
    assert str(get_response.json()["projects"][0]['completed']).upper() == str(context.project['completed']).upper()
    assert str(get_response.json()["projects"][0]['active']).upper() == str(context.project['active']).upper()
    assert str(get_response.json()["projects"][0]['description']).upper() == str(context.project['description']).upper()
    assert str(get_response.json()["projects"][0]['title']).upper() == str(context.project['title']).upper()


@step("The default project will be in the database")
def step_impl(context):
    get_response = requests.get("http://localhost:4567/projects/" + context.response.json()["id"])

    assert get_response.status_code == 200
    assert str(get_response.json()["projects"][0]['completed']).upper() == "FALSE"
    assert str(get_response.json()["projects"][0]['active']).upper() == "FALSE"
    assert str(get_response.json()["projects"][0]['description']).upper() == ""
    assert str(get_response.json()["projects"][0]['title']).upper() == ""


@then("The user will get a Bad Request HTTP status code (400)")
def step_impl(context):
    assert context.response.status_code == 400


@step("The user gets an error message {err}")
def step_impl(context, err):
    assert context.response.json()["errorMessages"][0] == err