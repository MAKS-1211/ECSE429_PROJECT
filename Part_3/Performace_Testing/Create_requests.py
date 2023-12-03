import timeit
import os
import subprocess
import time
import json
import requests


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


def setUp():
    responses = list()
    response = requests.get("http://localhost:4567/todos")

    for data_points in response.json()['todos']:
        deleted_id = str(data_points['id'])
        requests.delete("http://localhost:4567/todos/" + deleted_id)


code_to_run = '''
import json
import requests
import os
import subprocess
import time
import random
import string
import psutil

def setUp():
    responses = list()
    response = requests.get("http://localhost:4567/todos")

    for data_points in response.json()['todos']:
        deleted_id = str(data_points['id'])
        requests.delete("http://localhost:4567/todos/" + deleted_id)

def one_post_objects():
    new_todo = {
        "doneStatus": False,
        "description": "Writing code",
        "title": "Unit Testing"
    }

    requests.post("http://localhost:4567/todos", data=json.dumps(new_todo))
    print("The available free memory is:", str(psutil.virtual_memory().available))
    print("The CPU usage rate is:", str(psutil.cpu_percent()))  


def fifty_post_objects():
    for a in range(0, 50):
        random_boolean = random.choice([True, False])

        possible_characters = string.ascii_letters

        random_description = ''.join(random.choice(possible_characters) for _ in range(a+1))
        random_title = ''.join(random.choice(possible_characters) for _ in range(a+1))

        new_todo = {
            "doneStatus": random_boolean,
            "description": random_description,
            "title": random_title
        }

        requests.post("http://localhost:4567/todos", data=json.dumps(new_todo))
        
    print("The available free memory is:", str(psutil.virtual_memory().available))
    print("The CPU usage rate is:", str(psutil.cpu_percent()))    


def hundred_post_objects():
    for a in range(0, 100):
        random_boolean = random.choice([True, False])

        possible_characters = string.ascii_letters

        random_description = ''.join(random.choice(possible_characters) for _ in range(a+1))
        random_title = ''.join(random.choice(possible_characters) for _ in range(a+1))

        new_todo = {
            "doneStatus": random_boolean,
            "description": random_description,
            "title": random_title
        }

        requests.post("http://localhost:4567/todos", data=json.dumps(new_todo))
        if a == 98:
            print("The available free memory is:", str(psutil.virtual_memory().available))
            print("The CPU usage rate is:", str(psutil.cpu_percent()))    

def two_hundred_post_objects():
    for a in range(0, 200):
        random_boolean = random.choice([True, False])

        possible_characters = string.ascii_letters

        random_description = ''.join(random.choice(possible_characters) for _ in range(a+1))
        random_title = ''.join(random.choice(possible_characters) for _ in range(a+1))

        new_todo = {
            "doneStatus": random_boolean,
            "description": random_description,
            "title": random_title
        }

        requests.post("http://localhost:4567/todos", data=json.dumps(new_todo))
        if a == 198:
            print("The available free memory is:", str(psutil.virtual_memory().available))
            print("The CPU usage rate is:", str(psutil.cpu_percent()))      

def five_hundred_post_objects():
    for a in range(0, 500):
        random_boolean = random.choice([True, False])

        possible_characters = string.ascii_letters

        random_description = ''.join(random.choice(possible_characters) for _ in range(a+1))
        random_title = ''.join(random.choice(possible_characters) for _ in range(a+1))

        new_todo = {
            "doneStatus": random_boolean,
            "description": random_description,
            "title": random_title
        }

        requests.post("http://localhost:4567/todos", data=json.dumps(new_todo))
        if a == 498:
            print("The available free memory is:", str(psutil.virtual_memory().available))
            print("The CPU usage rate is:", str(psutil.cpu_percent()))    

def one_thousand_post_objects():
    for a in range(0, 1000):
        random_boolean = random.choice([True, False])

        possible_characters = string.ascii_letters

        random_description = ''.join(random.choice(possible_characters) for _ in range(a+1))
        random_title = ''.join(random.choice(possible_characters) for _ in range(a+1))

        new_todo = {
            "doneStatus": random_boolean,
            "description": random_description,
            "title": random_title
        }

        requests.post("http://localhost:4567/todos", data=json.dumps(new_todo))
        if a == 998:
            print("The available free memory is:", str(psutil.virtual_memory().available))
            print("The CPU usage rate is:", str(psutil.cpu_percent()))    
    
class main:
    #one_post_objects()
    #fifty_post_objects()
    hundred_post_objects()
    #two_hundred_post_objects()
    #five_hundred_post_objects()
    #one_thousand_post_objects()
    
    
'''
jar_process = setUpClass()
setUp()
execution_time = timeit.timeit(code_to_run, number=1)
print("The execution time for the following post request is: ", execution_time)
tearDownClass(jar_process)
