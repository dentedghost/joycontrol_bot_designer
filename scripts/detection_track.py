import logging.config
import pyautogui
import numpy as np
from PIL import Image
import time

from scripts.share  import IMAGE_LEFT, IMAGE_TOP

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})


def script():

    pil_logger = logging.getLogger('PIL')
    pil_logger.setLevel(logging.INFO)
    print("Inside detection_track")

    start_time = time.time()
    seconds = 90
    track_name = ''

    image_path = "scripts/images/"

    tracks = [
        'ak_starting_grid', 'ak_auckland_track', 'ak_straights_and_hairpins', 'ak_industrial_run', 'ak_out_of_bounds',
        'cb_beach_landing', 'cb_paradise_resort', 'cb_pier_pressure', 'cb_thundering_start',
        'ci_ancient_wonders', 'ci_nile_river', 'ci_thousand_minarets',
        'hm_cave_heat', 'hm_downhill_run', 'hm_frozen_route', 'hm_mountain_poles',
        'mw_canyon_launch', 'mw_gold_rush', 'mw_transcontinental_race', 'mw_whirlwind_curve',
        'ny_the_city_that_never_sleeps', 'ny_leaps_and_bounds', 'ny_subway_surfing', 'ny_uptown', 'ny_quantum_jumps',
        "nv_dam_buster", "nv_desert_drift", "nv_desert_run", 'nv_long_run', "nv_the_curve",
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

    loading_race_expected_image = image_path + 'loading_race' + ".png"
    loading_race_image = np.array(Image.open(loading_race_expected_image).convert('RGB')).ravel()
    track_images.update({'loading_race': loading_race_image})

    waiting_for_players_expected_image = image_path + 'waiting_for_players' + ".png"
    waiting_for_players_image = np.array(Image.open(waiting_for_players_expected_image).convert('RGB')).ravel()
    track_images.update({'waiting_for_players': waiting_for_players_image})

    current_loading_race_image = image_path + 'current_loading_race' + ".png"
    current_track_expected_image = image_path + 'current_track_image' + ".png"
    current_waiting_for_players_expected_image = image_path + 'current_waiting_for_players' + ".png"

    detected_loading_race = False
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
        left_corner = IMAGE_LEFT + 65
        top_corner = IMAGE_TOP + 25
        im_current = pyautogui.screenshot(current_track_expected_image, region=(left_corner, top_corner, 75, 75))
        current = np.array(Image.open(current_track_expected_image).convert('RGB')).ravel()
        # TODO increament track and if no match save into possible tracks, maybe time stamp or move into directory
        #  maybe delete
        for track in tracks:

            # Calculate the sum of the absolute differences divided by number of elements
            image_match_percentage = np.sum(np.abs(np.subtract(current, track_images[track], dtype=np.float))) / current.shape[0]

            if image_match_percentage < 2:
                print(str(image_match_percentage) + ' ' + str(track))
                detected_track_name = track
                detected_track = True
                break

        if detected_track:
            break

        # print(f'Check if no track')
        # Check if there's a track we don't have
        left_corner = IMAGE_LEFT + 10
        top_corner = IMAGE_TOP + 10
        im_current = pyautogui.screenshot(current_loading_race_image, region=(left_corner, top_corner, 40, 40))

        # Load images, convert to RGB, then to numpy arrays and ravel into long, flat things
        current = np.array(Image.open(current_loading_race_image).convert('RGB')).ravel()

        # Calculate the sum of the absolute differences divided by number of elements
        image_match_percentage = np.sum(np.abs(np.subtract(current,
                                                           track_images['loading_race'],
                                                           dtype=np.float))) / current.shape[0]
        # print(str(image_match_percentage))
        if image_match_percentage < 2:
            detected_loading_race = True
        elif detected_loading_race:
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
        left_corner = IMAGE_LEFT + 10
        top_corner = IMAGE_TOP + 10
        im_current = pyautogui.screenshot(current_waiting_for_players_expected_image,
                                          region=(left_corner, top_corner, 40, 40))

        # Load images, convert to RGB, then to numpy arrays and ravel into long, flat things
        current = np.array(Image.open(current_waiting_for_players_expected_image).convert('RGB')).ravel()

        # Calculate the sum of the absolute differences divided by number of elements
        image_match_percentage = np.sum(np.abs(np.subtract(current,
                                                           track_images['waiting_for_players'],
                                                           dtype=np.float))) / current.shape[0]
        # print(str(image_match_percentage))
        if image_match_percentage > 2:
            print(f'Start the races')
            break

    return detected_track_name
