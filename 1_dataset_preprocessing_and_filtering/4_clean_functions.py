import pandas as pd
import py_compile
import tqdm

def clean_function(function):
    function_lines = function.split('\n')
    cleaned_function_lines = []
    for line in function_lines:
        if '#' in line:
            line = line[:line.index('#')]
        cleaned_function_lines.append(line)
    return '\n'.join(cleaned_function_lines)

def replace_tabs(text):
    index = text.index(text.strip()[0])
    text = text[:index].replace('    ', '<TAB>') + text[index:]
    text = text[:index].replace('\t', '<TAB>') + text[index:]
    return text

def remove_extra_tabs(method_lines):
    if method_lines[0].startswith('<TAB>'):
        count_ind = len(method_lines[0].split('<TAB>')) - 1
        for j in range(len(method_lines)):
            if method_lines[j].startswith('<TAB>'):
                method_lines[j] = method_lines[j][5 * count_ind:]
            else:
                method_lines[j] = method_lines[j]
    return method_lines

def save_content_in_file(content, file_name = 'file.py'):
    f = open(file_name, 'w')
    f.write(content)
    f.close()

def fix_indentation(function):
    # fix indentation using temporary <TAB>
    function_lines = function.split('\n')
    m_indent = [replace_tabs(line) for line in function_lines if line.strip() != '']
    m_indent = remove_extra_tabs(m_indent)
    return '\n'.join([line.replace('<TAB>', '    ') for line in m_indent])
    

print('reading data...')
data_path = './data/cleaned_docs_and_functioncs.csv'
df = pd.read_csv(data_path, index_col=0)
print('data:', len(df))


docs = []
functions = []
functions_to_clean = []
for i in tqdm.tqdm(range(len(df))):
    function = df.iloc[i]['function']
    # remove comments
    if '#' in function:
        function = clean_function(function)
    # fix indentation
    function = fix_indentation(function)

    save_content_in_file(function)
    # # check compilation error
    # py_compile.compile('file.py')

    docs.append(df.iloc[i]['cleaned_doc'])
    functions.append(df.iloc[i]['function'])

df = pd.DataFrame({
    'function' : functions,
    'doc' : docs
})
df.to_csv('./data/cleaned_docs_and_functioncs.csv')

######################################################################################################

df.reset_index(drop=True, inplace=True)

indexes_to_remove = []
for i in tqdm.tqdm(range(len(df))):
    function = df.iloc[i]['function']

    function_lines = function.strip().split('\n')
    if len(function_lines) == 1:
        indexes_to_remove.append(i)

df.drop(indexes_to_remove, inplace=True)
df.reset_index(drop=True, inplace=True)
df.to_csv('./data/cleaned_docs_and_functioncs.csv')

######################################################################################################