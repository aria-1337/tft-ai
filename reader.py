import easyocr
import os
import mss
from PIL import Image

class Reader:
    def __init__(self):
        self.reader = easyocr.Reader(['en'], detector='dbnet18')

        # Formatted from strings to ints for easier use ("1-1"=11)
        self.stage = 21 #None

        self.galaxy_options = [] 
        self.galaxy = None

        self.gold = 0


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
    

    def get_game_stage(self):
        if self.stage is None or self.stage < 21:
            self.crop('./test/galaxy-picker.png', 820, 0, 870, 35, 'images/stage-number.png') # HARD CODED FOR TESTING
            stage_raw = self.read_image('./images/stage-number.png')
            self.stage = int(stage_raw[0][0] + stage_raw[0][2])
            
            # Invoke galaxy parser
            if self.stage == 11:
                self.get_galaxy_options()

        else:
            self.crop('./test/board.png', 770, 0, 810, 35, 'images/stage-number.png') # HARD CODED FOR TESTING
            stage_raw = self.read_image('./images/stage-number.png')
            self.stage = int(stage_raw[0][0] + stage_raw[0][2])

    def get_galaxy_options(self):
        left = 62
        start_top = 315
        right = 190
        start_bottom = 375

        for i in range(0, 3):
            top = (start_top + (i * 90))
            bottom = (start_bottom + (i * 90))
            self.crop('./test/galaxy-picker.png', left, top, right, bottom, f'images/galaxy-option-{i}.png') # HARD CODED FOR TESTING
            option_raw = self.read_image(f'images/galaxy-option-{i}.png')
            self.galaxy_options.append(option_raw[0])

    def get_augments_and_galaxy(self):
        # TODO: This should get invoked on 1-2, and every augment picking stage, will have to right click boombox and screenshot to get info
        return None

    def get_gold(self):
        self.crop('./test/board.png', 840, 880, 920, 910, 'images/gold.png') # HARD CODED FOR TESTING
        gold_raw = self.read_image('./images/gold.png')
        self.gold = gold_raw
        print(self.gold)

if __name__ == "__main__":
    r = Reader()
    r.get_gold()

