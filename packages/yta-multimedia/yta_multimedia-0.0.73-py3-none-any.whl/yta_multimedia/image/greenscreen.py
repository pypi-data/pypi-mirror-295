from typing import Union
from yta_general_utils.type_checker import variable_is_type

import cv2
import numpy as np
import skimage.exposure

def remove_greenscreen_from_image(image_filename: Union[str, cv2.typing.MatLike], output_filename: str):
    """
    This methods gets a greenscreen image (one with lots of uniform
    green pixels), does some modifications and replaces the green
    pixels with transparent pixels (due to alpha channel).
    """
    # Found here: https://stackoverflow.com/questions/51719472/remove-green-background-screen-from-image-using-opencv-python
    if not image_filename:
        return None
    
    img = image_filename
    if variable_is_type(image_filename, str):
        # TODO: Implement 'file_is_image_file' when available
        img = cv2.imread(image_filename)

    # TODO: This is not working, it raises
    # TypeError: Subscripted generics cannot be used with class and instance checks
    # if not variable_is_type(img, cv2.typing.MatLike):
    #     # TODO: Raise Exception
    #     return None

    # 1. Perform a basic masking
    # Convert the image to LAB space
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    # Threshold the alpha channel to isolate green background
    a_channel = lab[:, :, 1]
    th = cv2.threshold(a_channel, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Mask the original image with binary mask
    masked = cv2.bitwise_and(img, img, mask = th)    # contains dark background
    m1 = masked.copy()
    m1[th == 0] = (255, 255, 255)                    # contains white background

    # 2. Remove green shade along the border
    # Convert masked image to LAB space
    mlab = cv2.cvtColor(masked, cv2.COLOR_BGR2LAB)

    # Normalize the alph achannel mlab[:, :, 1] to use the 
    # entire intensity range between [0 - 255]
    dst = cv2.normalize(mlab[:, :, 1], dst = None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_8U)

    # Green color represents the lower end of the range [0-255] 
    # while red color represents the higher end in the a-channel
    threshold_value = 100
    dst_th = cv2.threshold(dst, threshold_value, 255, cv2.THRESH_BINARY_INV)[1]

    # Set intensity value in the a-channel of the selected pixels to 127
    mlab2 = mlab.copy()
    mlab[:, :, 1][dst_th == 255] = 127

    # Convert the image to BGRA and the pixels that were dark we 
    # transform to green but with max alpha to be transparent
    img2 = cv2.cvtColor(mlab, cv2.COLOR_LAB2BGR)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2BGRA)
    # We add the alpha channel
    img2[th == 0] = (0, 255, 0, 0)

    if output_filename:
        cv2.imwrite(output_filename, img2)

    # Check this, is interesting: https://stackoverflow.com/questions/44290606/alpha-masking-a-non-square-region-python-cv2

    return img
    
def remove_greenscreen_from_image_with_blur(image_filename: str, output_filename: str):
    """
    This methods gets a greenscreen image (one with lots of uniform
    green pixels), does some modifications and replaces the green
    pixels with transparent pixels (due to alpha channel).

    The result is worse in the test cases than the 
    'remove_greenscreen_from_image' method.
    """
    # Found here: https://stackoverflow.com/questions/51719472/remove-green-background-screen-from-image-using-opencv-python
    if not image_filename:
        return None

    img = image_filename
    if variable_is_type(image_filename, str):
        # TODO: Implement 'file_is_image_file' when available
        img = cv2.imread(image_filename)

    # TODO: This is not working, it raises
    # TypeError: Subscripted generics cannot be used with class and instance checks
    # if not variable_is_type(img, cv2.typing.MatLike):
    #     # TODO: Raise Exception
    #     return None

    # Convert to LAB
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    # Extract A channel
    A = lab[:, :, 1]

    # Threshold A channel
    thresh = cv2.threshold(A, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Blur threshold image
    blur = cv2.GaussianBlur(thresh, (0, 0), sigmaX = 5, sigmaY = 5, borderType = cv2.BORDER_DEFAULT)

    # Stretch so that 255 -> 255 and 127.5 -> 0
    mask = skimage.exposure.rescale_intensity(blur, in_range = (127.5, 255), out_range = (0, 255)).astype(np.uint8)

    # Add mask to image as alpha channel
    result = img.copy()
    result = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    result[:, :, 3] = mask

    if output_filename:
        cv2.imwrite(output_filename, result)

    return result