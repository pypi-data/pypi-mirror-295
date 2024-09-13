import logging
import json
from typing import Dict, List, Tuple, Any, Optional
from transformers import (
    HfArgumentParser,
    AutoTokenizer,
    AutoModelForTokenClassification,
    TrainingArguments,
    PreTrainedTokenizer,
    PreTrainedModel,
)
from integral_deid.dataset_creator import DatasetCreator
from integral_deid.model_arguments import ModelArguments
from integral_deid.data_training_arguments import DataTrainingArguments
from integral_deid.evaluation_arguments import EvaluationArguments
from integral_deid.sequence_tagging import SequenceTagger
from integral_deid.text_deid import TextDeid
from integral_deid.config import MODEL_CONFIG, DATASET_CREATOR_CONFIG

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class DeIDApplication:
    def __init__(self, model_config: Dict[str, Any] = None, dataset_creator_config: Dict[str, Any] = None):
        self.model_config = model_config or MODEL_CONFIG
        self.dataset_creator_config = dataset_creator_config or DATASET_CREATOR_CONFIG

        self.tokenizer, self.model = self.load_model_and_tokenizer()
        self.dataset_creator = self.create_dataset_creator()
        self.model_args, self.data_args, self.evaluation_args, self.training_args = self.parse_arguments()
        self.sequence_tagger = self.create_sequence_tagger()

    def load_model_and_tokenizer(self) -> Tuple[PreTrainedTokenizer, PreTrainedModel]:
        logger.info("Loading model and tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(self.model_config["model_name_or_path"])
        model = AutoModelForTokenClassification.from_pretrained(self.model_config["model_name_or_path"])
        return tokenizer, model

    def create_dataset_creator(self) -> DatasetCreator:
        logger.info("Creating dataset creator...")
        return DatasetCreator(**self.dataset_creator_config)

    def parse_arguments(self) -> Tuple[
        ModelArguments,
        DataTrainingArguments,
        EvaluationArguments,
        TrainingArguments,
    ]:
        logger.info("Parsing arguments...")
        parser = HfArgumentParser(
            (
                ModelArguments,
                DataTrainingArguments,
                EvaluationArguments,
                TrainingArguments,
            )
        )
        return parser.parse_dict(self.model_config)

    def create_sequence_tagger(self) -> SequenceTagger:
        logger.info("Creating sequence tagger...")
        tagger = SequenceTagger(
            task_name=self.data_args.task_name,
            notation=self.data_args.notation,
            ner_types=self.data_args.ner_types,
            model_name_or_path=self.model_args.model_name_or_path,
            config_name=self.model_args.config_name,
            tokenizer_name=self.model_args.tokenizer_name,
            post_process=self.model_args.post_process,
            cache_dir=self.model_args.cache_dir,
            model_revision=self.model_args.model_revision,
            use_auth_token=self.model_args.use_auth_token,
            threshold=self.model_args.threshold,
            do_lower_case=self.data_args.do_lower_case,
            fp16=self.training_args.fp16,
            seed=self.training_args.seed,
            local_rank=self.training_args.local_rank,
        )
        tagger.load()
        return tagger

    def process_text(self, text: str, meta: Dict[str, Any]) -> List[Dict[str, Any]]:
        logger.info("Processing text...")
        note_data = {
            "text": text,
            "meta": meta,
            "note_id": meta.get("note_id", ""),
        }

        ner_notes = list(
            self.dataset_creator.create(
                input_data=[note_data],
                mode="predict",
                notation=self.data_args.notation,
                token_text_key="text",
                metadata_key="meta",
                note_id_key="note_id",
                label_key="label",
                span_text_key="spans",
            )
        )

        self.sequence_tagger.set_predict(
            test_data=ner_notes,
            max_test_samples=self.data_args.max_predict_samples,
            preprocessing_num_workers=1,
            overwrite_cache=self.data_args.overwrite_cache,
        )

        self.sequence_tagger.setup_trainer(training_args=self.training_args)
        return list(self.sequence_tagger.predict())

    def deid_text(self, note_data: Dict[str, Any], predictions: List[Dict[str, Any]]) -> str:
        logger.info("De-identifying text...")
        text_deid = TextDeid(notation=self.data_args.notation, span_constraint="super_strict")
        deid_notes = list(
            text_deid.run_deid(
                input_data=note_data,
                prediction_data=predictions,
                deid_strategy="replace_informative",
                keep_age=False,
                metadata_key="meta",
                note_id_key="note_id",
                tokens_key="tokens",
                predictions_key="predictions",
                text_key="text",
            )
        )
        return deid_notes[0]["deid_text"]

    def run(self, input_text: str, meta: Dict[str, Any]) -> Dict[str, Any]:
        try:
            predictions = self.process_text(input_text, meta)
            note_data = {"text": input_text, "meta": meta, "note_id": meta.get("note_id", "")}
            deid_text_result = self.deid_text(note_data, predictions)

            result = {
                "deid_text": deid_text_result,
                "tokens": json.dumps(predictions[0]["tokens"]),
                "predictions": predictions[0]["predictions"],
            }
            return result
        except Exception as e:
            return {"error": str(e)}
