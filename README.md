# Quality In, Quality Out: Investigating Training Data’s Role in AI Code Generation

This repository is the replication package of the work "Quality In, Quality Out: Investigating Training Data’s Role in AI Code Generation". It contains the entire pipeline of code, datasets and results to replicate our experiments. 

## 1. Dataset cleaning 

The ``1_dataset_cleaning_pipeline`` folder contains the scripts to clean the ~24M Python files downloaded from [*The Stack*](https://huggingface.co/datasets/bigcode/the-stack), resulting in the 5,516,412 cleaned pairs of \<docstring + signature, code\>. Specifically: 

*
*
*

All the processed data can be found on Zenodo at the following link: [datasets](https://zenodo.org/records/12773308).

## 2. Model training and inference 

The ``2_training_and_inference`` contains the code to perform the fine-tuning and inference for DeepSeek-Coder-1.3B and evaluate its performance in code generation using *Exact Match* accuracy and *CrystalBLEU* score. Specifically:

* ``requirements.txt`` lists all the required packages, which can be installed with the following command: ```bash
pip install -r requirements.txt
```
* Use the ``run_finetuning_and_eval.sh`` script to fine-tune DeepSeek-Coder-1.3B, specifying the ``TRAIN_PATH``, ``EVAL_PATH``, ``OUTPUT_PATH`` and the appropriate hyper-parameters. 
* Use the ``finetune_and_eval_deepseek.py`` script to generate and automatically evaluate the predictions with EM and CrystalBLEU scores. 

All the trained models checkpoints (for each model we stored the final/best chekpoint only) are available on Zenodo at the following link: [models chekpoints](https://zenodo.org/records/12773308).
The folder also contains the graphs of the evaluation loss curve for both DeepSeek-Coder full (DSCf) and DeepSeek-Coder cleaned (DSCc) models. 

## 3. Detection of quality issues

The ``3_quality_issues_detection`` folder contains the code to detect and process the quality issues in both the training set and the model's predictions using the Semgrep static analyzer. It also contains the code to remove the found low-quality functions from the training set, resulting in the *clean training set* also stored on Zenodo.
The ``analyze_code.py`` script contains the complete list of Semgrep rules used in our study. 

* Install Semgrep by running the following command: ```bash
python3 -m pip install semgrep
```
* Run ```semgrep login``` to create your account and login to Semgrep to be able to use all the detection rules. Further details on [Semgrep](https://github.com/semgrep/semgrep).
* To run Semgrep on the Python functions use the following command: ```bash
python3 analyze_code.py <training_set/predictions>.json
```
* The training set/predictions are processed in batches of 20000 samples and the result of the analysis will be a set of json files containing all the detected issues. To process the results and extract the information on low-quality and syntactically incorrect functions use: ```bash
python3 process_results.py <training_set/predictions>_semgrep_result_batch <number_of_batches>
```
* The result of the analysis will be (i) a report of the detected code quality issues; (ii) the list of training set indexes containing low-quality functions and syntactically incorrect functions.
* To remove all low-quality and incorrect functions from the training set, use the following command: ```bash
python3 clean_dataset.py <training_set>.json
```

The ``quality_issues_results`` folder contains the results of our analysis, both in terms of Semgrep reports on quality issues and full list of low-quality and syntactically incorrect functions, for the training set, pre-trained only (PTO), DeepSeek-Coder full (DSCf) and DeepSeek-Coder cleaned (DSCc) predictions.

## 4. Statistical analysis

The ``4_statistical-analysis`` folder contains the script and data to replicate all the statistical tests performed in our study.