"""
airtest核心api的二次封装，操作具体实现类
"""
import os

from airtestProject.airtest.core import api as air
from airtestProject.airtest.core.android import Android
from airtestProject.airtest.core.error import TargetNotFoundError
from airtestProject.airtest.core.helper import G

from airtestProject.commons.utils.logger import log
from airtestProject.abstractBase.OperateBase import OperateABC
import time

from airtestProject.commons.utils.myTemplate import myTemplate
from airtestProject.commons.utils.ocrTemplate import OcrTemplate
from airtestProject.commons.utils.tools import get_folder_path_up


class myAirTest(OperateABC):

    def __init__(self, language):
        super(myAirTest, self).__init__()
        self.this_dict = None
        self.language = language

    def set_language(self, language):
        self.language = language

    def set_dict(self, script_root: str, project=None):
        """
        各种兼容还有路径转换。ps images文件夹只能在脚本的上级或者同级否则无法正常工作
        :param script_root: 脚本当前目录
        :param project: 定位到的具体图片文件夹
        :return:
        """
        if self.this_dict is None:
            files_dict = {}
            images_abs_path = get_folder_path_up(script_root, 'images')  # 获取图片文件夹的绝对路径
            # script_root_dir = os.path.dirname(script_root)  # 获取脚本文件夹的绝对路径
            # images_relative_path = os.path.relpath(images_abs_path, script_root_dir)  # 构造为图片文件夹的相对路径
            if project:
                images_project_relative_path = os.path.join(images_abs_path, project)  # 构造为图片文件夹和project的相对路径
            else:
                images_project_relative_path = images_abs_path
            # 遍历指定目录下的所有文件
            for filename in os.listdir(images_project_relative_path):
                file_path = os.path.join(images_project_relative_path, filename)
                if os.path.isfile(file_path):
                    file_name_without_ext, _ = os.path.splitext(filename)
                    files_dict[file_name_without_ext] = myTemplate(file_path)
            print(files_dict)
            self.this_dict = files_dict

    def init_device(self, platform=None, uuid=None, **kwargs):
        try:
            air.init_device(platform=platform, uuid=uuid, **kwargs)
            log.info(f"init device success, platform: {platform}, uuid:  {uuid}")
        except Exception as e:
            log.error(f"failed to init device, platform: {platform}, uuid:  {uuid}")
            raise e

    def connect_device(self, uri):
        log.info('🍇 🍉 ready to connect device host ...')
        try:
            air.connect_device(uri)
            log.info(f'🍊 🍋 connect device succeeded... host: {uri}')
        except ConnectionError as e:
            log.error(f'connect device failed... host: {uri}')
            raise ConnectionError from e

    def device(self):
        current_active_device = air.device()
        log.info(f'get current active device: {current_active_device}')
        return current_active_device

    def set_current(self, idx):
        try:
            log.info(f"set current active device idx: {idx}")
            air.set_current(idx)
        except Exception as e:
            log.error(f"failed to set current active device idx: {idx}")
            raise e

    def auto_setup(self, basedir=None, devices=None, logdir=None, project_root=None, compress=None):
        air.auto_setup(basedir=basedir, devices=devices, logdir=logdir, project_root=project_root, compress=compress)

    def shell(self, cmd):
        try:
            log.info(f"execute adb shell command: {cmd}")
            return air.shell(cmd)
        except Exception as e:
            log.error(f"failed to execute adb shell command: {cmd}")
            raise e

    def start_app(self, package, activity=None):
        try:
            air.start_app(package, activity)
            log.info(f"start app: {package}, activity: {activity}")
        except Exception as e:
            log.error(f"failed start app {package}, activity: {activity}")
            raise e

    def stop_app(self, package):
        try:
            air.stop_app(package)
            log.info(f"stop the application on device, package: {package}")
        except Exception as e:
            log.error(f"failed to stop the application on device, package: {package}")
            raise e

    def clear_app(self, package):
        try:
            air.clear_app(package)
            log.info(f"clear data of the application on device, package: {package}")
        except Exception as e:
            log.error(f"failed to clear data of the application on device, package: {package}")
            raise e

    def install(self, filepath, **kwargs):
        try:
            log.info(f"install application: {filepath}")
            return air.install(filepath, **kwargs)
        except Exception as e:
            log.error(f"failed to install application: {filepath}")
            raise e

    def uninstall(self, package):
        try:
            log.info(f"uninstall application: {package}")
            return air.uninstall(package)
        except Exception as e:
            log.error(f"failed to uninstall application: {package}")
            raise e

    def snapshot(self, quality=None, max_size=None):
        try:
            return G.DEVICE.snapshot()
        except Exception as e:
            log.error(f"failed to wake up and unlock the device")
            raise e

    def wake(self):
        try:
            log.info(f"wake up and unlock the device")
            return air.wake
        except Exception as e:
            log.error(f"failed to wake up and unlock the device")
            raise e

    def home(self, package):
        raise NotImplementedError

    def click(self, pos, times=1, ocrPlus=False, rgb=False, translucent=False, **kwargs):
        try:
            log.info(f"perform the touch action on the device screen, pos: {pos}")
            kwargs.pop('focus', None)
            kwargs.pop('sleep_interval', None)
            value = self.check_value(pos, ocrPlus, rgb=rgb, translucent=translucent)
            return air.touch(value, times, **kwargs)
        except Exception as e:
            log.error(f"failed to perform the touch action on the device screen, pos: {value}")
            raise e

    def double_click(self, v1, v2=None, vector=None, **kwargs):
        log.info(f"perform double click")
        return air.double_click(v1, v2, vector, **kwargs)

    def swipe(self, value, v2=None, vector_direction=None, ocrPlus=False, rgb=False, translucent=False, **kwargs):
        kwargs.pop('duration', None)
        kwargs.pop('focus', None)
        if vector_direction is None:
            vector_direction = [0, -3.0]
        log.info("Perform the swipe action on the device screen.")
        value = self.check_value(value, ocrPlus=ocrPlus, rgb=rgb, translucent=translucent)
        if v2 is not None:
            v2 = self.check_value(v2, ocrPlus=ocrPlus, rgb=rgb, translucent=translucent)
        return air.swipe(value, v2, vector=vector_direction, **kwargs)

    def swipe_along(self, pos, coordinates_list, duration=0.8, step=5, rgb=False, translucent=False):
        if isinstance(pos, tuple) or isinstance(pos, list):
            first_pos = pos
        else:
            first_pos = self.exists(pos, rgb=rgb, translucent=translucent)
        coordinates_list.insert(0, first_pos)
        if isinstance(air.device(), Android):
            air.device().swipe_along(coordinates_list, duration, step=step)
            return True
        else:
            raise TypeError("Device is not an Android device")

    def swipe_plus(self, value, v2=None, down_event_sleep=None, vector_direction=None, ocrPlus=False, rgb=False, translucent=False, **kwargs):
        value = self.check_value(value, ocrPlus=ocrPlus, rgb=rgb, translucent=translucent)
        if isinstance(value, (myTemplate, OcrTemplate)):
            pos1 = air.exists(value)
            if pos1:
                print(pos1)
            else:
                raise TargetNotFoundError(value)
        else:
            pos1 = value
        if v2:
            v2 = self.check_value(v2, ocrPlus=ocrPlus, rgb=rgb, translucent=translucent)
            if isinstance(v2, (myTemplate, OcrTemplate)):
                pos2 = air.exists(v2)
                if pos2 is False:
                    raise TargetNotFoundError(v2)
            else:
                pos2 = v2
            print(pos2)
        elif vector_direction:
            if vector_direction[0] <= 1 and vector_direction[1] <= 1:
                w, h = G.DEVICE.get_current_resolution()
                vector_direction = (int(vector_direction[0] * w), int(vector_direction[1] * h))
            pos2 = (pos1[0] + vector_direction[0], pos1[1] + vector_direction[1])
        else:
            raise Exception("no enough params for swipe")
        if isinstance(air.device(), Android):
            air.device().swipe_plus(pos1, pos2, down_event_sleep, **kwargs)
            return True
        else:
            raise TypeError("Device is not an Android device")

    def pinch(self, in_or_out='in', percent=0.5, center=None):
        log.info(f"perform the pinch action on the device screen")
        return air.pinch(in_or_out, center, percent)

    def keyevent(self, keyname, **kwargs):
        log.info(f"perform key event keyname: {keyname} on the device.")
        return air.keyevent(keyname, **kwargs)

    def set_text(self, pos=None, text=None, enter=True, rgb=False, translucent=False, **kwargs):
        try:
            self.click(pos, rgb=rgb, translucent=translucent)
            log.info(f"input {text} on the target device")
            for i in range(20):
                air.keyevent("KEYCODE_DEL")
                log.info(f"我在删除")
            return air.text(text, enter, **kwargs)
        except Exception as e:
            log.error(f"failed to input {text} on the target device")
            raise e

    def sleep(self, secs=1.0):
        time.sleep(secs)
        log.info(f'time sleep {secs} seconds')

    def wait(self, pos, timeout=None, interval=0.5, ocrPlus=False, intervalfunc=None, rgb=False, translucent=False, **kwargs):
        try:
            pos = self.check_value(pos, ocrPlus=ocrPlus, rgb=rgb, translucent=translucent)
            return air.wait(pos, timeout, interval, intervalfunc)
        except Exception as e:
            log.error(f"failed to input {pos} on the target device")
            raise e

    def wait_disappear_element(self, pos, timeout=180, rgb=False, translucent=False):
        start_loading_time = time.time()
        while self.exists(pos, rgb=rgb, translucent=translucent) is not False:
            if time.time() - start_loading_time > timeout:
                log.info(f"{pos}存在超时，请注意查看")
                return False
        log.info(f"{pos}消失")
        return True

    def wait_element_appear(self, pos, timeout=180, rgb=False, translucent=False):
        start_loading_time = time.time()
        while self.exists(pos, rgb=rgb, translucent=translucent) is False:
            if time.time() - start_loading_time > timeout:
                log.info(f"{pos}寻找超时，请注意查看")
                return False
        log.info(f"{pos}出现")
        return True

    def exists(self, pos, ocrPlus=False, rgb=False, translucent=False):
        try:
            pos = self.check_value(pos, ocrPlus, rgb=rgb, translucent=translucent)
            return air.exists(pos)
        except Exception as e:
            log.error(f"the node: {pos} not exists.")
            raise e

    def persistent_element_exists(self, pos):
        pass

    def wait_for_any(self, pos_list: list, timeout=30, rgb=False, translucent=False):
        """

        :param translucent: 是否为半透
        :param rgb: 开启色值判断
        :param pos_list: 需要等待的列表元素
        :param timeout: 超出时长
        :return:
        """
        start = time.time()
        while True:
            for pos in pos_list:
                if self.exists(pos, rgb=rgb, translucent=translucent):
                    return pos
            if time.time() - start > timeout:
                raise TargetNotFoundError(f'any to appear{pos_list}')

    def wait_for_all(self, pos_list: list, timeout=30, rgb=False, translucent=False):
        start = time.time()
        while True:
            all_exist = True
            for pos in pos_list:
                if not self.exists(pos, rgb=rgb, translucent=translucent):
                    all_exist = False
                    break
            if all_exist:
                return
            if time.time() - start > timeout:
                raise TargetNotFoundError(f'all to appear{pos_list}')

    def wait_next_element(self, last_click_pos, next_pos, timeout=180, rgb=False, translucent=False):
        """
        等待下一个元素出现
        :param timeout: 超时时间
        :param last_click_pos: 需要点击的元素
        :param next_pos: 将会出现的元素
        :param translucent: 是否为半透
        :param rgb: 开启色值判断
        :return:
        """
        start_time = time.time()
        while self.exists(next_pos, rgb=rgb, translucent=translucent) is False:
            log.info(f"{next_pos}没有出现正在尝试点击")
            self.click(last_click_pos, rgb=rgb, translucent=translucent)
            air.sleep(0.5)
            if time.time() - start_time > timeout:
                log.info(f"{next_pos}没有出现")
                return False
        return True

    def wait_last_element_disappear(self, last_click_pos, last_pos, timeout=180, rgb=False, translucent=False):
        start_time = time.time()
        while self.exists(last_pos, rgb=rgb, translucent=translucent):
            log.info(f"{last_pos}没有消失正在尝试点击")
            self.click(last_click_pos, rgb=rgb, translucent=translucent)
            air.sleep(0.5)
            if time.time() - start_time > timeout:
                log.info(f"{last_pos}没有消失")
                return False
        return True

    def get_text(self, pos=None):
        if pos is not None:
            return OcrTemplate().find_text(pos)
        else:
            image = G.DEVICE.snapshot()
            return OcrTemplate().find_text(image)

    def check_value(self, val, ocrPlus=False, threshold=0.7, translucent=False, rgb=False):
        """
        用于判定是否是可以直接使用字典取值。如果不可以判断是否为文件夹路径是的话采用图片识别
        :param rgb: 图像识别是否开启rgb对比
        :param translucent: 图像识别是否半透
        :param threshold: 图像识别匹配阈值
        :param ocrPlus: 主要用于传递是否开启增强识别(不一定增强)
        :param val: 需要检查的参数
        :return:
        """
        if isinstance(val, str):
            dict_value = None
            if self.this_dict:
                dict_value = self.this_dict.get(val)
            if dict_value is not None:
                return dict_value
            log.info(f"图片字典中不存在{val}对应的路径，不会读取图片字典进行索引，改用正常的图片识别或是文字识别")
            return myTemplate(val, threshold=threshold, rgb=rgb, translucent=translucent) if os.path.isfile(val) else OcrTemplate(val, language=self.language, ocrPlus=ocrPlus)
        return val


if __name__ == '__main__':
    air.sleep()
