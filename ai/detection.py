import pyautogui
# from skimage.measure import compare_ssim
# import cv2
import numpy as np
from PIL import Image


# ffplay -f v4l2 -video_size 640x480 -framerate 60 -i /dev/video0 -left 3000 -top 50 -an -sn -noborder -window_title asphalt9
# 0.0037925925925925926 mw_gold_rush.png
# 0.0 sf_rush_minute.png
# 0.0 os_naniwa_tour.png
# 0.009896296296296297 cb_thundering_start.png
# 0.002074074074074074 sl_ancient_ruins.png
# 0.0 sl_wildlands.png
# 0.0 os_budding_start.png
# 0.0 sl_path_wind.png
# 0.0 hm_downhill_run.png
# 0.0 mw_gold_rush.png
# 0.001362962962962963 sf_city_by_the_bay.png
# 0.0 os_budding_start.png


tracks = [
    'cb_beach_landing.png', 'cb_thundering_start.png',
    'ci_ancient_wonders.png',
    'hm_cave_heat.png', 'hm_downhill_run.png', 'hm_frozen_route.png',
    'mw_canyon_launch.png', 'mw_gold_rush.png', 'mw_whirlwind_curve.png',
    'os_budding_start.png', 'os_industrial_revolution.png', 'os_kita_run.png', 'os_moat_finale.png',
    'os_naniwa_tour.png', 'os_refined_finish.png',
    'rm_captial.png', 'rm_eternal_city.png', 'rm_pantheon_split.png', 'rm_saint_peter_kickoff.png',
    'sf_city_by_the_bay.png', 'sf_downtown_rise.png', 'sf_rush_minute.png', 'sf_tunnel_jam.png',
    'sh_pudong_rise.png',
    'sl_ancient_ruins.png', 'sl_the_cave.png', 'sl_path_wind.png', 'sl_wildlands.png', ]

region_track = (3065, 75, 75, 75)

while True:
    im_current = pyautogui.screenshot('current_image.png', region=(3065, 75, 75, 75))
    for track in tracks:
        # before = cv2.imread('current_image.png')
        # after = cv2.imread(track)

        # Load images, convert to RGB, then to numpy arrays and ravel into long, flat things
        current = np.array(Image.open('current_image.png').convert('RGB')).ravel()
        match = np.array(Image.open(track).convert('RGB')).ravel()

        # Calculate the sum of the absolute differences divided by number of elements
        MAE = np.sum(np.abs(np.subtract(current, match, dtype=np.float))) / current.shape[0]
        if MAE < 1:
            print(str(MAE) + ' ' + str(track))

        # # Convert images to grayscale
        # before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
        # after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)
        #
        # # Compute SSIM between two images
        # (score, diff) = compare_ssim(before_gray, after_gray, full=True)
        # print("Image similarity", score)