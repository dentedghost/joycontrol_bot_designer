import pyautogui
import sys

if len(sys.argv[1]):
    image_name = sys.argv[1] + ".png"
else:
    image_name = 'test.png'

im1 = pyautogui.screenshot(image_name, region=(3000, 50, 640, 480))

