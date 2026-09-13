import logging
import os
from pathlib import Path

import ctranslate2
from huggingface_hub import hf_hub_download
from transformers import AutoTokenizer


logger = logging.getLogger(__name__)


HF_MODEL_ID = "Ayush1082/BharatBrief-T5-CT2-INT8"
TOKENIZER_ID = "Ayush1082/BharatBrief-T5"

BASE_DIR = Path(__file__).resolve().parents[2]
LOCAL_MODEL_DIR = BASE_DIR / "model" / "bharatbrief_ct2_int8"


class ModelService:
    def __init__(self):
        self.translator = None
        self.tokenizer = None
        self.model = None
        self.loaded = False

    def load_model(self):
        if self.loaded:
            return

        logger.info("=" * 60)
        logger.info("Loading BharatBrief CTranslate2 INT8 model")
        logger.info("=" * 60)

        try:
            use_huggingface = (
                os.getenv("USE_HUGGINGFACE_MODEL", "true").lower() == "true"
            )

            # ---------------------------------------------------------
            # Locate CTranslate2 model
            # ---------------------------------------------------------
            if use_huggingface:
                logger.info(
                    f"Downloading CTranslate2 model from Hugging Face: {HF_MODEL_ID}"
                )

                model_bin = hf_hub_download(
                    repo_id=HF_MODEL_ID,
                    filename="model.bin",
                )

                config_file = hf_hub_download(
                    repo_id=HF_MODEL_ID,
                    filename="config.json",
                )

                vocabulary_file = hf_hub_download(
                    repo_id=HF_MODEL_ID,
                    filename="shared_vocabulary.json",
                )

                model_dir = Path(model_bin).parent

                logger.info(f"CTranslate2 model directory: {model_dir}")

            else:
                model_dir = LOCAL_MODEL_DIR

                if not model_dir.exists():
                    raise FileNotFoundError(
                        f"Local CTranslate2 model not found: {model_dir}"
                    )

            # ---------------------------------------------------------
            # Load tokenizer
            # ---------------------------------------------------------
            logger.info(f"Loading tokenizer from: {TOKENIZER_ID}")

            self.tokenizer = AutoTokenizer.from_pretrained(
                TOKENIZER_ID,
                use_fast=True,
            )

            # ---------------------------------------------------------
            # Load CTranslate2
            # ---------------------------------------------------------
            logger.info("Loading CTranslate2 INT8 model...")

            self.translator = ctranslate2.Translator(
                str(model_dir),
                device="cpu",
                inter_threads=1,
                intra_threads=1,
            )

            self.model = self.translator

            self.loaded = True

            logger.info("BharatBrief CTranslate2 INT8 model loaded successfully")

            # ---------------------------------------------------------
            # Warmup
            # ---------------------------------------------------------
            try:
                self.summarize(
                    "BharatBrief is an AI-powered article summarization system."
                )
                logger.info("Model warmup completed")
            except Exception as warmup_error:
                logger.warning(f"Warmup failed: {warmup_error}")

        except Exception:
            logger.exception("Failed to load BharatBrief model")
            raise

    def summarize(
        self,
        text: str,
        max_length: int = 128,
        min_length: int = 15,
    ) -> str:

        if not self.loaded:
            self.load_model()

        if not text or not text.strip():
            return ""

        text = text.strip()

        # Prevent excessive memory usage
        text = text[:12000]

        input_text = "summarize: " + text

        # Convert text to T5 tokens
        encoded = self.tokenizer(
            input_text,
            add_special_tokens=True,
            truncation=True,
            max_length=512,
        )

        input_tokens = self.tokenizer.convert_ids_to_tokens(
            encoded["input_ids"]
        )

        # Generate summary
        results = self.translator.translate_batch(
            [input_tokens],
            beam_size=2,
            max_decoding_length=max_length,
            min_decoding_length=min_length,
            repetition_penalty=1.2,
            no_repeat_ngram_size=3,
        )

        output_tokens = results[0].hypotheses[0]

        output_ids = self.tokenizer.convert_tokens_to_ids(
            output_tokens
        )

        summary = self.tokenizer.decode(
            output_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True,
        )

        return summary.strip()


model_service = ModelService()