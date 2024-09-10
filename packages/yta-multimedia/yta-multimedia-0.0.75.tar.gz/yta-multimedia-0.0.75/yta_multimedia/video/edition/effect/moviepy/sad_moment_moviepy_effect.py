from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, AudioFileClip, ColorClip, vfx
from typing import Union
from yta_multimedia.resources.video.effect.sound.drive_urls import SAD_MOMENT_GOOGLE_DRIVE_DOWNLOAD_URL
from yta_multimedia.resources import get_resource
from yta_multimedia.video.edition.effect.constants import EFFECTS_RESOURCES_FOLDER

class SadMomentMoviepyEffect:
    """
    This method gets the first frame of the provided 'clip' and returns a
    new clip that is an incredible 'sad_moment' effect with black and white
    filter, zoom in and rotating effect and also sad violin music.

    The 'duration' parameter is to set the returned clip duration, but the
    default value is a perfect one.
    """
    __parameters = {}

    def __init__(self, clip: Union[VideoFileClip, CompositeVideoClip, ImageClip], duration = 4.8):
        self.__clip = clip
        self.__parameters['duration'] = duration

    def __process_parameters(self):
        if not self.__parameters['duration']:
            self.__parameters['duration'] = 4.8
        else:
            # Zoom is by now limited to [1 - 10] ratio
            if self.__parameters['duration'] > 10:
                self.__parameters['duration'] = 10
            elif self.__parameters['duration'] <= 1:
                self.__parameters['duration'] = 1

        return self.__parameters
    
    def apply(self):
        """
        Applies the effect to the provided 'clip' and with the also
        provided parameters needed by this effect.
        """
        if not self.__clip:
            return None
        
        self.__process_parameters()
        
        # We freeze the first frame
        aux = ImageClip(self.__clip.get_frame(0), duration = self.__parameters['duration'])
        aux.fps = self.__clip.fps
        self.__clip = aux
        # We then build the whole effect
        self.__clip = self.__clip.fx(vfx.blackwhite).resize(lambda t: 1 + 0.30 * (t / self.__clip.duration)).set_position(lambda t: (-(0.15 * self.__clip.w * (t / self.__clip.duration)), -(0.15 * self.__clip.h * (t / self.__clip.duration)))).rotate(lambda t: 5 * (t / self.__clip.duration), expand = False)
        # We set the effect audio
        TMP_FILENAME = get_resource(SAD_MOMENT_GOOGLE_DRIVE_DOWNLOAD_URL, EFFECTS_RESOURCES_FOLDER + 'sounds/sad_moment.mp3')
        self.__clip.audio = AudioFileClip(TMP_FILENAME).set_duration(self.__clip.duration)

        return CompositeVideoClip([
            ColorClip(color = [0, 0, 0], size = self.__clip.size, duration = self.__clip.duration),
            self.__clip,
        ])