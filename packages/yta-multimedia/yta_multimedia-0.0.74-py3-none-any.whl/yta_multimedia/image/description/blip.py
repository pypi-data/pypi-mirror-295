from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from yta_general_utils.type_checker import variable_is_type
from typing import Union

def describe_image(image_filename: Union[str, Image.Image]):
    """
    Describes the provided 'image_filename' by using the Salesforce
    blip image captioning system.
    """
    if not image_filename:
        return None
    
    if variable_is_type(image_filename, str):
        image_filename = Image.open(image_filename)

    # models are stored in C:\Users\USERNAME\.cache\huggingface\hub
    processor = BlipProcessor.from_pretrained('Salesforce/blip-image-captioning-base')
    model = BlipForConditionalGeneration.from_pretrained('Salesforce/blip-image-captioning-base')
    inputs = processor(image_filename, return_tensors = 'pt')
    out = model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokes = True)

    return description