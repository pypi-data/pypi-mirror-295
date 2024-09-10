from openai import OpenAI
from yta_general_utils.file_downloader import download_image
from yta_general_utils.image_processor import resize_without_scaling
from yta_general_utils.file_processor import get_project_abspath
from dotenv import load_dotenv

import os

# We need to load the .env in the project that is
# being executing the code, not this library
dotenv_path = os.path.join(get_project_abspath(), '.env')
load_dotenv(dotenv_path)

# TODO: Is this actually useful? I think it could be removed...

def generate_image(prompt, output_filename):
    client = OpenAI()

    response = client.images.generate(
        model = "dall-e-3",
        prompt = prompt,
        size = "1792x1024",
        quality = "standard",
        n = 1,
    )

    image_url = response.data[0].url

    download_image(image_url, output_filename)
    resize_without_scaling(output_filename)