import pyautogui

# 0,0->1919,1079 based display
class Game_Controller:
    def __init__(self):
        self.mouse_pos = []
        self.set_mouse_pos(1, 1)

    def set_mouse_pos(self, x, y):
        pyautogui.moveTo(x, y)
        self.mouse_pos = [x, y]

    def click(self, x, y, type):
        self.set_mouse_pos(x, y)
        pyautogui.click(button=type)

    def click_and_drag(self, fromXY, toXY):
        self.set_mouse_pos(fromXY[0], fromXY[1])
        pyautogui.mouseDown();
        pyautogui.mouseUp(x = toXY[0], y= toXY[1])

    def key_press(self, key):
        pyautogui.press(key)
