import pyautogui
import sys

from scripts.share  import IMAGE_LEFT, IMAGE_TOP

if len(sys.argv[1]):
    image_name = sys.argv[1] + ".png"
else:
    image_name = 'test.png'

# im_base = pyautogui.screenshot(image_name, region=(3000, 50, 640, 480))
next_button = pyautogui.screenshot(image_name, region=(3250, 370, 40, 40))
