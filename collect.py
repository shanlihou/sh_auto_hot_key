import pyautogui
import time
import global_data
import const
from hot_key import Hotkey
import screen
import logging
import utils
import sys
import functools


class RunFlag(object):
    START = 1
    EXCHANGE = 2
    FAVO = 3
    SHENG_HUO = 4
    SHENG_HUO_TAB = 5
    SEARCH = 6
    COLLECT = 7
    COLLECT_WAIT = 8
    FIX = 9


@functools.lru_cache(100)
def get_flag_name(flag_id):
    for k, v in RunFlag.__dict__.items():
        if flag_id == v:
            return k


class Collect(object):
    def __init__(self) -> None:
        if global_data.IS_GLOBAL:
            self._screen_utils = screen.Screen('玄中记', 'Chrome_WidgetWin')
        else:
            self._screen_utils = screen.Screen('TCGamer', 'WindowIcon')
        self._flag = RunFlag.START
        self._attack_step = 0
        self._collect_png = 'zi_su.png'
        self._search_time_out = 60
        self._wait_time_out = 3
        self._time_out = 5
        self._cache_dic = {}

    def is_bind(self):
        return self._screen_utils.is_bind()

    def capture(self):
        if global_data.IS_GLOBAL:
            self._screen_utils.capture_global()
        else:
            self._screen_utils.capture()

    def run_once(self):
        if self._flag == RunFlag.START:
            pos = self._screen_utils.get_target_pos('jiao_yi.png', 0.05)
            left_pos = self._screen_utils.get_target_pos('zuo_la.png', 0.1)

            if pos is not None:
                self._screen_utils.click(pos[0] + 10, pos[1] + 10)
                self._flag = RunFlag.EXCHANGE

            elif left_pos is not None:
                self._screen_utils.click(left_pos[0] + 10, left_pos[1] + 10)

        elif self._flag == RunFlag.EXCHANGE:
            pos = self._screen_utils.get_target_pos('guan_zhu.png', 0.05)
            if pos is not None:
                self._screen_utils.click(pos[0] + 10, pos[1] + 10)
                self._flag = RunFlag.FAVO
                self._time_out = 5
        
        elif self._flag == RunFlag.FAVO:
            self._time_out -= 1
            pos = self._screen_utils.get_target_pos(self._collect_png, 0.01)
            get_pos = self._screen_utils.get_target_pos('huo_qu.png', 0.02)
            if self._time_out <= 0:
                self._flag = RunFlag.FIX

            elif get_pos:
                self._screen_utils.click(get_pos[0] + 10, get_pos[1] + 10)
                self._flag = RunFlag.SHENG_HUO
                
            elif pos is not None:
                self._screen_utils.click(pos[0] + 10, pos[1] + 10)

        elif self._flag == RunFlag.SHENG_HUO:
            pos = self._screen_utils.get_target_pos('sheng_huo.png', 0.03)
            if pos is not None:
                self._screen_utils.click(pos[0] + 10, pos[1] + 10)
                self._flag = RunFlag.SHENG_HUO_TAB
                self._cache_dic.pop('push_qian_wang', None)

        elif self._flag == RunFlag.SHENG_HUO_TAB:
            pos = self._screen_utils.get_target_pos('wang.png', 0.02)
            if pos is not None:
                self._screen_utils.click(pos[0] + 10, pos[1] + 10)
                self._cache_dic['push_qian_wang'] = 1

            elif self._cache_dic.get('push_qian_wang', 1):
                self._flag = RunFlag.SEARCH
                self._search_time_out = 60

        elif self._flag == RunFlag.SEARCH:
            pos = self._screen_utils.get_target_pos('cai_ji.png', 0.1)
            self._search_time_out -= 1
            if self._search_time_out <= 0:
                self._flag = RunFlag.START

            elif pos is not None:
                self._flag = RunFlag.COLLECT

        elif self._flag == RunFlag.COLLECT:
            pos = self._screen_utils.get_target_pos('cai_ji.png', 0.1)
            print('cai ji pos:', pos)
            if pos is not None:
                self._screen_utils.click(pos[0] + 10, pos[1] + 10)
                self._flag = RunFlag.COLLECT_WAIT
                self._wait_time_out = 3
            
            else:
                self._flag = RunFlag.START

        elif self._flag == RunFlag.COLLECT_WAIT:
            self._wait_time_out -= 1
            if self._wait_time_out <= 0:
                self._flag = RunFlag.COLLECT

        elif self._flag == RunFlag.FIX:
            self._flag = RunFlag.START

        utils.INFO(get_flag_name(self._flag))

def main():
    #auto_go()
    shenlong = Collect()
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
