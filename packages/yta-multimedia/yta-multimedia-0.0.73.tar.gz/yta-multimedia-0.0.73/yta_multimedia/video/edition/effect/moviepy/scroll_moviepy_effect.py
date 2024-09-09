from moviepy.editor import vfx, VideoFileClip, CompositeVideoClip, ImageClip
from typing import Union

class ScrollMoviepyEffect:
    """
    This effect will make the clip appear in black and
    white colors.
    """
    __MOVIEPY_EFFECT_NAME = 'scroll'
    __parameters = {}

    def __init__(self, clip: Union[VideoFileClip, CompositeVideoClip, ImageClip], width: int = 960, height: int = 540, x_speed: int = 20, y_speed: int = 20, x_start: int = 100, y_start: int = 100):
        self.__clip = clip
        self.__parameters['w'] = width
        self.__parameters['h'] = height
        self.__parameters['x_speed'] = x_speed
        self.__parameters['y_speed'] = y_speed
        self.__parameters['x_start'] = x_start
        self.__parameters['y_start'] = y_start

    def __get_moviepy_vfx_effect(self):
        return getattr(vfx, self.__MOVIEPY_EFFECT_NAME, None)
    
    def __process_parameters(self):
        if not self.__parameters['w']:
            self.__parameters['w'] = self.__clip.w / 2 - self.__clip.w / 2
            self.__parameters['h'] = self.__clip.h / 2 - self.__clip.h / 2
            self.__parameters['x_speed'] = 5
            self.__parameters['y_speed'] = 5
            self.__parameters['x_start'] = self.__clip.w / 2 - self.__clip.w / 2
            self.__parameters['y_start'] = self.__clip.h / 2 - self.__clip.h / 2

        return self.__parameters
    
    def apply(self):
        """
        Applies the effect to the provided 'clip' and with the also
        provided parameters needed by this effect.
        """
        return self.__clip.fx(self.__get_moviepy_vfx_effect(), **self.__process_parameters()).resize(self.__clip.size)
