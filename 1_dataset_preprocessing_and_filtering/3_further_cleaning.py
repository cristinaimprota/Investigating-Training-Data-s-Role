import pandas as pd
import tqdm
import re 
import os
from functools import reduce

## Put all files together

data_files = [file for file in os.listdir('./data/processed_functions') if file.endswith('.csv')]
df = []
for filename in tqdm.tqdm(data_files):
    path = './data/processed_functions/' + filename
    print('analyzing file:', path)
    df.append(pd.read_csv(path, index_col=0))

print('concatenating dfs...')
df = pd.concat(df)
print('data:', len(df))

print('removing duplicates...')
df.drop_duplicates(['function', 'cleaned_doc'], inplace=True)
print('data without duplicates:', len(df))
df.to_csv('./data/processed_all.csv')

#######################################################################################################

## Remove docs with links

# print('reading data...')
# data_path = './data/processed_all.csv'
# df = pd.read_csv(data_path, index_col=0)
# print('data:', len(df))

df.reset_index(drop=True, inplace=True)
all_docs = df.cleaned_doc.to_list()
print(len(all_docs))

indexes_to_remove = []
for i in tqdm.tqdm(range(len(all_docs))):
    doc = all_docs[i]
    if 'http' in doc:
       indexes_to_remove.append(i)

df.drop(indexes_to_remove, inplace=True)
print('docs with links:', len(indexes_to_remove))
print('remaining data:', len(df))
print('saving data...')
df.to_csv('./data/processed_without_links.csv')

#######################################################################################################

## Further clean data

def clean_note(doc):
    doc_lines = doc.split('\n')
    cleaned_doc_lines = []
    for line in doc_lines:
        if '> **NOTE' in line:
            break
        cleaned_doc_lines.append(line)
    return '\n'.join(cleaned_doc_lines)

def clean_noqa(doc):
    doc_lines = doc.split('\n')
    cleaned_doc_lines = []
    for line in doc_lines:
        if '# noqa' in line:
            line = line[:line.index('# noqa')-1]
        if '#noqa' in line:
            line = line[:line.index('#noqa')-1]
        cleaned_doc_lines.append(line)
    return '\n'.join(cleaned_doc_lines)

def clean_see(doc):
    doc_lines = doc.split('\n')
    cleaned_doc_lines = []
    for line in doc_lines:
        if '**see ' in line.lower():
            break
        cleaned_doc_lines.append(line)
    return '\n'.join(cleaned_doc_lines)

def check_last_line(doc_lines):
    last_line = doc_lines[-1]
    if last_line.lower() == 'see its docstring for more information.' or\
        (last_line.lower().startswith('see') and 'info' in last_line.lower()):
        return '\n'.join(doc_lines[:-1])
    return '\n'.join(doc_lines)

def check_see_info(doc_lines):
    cleaned_doc_lines = []
    for line in doc_lines:
        if line == 'For information about managing receipt rule sets, see the Amazon SES Developer Guide .':
            continue
        cleaned_doc_lines.append(line)
    return '\n'.join(cleaned_doc_lines)

def clean_purpose(doc):
    cleaned_doc_lines = []
    doc_lines = doc.split('\n')
    for line in doc_lines:
        if line.lower() == '<purpose>':
            continue
        if line.lower() == '<arguments>' or  line.lower() == '<exceptions>' or\
            line.lower() == '<side fffects>' or line.lower() == '<returns>':
            break
        cleaned_doc_lines.append(line)
    return '\n'.join(cleaned_doc_lines)

def clean_tags(doc):
    doc.replace('<remarks>', '').replace('</remarks>', '').replace('<summary>', '').replace('</summary>', '')
    cleaned_doc_lines = []
    doc_lines = doc.split('\n')
    for line in doc_lines:
        if line.strip() == '':
            continue
        if line.lower() == '<summary>' or line.lower() == '</summary>':
            continue
        if line.lower() == '<remarks>' or line.lower() == '</remarks>':
            continue
        if line.lower() == '<figure class="notice">' or line.lower() == '</figure>':
            continue
        if line.lower() == '<note>':
            continue
        if line.lower() == '<p/>':
            continue
        if line.lower() == '<algorithm>':
            continue
        if line.lower() == '<blockquote class="info">':
            break
        if line.lower() == '<tip>':
            break
        cleaned_doc_lines.append(line)
    return '\n'.join(cleaned_doc_lines)
    
# print('reading data...')
# data_path = './data/processed_without_links.csv'
# df = pd.read_csv(data_path, index_col=0)
# print(df.columns)
# print('data:', len(df))

df.reset_index(drop=True, inplace=True)
all_docs = df.cleaned_doc.to_list()

# print(len(all_docs))

docs = []
cleaned_docs = []
function = []

