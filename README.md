# Quality In, Quality Out: Investigating Training Data’s Role in AI Code Generation

This repository is the replication package of the work "Quality In, Quality Out: Investigating Training Data’s Role in AI Code Generation". It contains the entire pipeline of code, datasets and results to replicate our experiments. 

## 1. Dataset preprocessing and filtering  

The ``1_dataset_preprocessing_and_filtering`` folder contains the scripts to preprocess and filter the ~24M Python files downloaded from [*The Stack dataset*](https://huggingface.co/datasets/bigcode/the-stack), resulting in the 5,516,412 final pairs of \<docstring + signature, code\>. Specifically: 

*
*
*

All the processed data can be found on Zenodo at the following link: [datasets](https://zenodo.org/doi/10.5281/zenodo.12773307). The *datasets.zip* file contains: (i) the original ~4.4M training set obtained by preprocessing and filtering The Stack (*full_data_training_set.json*); (ii) the cleaned ~4.2 training set (i.e., from which we removed low-quality and syntactically incorrect functions using Semgrep, as described in [**3. Detection of quality issues**](#3.-detection-of-quality-issues)) (*clean_training_set.json*); (iii) the ~551k validation and test sets also obtained by preprocessing and filtering The Stack (*validation_set.json*, *test_set.json*).

## 2. Model training and inference 

The ``2_training_and_inference`` folder contains the code to perform the fine-tuning and inference for DeepSeek-Coder-1.3B and evaluate its performance in code generation using *Exact Match (EM)* accuracy and *CrystalBLEU* score. Specifically:

* ``requirements.txt`` lists all the required packages, which can be installed with the following command: ```pip install -r requirements.txt```
* Use the ``run_finetuning_and_eval.sh`` script to fine-tune DeepSeek-Coder-1.3B, specifying the ``TRAIN_PATH``, ``EVAL_PATH``, ``OUTPUT_PATH``. 
* Use the ``finetune_and_eval_deepseek.py`` script to generate and automatically evaluate the predictions with EM and CrystalBLEU scores. 

The folder also contains the graphs of the evaluation loss curve for both DeepSeek-Coder full (DSCf) and DeepSeek-Coder cleaned (DSCc) models. 
All the trained models checkpoints (for each model we stored the final/best chekpoint only) are available on Zenodo at the following link: [models chekpoints](https://zenodo.org/doi/10.5281/zenodo.12773307). The *models chekpoints.zip* file contains: (i) the checkpoint for *DSC_full* (DSCf), i.e., the model trained on the full training set (*full_data_training_set.json*); and (ii) the checkpoint for *DSC_cleaned* (DSCc), i.e., the model trained on the cleaned version of the training set (*clean_training_set.json*).

All models predictions are available on Zenodo at the following link: [models predictions](https://zenodo.org/doi/10.5281/zenodo.12773307). The *models predictions.zip* file contains: the functions predicted by the two fine-tuned models (i.e., DSCf and DSCc) and by the pre-trained only (PTO) model when tested (i) on our test set (*our_testset_predictions*); and (ii) on the [HumanEval benchmark](https://github.com/openai/human-eval) (*humaneval_predictions*).

## 3. Detection of quality issues

The ``3_quality_issues_detection`` folder contains the code to detect and process the quality issues in both the training set and the model's predictions using the Semgrep static analyzer. It also contains the code to remove the found low-quality functions from the training set, resulting in the *clean training set* also stored on Zenodo (*clean_training_set.json*).
The ``analyze_code.py`` script contains the complete list of Semgrep rules used in our study. 
***Important note:*** *Semgrep's list of rules varies over time, thereby experiments may produce slightly different results.*

* Install Semgrep by running the following command: ```python3 -m pip install semgrep```
* Run ```semgrep login``` to create your account and login to Semgrep to be able to use all the detection rules. Further details on [Semgrep](https://github.com/semgrep/semgrep).
* To run Semgrep on the Python functions use the following command: ```python3 analyze_code.py <training_set/predictions>.json```
* The training set/predictions are processed in batches of 20000 samples and the result of the analysis will be a set of json files containing all the detected issues. To process the results and extract the information on low-quality and syntactically incorrect functions use: ```python3 process_results.py <training_set/predictions>_semgrep_result_batch <number_of_batches>```
* The result of the analysis will be (i) a report of the detected code quality issues; (ii) the list of training set indexes containing low-quality functions and syntactically incorrect functions.
* To remove all low-quality and incorrect functions from the training set, use the following command: ```python3 clean_dataset.py <training_set>.json```

The ``quality_issues_results`` folder contains the results of our analysis, both in terms of Semgrep reports on quality issues and full list of low-quality and syntactically incorrect functions, for the training set, pre-trained only (PTO), DeepSeek-Coder full (DSCf) and DeepSeek-Coder cleaned (DSCc) predictions.

The ``semgrep_manual_validation`` folder contains the results of the manual validation of a random sample of 400 quality issues identified by Semgrep. Each file reports the affected function, the issue category, the defective line(s), the message outputted by Semgrep and the *correct/incorrect* classification. 

## 4. Statistical analysis

The ``4_statistical-analysis`` folder contains the script and data to replicate all the statistical tests performed in our study.
