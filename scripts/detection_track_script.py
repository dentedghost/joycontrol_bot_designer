import pyautogui
# from skimage.measure import compare_ssim
# import cv2
import numpy as np
from PIL import Image

from scripts.share  import IMAGE_LEFT, IMAGE_TOP


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
    'cb_beach_landing', 'cb_thundering_start', 'cb_paradise_resort',
    'ci_ancient_wonders',
    'hm_cave_heat', 'hm_downhill_run', 'hm_frozen_route', 'hm_mountain_poles',
    'mw_canyon_launch', 'mw_gold_rush', 'mw_whirlwind_curve',
    'os_budding_start', 'os_industrial_revolution', 'os_kita_run', 'os_moat_finale',
    'os_naniwa_tour', 'os_refined_finish',
    'rm_captial', 'rm_eternal_city', 'rm_pantheon_split', 'rm_saint_peter_kickoff',
    'sf_city_by_the_bay', 'sf_downtown_rise', 'sf_roller_coaster_ride', 'sf_rush_minute',
    'sf_street_of_san_francisco',
    'sf_tunnel_jam', 'sh_pudong_rise',
    'sl_ancient_ruins', 'sl_the_cave', 'sl_path_wind', 'sl_wildlands', ]


track_images = {}

for track in tracks:
    path_plus_track = "images/" + track + ".png"
    # Probably improve performance by capture image_array_into_an_array
    # https://stackoverflow.com/questions/31250129/python-numpy-array-of-numpy-arrays
    match = np.array(Image.open(path_plus_track).convert('RGB')).ravel()
    track_images.update({track: match})


waiting_for_players_image = np.array(Image.open('images/waiting_for_players.png').convert('RGB')).ravel()
track_images.update({'waiting_for_players': waiting_for_players_image})

while True:
    left_corner = IMAGE_LEFT + 65
    top_corner = IMAGE_TOP + 25
    im_current = pyautogui.screenshot('images/current_track_image.png', region=(left_corner, top_corner, 75, 75))
    for track in tracks:
        # before = cv2.imread('current_image.png')
        # after = cv2.imread(track)

        # Load images, convert to RGB, then to numpy arrays and ravel into long, flat things
        current = np.array(Image.open('images/current_track_image.png').convert('RGB')).ravel()


        # Calculate the sum of the absolute differences divided by number of elements
        MAE = np.sum(np.abs(np.subtract(current, track_images[track], dtype=np.float))) / current.shape[0]
        if MAE < 1:
            print(str(MAE) + ' ' + str(track))
        # else:
        #     print(str(MAE) + '+' + str(track))

        # # Convert images to grayscale
        # before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
        # after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)
        #
        # # Compute SSIM between two images
        # (score, diff) = compare_ssim(before_gray, after_gray, full=True)
        # print("Image similarity", score)

    # Check if there's a track we don't have
    left_corner = IMAGE_LEFT + 10
    top_corner = IMAGE_TOP + 10
    im_current = pyautogui.screenshot('images/current_waiting_for_players.png',
                                      region=(left_corner, top_corner, 40, 40))

    # Load images, convert to RGB, then to numpy arrays and ravel into long, flat things
    current = np.array(Image.open('images/current_waiting_for_players.png').convert('RGB')).ravel()


    # Calculate the sum of the absolute differences divided by number of elements
    image_match_percentage = np.sum(np.abs(np.subtract(current,
                                                       track_images['waiting_for_players'],
                                                       dtype=np.float))) / current.shape[0]
    # print(str(image_match_percentage))
    if image_match_percentage < 1:
        print(f'Unknown Track: Use Default')

