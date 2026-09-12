from pathlib import Path

from transformers import AutoTokenizer
from optimum.onnxruntime import ORTModelForSeq2SeqLM


BASE_DIR = Path(__file__).resolve().parent

MODEL_DIR = (
    BASE_DIR
    / "model"
    / "bharatbrief_onnx_int8"
)

print("Loading BharatBrief ONNX INT8 model...")

tokenizer = AutoTokenizer.from_pretrained(
    str(MODEL_DIR)
)

model = ORTModelForSeq2SeqLM.from_pretrained(
    str(MODEL_DIR),
    encoder_file_name="encoder_model.onnx",
    decoder_file_name="decoder_model.onnx",
    decoder_with_past_file_name="decoder_with_past_model.onnx",
    provider="CPUExecutionProvider",
    use_io_binding=False,
)

text = """
BharatBrief is an AI-powered article summarization system
designed to generate concise summaries from long textual
content. The system uses a fine-tuned T5 model and also
provides source verification capabilities.
"""

inputs = tokenizer(
    "summarize: " + text,
    return_tensors="pt",
    max_length=1024,
    truncation=True,
)

outputs = model.generate(
    **inputs,
    max_length=128,
    min_length=30,
    num_beams=4,
    no_repeat_ngram_size=3,
    do_sample=False,
)

summary = tokenizer.decode(
    outputs[0],
    skip_special_tokens=True,
)

print("\nSUMMARY:")
print(summary)