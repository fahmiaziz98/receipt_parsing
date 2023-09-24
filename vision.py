from PIL import Image
import os
import re
import torch
from transformers import DonutProcessor, VisionEncoderDecoderModel

def get_predictions(image_path):
    """
    Generate predictions for an image using a pretrained Donut model.

    Args:
        image_path (str): Path to the input image file.

    Returns:
        Json format
    """
    # Load pretrained Donut processor and model
    processor = DonutProcessor.from_pretrained("fahmiaziz/finetune-donut-cord-v2.5")
    model = VisionEncoderDecoderModel.from_pretrained("fahmiaziz/finetune-donut-cord-v2.5")

    # Check and set the device (CPU or GPU)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    # Open the input image
    image = Image.open(image_path)

    # Prepare encoder inputs
    pixel_values = processor(image, return_tensors="pt").pixel_values

    # Prepare decoder inputs
    task_prompt = "<s_cord-v2>"
    decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids

    # Generate answer
    outputs = model.generate(
        pixel_values.to(device),
        decoder_input_ids=decoder_input_ids.to(device),
        max_length=model.decoder.config.max_position_embeddings,
        early_stopping=True,
        pad_token_id=processor.tokenizer.pad_token_id,
        eos_token_id=processor.tokenizer.eos_token_id,
        use_cache=True,
        num_beams=1,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
        return_dict_in_generate=True,
    )

    # Postprocess the generated sequence
    sequence = processor.batch_decode(outputs.sequences)[0]
    sequence = sequence.replace(processor.tokenizer.eos_token, "").replace(processor.tokenizer.pad_token, "")
    sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()  # Remove the first task start token

    return processor.token2json(sequence)
