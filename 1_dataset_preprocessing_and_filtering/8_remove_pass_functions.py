import pandas as pd
from tqdm import tqdm

print('reading data...')
data_path = './data/final_formatted_cleaned_data.csv'
df = pd.read_csv(data_path, index_col=0)
print('data:', len(df))

functions = df.function.to_list()
signatures = df.signature.to_list()
indexes_to_remove = []
for i in tqdm(range(len(functions))):
    function = functions[i]
    signature = signatures[i]

    function_without_signature = function.replace(signature, '')
    if function_without_signature.strip() == 'pass':
        indexes_to_remove.append(i)

df.drop(indexes_to_remove, inplace=True)
df.reset_index(drop=True, inplace=True)

print('final data:', len(df))
df.to_csv('./data/final_formatted_cleaned_data.csv')