import logging.config
import numpy as np
import pyautogui
from PIL import Image
import time

from scripts.share  import IMAGE_LEFT, IMAGE_TOP

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})


def script():

    pil_logger = logging.getLogger('PIL')
    pil_logger.setLevel(logging.INFO)

    start_time = time.time()
    seconds = 30

    print("Inside detection claim button")
    match = np.array(Image.open('scripts/images/claim_button.png').convert('RGB')).ravel()
    match_play_center_button = np.array(Image.open('scripts/images/play_center_button.png').convert('RGB')).ravel()

    while True:

        current_time = time.time()
        elapsed_time = current_time - start_time
        print(f'elapsed time {elapsed_time}')

        if elapsed_time > seconds:
            print("Finished iterating in: " + str(int(elapsed_time)) + " seconds")
            return False

        # Load images, convert to RGB, then to numpy arrays and ravel into long, flat things
        left_corner = IMAGE_LEFT + 250
        top_corner = IMAGE_TOP + 320
        im_current = pyautogui.screenshot('scripts/images/current_claim_button.png',
                                          region=(left_corner, top_corner, 40, 40))
        current = np.array(Image.open('scripts/images/current_claim_button.png').convert('RGB')).ravel()


        # Calculate the sum of the absolute differences divided by number of elements
        image_match_percentage = np.sum(np.abs(np.subtract(current, match, dtype=np.float))) / current.shape[0]
        if image_match_percentage < 2:
            return True

        # Now check if the center button is displayed so we can skip
        left_corner = IMAGE_LEFT + 140
        top_corner = IMAGE_TOP + 270
        im_current = pyautogui.screenshot('scripts/images/current_play_center_button.png',
                                          region=(left_corner, top_corner, 25, 25))
        current = np.array(Image.open('scripts/images/current_play_center_button.png').convert('RGB')).ravel()

        # Calculate the sum of the absolute differences divided by number of elements
        image_match_percentage = np.sum(
            np.abs(np.subtract(current, match_play_center_button, dtype=np.float))) / current.shape[0]
        print(str(image_match_percentage))
        if image_match_percentage < 2:
            return False
