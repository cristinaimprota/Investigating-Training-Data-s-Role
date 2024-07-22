TRAIN_PATH=""
EVAL_PATH=""
OUTPUT_PATH=$1
MODEL_PATH="deepseek-ai/deepseek-coder-1.3b-instruct"

# evaluate 5 times, every 20% of epoch, based on total steps number

accelerate launch --config_file /evo/homes/improtac/.cache/huggingface/accelerate/default_config.yaml --num_processes=3 finetune_and_eval_deepseek.py \
    --model_name_or_path $MODEL_PATH \
    --train_path $TRAIN_PATH \
    --eval_path $EVAL_PATH \
    --output_dir $OUTPUT_PATH \
    --num_train_epochs 1 \
    --model_max_length 1024 \
    --per_device_train_batch_size 12 \
    --per_device_eval_batch_size 1 \
    --gradient_accumulation_steps 4 \
    --evaluation_strategy "steps" \
    --eval_steps 5772 \
    --do_train True \
    --do_eval True \
    --save_strategy "steps" \
    --save_total_limit 5 \
    --save_steps 5772 \
    --load_best_model_at_end True \
    --learning_rate 2e-5 \
    --warmup_steps 10 \
    --logging_steps 1 \
    --lr_scheduler_type "cosine" \
    --gradient_checkpointing True \
    --report_to "tensorboard" \
    --bf16 True \
    --metric_for_best_model "eval_loss"
