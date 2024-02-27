import easyocr
import os
from mss import mss

class Reader:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])

        # galaxy-picker | my-board | augment-selection | enemy-board | item-picker | game-end 
        # Games always start on galaxy-picker
        self.game_state = "galaxy-picker"

    def update_game_state(self, new_state):
        self.game_state = new_state

    def read_image(self, path):
        prediction = self.reader.recognize(path, detail=0)
        return prediction

    # Idk if cropping would be faster than taking individual segments...
    def screenshot_area(self, top, left, width, height, name):
        with mss.mss() as sct:
            monitor = {"top": top, "left": left, "width": width, height: height}
            output = "sct-{top}x{left}_{width}x{height}.png".format(**mointor)

            sct_img = sct.grab(mointor)

            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
            os.rename(output, name)
