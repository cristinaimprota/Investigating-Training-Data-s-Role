import pandas as pd
import subprocess
from tqdm import tqdm

def save_content_in_file(content, file_name):
    f = open(file_name, 'w')
    f.write(content)
    f.close()



data_path = '../data/data_x.csv'
temp_filename = 'code_x.txt'
format_file = './format_x.sh'
output_file = '../data/formatted_data_x.csv'


def write_format_file(format_file):
    f = open(format_file, 'w')
    f.write('#!/usr/bin/bash\nblack ' + temp_filename)
    f.close()
    subprocess.run(['chmod +x ' + format_file], shell=True)

print('writing format file...')
write_format_file(format_file)

print('reading data...')
df = pd.read_csv(data_path, index_col=0)
print('data:', len(df))

functions = df.function.to_list()
signatures = df.signature.to_list()
docs = df.doc.to_list()

signatures_ = []
docs_ = []
functions_ = []
input_with_signature = []
for i in tqdm(range(len(functions))):
    function = functions[i]
    
    save_content_in_file(function, temp_filename)
    subprocess.run(format_file)
    formatted_function_lines = [line for line in open(temp_filename, 'r') if line.strip() != '']
    formatted_function = ''.join(formatted_function_lines)

    signatures_.append(signatures[i])
    functions_.append(formatted_function)
    docs_.append(docs[i])
    input_with_signature.append('def ' + signatures[i] + ':\n"""\n' + docs[i] + '\n"""')

print('cleaned data:', len(signatures_))
print('saving data...')
pd.DataFrame({
    'function' : functions_,
    'signature' : signatures_,
    'doc' : docs_,
    'input_with_signature' : input_with_signature
}).to_csv(output_file)
