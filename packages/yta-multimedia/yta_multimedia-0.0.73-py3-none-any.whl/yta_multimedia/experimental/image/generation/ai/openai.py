from openai import OpenAI
from dotenv import load_dotenv
from yta_general_utils.file_downloader import download_image
from yta_general_utils.image_processor import resize_without_scaling

load_dotenv()

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