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
        'cb_hell_vale', 'cb_hotel_road', 'cb_islet_race', 'cb_resort_dash',
        'ci_a_kings_revival', 'ci_gezira_island', 'ci_subterranean_dash', 'ci_cairo_tower_finish',
        'hm_freefall', 'hm_landslide', 'hm_leap_of_faith', 'hm_snow_vault',
        'mw_trainspotter',
        'os_namba_park', 'os_rat_race', 'os_sakura_castle',
        'rm_bread_and_circuses', 'rm_roman_byroads', 'rm_tiber_cross',
        'sf_city_dash', 'sf_railroad_bustle', 'sf_the_tunnel', 'sf_waterslide',
        'sh_double_roundabout', 'sh_future_road', 'sh_reach_for_the_sky', 'sh_paris_of_the_east',
        'sl_the_enchanted_island', 'sl_rocky_valley',
        ]

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
