import pyautogui
# from skimage.measure import compare_ssim
# import cv2
import numpy as np
from PIL import Image

# im_base = pyautogui.screenshot(image_name, region=(3000, 50, 640, 480))
while True:
    im_current = pyautogui.screenshot('current_claim_button.png', region=(3250, 370, 40, 40))

    # Load images, convert to RGB, then to numpy arrays and ravel into long, flat things
    current = np.array(Image.open('current_claim_button.png').convert('RGB')).ravel()
    match = np.array(Image.open('claim_button.png').convert('RGB')).ravel()

    # Calculate the sum of the absolute differences divided by number of elements
    MAE = np.sum(np.abs(np.subtract(current, match, dtype=np.float))) / current.shape[0]
#    if MAE < 1:
    print(str(MAE))
