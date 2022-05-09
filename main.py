import pyautogui
import time
import global_data
import const
from hot_key import Hotkey
import screen
import logging


class RunFlag(object):
    START = 1
    CLICK_SHEN_LONG = 2
    QIAN_WANG_SHEN_LONG = 3
    PI_PEI_SHEN_LONG = 4
    ENTER_SHEN_LONG = 5
    GO_POINT = 6
    ATTACK = 7


class ShenLong(object):
    def __init__(self) -> None:
        self._screen_utils = screen.Screen('TCGamer', 'WindowIcon')
        self._flag = RunFlag.GO_POINT
        self._attack_step = 0

    def is_bind(self):
        return self._screen_utils.is_bind()

    def capture(self):
        self._screen_utils.capture()

    def run_once(self):
        if self._flag == RunFlag.START:
            pos = self._screen_utils.get_target_pos('huo_dong.bmp', 0.01)
            if pos is not None:
                self._screen_utils.click(pos[0] + 10, pos[1] + 10)
                self._flag = RunFlag.CLICK_SHEN_LONG

        elif self._flag == RunFlag.CLICK_SHEN_LONG:
            pos = self._screen_utils.get_target_pos('shen_long_pan.png')
            if pos is not None:
                self._screen_utils.click(pos[0] + 10, pos[1] + 10)
                self._flag = RunFlag.QIAN_WANG_SHEN_LONG

        elif self._flag == RunFlag.QIAN_WANG_SHEN_LONG:
            pos = self._screen_utils.get_target_pos('qian_wang.png')
            if pos is not None:
                self._screen_utils.click(pos[0] + 10, pos[1] + 10)
                self._flag = RunFlag.PI_PEI_SHEN_LONG

            else:
                self._flag = RunFlag.CLICK_SHEN_LONG

        elif self._flag == RunFlag.PI_PEI_SHEN_LONG:
            pos = self._screen_utils.get_target_pos('pi_pei.png')
            if pos is not None:
                self._screen_utils.click(pos[0] + 10, pos[1] + 10)
                self._flag = RunFlag.ENTER_SHEN_LONG

        elif self._flag == RunFlag.ENTER_SHEN_LONG:
            pos = self._screen_utils.get_target_pos('jin_ru.png')
            if pos is not None:
                self._screen_utils.click(pos[0] + 10, pos[1] + 10)
                self._flag = RunFlag.GO_POINT

        elif self._flag == RunFlag.GO_POINT:
            pos = self._screen_utils.get_target_pos('shen_long1.png')
            pos2 = self._screen_utils.get_target_pos('shen_long2.png')
            confirm_pos = self._screen_utils.get_target_pos('que_ding.png')
            if pos is not None:
                self._screen_utils.click(1469, 348)
                self._attack_step = 0
                self._flag = RunFlag.ATTACK

            elif pos2 is not None:
                self._screen_utils.click(1469, 348)
                self._attack_step = 0
                self._flag = RunFlag.ATTACK

            elif confirm_pos is not None:
                self._screen_utils.click(confirm_pos[0] + 10, confirm_pos[1] + 10)
                self._flag = RunFlag.START

        elif self._flag == RunFlag.ATTACK:
            self._screen_utils.click(1617, 874)
            self._attack_step += 1
            if self._attack_step == 3:
                self._flag = RunFlag.GO_POINT

        logging.INFO(self._flag)

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

        shenlong.capture()
        shenlong.run_once()
        time.sleep(1)

if __name__ == '__main__':
    logging.basicConfig(filename='auto.log', level = getattr(logging, 'DEBUG'), format='%(levelname)s %(asctime)s %(message)s')
    global_data.GAME_STATE = const.GameState.RUNNING
    hotkey = Hotkey()
    hotkey.start()
    main()

    hotkey.join()
    # print(user32.RegisterHotKey(None, ID1, 0, win32con.VK_F10))
    # auto_go()
    # auto_shen_long_pan_one_turn()
