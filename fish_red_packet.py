import pyautogui
import time
import global_data
import const
from hot_key import Hotkey
import screen
import logging
import utils
import sys


class RunFlag(object):
    START = 1


class ShenLong(object):
    def __init__(self) -> None:
        if global_data.IS_GLOBAL:
            self._screen_utils = screen.Screen('玄中记', 'Chrome_WidgetWin')
        else:
            self._screen_utils = screen.Screen('TCGamer', 'WindowIcon')
        self._flag = RunFlag.START
        self._attack_step = 0

    def is_bind(self):
        return self._screen_utils.is_bind()

    def capture(self):
        if global_data.IS_GLOBAL:
            self._screen_utils.capture_global()
        else:
            self._screen_utils.capture()

    def run_once(self):
        if self._flag == RunFlag.START:
            self._screen_utils.click(425, 361)

        utils.INFO(self._flag)

def main():
    #auto_go()
    shenlong = ShenLong()
    if not shenlong.is_bind():
        return

    while 1:
        if global_data.GAME_STATE == const.GameState.PAUSE:
            time.sleep(1)
            continue

        elif global_data.GAME_STATE == const.GameState.EXIT:
            break

        # shenlong.capture()
        shenlong.run_once()
        time.sleep(0.25)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        global_data.IS_GLOBAL = int(sys.argv[1])
    else:
        global_data.IS_GLOBAL = 0

    logging.basicConfig(filename='auto.log', level = getattr(logging, 'DEBUG'), format='%(levelname)s %(asctime)s %(message)s')
    global_data.GAME_STATE = const.GameState.RUNNING

    if global_data.IS_GLOBAL:
        hotkey = Hotkey()
        hotkey.start()
        main()
        hotkey.join()
    else:
        main()
    # print(user32.RegisterHotKey(None, ID1, 0, win32con.VK_F10))
    # auto_go()
    # auto_shen_long_pan_one_turn()
