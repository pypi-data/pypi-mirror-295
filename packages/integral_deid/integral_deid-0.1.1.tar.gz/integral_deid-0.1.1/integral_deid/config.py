# config.py
MODEL_CONFIG = {
    "post_process": "threshold_max",
    "threshold": 0.85,  # pulled out of thin air, but reasonable
    "model_name_or_path": "obi/deid_roberta_i2b2",
    "task_name": "ner",
    "notation": "BILOU",
    "ner_types": ["PATIENT", "STAFF", "AGE", "DATE", "PHONE", "ID", "EMAIL", "PATORG", "LOC", "HOSP", "OTHERPHI"],
    "truncation": True,
    "max_length": 512,
    "label_all_tokens": False,
    "return_entity_level_metrics": True,
    "text_column_name": "tokens",
    "label_column_name": "labels",
    "output_dir": "/tmp/run/models",
    "logging_dir": "/tmp/run/logging_steps",
    "overwrite_output_dir": True,
    "do_train": False,
    "do_eval": False,
    "do_predict": True,
    "report_to": None,
    "per_device_train_batch_size": 0,
    "per_device_eval_batch_size": 16,
    "logging_steps": 1000,
}

DATASET_CREATOR_CONFIG = {
    "sentencizer": "en_core_web_sm",
    "tokenizer": "en_core_web_sm",
    "max_tokens": 128,
    "max_prev_sentence_token": 32,
    "max_next_sentence_token": 32,
    "default_chunk_size": 32,
    "ignore_label": "NA",
}
