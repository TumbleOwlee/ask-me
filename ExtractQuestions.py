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

import argparse
import requests
import yaml
import json
import re

def load_yaml(filename):
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)
    return data

def dump_yaml(filename, data):
    with open(filename, 'w') as outfile:
        yaml.dump(data, outfile)

def load_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def dump_json(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def import_questions(config):
    table = {}
    for idx in config["general"]["id_mapping"]:
        body = {
            "feladatcsoport_id": idx,
            "fejezet_id": None,
            "tol": 0,
            "darab": config["import"]["max_questions_per_section"],
            "token": None
        }
        req = requests.post(config["import"]["url"], data=json.dumps(body), headers=config["import"]["headers"])
        if req:
            table[config["general"]["id_mapping"][idx]] = req.json()
        else:
            print("Request failed with status code: " + str(req.status_code))
    return table

def remove_html(str_input):
    str_output = str_input.replace("\n", " ")
    str_output = re.sub(r'<.+?>', " ", str_output)
    str_output = str_output.replace("&nbsp;", " ")
    str_output = re.sub(r'\s+', " ", str_output)
    str_output = str_output.replace('\r', '')
    str_output = str_output.replace('\n', ' ')
    return str_output.strip()

def format_questions(config, data):
    # For easier access
    cfg_choice_task = config["processing"]["field-mapping"]["choice-task"]
    cfg_mapping_task = config["processing"]["field-mapping"]["mapping-task"]
    
    # Create empty table
    formatted_data = {}

    # Parse all entries and reformat
    # over all sections
    for section in data:
        formatted_data[section] = []
        # over all questions
        for entry in data[section]:
            # Empty table for new question
            question = {}
            # Choice task
            if cfg_choice_task["option-list"]["options"] in entry:
                # Create question title
                question["question"] = remove_html(entry[cfg_choice_task["question-number"]]) + ": " + remove_html(entry[cfg_choice_task["question-text"]])
                question["type"] = "choice"
                if cfg_choice_task["description-tag"] in entry: 
                    # Description
                    question["description"] = remove_html(entry[cfg_choice_task["description-tag"]][cfg_choice_task["description-field"]])
                # Check for info text
                if cfg_choice_task["info-list"]["elements"] in entry:
                    # Get all info points 
                    question["info"] = []
                    opt_len = len(entry[cfg_choice_task["info-list"]["elements"]])
                    for num in range(1, opt_len+1):
                        for elem in entry[cfg_choice_task["info-list"]["elements"]]:
                            elem_num = remove_html(elem[cfg_choice_task["info-list"]["element-number"]])
                            if (elem_num == str(num)):
                                question["info"].append(elem_num + '. ' + remove_html(elem[cfg_choice_task["info-list"]["element-text"]]))
                    question["info"] = sorted(question["info"])
                # Get all selectable options
                question["options"] = []
                for opt in entry[cfg_choice_task["option-list"]["options"]]:
                    txt = remove_html(opt[cfg_choice_task["option-list"]["option-number"]]) + ". " + remove_html(opt[cfg_choice_task["option-list"]["option-text"]])
                    if opt[cfg_choice_task["option-list"]["option-correct"]] == 1:
                        question["solution"] = txt;
                    question["options"].append(txt)
                question["options"] = sorted(question["options"])
            # Mapping task
            elif cfg_mapping_task["tag"] in entry:
                question["type"] = "mapping"
                question["question"] = remove_html(entry[cfg_mapping_task["question-number"]]) + ": " + remove_html(entry[cfg_mapping_task["tag"]][cfg_mapping_task["question-name"]])
                question["options"] = []
                question["task"] = remove_html(entry[cfg_mapping_task["question-name"]])

                entryId = entry[cfg_mapping_task["id"]]
                for ass_opt in entry[cfg_mapping_task["tag"]][cfg_mapping_task["association"]]:
                    opt = remove_html(ass_opt[cfg_mapping_task["association-num"]]) + ". " + remove_html(ass_opt[cfg_mapping_task["association-text"]])
                    for tetel in ass_opt[cfg_mapping_task["association-opt"]]:
                        if tetel[cfg_mapping_task["id_target"]] == entryId:
                            question["solution"] = opt
                    if not (opt in question["options"]):
                        question["options"].append(opt)
                question["options"] = sorted(question["options"])
            formatted_data[section].append(question)
    return formatted_data

if __name__ == "__main__":
    print("Version 1.2")
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="optional path to custom config")
    parser.add_argument("--json", action="store_true", help="output as json instead of yaml")
    parser.add_argument("filename", help="output filename for yaml data")
    args = parser.parse_args()

    if args.config:
        config = load_yaml(args.config)
    else:
        config = load_yaml("config.yml")
    data = import_questions(config)
    data = format_questions(config, data)
    if args.json:
        dump_json(args.filename, data)
    else:
        dump_yaml(args.filename, data)
