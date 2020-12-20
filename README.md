# roberta-mrc
Machine reading comprehension with RoBERTa

## Run with

- Python 3.7.3
- Transformers 2.11.0

## Result (RoBERTa-large)

##### RACE Run 1
- Test: 84.0% (loss: 0.773) / dev: 84.6% (loss: 0.736...)

```
Namespace(adam_epsilon=1e-08, cache_dir='', config_name='', data_dir='XXX', device=device(type='cuda'), do_eval=True, do_lower_case=True, do_test=False, do_train=True, eval_all_checkpoints=False, evaluate_during_training=False, fp16=True, fp16_opt_level='O1', gradient_accumulation_steps=2, learning_rate=1e-05, local_rank=-1, logging_steps=500, max_grad_norm=1.0, max_seq_length=512, max_steps=-1, model_name_or_path='roberta-large', model_type='roberta', n_gpu=4, no_cuda=False, num_train_epochs=4.0, output_dir='models_roberta/roberta-large-race', overwrite_cache=False, overwrite_output_dir=False, per_gpu_eval_batch_size=2, per_gpu_train_batch_size=2, save_steps=500, seed=42, server_ip='', server_port='', task_name='race', tokenizer_name='', train_batch_size=8, warmup_ratio=0.06, warmup_steps=1318.08, weight_decay=0.1)
```

##### RACE Run 2

- Test: 83.5% (loss: 1.403) / dev: 85.1% (loss: 1.191)

```
Namespace(adam_epsilon=1e-08, cache_dir='', config_name='', data_dir='XXX', device=device(type='cuda'), do_eval=True, do_lower_case=True, do_test=False, do_train=True, eval_all_checkpoints=False, eval_batch_size=2, evaluate_during_training=True, fp16=True, fp16_opt_level='O1', gradient_accumulation_steps=2, learning_rate=1e-05, local_rank=-1, logging_steps=500, max_grad_norm=1.0, max_seq_length=512, max_steps=-1, model_name_or_path='roberta-large', model_type='roberta', n_gpu=1, no_cuda=False, num_train_epochs=4.0, output_dir='models_roberta/roberta-large-race2', overwrite_cache=False, overwrite_output_dir=False, per_gpu_eval_batch_size=2, per_gpu_train_batch_size=2, save_steps=500, seed=45, server_ip='', server_port='', task_name='race', tokenizer_name='', train_batch_size=2, warmup_ratio=0.06, warmup_steps=5271.84, weight_decay=0.1)
```