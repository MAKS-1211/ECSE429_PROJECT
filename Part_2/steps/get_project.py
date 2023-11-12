from behave import *
import os
import time
import json
import requests
import subprocess

@when("The user tries to get the project using its id")
def step_impl(context):
    context.response = requests.get("http://localhost:4567/projects/" + context.id)
    assert context.response.status_code == 200


@when("The user tries to get all existing projects in the database")
def step_impl(context):
    context.response = requests.get("http://localhost:4567/projects")
    assert context.response.status_code == 200


@step("The project will be in the collection of all projects that were returned")
def step_impl(context):
    found = False
    for data_points in context.response.json()['projects']:
        if data_points['id'] == context.id:
            found = True
            assert data_points['active'].upper() == str(context.existing_project['active']).upper()
            assert data_points['completed'].upper() == str(context.existing_project['completed']).upper()
            assert data_points['title'].upper() == str(context.existing_project['title']).upper()
            assert data_points['description'].upper() == str(context.existing_project['description']).upper()

    assert found == True

@when("The user tries to get the project using an id {id}")
def step_impl(context, id):
    context.response = requests.get("http://localhost:4567/projects/" + id)


@then("The user will get a Not Found HTTP status code (404)")
def step_impl(context):
    assert context.response.status_code == 404


@step("The user receives the existing project back in response")
def step_impl(context):
    assert str(context.response.json()["projects"][0]['completed']).upper() == str(context.existing_project['completed']).upper()
    assert str(context.response.json()["projects"][0]['active']).upper() == str(context.existing_project['active']).upper()
    assert str(context.response.json()["projects"][0]['title']).upper() == str(context.existing_project['title']).upper()
    assert str(context.response.json()["projects"][0]['description']).upper() == str(context.existing_project['description']).upper()
