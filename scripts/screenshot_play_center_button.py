import pyautogui
import sys

if len(sys.argv[1]):
    image_name = 'images/' + sys.argv[1] + ".png"
else:
    image_name = 'test.png'

# im_base = pyautogui.screenshot(image_name, region=(3000, 50, 640, 480))
next_button = pyautogui.screenshot(image_name, region=(3279, 460, 25, 25))
