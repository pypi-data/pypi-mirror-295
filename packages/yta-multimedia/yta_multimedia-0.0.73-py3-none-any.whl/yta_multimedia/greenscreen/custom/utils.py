from yta_general_utils.file_downloader import get_id_from_google_drive_url
from yta_general_utils.tmp_processor import create_tmp_filename
from yta_multimedia.greenscreen.utils import get_greenscreen_area_details
from yta_general_utils.type_checker import is_google_drive_url
from yta_multimedia.greenscreen.classes.greenscreen_details import GreenscreenDetails
from yta_multimedia.greenscreen.classes.greenscreen_area_details import GreenscreenAreaDetails
from yta_multimedia.video.frames import get_frame_from_video_by_frame_number
from yta_multimedia.greenscreen.enum.greenscreen_type import GreenscreenType
from yta_multimedia.greenscreen.utils import GREENSCREENS_FOLDER
from yta_multimedia.resources import get_resource

def get_greenscreen_details(greenscreen_filename_or_google_drive_url: str, type: GreenscreenType):
    """
    Method to obtain greenscreen area and details that must be
    used by ImageGreenscreen and VideoGreenscreen to automatically
    detect greenscreens in their resources.
    """
    if not greenscreen_filename_or_google_drive_url:
        return None
    
    # TODO: Check that 'type' is GreenscreenType type

    # We will need the resource filename or google drive url and
    # the image to extract the data from
    RESOURCE_FILENAME = greenscreen_filename_or_google_drive_url
    TMP_FILENAME = greenscreen_filename_or_google_drive_url

    if type == GreenscreenType.IMAGE:
        # We have the final resource and the image to extract data
        if is_google_drive_url(greenscreen_filename_or_google_drive_url):
            google_drive_id = get_id_from_google_drive_url(greenscreen_filename_or_google_drive_url)
            filename = GREENSCREENS_FOLDER + google_drive_id + '/greenscreen.png'
            TMP_FILENAME = get_resource(greenscreen_filename_or_google_drive_url, filename)
    else: # GreenscreenType.VIDEO
        if is_google_drive_url(greenscreen_filename_or_google_drive_url):
            google_drive_id = get_id_from_google_drive_url(greenscreen_filename_or_google_drive_url)
            filename = GREENSCREENS_FOLDER + google_drive_id + '/greenscreen.mp4'
            RESOURCE_FILENAME = get_resource(greenscreen_filename_or_google_drive_url, filename)
            TMP_FILENAME = create_tmp_filename('tmp_gs_autodetect.png')
            get_frame_from_video_by_frame_number(RESOURCE_FILENAME, 0, TMP_FILENAME)

    # TODO: Autodetect and instantiate a Greenscreen
    details = get_greenscreen_area_details(TMP_FILENAME)

    if not details['rgb_color']:
        raise Exception('No automatic greenscreen detected in "' + greenscreen_filename_or_google_drive_url + '". Aborting.')

    greenscreen_filename_or_google_drive_url = GreenscreenDetails(
        greenscreen_areas = [
            GreenscreenAreaDetails(
                rgb_color = details['rgb_color'],
                upper_left_pixel = details['upper_left_pixel'],
                lower_right_pixel = details['lower_right_pixel'],
                frames = None # TODO: Implement a way of handling frames
            )
        ],
        filename_or_google_drive_url = RESOURCE_FILENAME,
        type = type
    )

    return greenscreen_filename_or_google_drive_url