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


def one_change_object(responses):

    random_datapoint = random.choice(responses)
    random_id = random_datapoint.json()['id']

    new_todo = {
        "doneStatus": False,
        "description": "Writing code",
        "title": "Unit Testing"
    }

    requests.post("http://localhost:4567/todos/"+random_id, data=json.dumps(new_todo))
    print("The CPU usage rate is:", str(psutil.cpu_percent()))
    print("The available free memory is:", str(psutil.virtual_memory().available))


def fifty_change_objects(responses):
    usage_rate = 0
    available_memory = 0
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

        response = requests.post("http://localhost:4567/todos/"+random_id, data=json.dumps(new_todo))
        usage_rate = usage_rate + int(psutil.cpu_percent())
        available_memory = available_memory + (psutil.virtual_memory().available)
        
    average_usage_rate = usage_rate / 50
    average_memory =  available_memory / 50
    print("The average available free memory is:", str(average_memory))
    print("The average CPU usage rate is:", str(average_usage_rate)) 

def hundred_change_objects(responses):
    usage_rate = 0
    available_memory = 0
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

        response = requests.post("http://localhost:4567/todos/"+random_id, data=json.dumps(new_todo))
        usage_rate = usage_rate + int(psutil.cpu_percent())
        available_memory = available_memory + (psutil.virtual_memory().available)
        
    average_usage_rate = usage_rate / 100
    average_memory =  available_memory / 100
    print("The average available free memory is:", str(average_memory))
    print("The average CPU usage rate is:", str(average_usage_rate)) 


def two_hundred_change_objects(responses):
    usage_rate = 0
    available_memory = 0
    for a in range(0, 200):
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

        response = requests.post("http://localhost:4567/todos/"+random_id, data=json.dumps(new_todo))
        usage_rate = usage_rate + int(psutil.cpu_percent())
        available_memory = available_memory + (psutil.virtual_memory().available)
    
    average_usage_rate = usage_rate / 200
    average_memory =  available_memory / 200
    print("The average available free memory is:", str(average_memory))
    print("The average CPU usage rate is:", str(average_usage_rate)) 


def five_hundred_change_objects(responses):
    usage_rate = 0
    available_memory = 0
    for a in range(0, 500):
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

        response = requests.post("http://localhost:4567/todos/"+random_id, data=json.dumps(new_todo))
        usage_rate = usage_rate + int(psutil.cpu_percent())
        available_memory = available_memory + (psutil.virtual_memory().available)
        
    average_usage_rate = usage_rate / 500
    average_memory =  available_memory / 500
    print("The average available free memory is:", str(average_memory))
    print("The average CPU usage rate is:", str(average_usage_rate))    
    
def thousand_change_objects(responses):
    usage_rate = 0
    available_memory = 0
    for a in range(0, 1000):
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

        response = requests.post("http://localhost:4567/todos/"+random_id, data=json.dumps(new_todo))
        usage_rate = usage_rate + int(psutil.cpu_percent())
        available_memory = available_memory + (psutil.virtual_memory().available)
        
    average_usage_rate = usage_rate / 1000
    average_memory =  available_memory / 1000
    print("The average available free memory is:", str(average_memory))
    print("The average CPU usage rate is:", str(average_usage_rate))    


class main:
    responses = setUp()
    #one_change_object(responses)
    #fifty_change_objects(responses)
    #hundred_change_objects(responses)
    #two_hundred_change_objects(responses)
    #five_hundred_change_objects(responses)
    thousand_change_objects(responses)



'''
jar_process = setUpClass()
execution_time = timeit.timeit(code_to_run, number=1)
print("The execution time for the following post request is: ", execution_time)
tearDownClass(jar_process)
