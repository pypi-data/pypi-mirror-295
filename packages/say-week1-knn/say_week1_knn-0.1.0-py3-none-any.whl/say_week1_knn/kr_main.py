# src/say_week1_knn/main.py

import numpy as np
import os
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import pickle
import random

kn = KNeighborsClassifier(n_neighbors=5)
x_data, y_data = [], []

# Creates dummy data of size 10
def create_dummy():
    global x_data, y_data
    x_data, y_data = [], []
    for i in range (10):
        x_data.append( [round(random.uniform(10, 41), 2), round(random.uniform(10, 1000), 2) ])
        y_data.append( random.choice( ["Bream", "Smelt"] ) )

# yes, no, exit handling
def yes_or_no(prompt):
    while True:
        yn = input(prompt + " [y/n] ")
        if yn == "y" or yn == "Y":
            return 1
        elif yn == "n" or yn == "N":
            return 0
        elif yn == "exit":
            return -1
        else:
            print("Wrong format. Please input one of 'y', 'n' or 'exit'. Retrying...")
            continue

def grab_data_path(data="testdata.csv"):
    this_path = os.path.abspath(__file__)
    data_path = os.path.dirname(this_path) + "/data/" + data
    return data_path

def grab_model_path(model="model.pkl"):
    this_path = os.path.abspath(__file__)
    model_path = os.path.dirname(this_path) + "/data/" + model
    return model_path

def parse_data(data_path):
    global x_data, y_data
    x_data, y_data = [], []     # should only be called once, but redundancy

    with open(data_path, "r") as data:
        next(data)                         # skips line "Length,Width,Label"
        for line in data:
            length, width, answer = line.strip().split(",")
            val = 1 if answer == "Smelt" else 0     # Smelt: 1, Bream: 0

            x_data.append([float(length), float(width)])
            y_data.append(val)
    print(f"[INFO] data collected from: {data_path}")

def bulk_train(x_list=[], y_list=[]):
    global x_data, y_data
    for i in range (len(x_list)):
        x_data.append(x_list[i])
        y_data.append(y_list[i])

    if len(x_data) > 25:     # needs at least 25 to split 1:4 and still be testable!!
        x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2, random_state=42)
    else:
        x_train, y_train, x_test, y_test = x_data, y_data, x_data, y_data

    kn.fit(x_train, y_train)
    if len(x_test) > 5:
        bulk_test(x_test, y_test)
    else:
        print("[INFO] Not enough data to test accuracy yet! Continuing...")

# testing accuracy. Usually overfitted, so 100%.
def bulk_test(x_test, y_test):
    prediction = kn.predict(x_test)
    tmp = 0

    for i in range(len(y_test)):
        if prediction[i] == y_test[i]:
            tmp += 1
    
    acc = tmp/len(y_test) * 100
    print(f"RESULT: {acc} % accuracy\n")

def prompt():
    print("[INFO] Proceeding to manual prompt.\n")
    print("[INFO] User prompt activated! Please input the length and width.\n")
    while True:
        try:
            line = input("length, width [whitespace-separated]: ")
            if line == 'exit':
                return

            length, width = line.strip().split()
            length = float(length)
            width = float(width)

        except ValueError:
            print("[ERROR] There was an ValueError. length/width should be convertable to floating point values. Please try again.\n")
            continue

        else:
            val, prediction = predict(length, width)
            print(f"The prediction for given length: {length}, width: {width} is: {prediction}")
            correct = yes_or_no("Was this prediction correct?")

            if correct == 1:
                update(length, width, val) # updates model
            elif correct == 0:
                update(length, width, 1-val)
            else:
                print("Exiting...")
                return

def predict(length, width):
    try:
        if kn.predict([[length, width]])[0] == 1: # 1 == Smelt
            return 1, "Smelt"
        else:
            return 0, "Bream"
    except Exception as e:
        print(f"An error occurred: {e}")
        print("[INFO] Creating dummy data...")
        create_dummy()

def update(length, width, val):
    bulk_train([[length, width]], [val])

def save_model():
    model_path = grab_model_path()
    with open(model_path, "wb") as model:
        pickle.dump(kn, model)

# debug

def main():
    print("[INFO] Beginning fish prediction program! type 'exit' to finish whenever an input prompt comes up.\n")

    import_model = yes_or_no("Welcome! Do you wish to import a preexisting model?")
    if import_model == 1:
        try:
            global kn
            with open(grab_model_path(), "rb") as f:
                kn = pickle.load(f)
        except:
            print("[INFO] Model doesn't exist! Creating dummy...")
            create_dummy()
            bulk_train()

    elif import_model == -1:
        print("[INFO] Finishing...")    # DOESNT save model b/c unloaded
        return

    # import model == 0: New model
    print("[INFO] Startingn from new model.\n")
    bulk = yes_or_no("Do you wish to bulk-train the model before entering prompt?")

    if bulk == 1:
        print("[INFO] Proceeding to bulk-train from prefab data...\n")
        parse_data(grab_data_path())
        bulk_train()

        print("[INFO] Bulk-train complete!\n")
        prompt()

    elif bulk == 0:
        prompt()

    print("[INFO] Finishing...")
    save_model()

main()
