import numpy as np
import pyautogui
from PIL import Image
import time


def script():
    print(f'Inside detection_waiting_for_players')
    start_time = time.time()
    seconds = 35

    # performance
    match = np.array(Image.open('ai/waiting_for_players.png').convert('RGB')).ravel()

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        # print(f'elapsed time waiting  {elapsed_time}')

        if elapsed_time > seconds:
            print("Finished iterating in: " + str(int(elapsed_time)) + " seconds")
            return False
        else:

            im_current = pyautogui.screenshot('ai/current_waiting_for_players.png', region=(3010, 60, 40, 40))

            # Load images, convert to RGB, then to numpy arrays and ravel into long, flat things
            current = np.array(Image.open('ai/current_waiting_for_players.png').convert('RGB')).ravel()

            # Calculate the sum of the absolute differences divided by number of elements
            image_match_percentage = np.sum(np.abs(np.subtract(current, match, dtype=np.float))) / current.shape[0]
            # print(str(image_match_percentage))
            if image_match_percentage < 1:
                break

    # Now wait for it to go away
    print(f'Inside detection_waiting_for_players: start race')
    start_time = time.time()
    seconds = 20

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        # print(f'elapsed time starting  {elapsed_time}')

        if elapsed_time > seconds:
            print("Finished iterating in: " + str(int(elapsed_time)) + " seconds")
            return False
        else:

            im_current = pyautogui.screenshot('ai/current_waiting_for_players.png', region=(3010, 60, 40, 40))

            # Load images, convert to RGB, then to numpy arrays and ravel into long, flat things
            current = np.array(Image.open('ai/current_waiting_for_players.png').convert('RGB')).ravel()

            # Calculate the sum of the absolute differences divided by number of elements
            image_match_percentage = np.sum(np.abs(np.subtract(current, match, dtype=np.float))) / current.shape[0]
            # print(str(image_match_percentage))
            if image_match_percentage > 1:
                print(f'START RACE')
                return True
