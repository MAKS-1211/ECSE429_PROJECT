from behave import *
import json
import requests


@when(
    "The user tries to amend the project with a new title {newtit}, a new description {newdesc}, a new active status {newact} and a new completed status {newcomp} using PUT")
def step_impl(context, newtit, newdesc, newact, newcomp):
    context.project = {
        "title": newtit,
        "description": newdesc,
        "active": bool(newact),
        "completed": bool(newcomp)
    }
    context.response = requests.put("http://localhost:4567/projects/" + context.id, data=json.dumps(context.project))


@when("The user tries to amend the project with no fields declared using PUT")
def step_impl(context):
    context.project = {}

    context.response = requests.put("http://localhost:4567/projects/" + context.id, data=json.dumps(context.project))


@when("The user tries to amend the project's id to {id} using PUT")
def step_impl(context, id):
    context.project = {
        "id": id
    }

    context.response = requests.put("http://localhost:4567/projects/" + context.id, data=json.dumps(context.project))