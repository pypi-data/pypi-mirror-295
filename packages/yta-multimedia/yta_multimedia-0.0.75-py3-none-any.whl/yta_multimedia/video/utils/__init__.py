from typing import Union
from moviepy.editor import ImageClip
from yta_general_utils.type_checker import variable_is_type

def generate_videoclip_from_image(image_filename: Union[ImageClip, str], duration: float = 1, output_filename: Union[str, None] = None):
    """
    Receives an image as 'image_filename' and creates an ImageClip of
    'duration' seconds. It will be also stored as a file if 
    'output_filename' is provided.

    # TODO: Should this method go into 'video.utils' instead of here (?)
    """
    if not image_filename:
        return None
    
    if duration <= 0:
        return None
    
    if not duration:
        return None
    
    if variable_is_type(output_filename, str):
        if not output_filename:
            return None
    
    if variable_is_type(image_filename, str):
        # ADV: By now we are limiting this to 60 fps
        image_filename = ImageClip(image_filename).set_fps(60).set_duration(duration)

    if output_filename:
        image_filename.write_videofile(output_filename)

    return image_filename