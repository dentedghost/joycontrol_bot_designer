import pyautogui
import sys


# from share import IMAGE_LEFT, IMAGE_TOP
IMAGE_LEFT = 3000
IMAGE_TOP = 50

if len(sys.argv[1]):
    image_name = sys.argv[1] + ".png"
else:
    image_name = 'test.png'

im1 = pyautogui.screenshot(image_name, region=(3000, 50, 640, 480))

