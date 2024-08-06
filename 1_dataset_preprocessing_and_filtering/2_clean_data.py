from DocCleaner import DocCleaner
import os
import pandas as pd
import tqdm

data_folder = str(input('insert the data folder path: '))
cleaned_data_folder = str(input('where do you want to save the cleaned data? '))

if not data_folder.endswith('/'):
    data_folder += '/'
print(data_folder)

data_files = [file for file in os.listdir(data_folder) if file.endswith('.csv')]

for filename in tqdm.tqdm(data_files[:2]):
    path = data_folder + filename
    print('analyzing file:', path)
    df = pd.read_csv(path, index_col=0)

    all_functions = []
    all_doc = []
    all_cleaned_doc = []
    all_doc_pattern = []
    for i in tqdm.tqdm(range(len(df))):
        doc = df.iloc[i]['doc']
        cleaner = DocCleaner(doc)
        cleaner.clean_doc()
        if cleaner.is_to_discard:
            continue

        all_doc.append(doc)
        all_cleaned_doc.append(cleaner.processed_doc)

        if len(cleaner.pattern) >= 3:
            print(doc)
            print('\n' + str(cleaner.pattern) + '\n')
            print(cleaner.processed_doc)
            print('-----------------------------')
        all_doc_pattern.append(cleaner.pattern)
        all_functions.append(df.iloc[i]['processed_function'])


    print('saving data...')
    df_processed = pd.DataFrame({
        'function' : all_functions,
        'doc' : all_doc,
        'cleaned_doc' : all_cleaned_doc,
        'pattern' : all_doc_pattern,
    })

    print('all starting functions:', len(df))
    print('accepted functions:', len(df_processed))
    df_processed.drop_duplicates(['function', 'cleaned_doc'], inplace=True)
    print('without duplicates:', len(df_processed))

    if not cleaned_data_folder.endswith('/'):
        cleaned_data_folder += '/'
    print('saving data (without duplicates) in:', cleaned_data_folder)
    
    df_processed.drop_duplicates(['function', 'cleaned_doc']).to_csv(cleaned_data_folder + filename + '.csv')