import pyautogui
import cv2
from PIL import ImageGrab
import time
import os
import global_data
import const
from hot_key import Hotkey


def get_target_pos(filename, reg_x_start, reg_y_start, reg_x_end, reg_y_end):
    filename = os.path.join('pic', filename)

    sc_region = (reg_x_start, reg_y_start, reg_x_end, reg_y_end) #距离左上右下的像素
    sc_img = ImageGrab.grab(sc_region)
    save_path = "screen_region.jpg"
    sc_img.save(save_path)

    screen = cv2.imread(save_path)
    target = cv2.imread(filename)

    result = cv2.matchTemplate(target, screen, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(min_val, max_val, min_loc, max_loc)
    if min_val < 0.01:
        _x, _y = min_loc
        return (reg_x_start + _x, reg_y_start + _y)

    return None


def auto_shen_long_pan_one_turn():
    pics = [
        'shen_you.png',
        'huo_dong.bmp',
        'shen_long_pan.png',
        'qian_wang.png',
        'pi_pei.png',
    ]

    for pic_name in pics:
        pos = get_target_pos(pic_name, 0, 0, 1900, 1000)

        if pos is None:
            if pic_name == 'huo_dong.bmp' or pic_name == 'shen_you.png':
                continue

            return

        pyautogui.click(pos[0] + 10, pos[1] + 10, duration=0.2)

        time.sleep(1)

    while 1:
        pos = get_target_pos('jin_ru.png', 0, 0, 1900, 1000)
        if pos is None:
            time.sleep(1)
            continue

        pyautogui.click(pos[0] + 10, pos[1] + 10, duration=0.2)
        return True


def attack_sleep(num):
    for i in range(num):
        time.sleep(1)

        pyautogui.click(1617, 874, duration=0.2)


def auto_go():
    while 1:
        pos = get_target_pos('shen_you.png', 0, 0, 1900, 1000)
        if pos is not None:
            pyautogui.click(pos[0] + 10, pos[1] + 10, duration=0.2)
            time.sleep(1)
            continue

        pos = get_target_pos('shen_long1.png', 0, 0, 1900, 1000)
        if pos is not None:
            pyautogui.click(1469, 348, duration=0.2)
            attack_sleep(5)
            continue

        pos = get_target_pos('shen_long2.png', 0, 0, 1900, 1000)
        if pos is not None:
            pyautogui.click(1469, 348, duration=0.2)
            attack_sleep(5)
            continue

        pos = get_target_pos('que_ren.png', 0, 0, 1900, 1000)
        if pos is not None:
            pyautogui.click(pos[0] + 10, pos[1] + 10, duration=0.2)
            attack_sleep(5)
            continue

        pos = get_target_pos('que_ding.png', 0, 0, 1900, 1000)
        if pos is not None:
            pyautogui.click(pos[0] + 10, pos[1] + 10, duration=0.2)
            break

        time.sleep(5)

def main():
    #auto_go()
    while 1:
        if global_data.GAME_STATE == const.GameState.PAUSE:
            time.sleep(1)
            continue

        elif global_data.GAME_STATE == const.GameState.EXIT:
            break

        ret = auto_shen_long_pan_one_turn()
        if ret is None:
            continue

        auto_go()

if __name__ == '__main__':
    global_data.GAME_STATE = const.GameState.RUNNING
    hotkey = Hotkey()
    hotkey.start()
    main()

    hotkey.join()
    # print(user32.RegisterHotKey(None, ID1, 0, win32con.VK_F10))
    # auto_go()
    # auto_shen_long_pan_one_turn()
