import os
import subprocess
import time
import json
import requests
import random
import string
import psutil
import csv


def setUpClass():
    current_directory = os.getcwd()
    api_path = current_directory + "/runTodoManagerRestAPI-1.5.22.jar"
    jar_process = subprocess.Popen(['java', '-jar', api_path])
    time.sleep(5)
    return jar_process


def tearDownClass(jar_process):
    jar_process.terminate()
    jar_process.wait()


def setUp():
    responses = list()
    response = requests.get("http://localhost:4567/todos")

    for data_points in response.json()['todos']:
        deleted_id = str(data_points['id'])
        requests.delete("http://localhost:4567/todos/" + deleted_id)

    for data_points1 in range(0, 100):
        random_boolean = random.choice([True, False])

        possible_characters = string.ascii_letters

        random_description = ''.join(random.choice(possible_characters) for _ in range(data_points1 + 1))
        random_title = ''.join(random.choice(possible_characters) for _ in range(data_points1 + 1))

        new_todo = {
            "doneStatus": random_boolean,
            "description": random_description,
            "title": random_title
        }

        responses.append(requests.post("http://localhost:4567/todos", data=json.dumps(new_todo)))

    # print(responses[10].json())
    return responses


def one_change_object(responses):
    random_datapoint = random.choice(responses)
    random_id = random_datapoint.json()['id']

    new_todo = {
        "doneStatus": False,
        "description": "Writing code",
        "title": "Unit Testing"
    }

    requests.post("http://localhost:4567/todos/" + random_id, data=json.dumps(new_todo))
    print("The CPU usage rate is:", str(psutil.cpu_percent()))
    print("The available free memory is:", str(psutil.virtual_memory().available))


def fifty_change_objects(responses):
    usage_rate = 0
    available_memory = 0
    total_time = 0

    for a in range(0, 50):
        random_datapoint = random.choice(responses)

        random_id = random_datapoint.json()['id']

        random_boolean = random.choice([True, False])

        possible_characters = string.ascii_letters

        random_description = ''.join(random.choice(possible_characters) for _ in range(a + 1))
        random_title = ''.join(random.choice(possible_characters) for _ in range(a + 1))

        new_todo = {
            "doneStatus": random_boolean,
            "description": random_description,
            "title": random_title
        }

        start_time = time.time()
        requests.post("http://localhost:4567/todos/" + random_id, data=json.dumps(new_todo))
        end_time = time.time()

        cpu_usage = int(psutil.cpu_percent())
        memory = int(psutil.virtual_memory().available)
        t_time = end_time - start_time

        usage_rate = usage_rate + cpu_usage
        available_memory = available_memory + memory
        total_time = total_time + t_time

    average_usage_rate = usage_rate / 50
    average_memory = available_memory / 50
    print("The average available free memory for 50 change objects is:", str(average_memory))
    print("The average CPU usage rate for 50 change objects is:", str(average_usage_rate))
    print("The transaction time for 50 change objects is: " + str(total_time))


def hundred_change_objects(responses):

    usage_rate = 0
    available_memory = 0
    total_time = 0
    for a in range(0, 100):
        random_datapoint = random.choice(responses)
        random_id = random_datapoint.json()['id']

        random_boolean = random.choice([True, False])

        possible_characters = string.ascii_letters

        random_description = ''.join(random.choice(possible_characters) for _ in range(a + 1))
        random_title = ''.join(random.choice(possible_characters) for _ in range(a + 1))

        new_todo = {
            "doneStatus": random_boolean,
            "description": random_description,
            "title": random_title
        }

        start_time = time.time()
        response = requests.post("http://localhost:4567/todos/" + random_id, data=json.dumps(new_todo))
        end_time = time.time()

        cpu_usage = int(psutil.cpu_percent())
        memory = int(psutil.virtual_memory().available)
        t_time = end_time - start_time

        usage_rate = usage_rate + cpu_usage
        available_memory = available_memory + memory
        total_time = total_time + t_time

    average_usage_rate = usage_rate / 100
    average_memory = available_memory / 100
    print("The average available free memory for 100 change objects is:", str(average_memory))
    print("The average CPU usage rate for 100 change objects is:", str(average_usage_rate))
    print("The transaction time for 100 change objects is: " + str(total_time))


def two_hundred_change_objects(responses):
    usage_rate = 0
    available_memory = 0
    total_time = 0

    for a in range(0, 200):
        random_datapoint = random.choice(responses)
        random_id = random_datapoint.json()['id']

        random_boolean = random.choice([True, False])

        possible_characters = string.ascii_letters

        random_description = ''.join(random.choice(possible_characters) for _ in range(a + 1))
        random_title = ''.join(random.choice(possible_characters) for _ in range(a + 1))

        new_todo = {
            "doneStatus": random_boolean,
            "description": random_description,
            "title": random_title
        }

        start_time = time.time()
        response = requests.post("http://localhost:4567/todos/" + random_id, data=json.dumps(new_todo))
        end_time = time.time()

        cpu_usage = int(psutil.cpu_percent())
        memory = int(psutil.virtual_memory().available)
        t_time = end_time - start_time

        usage_rate = usage_rate + cpu_usage
        available_memory = available_memory + memory
        total_time = total_time + t_time

    average_usage_rate = usage_rate / 200
    average_memory = available_memory / 200
    print("The average available free memory for 200 change objects is:", str(average_memory))
    print("The average CPU usage rate for 200 change objects is:", str(average_usage_rate))
    print("The transaction time for 200 change objects is: " + str(total_time))


