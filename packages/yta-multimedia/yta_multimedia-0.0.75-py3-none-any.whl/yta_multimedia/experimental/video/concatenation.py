from moviepy.editor import VideoFileClip, concatenate_videoclips
from yta_general_utils.type_checker import variable_is_type
from typing import Union

# TODO: Move this method to another site I think and refactor a little bit
# but it is working properly. I should receive a files list to merge 
# (maybe with abspath needed?).
def concatenate_videos_ffmpeg(abspath, output_filename = 'merged.mp4'):
    """
    This method concatenates the video files existing in the provided
    'abspath' and builds a new video with the name provided as
    'output_filename' in the same 'abspath' folder.

    This method uses the 'ffmpeg' to concatenate videos. Folder in
    'abspath' should contain only videos and with the same resolution.
    """
    # 1. List video files in folder
    import os
    from subprocess import run
    # Get the list of all files and directories
    files = os.listdir(abspath)
    files = [f for f in files if os.path.isfile(abspath + '/' + f)]

    # Write each file in a row with "file 'filename.ext'" format
    text = ''
    for file in files:
        text += "file '" + abspath + "/" + file + "'\n"

    filename = 'append_videos.txt'
    output_filename = abspath + '/' + output_filename
    with open(filename, 'w') as the_file:
        the_file.write(text)

    print(text)
    print(output_filename)

    command = 'ffmpeg -f concat -safe 0 -i ' + filename + ' -c copy ' + output_filename
    run(command)

def concatenate_moviepy(videoclips: list[VideoFileClip], output_filename: Union[str, None] = None):
    """
    Concatenates the provided moviepy 'videoclips' into a new one.

    If 'output_filename' provided, the new clip be stored with that
    name and that name.

    This method will return the new clips array.
    """
    if not videoclips:
        return None
    
    if variable_is_type(output_filename, str):
        if not output_filename:
            return None

    clip = concatenate_videoclips(videoclips)

    if output_filename:
        clip.write_videofile(output_filename)

    return clip

# TODO: This is being tested
def concatenate_images_ffmpeg(abspath, output_filename = 'merged.mp4'):
    # TODO: Do it
    from yta_general_utils.file_processor import list
    from subprocess import run
    # TODO: Check that abspath is a folder
    # TODO: Make this able to accept images array (?)
    images = list(abspath)

    text = ''
    for image in images:
        text += "file '" + image + "'\n"

    filename = 'append_videos.txt'
    #output_filename = abspath + '/' + output_filename
    output_filename = abspath + output_filename
    with open(filename, 'w') as the_file:
        the_file.write(text)

    # https://www.reddit.com/r/ffmpeg/comments/ks8zfs/comment/gieu7x6/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    # https://stackoverflow.com/questions/38368105/ffmpeg-custom-sequence-input-images/51618079#51618079
    # https://stackoverflow.com/a/66014158

    # TODO: Output needs to be an abspath or will be in images folder
    # ffmpeg -i %d.png -vcodec png z.mov   This is said in stackoverflow
    #command = 'ffmpeg -f concat -y -safe 0 -i ' + filename + ' -r 60 ' + output_filename
    #command = 'ffmpeg -f concat -i ' + filename + ' -r 60 ' + output_filename
    #command = 'ffmpeg -f concat -safe 0 -y -i ' + filename + ' -r 60 -vcodec png ' + output_filename
    #command = 'ffmpeg -f concat -safe 0 -y -i ' + filename + ' -vcodec png ' + output_filename
    #command = 'ffmpeg -f concat -safe 0 -y -i ' + filename + ' -r 60 -c:v prores -pix_fmt yuva444p10le ' + output_filename
    command = 'ffmpeg -f concat -safe 0 -y -r 60  -i ' + filename + ' -c:v qtrle -pix_fmt argb ' + output_filename
    run(command)
