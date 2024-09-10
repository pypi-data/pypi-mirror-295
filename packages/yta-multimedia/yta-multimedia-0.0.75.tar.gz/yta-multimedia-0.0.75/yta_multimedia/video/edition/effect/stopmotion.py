from yta_multimedia.video.frames import get_frame_from_video_by_frame_number
from yta_general_utils.type_checker import variable_is_type
from yta_general_utils.file_processor import file_is_video_file
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips
from typing import Union

class StopMotionVideoEffect:
    """
    Creates a Stop Motion effect in the provided video by dropping the frames
    per second but maintaining the original ratio.
    """
    def __init__(self, video: Union[VideoFileClip, ImageClip, CompositeVideoClip, str]):
        if not video:
            raise Exception('No "video" provided.')
        
        if variable_is_type(video, str):
            if not file_is_video_file(video):
                raise Exception('Provided "video" is not a valid video file.')
            
            video = VideoFileClip(video)

        self.video = video

    def apply(self):
        # This value is this one by default by now
        FRAMES_TO_JUMP = 5

        clips = []
        for frame_number in range((int) (self.video.fps * self.video.duration)):
            if frame_number % FRAMES_TO_JUMP == 0:
                frame = get_frame_from_video_by_frame_number(self.video, frame_number)
                clips.append(ImageClip(frame, duration = FRAMES_TO_JUMP / self.video.fps).set_fps(self.video.fps))

        return concatenate_videoclips(clips).set_audio(self.video.audio).set_fps(self.video.fps)


    