import pyautogui
# from skimage.measure import compare_ssim
# import cv2
import numpy as np
from PIL import Image


while True:
    im_current = pyautogui.screenshot('current_waiting_for_players.png', region=(3010, 60, 40, 40))

    # Load images, convert to RGB, then to numpy arrays and ravel into long, flat things
    current = np.array(Image.open('current_waiting_for_players.png').convert('RGB')).ravel()
    match = np.array(Image.open('waiting_for_players.png').convert('RGB')).ravel()

    # Calculate the sum of the absolute differences divided by number of elements
    MAE = np.sum(np.abs(np.subtract(current, match, dtype=np.float))) / current.shape[0]
#    if MAE < 1:
    print(str(MAE))

