import pandas as pd
from tqdm import tqdm

print('reading data...')
df = pd.read_csv('./data/all_formatted_data.csv', index_col=0) 
print('starting data:', len(df))


print('reading data...')
df = pd.read_csv('./data/final_formatted_cleaned_data.csv', index_col=0) 
print('final data:', len(df))



# functions = df.function.to_list()
# signatures = df.signature.to_list()
# docs = df.doc.to_list()


# def check_signature_function(function):
#     count_open_parenthesis = 1
#     count_closed_parentesis = 0
#     first_open_parenthesis_index = function.index('(')
#     j = first_open_parenthesis_index
#     try:
#         while True:
#             j += 1
#             if function[j] == ')':
#                 count_closed_parentesis += 1
#                 if count_open_parenthesis == count_closed_parentesis:
#                     # fine signature (senza freccina!!)
#                     end_part_signature_index = j
#                     break
#             if function[j] == '(':
#                 count_open_parenthesis += 1
#     except:
#         print('--------------------------------------')
#         print('ERROR!')
#         print(function)
#         print('--------------------------------------')
#         return 'error'
    
#     # check if there is the arrow "->"
#     if function[end_part_signature_index + 1] == ':' or function[end_part_signature_index + 2] == ':':
#         # caso normale
#         return function[: end_part_signature_index + 2]
        
#     elif function[end_part_signature_index + 2 : end_part_signature_index + 4] == '->':
#         # caso frecicna
#         signature_ = function[: end_part_signature_index + 1]
#         second_part = function[end_part_signature_index + 1:]
#         signature_ += second_part[:second_part.index(':') + 2]
#         return signature_
#     else:
#         print('--------------------------------------')
#         print('what?')
#         print(function)
#         print('--------------------------------------')
#         return 'error'
        


# functions_ = []
# docs_ = []
# fixed_signature = []
# fixed_input_with_signature = []
# for i in tqdm(range(len(functions))):
#     function = functions[i]

#     if function.startswith('def _emoji_normalize('):
#         print('REMOVED FUNCTION', i)
#         print(function[:250])
#         continue


#     function_lines = function.split('\n')
#     cleaned_function_lines = []
#     for line in function_lines:
#         if '#' in line:
#             line = line[:line.index('#')]
#         cleaned_function_lines.append(line)
#     function = '\n'.join(cleaned_function_lines)

#     signature = check_signature_function(function)
#     if signature == 'error':
#         continue
    
#     functions_.append(function)
#     docs_.append(docs[i])
#     fixed_signature.append(signature)    
#     fixed_input_with_signature.append(signature + '\n"""\n' + docs[i] + '\n"""')

#     # print(signature)
#     # print(fixed_input_with_signature[-1])
#     # print('---------------------------------------')
    

# df = pd.DataFrame({
#     'function' : functions_,
#     'signature' : fixed_signature,
#     'doc' : docs_,
#     'input' : fixed_input_with_signature
# })

# print('fixed data:', len(df))
# df.to_csv('./data/final_formatted_cleaned_data.csv')