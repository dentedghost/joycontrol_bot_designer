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
    seconds = 300

    print("Inside detection_next_button_long")
    match = np.array(Image.open('scripts/images/next_button.png').convert('RGB')).ravel()

    while True:

        current_time = time.time()
        elapsed_time = current_time - start_time
        print(f'elapsed time {elapsed_time}')

        if elapsed_time > seconds:
            print("Finished iterating in: " + str(int(elapsed_time)) + " seconds")
            return False

        # Load images, convert to RGB, then to numpy arrays and ravel into long, flat things
        left_corner = IMAGE_LEFT + 460
        top_corner = IMAGE_TOP + 410
        im_current = pyautogui.screenshot('scripts/images/current_next_button.png',
                                          region=(left_corner, top_corner, 40, 40))
        current = np.array(Image.open('scripts/images/current_next_button.png').convert('RGB')).ravel()


        # Calculate the sum of the absolute differences divided by number of elements
        image_match_percentage = np.sum(np.abs(np.subtract(current, match, dtype=np.float))) / current.shape[0]
        print(str(image_match_percentage))
        if image_match_percentage < 7:
            return True
