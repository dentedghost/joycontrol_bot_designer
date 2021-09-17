import numpy as np
import pyautogui
from PIL import Image

from scripts.share  import IMAGE_LEFT, IMAGE_TOP

while True:

    left_corner = IMAGE_LEFT + 493
    top_corner = IMAGE_TOP + 410
    im_current = pyautogui.screenshot('images/current_play_car_button.png',
                                      region=(left_corner, top_corner, 40, 40))

    # Load images, convert to RGB, then to numpy arrays and ravel into long, flat things
    current = np.array(Image.open('images/current_play_car_button.png').convert('RGB')).ravel()
    match = np.array(Image.open('images/play_car_button.png').convert('RGB')).ravel()

    # Calculate the sum of the absolute differences divided by number of elements
    image_match_percentage = np.sum(np.abs(np.subtract(current, match, dtype=np.float))) / current.shape[0]
    print(str(image_match_percentage))
    if image_match_percentage < 2:
        print ("Playbutton Found")
