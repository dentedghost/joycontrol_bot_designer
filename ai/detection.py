import pyautogui
from skimage.measure import compare_ssim
import cv2
import numpy as np

tracks = ['mw_gold_rush.png', 'mw_whirlwind_curve.png',
          'sh_pudong_rise.png',
          'os_kita_run.png', 'os_naniwa_tour.png', 'os_budding_start.png'
          'sf_downtown_rise.png', 'sf_city_by_the_bay.png',
          'sl_wildlands.png', 'sl_path_wind.png']

region_track = (3065, 75, 75, 75)

while True:
    im_current = pyautogui.screenshot('current_image.png', region=(3065, 75, 75, 75))
    for track in tracks:
        before = cv2.imread('current_image.png')
        after = cv2.imread(track)

        # Convert images to grayscale
        before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
        after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)

        # Compute SSIM between two images
        (score, diff) = compare_ssim(before_gray, after_gray, full=True)
        print("Image similarity", score)