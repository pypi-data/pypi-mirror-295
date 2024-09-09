from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, clips_array
from typing import Union
from math import log as math_log, pow as math_pow

class MultipliedMoviepyEffect:
    """
    Generates a clips array with the provided 'clip' being shown
    'times' times (this parameter must be a pow of 4). This
    method has been created to be used internally with our own
    default methods.
    """
    __parameters = {}

    def __init__(self, clip: Union[VideoFileClip, CompositeVideoClip, ImageClip], times: int = 4):
        self.__clip = clip
        self.__parameters['times'] = times

    def __process_parameters(self):
        if not self.__parameters['times']:
            self.__parameters['times'] = 4

        if self.__parameters['times'] <= 1 or not math_log(self.__parameters['times'], 4).is_integer():
            # TODO: Raise exception instead of forcing 4 (?)
            self.__parameters['times'] = 4

        return self.__parameters
    
    def apply(self):
        """
        Applies the effect to the provided 'clip' and with the also
        provided parameters needed by this effect.
        """
        if not self.__clip:
            return None
        
        self.__process_parameters()
        
        audio = self.__clip.audio
        size = (self.__clip.w, self.__clip.h)

        # We will dynamically build the matrix
        row = []
        group = []
        # 4^3 = 64 => 8x8 = 2^3x2^3  and  4^2 = 16 => 4x4 = 2^2x2^2
        range_limit_value = math_pow(2, math_log(self.__parameters['times'], 4))
        for i in range(int(self.__parameters['times'] / range_limit_value)):
            row = []
            for j in range(int(self.__parameters['times'] / range_limit_value)):
                row.append(self.__clip)
            group.append(row)

        # When building 'clips_array' you sum the resolutions, so if you add four videos
        # of 1920x1080, you'll get one video of 4x(1920x1080) that will be impossible to
        # exported and unexpected. We resize it to avoid this and we don't resize each
        # clip before because they lose quality
        return clips_array(group).resize(size).set_audio(audio)