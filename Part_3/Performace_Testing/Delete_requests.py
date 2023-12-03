import timeit
import os
import subprocess
import time


def setUpClass():
    current_directory = os.getcwd()
    api_path = current_directory + "/runTodoManagerRestAPI-1.5.22.jar"
    jar_process = subprocess.Popen(['java', '-jar', api_path])
    time.sleep(5)
    return jar_process


def tearDownClass(jar_process):
    jar_process.terminate()
    jar_process.wait()
    time.sleep(5)


code_to_run = '''
import json
import requests
import random
import string
import timeit
import psutil


def setUp():
    responses = list()
    response = requests.get("http://localhost:4567/todos")

    for data_points in response.json()['todos']:
        deleted_id = str(data_points['id'])
        requests.delete("http://localhost:4567/todos/" + deleted_id)

    for data_points1 in range(0, 100):
        random_boolean = random.choice([True, False])

        possible_characters = string.ascii_letters

        random_description = ''.join(random.choice(possible_characters) for _ in range(data_points1+1))
        random_title = ''.join(random.choice(possible_characters) for _ in range(data_points1+1))

        new_todo = {
            "doneStatus": random_boolean,
            "description": random_description,
            "title": random_title
        }

        responses.append(requests.post("http://localhost:4567/todos", data=json.dumps(new_todo)))

    #print(responses[10].json())
    return responses


def one_delete_object(responses):

    random_datapoint = random.choice(responses)
    random_id = random_datapoint.json()['id']


    requests.delete("http://localhost:4567/todos/"+random_id)
    print("The CPU usage rate is:", str(psutil.cpu_percent()))
    print("The available free memory is:", str(psutil.virtual_memory().available))


def ten_delete_objects(responses):
    for a in range(0, 10):
        random_datapoint = random.choice(responses)
        random_id = random_datapoint.json()['id']

        random_boolean = random.choice([True, False])

        possible_characters = string.ascii_letters

        random_description = ''.join(random.choice(possible_characters) for _ in range(a+1))
        random_title = ''.join(random.choice(possible_characters) for _ in range(a+1))

        new_todo = {
            "doneStatus": random_boolean,
            "description": random_description,
            "title": random_title
        }

        requests.delete("http://localhost:4567/todos/"+random_id)
    print("The CPU usage rate is:", str(psutil.cpu_percent()))
    print("The available free memory is:", str(psutil.virtual_memory().available))

def twenty_five_delete_objects(responses):
    for a in range(0, 25):
        random_datapoint = random.choice(responses)
        random_id = random_datapoint.json()['id']

        random_boolean = random.choice([True, False])

        possible_characters = string.ascii_letters

        random_description = ''.join(random.choice(possible_characters) for _ in range(a+1))
        random_title = ''.join(random.choice(possible_characters) for _ in range(a+1))

        new_todo = {
            "doneStatus": random_boolean,
            "description": random_description,
            "title": random_title
        }

        requests.delete("http://localhost:4567/todos/"+random_id)
    print("The CPU usage rate is:", str(psutil.cpu_percent()))
    print("The available free memory is:", str(psutil.virtual_memory().available))


def fifty_delete_objects(responses):
    for a in range(0, 50):
        random_datapoint = random.choice(responses)
        random_id = random_datapoint.json()['id']

        random_boolean = random.choice([True, False])

        possible_characters = string.ascii_letters

        random_description = ''.join(random.choice(possible_characters) for _ in range(a+1))
        random_title = ''.join(random.choice(possible_characters) for _ in range(a+1))

        new_todo = {
            "doneStatus": random_boolean,
            "description": random_description,
            "title": random_title
        }

        requests.delete("http://localhost:4567/todos/"+random_id)
    print("The CPU usage rate is:", str(psutil.cpu_percent()))
    print("The available free memory is:", str(psutil.virtual_memory().available))


def hundred_delete_objects(responses):
    for a in range(0, 100):
        random_datapoint = random.choice(responses)
        random_id = random_datapoint.json()['id']

        random_boolean = random.choice([True, False])

        possible_characters = string.ascii_letters

        random_description = ''.join(random.choice(possible_characters) for _ in range(a+1))
        random_title = ''.join(random.choice(possible_characters) for _ in range(a+1))

        new_todo = {
            "doneStatus": random_boolean,
            "description": random_description,
            "title": random_title
        }

        requests.delete("http://localhost:4567/todos/"+random_id)

    print("The CPU usage rate is:", str(psutil.cpu_percent()))
    print("The available free memory is:", str(psutil.virtual_memory().available))


class main:
    responses = setUp()
    # one_delete_object(responses)
    #ten_delete_objects(responses)
    # twenty_five_delete_objects(responses)
    # fifty_delete_objects(responses)
    hundred_delete_objects(responses)



'''
jar_process = setUpClass()
execution_time = timeit.timeit(code_to_run, number=1)
print("The execution time for the following delete request is: ", execution_time)
tearDownClass(jar_process)
