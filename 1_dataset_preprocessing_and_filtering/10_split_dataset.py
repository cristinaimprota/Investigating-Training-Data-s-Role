import pandas as pd
import json

def convert_data_in_json(data, filename):
    data_json = []
    for i in range(len(data)):
        data_json.append({
            'instruction' : data.iloc[i]['instruction'],
            'output' : data.iloc[i]['output']
        })

    with open('./data/' + filename, 'w') as jsonfile:
        json.dump(data_json, jsonfile)

################################################################################################
print('reading data...')
data_path = './data/final_formatted_cleaned_data.csv'
df = pd.read_csv(data_path, index_col=0)
print('data:', len(df))

df.rename(columns={"function": "output", "input": "instruction"}, inplace=True)
df.drop(['doc', 'signature'], axis=1, inplace=True)
df.reset_index(drop=True, inplace=True)

outputs = df.output.to_list()
instructions = df.instruction.to_list()

outputs_ = [elem.replace(' ', '').replace('\n', '').replace('\t', '') for elem in outputs]
instructions_ = [elem.replace(' ', '').replace('\n', '').replace('\t', '') for elem in instructions]

df['outputs_'] = outputs_
df['instructions_'] = instructions_

df.drop_duplicates(subset=['outputs_', 'instructions_'], inplace=True)
df.drop(['outputs_', 'instructions_'], axis=1, inplace=True)
df.reset_index(drop=True, inplace=True)
print('data:', len(df))

df.to_csv('./data/final_data.csv')
################################################################################################

training_set_size = int(len(df)*0.8) + 1
validation_set_size = int((len(df) - training_set_size)/2)
test_set_size = len(df) - training_set_size - validation_set_size

print()
print('training set size:', training_set_size)
print('validation set size:', validation_set_size)
print('test set size:', test_set_size)
print()

# split dataset
training_set = df.sample(training_set_size, random_state=42)
df.drop(training_set.index, inplace=True)
training_set.reset_index(drop=True, inplace=True)
df.reset_index(drop=True, inplace=True)
training_set.to_csv('./data/training.csv')

validation_set = df.sample(validation_set_size, random_state=42)
df.drop(validation_set.index, inplace=True)
validation_set.reset_index(drop=True, inplace=True)
df.reset_index(drop=True, inplace=True)
validation_set.to_csv('./data/validation.csv')

test_set = df
test_set.reset_index(drop=True, inplace=True)
test_set.to_csv('./data/test.csv')

print('training set:', len(training_set))
print('validation set:', len(validation_set))
print('test set:', len(test_set))


convert_data_in_json(training_set, 'training_set.json')
convert_data_in_json(validation_set, 'validation_set.json')
convert_data_in_json(test_set, 'test_set.json')



