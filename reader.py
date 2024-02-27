import easyocr
import time
import os
import mss
from game_controller import Game_Controller
from PIL import Image

class Reader:
    def __init__(self):
        # Game controller (to get information only available via mouse/keyboard navigation)
        self.gc = Game_Controller()
        self.game_positions = {}
        self.generate_position_matrix()

        # This thing is relatively good, but it still needs to be trained or we need to normalize
        self.reader = easyocr.Reader(['en'], detector='dbnet18')

        # Formatted from strings to ints for easier use ("1-1"=11)
        self.stage = 21 #None

        self.galaxy_options = [] 
        self.galaxy = None

        self.gold = 0

    def generate_position_matrix(self):
        # UNITS, TODO: Can probably make this neater
        self.game_positions['units'] = []
        x_offset = 135
        row1_x_start = 570
        row1_y = 660
        row1 = []
        row2_x_start = 535
        row2_y = 590
        row2 = []
        row3_x_start = 600
        row3_y = 500
        row3 = []
        row4_x_start = 560
        row4_y = 420
        row4 = []
        for i in range(0, 7):
            x1 = row1_x_start + (i * x_offset)
            x2 = row2_x_start + (i * x_offset-40)
            x3 = row3_x_start + (i * x_offset-50)
            x4 = row4_x_start + (i * x_offset-60)
            row1.append([x1, row1_y])
            row2.append([x2, row2_y])
            row3.append([x3, row3_y])
            row4.append([x4, row4_y])

        self.game_positions['units'].append(row1)
        self.game_positions['units'].append(row2)
        self.game_positions['units'].append(row3)
        self.game_positions['units'].append(row4)

    def read_image(self, path):
        prediction = self.reader.recognize(path, detail=0)
        return prediction


    def screenshot(self, top, left, width, height, path='images/screenshot.png'):
        with mss.mss() as sct:
            monitor = {"top": top, "left": left, "width": width, "height": height}
            output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

            sct_img = sct.grab(monitor)

            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
            os.rename(output, path)

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
    time.sleep(3)
    r = Reader()