for i in tqdm.tqdm(range(len(all_docs))):
    doc = df.iloc[i]['cleaned_doc']
    flag = False

    if '> **NOTE' in doc:
        doc = clean_note(doc)
        flag=True

    if '#noqa' in doc or '# noqa':
        doc = clean_noqa(doc)
        flag = True
    
    if '**see ' in doc.lower():
        doc = clean_see(doc)
        flag=True
    
    if '<purpose>' in doc.lower() or '<purspose>' in doc.lower():
        doc = clean_purpose(doc)
        flag=True
    
    doc_lines = doc.split('\n')
    lines_to_clean = [line for line in doc_lines if (line.startswith('<') and line.endswith('>'))]
    if len(lines_to_clean) > 1:
        doc = clean_tags(doc)
        flag = True

    doc_lines = doc.split('\n')
    if len([1 for line in doc_lines if line.startswith('<')]) == len(doc_lines):
        continue
    
    doc = check_last_line(doc_lines)
    doc = check_see_info(doc_lines)
    
    if len(doc.split()) < 10:
        # doc is too short
        continue
    
    docs.append(df.iloc[i]['doc'])
    function.append(df.iloc[i]['function'])
    if flag:
        cleaned_docs.append(doc)
    else:
        cleaned_docs.append(df.iloc[i]['cleaned_doc'])

df = pd.DataFrame({
    'function' : function,
    'doc' : docs,
    'cleaned_doc' : cleaned_docs,
})
df.to_csv('./data/cleaned_docs_and_functioncs.csv')

######################################################################################################

## remove test functions

# print('reading data...')
# data_path = './data/cleaned_docs.csv'
# df = pd.read_csv(data_path, index_col=0)
# print('data:', len(df))

indexes_to_remove = []
for i in tqdm.tqdm(range(len(df))):
    function = df.iloc[i]['function']
    first_line = function.split('\n')[0]
    if 'test' in first_line.lower():
        indexes_to_remove.append(i)

df.drop(indexes_to_remove, inplace=True)
df.reset_index(drop=True, inplace=True)

print('test functions:', len(indexes_to_remove))
print('remaining data:', len(df))
print('saving data...')
df.to_csv('./data/cleaned_docs_and_functioncs.csv')

######################################################################################################

# more cleaning

def clean_note(doc):
    doc_lines = doc.split('\n')
    cleaned_doc_lines = []
    for line in doc_lines:
        if line.lower().startswith('*note*'):
            break
        cleaned_doc_lines.append(line)
    return '\n'.join(cleaned_doc_lines)

def clean_param(doc):
    doc_lines = doc.split('\n')
    cleaned_doc_lines = []
    for line in doc_lines:
        if line.startswith('@param'):
            continue
        cleaned_doc_lines.append(line)
    return '\n'.join(cleaned_doc_lines)

# print('reading data...')
# data_path = './data/cleaned_docs_and_functioncs.csv'
# df = pd.read_csv(data_path, index_col=0)
# print('data:', len(df))

df.reset_index(drop=True, inplace=True)

docs = []
cleaned_docs = []
function = []

docs_to_clean = []
for i in tqdm.tqdm(range(len(df))):
    doc = df.iloc[i]['cleaned_doc']
    flag = False

    while True:
        if doc.startswith('"') or doc.startswith('*'):
            doc = doc[1:].strip()
            flag = True
        else:
            break
    if '! @brief' in doc:
        doc = doc.replace('! @brief', '').strip()
        flag = True
    if doc.startswith('***Property***'):
        doc = doc.replace('***Property***', '').strip()
        flag = True
    if doc.startswith('! @return'):
        doc = doc[3:].strip()
        flag = True
    if doc.startswith('____') and doc.endswith('____'):
        doc = doc.replace('____', '')
        flag = True
    if len(doc.split('\n')) == 1 and doc.startswith('[') and doc.endswith(']'):
        print(doc)
        doc = doc[1:-1].strip()
        flag = True
    if doc.startswith('(Updatable)'):
        doc = doc.replace('(Updatable)', '').strip()
        flag = True
    if doc.startswith('(Optional)'):
        doc = doc.replace('(Optional)', '').strip()
        flag = True
    if doc.startswith('(Read Only)'):
        doc = doc.replace('(Read Only)', '').strip()
        flag = True
    if doc.startswith('(read only)'):
        doc = doc.replace('(read only)', '').strip()
        flag = True
    if doc.startswith('(Input Only)'):
        doc = doc.replace('(Input Only)', '').strip()
        flag = True
    if doc.startswith('(Private)'):
        doc = doc.replace('(Private)', '').strip()
        flag = True
    if doc.startswith('[summary]'):
        doc = doc.replace('[summary]', '').strip()
        flag = True
    if doc.startswith('[Preview Feature]'):
        doc = doc.replace('[Preview Feature]', '').strip()
        flag = True
    if doc.startswith('**(private)**'):
        doc = doc.replace('**(private)**', '').strip()
        flag = True
    if doc.startswith('**Beta Feature**'):
        doc = doc.replace('**Beta Feature**', '').strip()
        flag = True
    if doc.startswith('(Computed)'):
        doc = doc.replace('(Computed)', '').strip()
        flag = True
    
    if len([line for line in doc.split('\n') if line.startswith('|')]) == len(doc.split('\n')):
        doc = '\n'.join([line[1:].strip() for line in doc.split('\n')])
        flag = True
    
    if '*NOTE*' in doc:
        doc = clean_note(doc)
        flag = True
    
    if '@param' in doc:
        doc = clean_param(doc)
        flag = True
    
    if len(doc.split()) < 10:
        # doc is too short
        continue


    docs.append(df.iloc[i]['doc'])
    function.append(df.iloc[i]['function'])
    if flag:
        cleaned_docs.append(doc)
    else:
        cleaned_docs.append(df.iloc[i]['cleaned_doc'])

