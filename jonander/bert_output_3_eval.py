import json
from argparse import ArgumentParser

def write_to_file(output_path, curr_span, curr_qid, curr_followup, curr_yesno):
    with open(output_path, 'a+', encoding='utf-8', errors='ignore') as output:
        output.write('{"best_span_str": [')
        for span in curr_span[:-1]:
            output.write('"' + span.replace('"', '\\"') + '",')
        output.write('"' + curr_span[-1].replace('"', '\\"') + '"], "qid": [')
        for qid in curr_qid[:-1]:
            output.write('"' + qid + '",')
        output.write('"' + curr_qid[-1] + '"], "yesno": [')
        for yesno in curr_yesno[:-1]:
            output.write('"' + yesno + '",')
        output.write('"' + curr_yesno[-1] + '"], "followup": [')
        for followup in curr_followup[:-1]:
            output.write('"' + followup + '",')
        output.write('"' + curr_followup[-1] + '"]}\n')

if __name__=='__main__':
    parser = ArgumentParser()
    parser.add_argument("--bert_model_output", type=str, required=True, help='file containing the output of the bert model')
    parser.add_argument("--output_path", type=str, required=True, help='Path for the QuAC evaluation script input')
    args = parser.parse_args()
    
    model_output = json.load(open(args.bert_model_output))
        
    curr_span = []
    curr_qid = []
    curr_followup = []
    curr_yesno = []
    prev_diag = ''
    for i, question in enumerate(model_output):
        curr_diag = question.split('#')[0]
        #write previous dialogue information 
        if curr_diag != prev_diag and i!=0:
            write_to_file(args.output_path,curr_span, curr_qid, curr_followup, curr_yesno)
            curr_span = []
            curr_qid = []
            curr_followup = []
            curr_yesno = []
        #Just get the best prediction
        for predictions in model_output[question]:
            ####
            if predictions['text'] == "":
                predictions['text'] = "CANNOTANSWER"
            ####
            curr_span.append(predictions['text'])
            curr_qid.append(question)
            ####
            curr_followup.append('x')
            curr_yesno.append('x')
            ####
            prev_diag = curr_diag
            break
    write_to_file(args.output_path, curr_span, curr_qid, curr_followup, curr_yesno)
