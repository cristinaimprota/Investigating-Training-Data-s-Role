from datasets import load_dataset
from tqdm import tqdm
import lizard
import pandas as pd
import sys

# https://huggingface.co/datasets/bigcode/the-stack
access_token = str(input('insert your access token: ')) # <- access token for the stack dataset
data_folder = str(input('where do you want to save the extracted data? ')) # 'data/functions'

def search_function(file_name):
    liz = lizard.analyze_file(file_name)
    functions_info = []
    for liz_elem in liz.function_list:
        functions_info.append([liz_elem.long_name, liz_elem.start_line, liz_elem.end_line])
    return functions_info

def save_content_in_file(content, file_name):
    f = open(file_name, 'w')
    f.write(content)
    f.close()

def find_and_remove_doc(function_lines):
    start_doc_line, end_doc_line = 0, 0
    flag_signature_end = False
    flag_comment = False
    for i in range(len(function_lines)):
        line = function_lines[i]
        if not flag_signature_end:
            if line.strip().endswith(':'):
                flag_signature_end = True
            continue

        if not flag_comment and line.strip() != '' and not line.strip().startswith('"""'):
            # missing doc
            break
        
        if not flag_comment and line.strip().startswith('"""'):
                flag_comment = True
                start_doc_line = i
                if line.strip().endswith('"""') and len(line.strip()) > 3:
                    end_doc_line = i
                    break
        elif flag_comment and (line.strip().startswith('"""') or line.strip().endswith('"""')):
                end_doc_line = i
                break
            
    if start_doc_line != 0 and end_doc_line != 0:
        funcion_without_doc = function_lines[:start_doc_line] + function_lines[end_doc_line+1:]
        return funcion_without_doc, function_lines[start_doc_line : end_doc_line+1]
    return [], []

def clean_function(function_lines):
    function_without_comments_lines = []
    for line in function_lines:
        if line.strip().startswith('#') or line.strip() == '':
            continue
        function_without_comments_lines.append(line)
    return function_without_comments_lines
    

def main():
    print('loading dataset...')
    ds = load_dataset("bigcode/the-stack",  data_dir="data/python", split="train", streaming=False, token=access_token, ignore_verifications=True, keep_in_memory=False)

    all_functions = []
    all_cleaned_functions = []
    all_docs = []
    max_sample = 50000
    count_samples = 0
    file_number = 1

    for sample in tqdm(iter(ds)): 
        count_samples += 1
        file_name = 'file.py'
        save_content_in_file(sample['content'], file_name)

        # search for functions
        functions_info = search_function(file_name)
        if len(functions_info) == 0:
            continue 

        file_lines = [line for line in open(file_name, 'r')]
        for elem in functions_info:
            # function_name = elem[0]
            current_function_lines = file_lines[elem[1]-1 : elem[2]] # start_function_line, end_function_line
            current_function_without_doc, current_doc_lines = find_and_remove_doc(current_function_lines)
            if len(current_doc_lines) == 0:
                continue
            else:
                all_functions.append(''.join(current_function_lines))
                all_cleaned_functions.append(''.join(clean_function(current_function_without_doc)))
                all_docs.append(''.join(current_doc_lines))
            
        if count_samples >= max_sample:

            print('saving file number:', file_number)
            print('functions found:', len(all_functions))
            print('count:', count_samples)

            pd.DataFrame({
                'function' : all_functions,
                'processed_function' : all_cleaned_functions,
                'doc' : all_docs
            }).to_csv(data_folder + '/data_' + str(file_number) + '.csv')

            all_functions = []
            all_cleaned_functions = []
            all_docs = []
            count_samples = 0
            file_number += 1
        

    print('functions found:', len(all_functions))
    pd.DataFrame({
        'function' : all_functions,
        'processed_function' : all_cleaned_functions,
        'doc' : all_docs
    }).to_csv(data_folder + '/data_' + str(file_number) + '.csv')
    sys.exit()


if __name__ == "__main__":
    main()