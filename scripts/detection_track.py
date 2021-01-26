import logging.config
import pyautogui
import numpy as np
from PIL import Image
import time

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})


def script():

    pil_logger = logging.getLogger('PIL')
    pil_logger.setLevel(logging.INFO)
    print("Inside detection_track")

    start_time = time.time()
    seconds = 180
    track_name = ''

    image_path = "scripts/images/"

    tracks = [
        'cb_beach_landing', 'cb_thundering_start', 'cb_paradise_resort', 'cb_pier_pressure',
        'ci_ancient_wonders', 'ci_nile_river', 'ci_thousand_minarets',
        'hm_cave_heat', 'hm_downhill_run', 'hm_frozen_route', 'hm_mountain_poles',
        'mw_canyon_launch', 'mw_gold_rush', 'mw_transcontinental_race', 'mw_whirlwind_curve',
        'os_budding_start', 'os_industrial_revolution', 'os_kita_run', 'os_moat_finale',
        'os_naniwa_tour', 'os_refined_finish',
        'rm_ancient_rome', 'rm_capital_of_the_world', 'rm_eternal_city', 'rm_pantheon_split', 'rm_saint_peter_kickoff',
        'rm_tiber_stream',
        'sf_city_by_the_bay', 'sf_downtown_rise', 'sf_roller_coaster_ride', 'sf_rush_minute',
        'sf_street_of_san_francisco', 'sf_tunnel_jam',
        'sh_nanjing_stroll', 'sh_the_pearl_of_orient', 'sh_pudong_rise', 'sh_shen_city',
        'sl_ancient_ruins', 'sl_the_cave', 'sl_path_wind', 'sl_wildlands', ]

    track_images = {}

    for track in tracks:
        path_plus_track = image_path + track + ".png"
        # Probably improve performance by capture image_array_into_an_array
        # https://stackoverflow.com/questions/31250129/python-numpy-array-of-numpy-arrays
        match = np.array(Image.open(path_plus_track).convert('RGB')).ravel()
        track_images.update({track: match})

    waiting_for_players_expected_image = image_path + 'waiting_for_players' + ".png"
    waiting_for_players_image = np.array(Image.open(waiting_for_players_expected_image).convert('RGB')).ravel()
    track_images.update({'waiting_for_players': waiting_for_players_image})

    current_track_expected_image = image_path + 'current_track_image' + ".png"
    current_waiting_for_players_expected_image = image_path + 'current_waiting_for_players' + ".png"

    detected_track = False
    detected_track_name = ''

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        print(f'elapsed time {elapsed_time}')

        if elapsed_time > seconds and not detected_track:
            print("Finished iterating in: " + str(int(elapsed_time)) + " seconds")
            return 'default'

        # Load images, convert to RGB, then to numpy arrays and ravel into long, flat things
        im_current = pyautogui.screenshot(current_track_expected_image, region=(3065, 75, 75, 75))
        current = np.array(Image.open(current_track_expected_image).convert('RGB')).ravel()

        for track in tracks:

            # Calculate the sum of the absolute differences divided by number of elements
            image_match_percentage = np.sum(np.abs(np.subtract(current, track_images[track], dtype=np.float))) / current.shape[0]

            if image_match_percentage < 1:
                print(str(image_match_percentage) + ' ' + str(track))
                detected_track_name = track
                detected_track = True
                break

        if detected_track:
            break

        # print(f'Check if no track')
        # Check if there's a track we don't have
        im_current = pyautogui.screenshot(current_waiting_for_players_expected_image, region=(3010, 60, 40, 40))

        # Load images, convert to RGB, then to numpy arrays and ravel into long, flat things
        current = np.array(Image.open(current_waiting_for_players_expected_image).convert('RGB')).ravel()

        # Calculate the sum of the absolute differences divided by number of elements
        image_match_percentage = np.sum(np.abs(np.subtract(current,
                                                           track_images['waiting_for_players'],
                                                           dtype=np.float))) / current.shape[0]
        # print(str(image_match_percentage))
        if image_match_percentage < 1:
            print(f'Unknown Track: Use Default')
            detected_track_name = 'default'
            detected_track = True
            break

    print("Check for end of waiting after sleeping")
    time.sleep(10)
    while True:
        # current_time = time.time()
        # elapsed_time = current_time - start_time
        # # print(f'elapsed time waiting  {elapsed_time}')
        #
        # if elapsed_time > seconds:
        #     print("Finished iterating in: " + str(int(elapsed_time)) + " seconds")
        #     return False
        # else:

        # Check if there's a track we don't have
        im_current = pyautogui.screenshot(current_waiting_for_players_expected_image, region=(3010, 60, 40, 40))

        # Load images, convert to RGB, then to numpy arrays and ravel into long, flat things
        current = np.array(Image.open(current_waiting_for_players_expected_image).convert('RGB')).ravel()

        # Calculate the sum of the absolute differences divided by number of elements
        image_match_percentage = np.sum(np.abs(np.subtract(current,
                                                           track_images['waiting_for_players'],
                                                           dtype=np.float))) / current.shape[0]
        # print(str(image_match_percentage))
        if image_match_percentage > 1:
            print(f'Start the races')
            break

    return detected_track_name
