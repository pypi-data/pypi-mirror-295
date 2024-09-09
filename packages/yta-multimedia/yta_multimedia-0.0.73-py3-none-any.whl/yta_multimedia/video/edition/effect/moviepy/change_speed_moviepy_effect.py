from moviepy.editor import vfx, VideoFileClip, CompositeVideoClip, ImageClip
from typing import Union

class ChangeSpeedMoviepyEffect:
    """
    This effect changes the speed of the video. A 'speed_factor'
    of 2 means a 2x speed (0:10s -> 0:05s). A 'speed_factor' of
    0.5 means a 0.5x speed (0:10s -> 0:20s)
    """
    __MOVIEPY_EFFECT_NAME = 'speedx'
    __parameters = {}

    def __init__(self, clip: Union[VideoFileClip, CompositeVideoClip, ImageClip], speed_factor: float = None):
        self.__clip = clip
        self.__parameters['speed_factor'] = speed_factor

    def __get_moviepy_vfx_effect(self):
        return getattr(vfx, self.__MOVIEPY_EFFECT_NAME, None)
    
    def __process_parameters(self):
        if not self.__parameters['speed_factor']:
            self.__parameters['speed_factor'] = 1
        else:
            # This is limited to x10 and x0.1
            if self.__parameters['duration'] > 10:
                self.__parameters['duration'] = 1
            elif self.__parameters['duration'] <= 0.1:
                self.__parameters['duration'] = 0.1

        return self.__parameters
    
    def apply(self):
        """
        Applies the effect to the provided 'clip' and with the also
        provided parameters needed by this effect.
        """
        return self.__clip.fx(self.__get_moviepy_vfx_effect(), **self.__process_parameters())