def five_hundred_change_objects(responses):

    usage_rate = 0
    available_memory = 0
    total_time = 0

    for a in range(0, 500):
        random_datapoint = random.choice(responses)
        random_id = random_datapoint.json()['id']

        random_boolean = random.choice([True, False])

        possible_characters = string.ascii_letters

        random_description = ''.join(random.choice(possible_characters) for _ in range(a + 1))
        random_title = ''.join(random.choice(possible_characters) for _ in range(a + 1))

        new_todo = {
            "doneStatus": random_boolean,
            "description": random_description,
            "title": random_title
        }

        start_time = time.time()
        response = requests.post("http://localhost:4567/todos/" + random_id, data=json.dumps(new_todo))
        end_time = time.time()

        cpu_usage = int(psutil.cpu_percent())
        memory = int(psutil.virtual_memory().available)
        t_time = end_time - start_time

        usage_rate = usage_rate + cpu_usage
        available_memory = available_memory + memory
        total_time = total_time + t_time

    average_usage_rate = usage_rate / 500
    average_memory = available_memory / 500
    print("The average available free memory for 500 change objects is:", str(average_memory))
    print("The average CPU usage rate for 500 change objects is:", str(average_usage_rate))
    print("The transaction time for 500 change objects is: " + str(total_time))


def thousand_change_objects(responses):
    cpu_data = list()
    memory_data = list()
    transaction_data = list()

    usage_rate = 0
    available_memory = 0
    total_time = 0
    for a in range(0, 1000):
        random_datapoint = random.choice(responses)
        random_id = random_datapoint.json()['id']

        random_boolean = random.choice([True, False])

        possible_characters = string.ascii_letters

        random_description = ''.join(random.choice(possible_characters) for _ in range(a + 1))
        random_title = ''.join(random.choice(possible_characters) for _ in range(a + 1))

        new_todo = {
            "doneStatus": random_boolean,
            "description": random_description,
            "title": random_title
        }

        start_time = time.time()
        response = requests.post("http://localhost:4567/todos/" + random_id, data=json.dumps(new_todo))
        end_time = time.time()

        cpu_usage = int(psutil.cpu_percent())
        memory = int(psutil.virtual_memory().available)
        t_time = end_time - start_time

        current_time = time.strftime("%H:%M:%S", time.localtime())
        cpu_data.append({"Sample Time": current_time, "CPU Usage": cpu_usage})
        memory_data.append({"Sample Time": current_time, "Available Memory": memory})
        transaction_data.append({"Sample Time": current_time, "Transaction Time": t_time})

        usage_rate = usage_rate + cpu_usage
        available_memory = available_memory + memory
        total_time = total_time + t_time

    csv_file = "change_requests_1000_data_points.csv"
    with open(csv_file, mode='w', newline='') as file:
        fieldnames = ["Sample Time", "CPU Usage"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cpu_data)

    csv_file = "change_requests_1000_data_points_available_memory.csv"
    with open(csv_file, mode='w', newline='') as file1:
        fieldnames1 = ["Sample Time", "Available Memory"]
        writer1 = csv.DictWriter(file1, fieldnames=fieldnames1)
        writer1.writeheader()
        writer1.writerows(memory_data)

    csv_file = "change_requests_1000_data_points_transaction_time.csv"
    with open(csv_file, mode='w', newline='') as file2:
        fieldnames2 = ["Sample Time", "Transaction Time"]
        writer2 = csv.DictWriter(file2, fieldnames=fieldnames2)
        writer2.writeheader()
        writer2.writerows(transaction_data)

    average_usage_rate = usage_rate / 1000
    average_memory = available_memory / 1000
    print("The average available free memory for 1000 change objects is:", str(average_memory))
    print("The average CPU usage rate for 1000 change objects is:", str(average_usage_rate))
    print("The transaction time for 1000 change objects is: " + str(total_time))


class main:
    jar_process = setUpClass()
    responses = setUp()
    one_change_object(responses)
    tearDownClass(jar_process)

    jar_process = setUpClass()
    responses = setUp()
    fifty_change_objects(responses)
    tearDownClass(jar_process)

    jar_process = setUpClass()
    responses = setUp()
    hundred_change_objects(responses)
    tearDownClass(jar_process)

    jar_process = setUpClass()
    responses = setUp()
    two_hundred_change_objects(responses)
    tearDownClass(jar_process)

    jar_process = setUpClass()
    responses = setUp()
    five_hundred_change_objects(responses)
    tearDownClass(jar_process)

    jar_process = setUpClass()
    responses = setUp()
    thousand_change_objects(responses)
    tearDownClass(jar_process)
