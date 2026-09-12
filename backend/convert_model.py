from pathlib import Path
import shutil

from transformers import AutoTokenizer
from optimum.onnxruntime import (
    ORTModelForSeq2SeqLM,
    ORTQuantizer,
)
from optimum.onnxruntime.configuration import AutoQuantizationConfig


BASE_DIR = Path(__file__).resolve().parent

SOURCE_MODEL = BASE_DIR / "model" / "fine_tuned_t5_small"
ONNX_DIR = BASE_DIR / "model" / "bharatbrief_onnx"
QUANTIZED_DIR = BASE_DIR / "model" / "bharatbrief_onnx_int8"


print("=" * 60)
print("BharatBrief T5 -> ONNX -> INT8")
print("=" * 60)

# Clean previous outputs
if ONNX_DIR.exists():
    shutil.rmtree(ONNX_DIR)

if QUANTIZED_DIR.exists():
    shutil.rmtree(QUANTIZED_DIR)

ONNX_DIR.mkdir(parents=True)
QUANTIZED_DIR.mkdir(parents=True)

# ---------------------------------------------------------
# STEP 1: Export fine-tuned T5 to ONNX
# ---------------------------------------------------------

print("\n[1/3] Exporting fine-tuned T5 to ONNX...")

model = ORTModelForSeq2SeqLM.from_pretrained(
    str(SOURCE_MODEL),
    export=True,
)

model.save_pretrained(str(ONNX_DIR))

tokenizer = AutoTokenizer.from_pretrained(str(SOURCE_MODEL))
tokenizer.save_pretrained(str(ONNX_DIR))

print("ONNX export complete.")

# ---------------------------------------------------------
# STEP 2: Dynamic INT8 quantization
# ---------------------------------------------------------

print("\n[2/3] Quantizing ONNX model to INT8...")

quant_config = AutoQuantizationConfig.avx2(
    is_static=False,
    per_channel=False,
)

model_files = [
    "encoder_model.onnx",
    "decoder_model.onnx",
    "decoder_with_past_model.onnx",
]

for filename in model_files:

    source_file = ONNX_DIR / filename

    if not source_file.exists():
        print(f"Skipping missing file: {filename}")
        continue

    print(f"Quantizing {filename}...")

    quantizer = ORTQuantizer.from_pretrained(
        ONNX_DIR,
        file_name=filename,
    )

    quantizer.quantize(
        save_dir=str(QUANTIZED_DIR),
        quantization_config=quant_config,
    )

print("Quantization complete.")

# ---------------------------------------------------------
# STEP 3: Rename quantized files to standard names
# ---------------------------------------------------------

print("\n[3/3] Preparing final model directory...")

quantized_files = [
    "encoder_model_quantized.onnx",
    "decoder_model_quantized.onnx",
    "decoder_with_past_model_quantized.onnx",
]

for filename in quantized_files:
    source = QUANTIZED_DIR / filename

    if source.exists():
        target = QUANTIZED_DIR / filename.replace(
            "_quantized.onnx",
            ".onnx",
        )

        source.rename(target)

# Copy configuration/tokenizer files
for filename in ONNX_DIR.iterdir():

    if filename.suffix.lower() != ".onnx":
        destination = QUANTIZED_DIR / filename.name

        if not destination.exists():
            if filename.is_file():
                shutil.copy2(filename, destination)

print("\n" + "=" * 60)
print("DONE")
print("=" * 60)
print(f"\nFinal model:")
print(QUANTIZED_DIR)

print("\nFiles:")
for file in sorted(QUANTIZED_DIR.iterdir()):
    print(f"  {file.name}")

print("\nYou can now test this model locally.")