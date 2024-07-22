from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re
import json
import time
from datasets import load_dataset
import csv
from output_similarity_metrics import *
from human_eval.data import write_jsonl

batch_eval=64
evaluate_humaneval=False
max_new_tokens=512

model_base_dir = ""
model_names = [""]
model_paths = [os.path.join(model_base_dir, model_name) for model_name in model_names]
# model_base_dir = ""
# model_names = ["baseline"]
# model_paths = ["deepseek-ai/deepseek-coder-1.3b-instruct"]


for model_id, model_path in enumerate(model_paths):

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.bfloat16, device_map="auto")
    print(f"Loaded model from {model_path}.")

    # def build_instruction_prompt(instruction: str):
    #     return '''{}'''.format(instruction)

    def build_instruction_prompt(instruction: str):
        return '''
You are an AI programming assistant, utilizing the DeepSeek Coder model, developed by DeepSeek Company, and you only answer questions related to computer science.
### Instruction:
{}
### Response:
'''.format(instruction.strip()).lstrip()
    
    if evaluate_humaneval:
        instruction_name='prompt'
        output_name='canonical_solution'
        examples = load_dataset("openai/openai_humaneval", split="test")
        dataset_name='humaneval'
        test_path=dataset_name
    else:
        instruction_name='instruction'
        output_name='output'
        test_path = "./test_set.json"
        examples = load_dataset('json', data_files=test_path, split="train")
        dataset_name='ours'

    prompts = [build_instruction_prompt(instruction) for instruction in examples[instruction_name]]
    snippets = [code for code in examples[output_name]]

    print(f"Samples loaded from {test_path}")

    json_name='predictions_{}_{}.json'.format(model_names[model_id], dataset_name)
    json_name_both='predictions_references_{}_{}.json'.format(model_names[model_id], dataset_name)
    log_name='log_{}_{}.txt'.format(model_names[model_id], dataset_name)
    csv_name = 'batch_predictions_{}_{}.csv'.format(model_names[model_id], dataset_name)

    with open(csv_name, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Predictions'])

    def generate_responses(prompts, batch_size=batch_eval):
        predictions = []
        print(f"Total samples: {len(prompts)}")
        start_total_time = time.time()
        for i in range(0, len(prompts), batch_size):
            start_time = time.time()
            print(f"Iteration: {i}")
            batch_prompts = prompts[i:i + batch_size]
            inputs = tokenizer(batch_prompts, return_tensors="pt", padding=True, truncation=True, max_length=1024).to(model.device)

            stop_id = tokenizer.convert_tokens_to_ids("<|EOT|>")
            outputs = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False, num_return_sequences=1, pad_token_id=stop_id, eos_token_id=stop_id).to(model.device)
                
            batch_predictions = []
            for j, output in enumerate(outputs):
                input_length = inputs['input_ids'][j].shape[0]
                response = tokenizer.decode(output[input_length:], skip_special_tokens=True)
                predictions.append(response)
                batch_predictions.append(response)

            with open(csv_name, 'a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                for prediction in batch_predictions:
                    csv_writer.writerow([prediction])
                    csv_writer.writerow(["------------"])

            elapsed_time = time.time() - start_time 
            total_elapsed_time = time.time() - start_total_time 
            print(f"Batch {i // batch_size + 1}/{len(prompts) // batch_size + 1} processed in {elapsed_time:.2f} seconds")
            print(f"Total elapsed time: {total_elapsed_time:.2f} seconds")

        return predictions

    predictions = generate_responses(prompts)

    for j in range(0,10):
        print(f"Sample:\n{j}\n")
        print(f"Instruction:\n{examples[instruction_name][j]}\n")
        print(f"Prediction:\n{predictions[j]}\n")
        print(f"Reference:\n{snippets[j]}\n")

    if evaluate_humaneval:
        jsonl_name='predictions_{}_{}.jsonl'.format(model_names[model_id], dataset_name)
        samples = []
        for i, ex in enumerate(examples):
            samples.append(dict(task_id=ex['task_id'], completion=predictions[i]))

        write_jsonl(jsonl_name, samples)

    else:

        with open(json_name, 'w') as file:
            json.dump(predictions, file)

        samples = []
        for pred, snip in zip(predictions, snippets):
            samples.append(dict(prediction=pred, reference=snip))
        with open(json_name_both, 'w') as file_both:
            json.dump(samples, file_both)

    results = []

    print(f"Number of predictions: {len(predictions)}")
    print(f"Number of references: {len(snippets)}")

    # Calculate evaluation metrics
    results.append(calc_crystalBLEU(predictions, snippets, True))
    results.append(calc_EM(predictions, snippets))

    with open(log_name, "w") as logfile:
        logfile.write(f"Total samples: {len(prompts)}\n")
        for res in results:
            logfile.write(f"{res}\n")

