from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
from typing import Union
from skimage.filters import gaussian

class BlurMoviepyEffect:
    """
    This effect will zoom out the clip, on the center.

    TODO: This effect is not smooth as it makes it have
    a black border. Maybe removing it (?)
    """
    __parameters = {}

    def __init__(self, clip: Union[VideoFileClip, CompositeVideoClip, ImageClip], blur_radius = 4):
        self.__clip = clip
        self.__parameters['blur_radius'] = blur_radius

    def __process_parameters(self):
        if not self.__parameters['blur_radius']:
            self.__parameters['blur_radius'] = 4
        else:
            # Zoom is by now limited to [2 - 64] ratio
            if self.__parameters['blur_radius'] > 64:
                self.__parameters['blur_radius'] = 64
            elif self.__parameters['blur_radius'] <= 2:
                self.__parameters['blur_radius'] = 2

        return self.__parameters
    
    def __effect_calculations(self, get_frame, t, blur_radius):
        return gaussian(get_frame(t).astype(float), sigma = blur_radius)
    
    def apply(self):
        """
        Applies the effect to the provided 'clip' and with the also
        provided parameters needed by this effect.
        """
        return self.__clip.fl(lambda get_frame, t: self.__effect_calculations(get_frame, t, **self.__process_parameters()))
