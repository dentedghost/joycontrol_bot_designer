import logging.config
import numpy as np
import pyautogui
from PIL import Image
import time

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})


def script():

    pil_logger = logging.getLogger('PIL')
    pil_logger.setLevel(logging.INFO)

    start_time = time.time()
    seconds = 60

    print("Inside detection_play center_button z")
    match = np.array(Image.open('scripts/images/play_center_button.png').convert('RGB')).ravel()

    while True:

        current_time = time.time()
        elapsed_time = current_time - start_time
        print(f'elapsed time {elapsed_time}')

        if elapsed_time > seconds:
            print("Finished iterating in: " + str(int(elapsed_time)) + " seconds")
            return False

        # Load images, convert to RGB, then to numpy arrays and ravel into long, flat things
        im_current = pyautogui.screenshot('scripts/images/current_play_center_button.png', region=(3279, 460, 25, 25))
        current = np.array(Image.open('scripts/images/current_play_center_button.png').convert('RGB')).ravel()


        # Calculate the sum of the absolute differences divided by number of elements
        image_match_percentage = np.sum(np.abs(np.subtract(current, match, dtype=np.float))) / current.shape[0]
        print(str(image_match_percentage))
        if image_match_percentage < 2:
            return True