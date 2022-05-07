import ctypes
import win32con
import threading
import global_data
import const


user32 = ctypes.windll.user32
ID1 = 105 #
ID2 = 106 #

class Hotkey(threading.Thread):  #创建一个Thread.threading的扩展类

    def run(self):

        if not user32.RegisterHotKey(None, ID1, 0, win32con.VK_F9):   # 注册快捷键F9并判断是否成功，该热键用于执行一次需要执行的内容。
            print("Unable to register id", ID1) # 返回一个错误信息

        if not user32.RegisterHotKey(None, ID2, 0, win32con.VK_F10):   # 注册快捷键F9并判断是否成功，该热键用于执行一次需要执行的内容。
            print("Unable to register id", ID2) # 返回一个错误信息

        #以下为检测热键是否被按下，并在最后释放快捷键

        try:
            msg = ctypes.wintypes.MSG()

            while True:
                if user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:

                    if msg.message == win32con.WM_HOTKEY:
                        if msg.wParam == ID1:

                            if global_data.GAME_STATE == const.GameState.RUNNING:
                                global_data.GAME_STATE = const.GameState.PAUSE
                            elif global_data.GAME_STATE == const.GameState.PAUSE:
                                global_data.GAME_STATE = const.GameState.RUNNING
                                
                        elif msg.wParam == ID2:

                            global_data.GAME_STATE = const.GameState.EXIT
                            break

                    user32.TranslateMessage(ctypes.byref(msg))
                    user32.DispatchMessageA(ctypes.byref(msg))

        finally:
            user32.UnregisterHotKey(None, ID1)#必须得释放热键，否则下次就会注册失败，所以当程序异常退出，没有释放热键，
            user32.UnregisterHotKey(None, ID2)#必须得释放热键，否则下次就会注册失败，所以当程序异常退出，没有释放热键，