import pandas as pd
import tqdm

print('reading data...')
data_path = './data/cleaned_docs_and_functioncs.csv'
df = pd.read_csv(data_path, index_col=0)
df.reset_index(drop=True, inplace=True)
print('data:', len(df))

functions = df.function.to_list()
docs = df.doc.to_list()

cleaned_docs = []
cleaned_functions = []
doc_len = []
function_len = []

count = 0
for i in tqdm.tqdm(range(len(docs))):
    doc = docs[i]
    function = functions[i]

    function_lines = function.split('\n')
    first_line = function_lines[0]
    if first_line.startswith(' '):
        count = 0
        while True:
            count += 1
            if first_line[count] != ' ':
                break
        cleaned_function_lines = []
        for line in function_lines:
            cleaned_function_lines.append(line[count:])
        function = '\n'.join(cleaned_function_lines)

print('cleaned data:', len(cleaned_functions))
pd.DataFrame({
    'doc' : cleaned_docs,
    'function' : cleaned_functions
}).to_csv('./data/cleaned_data.csv')
