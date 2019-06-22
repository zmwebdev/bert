import json
import argparse
import os

parser = argparse.ArgumentParser(description='QuAC to SQuAD')
parser.add_argument('--file', default='quac.json')
parser.add_argument('--out', default='squad.json')
args = parser.parse_args()


with open(args.file) as json_data:
    d = json.load(json_data)
    for l in d['data']:
        for q in l["paragraphs"][0]["qas"]:
            if q["orig_answer"]["text"] == "CANNOTANSWER":
                q["is_impossible"] = True
            else:
                q["is_impossible"] = False

with open(args.out, 'w') as outfile:
    json.dump(d, outfile)
