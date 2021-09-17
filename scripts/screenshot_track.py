import pyautogui
import sys

from scripts.share  import IMAGE_LEFT, IMAGE_TOP

if len(sys.argv[1]):
    image_name = 'images/' + sys.argv[1] + ".png"
else:
    image_name = 'test.png'

# im1 = pyautogui.screenshot(image_name, region=(3000, 50, 640, 480))
im2 = pyautogui.screenshot(image_name, region=(3065, 75, 75, 75))
