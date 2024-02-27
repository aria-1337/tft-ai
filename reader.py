import easyocr
import os
import mss
from PIL import Image

class Reader:
    def __init__(self):
        self.reader = easyocr.Reader(['en'], detector='dbnet18')

        # galaxy_picker | my_board | augment_selection | enemy_board | item_picker | game_end 
        # This data is obtained via the stage number at the top
        self.game_state = 'galaxy_picker'

        # formatted to an int for easier usage 1-1=11, 2-4=24...
        self.stage = 21 #None

    
    def get_game_stage(self):
        if self.stage is None or self.stage < 21:
            self.crop('./test/galaxy-picker.png', 820, 0, 870, 35, 'images/stage-number.png') # HARD CODED FOR TESTING
            stage_raw = self.read_image('./images/stage-number.png')
            self.stage = int(stage_raw[0][0] + stage_raw[0][2])
        else:
            self.crop('./test/board.png', 770, 0, 810, 35, 'images/stage-number.png')
            stage_raw = self.read_image('./images/stage-number.png')
            self.stage = int(stage_raw[0][0] + stage_raw[0][2])

    def read_image(self, path):
        prediction = self.reader.recognize(path, detail=0)
        return prediction


    def screenshot(self):
        with mss.mss() as sct:
            monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
            output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

            sct_img = sct.grab(monitor)

            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
            os.rename(output, 'images/screenshot.png')

    def crop(self, read_path, left, top, right, bottom, save_path):
        im = Image.open(read_path)
        im1 = im.crop((left, top, right, bottom))
        im1.save(save_path)

if __name__ == "__main__":
    r = Reader()
    r.get_game_stage()
