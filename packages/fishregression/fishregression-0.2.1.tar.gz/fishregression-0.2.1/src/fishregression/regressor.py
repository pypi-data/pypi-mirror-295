# src/fishregression/regressor.py

import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import os

def grab_path(filename):
    this_path = os.path.abspath(__file__)
    data_path = os.path.dirname(this_path) + "/data/" + filename
    return data_path

def load_csv(data_name="testdata.csv"):
    length_data, weight_data = [], []

    data_path = grab_path(data_name)
    with open(data_path, "r") as data:
        next(data)      # first line is not data
        for line in data:
            length, weight, answer = line.strip().split(",")

            # polynomial regression: x**2, x, c
            length_data.append([float(length)**2, float(length)])
            weight_data.append(float(weight))

    length_data = np.array(length_data)
    weight_data = np.array(weight_data).reshape(-1, 1)

    return length_data, weight_data
    
def train_lr(model_name="regressor.pkl"):
    lr = LinearRegression()
    length_data, weight_data = load_csv()
    lr.fit(length_data, weight_data)
    
    model_path = grab_path(model_name)
    with open(model_path, "wb") as model:
        pickle.dump(lr, model)
    print("[INFO] regressor.pkl updated!")

def test_lr(method=1, model_name="regressor.pkl"):
    if method == 1:
        lr = LinearRegression()
    elif method == 0:
        model_path = grab_path(model_name)
        with open(model_path, "rb") as model:
            lr = pickle.load(model)

    length_data, weight_data = load_csv()

    train_in, test_in, train_out, test_out = train_test_split(length_data, weight_data)    

    lr.fit(train_in, train_out)
    prediction = lr.predict(test_in)
    tmp = 0

    for i in range(len(test_in)):
        print(prediction[i]/test_out[i])

    #acc = round(tmp/len(test_in) * 100, 2)
    #print(f"RESULT: {acc}% accuracy\n")

train_lr()
#test_lr(0)
#test_lr(1)
