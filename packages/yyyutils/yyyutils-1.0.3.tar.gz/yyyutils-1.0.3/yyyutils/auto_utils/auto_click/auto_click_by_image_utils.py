import os
import time
import math
import cv2 as cv
import pywinauto.mouse
import win32gui
import win32con
from PIL import ImageGrab
from loguru import logger
import shutil
import keyboard


class AutoClickByImageUtils:
    """
    用于根据图像匹配自动点击的工具类——未完成
    """
    def __init__(self, window_name):
        self.window_name = window_name
        self.temp_dir = "../temp"
        self.image_dir = "../image"
        self.work_screen_path = os.path.join(self.temp_dir, "work_screen.png")
        self.app_screen_path = os.path.join(self.temp_dir, "app.png")
        self.img_folder_path = "./image"

        self.create_directories()

    def create_directories(self):
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)

    @staticmethod
    def show_window(handle):
        win32gui.ShowWindow(handle, True)
        time.sleep(0.5)

    def get_app_screenshot(self):
        original_position, handle = self.get_window_position(self.window_name)
        AutoClickByImageUtils.show_window(handle)
        img_ready = ImageGrab.grab(original_position)
        img_ready.save(self.app_screen_path)
        return original_position

    def get_workscreen_screenshot(self):
        screen_shot = ImageGrab.grab()
        if screen_shot:
            screen_shot.save(self.work_screen_path)
            return screen_shot
        return None

    def click_icon(self, icon_path):
        x, y = self.locate_icon(icon_path)
        pywinauto.mouse.click(button='left', coords=(x, y))

    def locate_icon(self, img_name, x_start_ratio=0, y_start_ratio=0, x_end_ratio=1, y_end_ratio=1, try_times=3):
        obj_path = os.path.join(self.img_folder_path, img_name)
        result_x, result_y = -1, -1
        for i in range(try_times):
            x_init, y_init = self.get_app_screenshot()[:2]
            source = cv.imread(self.app_screen_path)
            h, w, d = source.shape
            x_start = math.floor(w * x_start_ratio)
            y_start = math.floor(h * y_start_ratio)
            x_end = math.floor(w * x_end_ratio)
            y_end = math.floor(h * y_end_ratio)
            source = source[y_start:y_end + 1, x_start:x_end + 1]
            cv.imwrite(self.app_screen_path, source)
            template = cv.imread(obj_path)
            result = cv.matchTemplate(source, template, cv.TM_CCOEFF_NORMED)
            similaity = cv.minMaxLoc(result)[1]
            if similaity > 0.9:
                pos_start = cv.minMaxLoc(result)[3]
                result_x = x_init + x_start + int(pos_start[0]) + int(template.shape[1] / 2)
                result_y = y_init + y_start + int(pos_start[1]) + int(template.shape[0] / 2)
                break
            else:
                logger.info('low similarity')
        return result_x, result_y

    def check_icon(self, img_name, x_start_ratio=0, y_start_ratio=0, x_end_ratio=1, y_end_ratio=1):
        x, y = self.locate_icon(img_name, x_start_ratio, y_start_ratio, x_end_ratio, y_end_ratio, try_times=3)
        return x != -1 and y != -1

    def get_window_position(self, window_name):
        handle = win32gui.FindWindow(None, window_name)
        if handle == 0:
            raise Exception("Window not found")
        win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
        time.sleep(0.5)
        return win32gui.GetWindowRect(handle), handle

    def move_files(self, origin_folder, target_folder, suffix_list=[]):
        data_list = []
        dir_list = os.listdir(origin_folder)
        if len(suffix_list) == 0:
            data_list = dir_list
        else:
            for file_name in dir_list:
                for suffix in suffix_list:
                    if file_name.endswith(suffix):
                        data_list.append(file_name)
                        break
        if len(data_list) == 0:
            return
        cur_rime = time.strftime("%Y-%m-%d_%H-%M-%S")
        target_folder_new = os.path.join(target_folder, cur_rime)
        os.makedirs(target_folder_new)
        for file_name in data_list:
            source_file = os.path.join(origin_folder, file_name)
            target_file = os.path.join(target_folder_new, file_name)
            shutil.move(source_file, target_file)

    def running_program(self, window_name, origin_folder, target_folder, suffix_list=[], cycle_num=-1):
        exit_flag = False

        def on_key_event(event):
            nonlocal exit_flag
            if event.Key.upper() == 'Q':
                logger.info('exit')
                exit_flag = True

        keyboard.on_press_key(on_key_event)
        app = AutoClickByImageUtils(window_name)
        logger.info('start')
        cycle_count = 0
        while not exit_flag:
            try:
                if self.is_test_over(app):
                    self.move_files(origin_folder, target_folder, suffix_list)
                    logger.info(f"Cycle {cycle_count} finished")
                    if cycle_num != -1 and cycle_count >= cycle_num:
                        logger.info(f"finished {cycle_count} cycles")
                        return
                    cycle_count += 1
            except Exception as e:
                logger.error(e)
            try:
                print('test')
            except:
                pass
            time.sleep(1)

    def is_test_over(self, app):
        valid1 = app.check_icon("running1.png")
        if valid1:
            return False
        return True




if __name__ == '__main__':
    auto_click_utils = AutoClickByImageUtils("贝瑞蒲公英")
    auto_click_utils.get_workscreen_screenshot()
    auto_click_utils.get_app_screenshot()
