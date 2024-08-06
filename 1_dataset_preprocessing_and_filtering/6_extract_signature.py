import pandas as pd
from tqdm import tqdm
import lizard


def save_content_in_file(content, file_name):
    f = open(file_name, 'w')
    f.write(content)
    f.close()

print('reading data...')
data_path = './data/cleaned_data.csv'
df = pd.read_csv(data_path, index_col=0)
df.reset_index(drop=True, inplace=True)
print('data:', len(df))

functions = df.function.to_list()
docs = df.doc.to_list()
signatures = []
cleaned_functions = []
cleaned_docs = []
input_with_signature = []
for i in tqdm(range(len(functions))):
    function = functions[i]
    file_name = 'file.py'
    save_content_in_file(function, file_name)

    liz = lizard.analyze_file(file_name)
    if len(liz.function_list) > 1:
        signature = liz.function_list[-1].long_name
    elif len(liz.function_list) == 0:
        continue
    else:
        signature = liz.function_list[0].long_name
    #############################################
    if len(signature) == '':
        continue
    signatures.append(signature)
    cleaned_functions.append(function)
    cleaned_docs.append(docs[i])
    input_with_signature.append('def ' + signature + ':\n"""\n' + docs[i] + '\n"""')


print('cleaned data:', len(signatures))
print('saving data...')
pd.DataFrame({
    'function' : cleaned_functions,
    'signature' : signatures,
    'doc' : cleaned_docs,
    'input_with_signature' : input_with_signature
}).to_csv('cleaned_data.csv')



    

