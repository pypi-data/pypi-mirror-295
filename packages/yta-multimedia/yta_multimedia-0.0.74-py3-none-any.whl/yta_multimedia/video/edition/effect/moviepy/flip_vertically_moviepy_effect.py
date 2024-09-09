from moviepy.editor import vfx, VideoFileClip, CompositeVideoClip, ImageClip
from typing import Union

class FlipVerticallyMoviepyEffect:
    """
    This effect flips the video vertically.
    """
    __MOVIEPY_EFFECT_NAME = 'mirror_y'
    __parameters = {}

    def __init__(self, clip: Union[VideoFileClip, CompositeVideoClip, ImageClip]):
        self.__clip = clip

    def __get_moviepy_vfx_effect(self):
        return getattr(vfx, self.__MOVIEPY_EFFECT_NAME, None)
    
    def __process_parameters(self):
        return self.__parameters
    
    def apply(self):
        """
        Applies the effect to the provided 'clip' and with the also
        provided parameters needed by this effect.
        """
        return self.__clip.fx(self.__get_moviepy_vfx_effect(), **self.__process_parameters())
