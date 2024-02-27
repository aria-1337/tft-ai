import os
import mss
import time

time.sleep(4)
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)

with mss.mss() as sct:
    monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
    output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

    sct_img = sct.grab(monitor)

    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    os.rename(output, f'test/x-{current_time}')

