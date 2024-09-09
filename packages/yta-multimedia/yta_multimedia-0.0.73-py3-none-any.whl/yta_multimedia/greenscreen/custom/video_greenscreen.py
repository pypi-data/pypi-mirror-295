from yta_multimedia.greenscreen.classes.greenscreen_details import GreenscreenDetails
from yta_general_utils.type_checker import variable_is_type
from moviepy.editor import ImageClip
from typing import Union
from yta_multimedia.greenscreen.classes.greenscreen_details import GreenscreenDetails
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, vfx, concatenate_videoclips
from yta_general_utils.file_processor import file_is_video_file
from yta_multimedia.greenscreen.custom.utils import get_greenscreen_details
from yta_multimedia.greenscreen.enum.greenscreen_type import GreenscreenType

class VideoGreenscreen:
    greenscreen: GreenscreenDetails = None

    def __init__(self, greenscreen: Union[GreenscreenDetails, str]):
        if variable_is_type(greenscreen, str):
            # We need to automatically detect greenscreen details
            greenscreen = get_greenscreen_details(greenscreen, GreenscreenType.VIDEO)

        self.greenscreen = greenscreen
       
    def from_image_to_image(self):
        # TODO: Does this make sense? We are working with a video, so
        # trying to generate just a frame, an image, does make sense?
        # TODO: By the way, this is not working yet
        pass

    def from_image_to_video(self, image_filename: str, duration: float = 3.0, output_filename: Union[str, None] = None):
        """
        Receives an 'image_filename', places it into the greenscreen and generates
        a video of 'duration' seconds of duration that is returned. This method
        will store locally the video if 'output_filename' is provided.
        """
        if not image_filename:
            return None
        
        if not duration:
            return None
        
        if not output_filename:
            return None
        
        imageclip = ImageClip(image_filename, duration = duration)
        final_clip = self.from_video_to_video(imageclip)

        if output_filename:
            final_clip.write_videofile(output_filename)

        return final_clip
    
    def from_video_to_image(self):
        # TODO: Does this make sense? By now it is not implemented
        pass

    def from_video_to_video(self, video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip], output_filename: Union[str, None] = None):
        """
        Inserts the provided 'video' in the greenscreen and returns the
        CompositeVideoClip that has been created. If 'output_filename' 
        provided, it will be written locally with that file name.

        The provided 'video' can be a filename or a moviepy video clip.

        TODO: Careful when video is longer than greenscreen
        """
        if not video:
            return None
        
        if variable_is_type(video, str):
            if not file_is_video_file(video):
                return None
            
            video = VideoFileClip(video)

        # TODO: Change this 
        # We could have different areas in which append 1 or more 
        # videos, so it would be handled different. By now I'm
        # considering we only have one

        TMP_FILENAME = self.greenscreen.get_filename()

        # We choose the first greenscreen area to work with
        greenscreen_area = self.greenscreen.greenscreen_areas[0]
        
        # Create the clip
        green_screen_clip = VideoFileClip(TMP_FILENAME).fx(vfx.mask_color, color = greenscreen_area.rgb_color, thr = 100, s = 5)

        width = greenscreen_area.lower_right_pixel[0] - greenscreen_area.upper_left_pixel[0]
        # If the provided clip is shorter than our green screen: easy, crop the green screen
        # If the provided clip is longer than our green screen: I use the green screen duration
        # and let the clip be original the rest of the time
        # TODO: Improve resizing process as it is failing...
        if green_screen_clip.duration > video.duration:
            green_screen_clip = green_screen_clip.set_duration(video.duration)
            # Clip will be displayed inside the green screen area
            video = video.resize(width = width).set_position((greenscreen_area.upper_left_pixel[0], greenscreen_area.upper_left_pixel[1]))
            video = CompositeVideoClip([video, green_screen_clip], size = green_screen_clip.size)
        elif video.duration > green_screen_clip.duration:
            # First subclip will be displayed inside the green screen area
            first_clip = video.subclip(0, green_screen_clip.duration).resize(width = width).set_position((greenscreen_area.upper_left_pixel[0], greenscreen_area.upper_left_pixel[1]))
            # Second clip will be as the original one
            second_clip = video.subclip(green_screen_clip.duration, video.duration)
            video = concatenate_videoclips([
                CompositeVideoClip([first_clip, green_screen_clip], size = green_screen_clip.size),
                second_clip
            ])
        else:
            video = CompositeVideoClip([video, green_screen_clip], size = green_screen_clip.size)

        if output_filename:
            video.write_videofile(output_filename, fps = video.fps)

        return video