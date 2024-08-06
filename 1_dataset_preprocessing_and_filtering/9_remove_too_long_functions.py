import pandas as pd
from tqdm import tqdm
from statistics import mean, median

MAX_FUNCTION_CHAR = 800 


print('reading data...')
data_path = './data/final_formatted_cleaned_data.csv'
df = pd.read_csv(data_path, index_col=0)
df.reset_index(drop=True, inplace=True)
print('data:', len(df))
print(df.columns)

functions = df.function.to_list()
indexes_to_remove = []
for i in tqdm(range(len(functions))):
    processed_function = functions[i].replace(' ', '').replace('\n', '').replace('\t', '')
    if len(processed_function) > MAX_FUNCTION_CHAR:
        indexes_to_remove.append(i)

print('too long functions:', len(indexes_to_remove))
print('good data:', len(df) - len(indexes_to_remove))

df.drop(indexes_to_remove, inplace=True)
print('final data:', len(df))

df.drop_duplicates(inplace=True)
print('without duplicates:', len(df))
df.reset_index(drop=True, inplace=True)

print('final data:', len(df))
df.to_csv('./data/final_formatted_cleaned_data.csv')