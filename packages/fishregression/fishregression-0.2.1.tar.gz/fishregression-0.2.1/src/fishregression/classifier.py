# src/fishregression/classifier.py

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import pickle
import os

def grab_path(filename):
    this_path = os.path.abspath(__file__)
    data_path = os.path.dirname(this_path) + "/data/" + filename
    return data_path

def load_csv(data_name="testdata.csv"):
    data_path = grab_path(data_name)
    x_data, y_data = [], []

    with open(data_path, "r") as data:
        next(data)
        for line in data:
            length, weight, answer = line.strip().split(",")
            val = 1 if answer == "Smelt" else 0     # Smelt 1 / Bream 0
            
            x_data.append([float(length), float(weight)])
            y_data.append(val)

    x_data = np.array(x_data)
    y_data = np.array(y_data).reshape(-1, 1)

#    print(np.shape(x_data))
#    print(np.shape(y_data))

    return x_data, y_data

def train_kn(model_name="classifier.pkl"):
    kn = KNeighborsClassifier(n_neighbors=5)
    x_data, y_data = load_csv()
    kn.fit(x_data, y_data)

    model_path = grab_path(model_name)
    with open(model_path, "wb") as model:
        pickle.dump(kn, model)
    print("[INFO] classifier.pkl updated!")

def test_kn(method=1, model_name="classifier.pkl"):
    kn = KNeighborsClassifier()
    if method == 0:
        model_path = grab_path(model_name)
        with open(model_path, "rb") as model:
            kn = pickle.load(model)

    x_data, y_data = load_csv()
    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2, random_state=42)

    kn.fit(x_train, y_train)
    prediction = kn.predict(x_test)

    tmp = 0
    for i in range(len(y_test)):
        if prediction[i] == y_test[i]:
            tmp += 1

    acc = round(tmp/len(y_test) * 100, 2)
    print(f"ACCURACY: {acc}%")

#load_csv()
train_kn()
#test_kn(1)
#test_kn(2)
