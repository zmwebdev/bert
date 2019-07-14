import json
import argparse
import os

parser = argparse.ArgumentParser(description='SQuAD predictions 2 QuAC')
parser.add_argument('--file', default='predictions.json')
parser.add_argument('--out', default='predictions.quac.json')
args = parser.parse_args()

# {"loss": 4.697470664978027, "best_span_str": ["In May 1983, she married Nikos Karvelas, a composer, with whom she collaborated in 1975", "in November she gave birth to her daughter Sofia.", "CANNOTANSWER", "After their marriage, she started a close collaboration with Karvelas.", "CANNOTANSWER", "The lead single Pseftika (\"Fake\")", "CANNOTANSWER", "In 1986 I Epomeni Kinisi (\"The Next Move\") was released."], "qid": ["C_5ab583f64dbb47b995cf59328ea0af43_1_q#0", "C_5ab583f64dbb47b995cf59328ea0af43_1_q#1", "C_5ab583f64dbb47b995cf59328ea0af43_1_q#2", "C_5ab583f64dbb47b995cf59328ea0af43_1_q#3", "C_5ab583f64dbb47b995cf59328ea0af43_1_q#4", "C_5ab583f64dbb47b995cf59328ea0af43_1_q#5", "C_5ab583f64dbb47b995cf59328ea0af43_1_q#6", "C_5ab583f64dbb47b995cf59328ea0af43_1_q#7"], "yesno": ["x", "y", "x", "x", "x", "x", "x", "y"], "followup": ["y", "y", "n", "y", "n", "y", "n", "y"]}

data = []
with open(args.file) as json_data:
    d = json.load(json_data)
    id_old = ""
    line = {"loss":1, "best_span_str":[], "qid":[], "yesno":[], "followup":[]}
    for key, value in d.items():
        id_new = key[0:key.find("_q#")]
        if id_old == "":
            id_old = id_new
        
        if id_old != id_new:
            data.append(line)
            id_old = id_new
            line = {"loss":1, "best_span_str":[], "qid":[], "yesno":[], "followup":[]}

        line["best_span_str"].append(value)
        line["qid"].append(key)
        line["yesno"].append("x")
        line["followup"].append("o")

    # append the last
    data.append(line)

# fitxategia reset
open(args.out, 'w').close()

# append
with open(args.out, mode='a', encoding='utf-8') as f:
    for l in data:
        json.dump(l, f)
        f.write(os.linesep)