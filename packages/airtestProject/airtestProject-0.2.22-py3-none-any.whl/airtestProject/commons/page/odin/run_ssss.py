import time

from airtestProject.commons.stateMachine.task import TaskCaseTemplate, check_func, TaskRunner, put_Task
from airtestProject.commons.utils.logger import log
from airtestProject.factory.operateFactory import operate


@check_func('点击场景按钮成功')
def click_scene(self, scenes_pos, scenes_view_pos, fun_name="air"):
    start_time = time.time()
    while operate(fun_name).exists(scenes_view_pos) is False:
        operate(fun_name).click(scenes_pos)
        log.step('点击场景按钮')
        if start_time - time.time() > 30:
            log('点击失败')
            break
    log.step('弹出场景选择页面')
    #
    # for i in range(5):
    #     if not operate(fun_name).exists(scenes_view_pos):
    #         operate(fun_name).click(scenes_pos)
    #         log.step('点击场景按钮')
    #     else:
    #         log.step('弹出场景选择界面')
    #         break
    #     return False


@check_func('点击斗罗流式加载场景按钮')
def click_streaming_scenes(self, streaming_scenes_pos, fun_name="air"):
    operate(fun_name).click(streaming_scenes_pos)


@check_func('关闭场景页面')
def close_scene_view(self, scenes_view_pos, scenes_pos, fun_name="air"):
    for i in range(5):
        if operate(fun_name).exists(scenes_view_pos):
            operate(fun_name).click(scenes_pos)
            return True
        else:
            log.step("等待")
            operate(fun_name).sleep(1.0)
    log.error("没有关闭场景页面")


@check_func('点击功能按钮')
def click_fun(self, fun_pos, fun_view, fun_name="air"):
    operate(fun_name).wait_next_element(fun_pos, fun_view)


@check_func('滑动功能列表至最底')
def swipe_fun_view_last(self, running_pos, fun_view_pos, fun_name="air"):
    for i in range(3):
        if not operate(fun_name).exists(running_pos):
            log.step('未找到自动跑图,尝试滑动')
            operate(fun_name).swipe(fun_view_pos, v2=None, vector_direction=[0, -1.0], duration=0.5)
        else:
            break


@check_func('点击自动跑图按钮')
def click_running(self, running_pos, fun_name="air"):
    operate(fun_name).click(running_pos)


@check_func('点击退出按钮')
def click_exit(self, exit_pos, fun_name="air"):
    operate(fun_name).click(exit_pos)


@check_func('设置跑图参数')
def set_scene_param(self, running_param_1, running_param_2, running_param_3, params: list, fun_name="air"):
    operate(fun_name).set_text(running_param_1, params[0])
    operate(fun_name).set_text(running_param_2, params[1])
    operate(fun_name).set_text(running_param_3, params[2])


def start_run(self, start_running_pos, fun_name="air"):
    for i in range(3):
        if operate(fun_name).exists(start_running_pos):
            operate(fun_name).click(start_running_pos)
        else:
            break


@check_func('关闭跑图界面')
def close_running_view(self, close_running_pos, fun_name="air"):
    for i in range(3):
        if operate(fun_name).exists(close_running_pos):
            operate(fun_name).click(close_running_pos)
        else:
            break


def check_running_end(self, fun_name="air", apm=None):
    print("进入检查结束")
    apm.collectAll(True)
    if fun_name == "poco":
        while True:
            axis = index.findall(operate(fun_name).get_text(axis_pos))
            log.step(f'当前坐标为-{axis}')
            operate(fun_name).sleep(5)
            if axis == running_pos_end_1:
                break
    else:
        print("执行等待1500")
        while True:
            time.sleep(1500)
            break
    apm.collectAll(False)
    print("出来了")


@log.wrap('打开自动跑图界面，输入参数')
def start_running_1(self, button_dict, fun_name="air"):
    self.click_scene()
    self.click_streaming_scenes()
    operate(fun_name).sleep(10.0)
    self.click_fun()
    operate(fun_name).sleep(1.0)
    self.swipe_fun_view_last()
    operate(fun_name).sleep(2.0)
    self.click_running()
    operate(fun_name).sleep(0.5)
    self.set_scene_param(["20002", "1", "1"])


@log.wrap('点击开启跑图')
def start_running_2(self):
    self.funcListCheck.open_list("功能", "功能列表")
    self.funcListCheck.open_ui_from_ui_list("自动跑图", "开始跑图", "FuncListSwipe", "LanguageRoom", "Multilingual")
    self.set_scene_param("场景:", "路径下标：", "路点下标  从1开始:", ["20002", "1", "1"])
    self.start_run("开始跑图")
    self.check_running_end()





class RunSss(TaskCaseTemplate):
    def __init__(self):
        super().__init__()


    def start_running_3(self):
        self.funcListCheck.open_list("功能", "功能列表")
        self.funcListCheck.open_ui_from_ui_list("自动跑图", "开始跑图", "FuncListSwipe", "LanguageRoom", "Multilingual")
        set_scene_param("场景:", "路径下标：", "路点下标  从1开始:", ["20002", "1", "1"])
        start_run("开始跑图")
        close_running_view()


tt = TaskRunner(RunSss())
tt.setup_task_runner(__file__)
tt.start_app("dhjashdas")
tt.run(1)
tt.to_report()

