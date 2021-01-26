import pyautogui
# from skimage.measure import compare_ssim
# import cv2
import numpy as np
from PIL import Image


while True:
    im_current = pyautogui.screenshot('current_play_center_button.png', region=(3220, 460, 40, 40))

    # Load images, convert to RGB, then to numpy arrays and ravel into long, flat things
    current = np.array(Image.open('current_play_center_button.png').convert('RGB')).ravel()
    match = np.array(Image.open('play_center_button.png').convert('RGB')).ravel()

    # Calculate the sum of the absolute differences divided by number of elements
    MAE = np.sum(np.abs(np.subtract(current, match, dtype=np.float))) / current.shape[0]
#    if MAE < 1:
    print(str(MAE))