df = pd.DataFrame({
    'function' : function,
    'doc' : docs,
    'cleaned_doc' : cleaned_docs,
})
df.to_csv('./data/cleaned_docs_and_functioncs.csv')

######################################################################################################

def clean_param(doc):
    doc_lines = doc.split('\n')
    cleaned_doc_lines = []
    for line in doc_lines:
        if line.startswith('@param'):
            continue
        cleaned_doc_lines.append(line)
    return '\n'.join(cleaned_doc_lines)

df.reset_index(drop=True, inplace=True)

docs = []
cleaned_docs = []
function = []

docs_to_clean = []
for i in tqdm.tqdm(range(len(df))):
    doc = df.iloc[i]['cleaned_doc']
    flag = False

    while True:
        if len([line for line in doc.split('\n') if line.startswith('-')]) == len(doc.split('\n')):
            doc = '\n'.join([line[1:].strip() for line in doc.split('\n')])
            flag = True
        else:
            break

    while True:
        if len([line for line in doc.split('\n') if line.startswith('*')]) == len(doc.split('\n')):
            doc = '\n'.join([line[1:].strip() for line in doc.split('\n')])
            flag = True
        else:
            break
    
    if '@param' in doc:
        doc = clean_param(doc)
        flag = True
    
    if len(doc.split()) < 10:
        # doc is too short
        continue


    docs.append(df.iloc[i]['doc'])
    function.append(df.iloc[i]['function'])
    if flag:
        cleaned_docs.append(doc)
    else:
        cleaned_docs.append(df.iloc[i]['cleaned_doc'])

df = pd.DataFrame({
    'function' : function,
    'doc' : docs,
    'cleaned_doc' : cleaned_docs,
})
df.to_csv('./data/cleaned_docs_and_functioncs.csv')

######################################################################################################

def clean_note(doc):
    doc_lines = doc.split('\n')
    cleaned_doc_lines = []
    for line in doc_lines:
        if line.startswith('! NOTE ! '):
            break
        cleaned_doc_lines.append(line)
    return '\n'.join(cleaned_doc_lines)

def clean_doc(doc):
    doc_lines = doc.split('\n')
    cleaned_doc_lines = []
    for line in doc_lines:
        if line.startswith('\\brief'):
            line = line.replace('\\brief', '').strip()
        if line.startswith('\\remarks') or line.startswith('\sa') or line.startswith('\param') or line.startswith('\\return'):
            continue
        cleaned_doc_lines.append(line)
    return '\n'.join(cleaned_doc_lines)

# print('reading data...')
# data_path = './data/cleaned_docs_and_functioncs.csv'
# df = pd.read_csv(data_path, index_col=0)
# print('data:', len(df))

df.reset_index(drop=True, inplace=True)

docs = []
cleaned_docs = []
function = []

docs_to_clean = []
for i in tqdm.tqdm(range(len(df))):
    doc = df.iloc[i]['cleaned_doc']
    
    if '! NOTE ! ' in doc:
        doc = clean_note(doc)

    if doc.startswith("!!! Please read this completely. Otherwise you'll suck :( !!!"):
        doc = '\n'.join(doc.split('\n')[1:])
    
    if '\\brief' in doc or '\\remarks' in doc or '\sa' in doc or '\param' in doc or '\\return' in doc:
        doc = clean_doc(doc)

    
    if len(doc.split()) < 10:
        # doc is too short
        continue

    docs.append(df.iloc[i]['doc'])
    function.append(df.iloc[i]['function'])
    cleaned_docs.append(doc)


df = pd.DataFrame({
    'function' : function,
    'doc' : docs,
    'cleaned_doc' : cleaned_docs,
})
df.to_csv('./data/cleaned_docs_and_functioncs.csv')

######################################################################################################
import string

df = pd.read_csv(data_path, index_col=0)
print('data:', len(df))

df.reset_index(drop=True, inplace=True)

indexes_to_remove = []
for i in tqdm.tqdm(range(len(df))):
    doc = df.iloc[i]['cleaned_doc']
    
    count = 0
    for c in doc:
        if c in string.punctuation:
            count += 1
    if count > len(doc)/2:
        indexes_to_remove.append(i)
        continue

df.drop(indexes_to_remove, inplace=True)
df.reset_index(drop=True, inplace=True)
df.to_csv('./data/cleaned_docs_and_functioncs.csv')
print('remaining data:', len(df))
######################################################################################################
