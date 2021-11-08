# Copyright (c) 2021 David Loewe
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import argparse
import yaml
import json
import numpy as np
from signal import signal, SIGINT

def run_questionaire(data):
    # Mapping of input to index
    answer_options = { "A": 0, "a": 0, "B": 1, "b": 1, "C": 2, "c": 2, "D": 3, "d": 3, "E": 4, "e": 4, "F": 5, "f": 5, "G": 6, "g": 6 }
    # Number of questions to ask
    num_of_questions = []
    for key in data:
        while True:
            try:
                num_of_questions.append([key, min(len(data[key]), int(input("How many questions out of '" + key + "'? [0.." + str(len(data[key])) + "]  ")))])
                break
            except SystemExit:
                exit(0)
    total_question_num = 0
    wrong_answers = []
    print("Let's start...")
    # Loop over all chapters
    # val[0] = chapter name
    # val[1] = number of questions to ask
    for val in num_of_questions:
        key = val[0]
        total_question_num += val[1]
        if val[1] > 0:
            print("===================================================")
            print(" Chapter: " + val[0])
            print("===================================================")
        # Get permutation to choose questions "randomly"
        perm = np.random.permutation(len(data[key]))
        for idx in range(val[1]):
            if data[key][perm[idx]]["type"] == "choice":
                continue
            print("-------------------" + str(idx+1) + " / " + str(val[1]) + "---------------------------")
            print(" Question: " + data[key][perm[idx]]["question"])
            if "description" in data[key][perm[idx]]:
                print("")
                print(data[key][perm[idx]]["description"])
            if "info" in data[key][perm[idx]]:
                for info in data[key][perm[idx]]["info"]:
                    print(" " + info)
            print("")
            for opt in data[key][perm[idx]]["options"]:
                print(" " + opt)
            print("")

            input_correct = False
            while not input_correct:
                if data[key][perm[idx]]["type"] == "mapping":
                    choice = input(" " + data[key][perm[idx]]["task"] + " [A,B,C,..]: ")
                else:
                    choice = input(" Answer [A,B,C,..]: ")
                if (choice in answer_options) and (answer_options[choice] < len(data[key][perm[idx]]["options"])):
                    input_correct = True

            if data[key][perm[idx]]["solution"] != data[key][perm[idx]]["options"][answer_options[choice]]:
                # Store wrong answers
                # key: Chapter
                # perm[idx]: Number of question
                # choice: Wrong choice by user
                wrong_answers.append([key, perm[idx], answer_options[choice]])

    # Print statistics
    print("===================================================")
    print(" Result: " + str(total_question_num - len(wrong_answers)) + " / " + str(total_question_num) + " correct")
    print("===================================================")
    input(" Press ENTER to continue with recap.")
    print()

    last_chapter = None
    # Print wrong answers again
    for answer in wrong_answers:
        if last_chapter != answer[0]:
            print("===================================================")
            print(" Chapter: " + answer[0])
            print("===================================================")
            last_chapter = answer[0]
        print("---------------------------------------------------")
        print(" Question: " + data[answer[0]][answer[1]]["question"])
        if "description" in data[answer[0]][answer[1]]:
            print("")
            print(data[answer[0]][answer[1]]["description"])
        if "info" in data[answer[0]][answer[1]]:
            for val in data[answer[0]][answer[1]]["info"]:
                print(" " + val)
        print("")
        for val in data[answer[0]][answer[1]]["options"]:
            if data[answer[0]][answer[1]]["options"][answer[2]] == val:
                print(" " + val + " << YOU")
            elif data[answer[0]][answer[1]]["solution"] == val:
                print(" " + val + " << SOLUTION")
            else:
                print(" " + val)
        input("")
    input("Exiting... Press ENTER")

def signal_handler(signal, frame):
    print("\nSIGINT received - exiting...")
    exit(0)

def load_yaml(filename):
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)
    return data

def load_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

if __name__ == "__main__":
    print("Version 1.2")
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="optional path to custom config")
    parser.add_argument("data", help="input filename for question data")
    parser.add_argument("--json", action="store_true", help="input is json instead of yaml")
    args = parser.parse_args()

    signal(SIGINT, signal_handler)

    if args.config:
        config = load_yaml(args.config)
    else:
        config = load_yaml("config.yml")
    if args.json:
        data = load_json(args.data)
    else:
        data = load_yaml(args.data)

    run_questionaire(data)
