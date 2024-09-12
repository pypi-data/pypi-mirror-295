# src/fishregresssion/cli.py
import requests
import os

URL = "http://" + os.environ["AWS_PIP"] + ":8080/"

def main():
    print("[INFO] Starting CLI for fish predictor...")
    while True:
        try:
            length = input("length: ")
            length = float(length)
        except ValueError:
            print("[ERROR] please input a floating-point value as length.")
            length = -1
            continue
        except KeyboardInterrupt:
            print("[INFO] Finishing...")
            return

        if length < -1:
            print("[ERROR] please input a positive number for length.")
            continue     

        regressor_url = URL + f"regressor/fish?length={length}"
        response = requests.get(regressor_url).json()
        weight_pred = round(response["weight"], 2)
        print(f"[INFO] Fetched predicted weight: {weight_pred}")
        
        classifier_url = URL + f"classifier/fish?length={length}&weight={weight_pred}"
        response = requests.get(classifier_url).json()
        type_pred = response["answer"]
        print(f">>> Based on length: {length}, weight: {weight_pred}, My guess is:")
        print(f"🐋 {type_pred}! 🐋")

        while True:
            yn = input("Was I right? [y/n] ")
            if yn == 'y' or yn == 'Y':
                print("Yay!")
                break
            elif yn == 'n' or yn == 'N':
                print("...oh...")
                break
            else:
                print("Please type in either 'y' or 'n'.")

        while True:
            yn = input("Continue? [y/n] ")
            if yn == 'y' or yn == 'Y':
                print("[INFO] Continue...\n")
                break
            elif yn == 'n' or yn == 'N':
                print("Goodbye!")
                return
            else:
                print("Please type in either 'y' or 'n'.")
        length = -1
#main()
