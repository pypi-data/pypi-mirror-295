from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, CompositeAudioClip, AudioFileClip, concatenate_videoclips
from yta_multimedia.resources.video.effect.sound.drive_urls import PHOTO_GOOGLE_DRIVE_DOWNLOAD_URL
from yta_multimedia.video.edition.effect.moviepy.blink_moviepy_effect import BlinkMoviepyEffect
from yta_multimedia.resources import get_resource
from yta_multimedia.video.edition.effect.constants import EFFECTS_RESOURCES_FOLDER
from typing import Union

class PhotoMoviepyEffect:
    """
    TODO: Add description
    """
    __parameters = {}

    def __init__(self, clip: Union[VideoFileClip, CompositeVideoClip, ImageClip]):
        self.__clip = clip

    def __process_parameters(self):
        return self.__parameters
    
    def apply(self):
        """
        Applies the effect to the provided 'clip' and with the also
        provided parameters needed by this effect.
        """
        if not self.__clip:
            return None
        
        self.__process_parameters()

        # Change this parameter to adjust the effect
        effect_duration = 0.2
        if self.__clip.duration < effect_duration:
            effect_duration = self.__clip.duration

        TMP_FILENAME = get_resource(PHOTO_GOOGLE_DRIVE_DOWNLOAD_URL, EFFECTS_RESOURCES_FOLDER + 'sounds/photo_taken.mp3')

        if self.__clip.duration == effect_duration:
            # If clip is shorter than our default effect duration time, do it with
            # the clip duration
            self.__clip = BlinkMoviepyEffect(self.__clip, effect_duration, [255, 255, 255]).apply()
        else:
            # We force the effect to be 'effect_duration' seconds longer and in the
            # middle of the provided clip
            half_duration = self.__clip.duration / 2
            half_effect_duration = effect_duration / 2
            self.__clip = concatenate_videoclips([
                self.__clip.subclip(0, half_duration - effect_duration),
                BlinkMoviepyEffect(self.__clip.subclip(half_duration - half_effect_duration, half_duration + half_effect_duration), effect_duration, [255, 255, 255]).apply(),
                self.__clip.subclip(half_duration + half_effect_duration, self.__clip.duration)
            ])
        
        self.__clip.audio = CompositeAudioClip([
            self.__clip.audio,
            AudioFileClip(TMP_FILENAME).set_duration(effect_duration)
        ])

        return self.__clip