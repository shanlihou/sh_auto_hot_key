from PyQt5.QtWidgets import QApplication
import win32gui
from numpy import array,uint8,ndarray
import win32api
import win32con
import cv2
from PIL import ImageGrab
import const
import os


def to_cvimg(pix):
    '将self.screen.grabWindow 返回的 Pixmap 转换为 ndarray，方便opencv使用'
    qimg = pix.toImage()
    temp_shape = (qimg.height(), qimg.bytesPerLine() * 8 // qimg.depth())
    temp_shape += (4,)
    ptr = qimg.bits()
    ptr.setsize(qimg.byteCount())
    result = array(ptr, dtype=uint8).reshape(temp_shape)
    return result[..., :3]


# 直接写一个类，方便以后使用
class Screen:
    def __init__(self, win_title=None, win_class=None, hwnd=None) -> None:
        self.app = QApplication(['WindowCapture'])
        self.screen = QApplication.primaryScreen()
        self.bind(win_title,win_class,hwnd)
        self._screen_cv2 = None

    def bind(self, win_title=None,win_class=None,hwnd=None):
        '可以直接传入句柄，否则就根据class和title来查找，并把句柄做为实例属性 self._hwnd'
        if not hwnd:
            self._hwnd = win32gui.FindWindow(win_class, win_title)
            print('bind:', self._hwnd)
        else:
            self._hwnd = hwnd

    def capture(self) -> ndarray:
        '截图方法，在窗口为 1920 x 1080 大小下，最快速度25ms (grabWindow: 17ms, to_cvimg: 8ms)'
        self.pix = self.screen.grabWindow(self._hwnd)
        self.img = to_cvimg(self.pix)
        self.pix.save(const.SCREEN_PATH)
        self._screen_cv2 = cv2.imread(const.SCREEN_PATH)

        return self.img

    def get_target_pos(self, filename):
        filename = os.path.join('pic', filename)
        target = cv2.imread(filename)

        result = cv2.matchTemplate(target, self._screen_cv2, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print(min_val, max_val, min_loc, max_loc)
        if min_val < 0.01:
            _x, _y = min_loc
            return _x, _y

        return None

    def click(self, cx, cy):
        long_position = win32api.MAKELONG(cx, cy)#模拟鼠标指针 传送到指定坐标
        win32api.SendMessage(self._hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)#模拟鼠标按下
        win32api.SendMessage(self._hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)#模拟鼠标弹起

if __name__ =='__main__':
    screen = Screen('TCGamer', 'Qt5152QWindowIcon')
    screen.capture('test.bmp')