import time
import pygetwindow as gw
import pyautogui
import logging
import os
from pywinauto import Application

# user config begin
#  config  the  poll  interval
interval_time = 60
#  config  the  window  title that need to be close
# 经过测试,标题中带空格的东西也可以被关闭
wind = [
    r'Everything',
    r'微信',
    r'QQ',
    r'所有笔记本 - fdssf3x4 - 印象笔记',
    r'Evernote',
    r'任务管理器',

]

# 这里其实有一个bug ,那就是不支持多语言 国际化
window_title_maybe_pattern = [
    r'Task Manager',
    r'Everything',
    r'微信',
    r'QQ',
    r'印象笔记$',
    r'Evernote',
    r'^[a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*$',
    r'^文件资源管理器$',
    r'^utools$',
]


# user config end

def close_window(program_name):
    # 获取所有窗口的标题
    window_titles = [window.pattern for window in pyautogui.getAllWindows()]

    # 遍历所有窗口的标题
    for title in window_titles:
        # 如果窗口的标题中包含程序的名称，则关闭该窗口
        if program_name in title and True:
            os.system(f'taskkill /F /IM {program_name}.exe')


def close_window(program_name, window_title):
    # 连接到程序
    app = Application().connect(path=f"{program_name}.exe")

    # 获取程序的主窗口
    main_window = app.window(title_re=window_title)

    # 如果窗口是可见的，那么关闭它
    if main_window.is_visible():
        main_window.close()


# TODO there is a bug  when the  program  don not run  on  a terminal  singly
# 获取环境变量LOG_LEVEL的值，如果没有设置，则默认为'ERROR'
log_level = os.getenv('LOG_LEVEL', 'ERROR').upper()
# 设置日志级别  动态设置日志等级
logging.basicConfig(level=getattr(logging, log_level))
logging.debug('这是一个debug信息')
logging.info('这是一个info信息')
logging.warning('这是一个warning信息')
logging.error('这是一个error信息')

import logging
import os

# 创建一个logger
my_logger = logging.getLogger('my_logger_name')
# 获取环境变量LOG_LEVEL的值，如果没有设置，则默认为'ERROR'
log_level = os.getenv('LOG_LEVEL', 'ERROR').upper()

# 设置logger的日志级别
my_logger.setLevel(getattr(logging, log_level))
# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('my_logger.log')
# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
# 给logger添加handler
# my_logger.addHandler(fh)
my_logger.debug('这是一个debug信息')
my_logger.info('这是一个info信息')
my_logger.warning('这是一个warning信息')
my_logger.error('这是一个error信息')

# while True:
#     time.sleep(interval_time)  # 每10秒检测一次
#     for title in window_title:
#         try:
#             win = gw.getWindowsWithTitle(title)[0]  # 获取名为'everything'的窗体
#             logging.info(win)
#             if win.isActive == False:  # 如果该窗体不是当前窗体
#                 win.close()  # 关闭该窗体
#         except IndexError:
#             continue  # 如果没有找到名为'everything'的窗体，继续检测
#


import re


def find_matches(string_list, regex):
    string_qualifid_list = [string for string in string_list if re.search(regex, string)]
    return string_qualifid_list


import re


def is_windows_path(path):
    pattern = r'^[a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*$'
    return bool(re.match(pattern, path))


while not time.sleep(interval_time) :
    # get current all windows
    # current_all_windows_dic_with_handle_to_title ={window : window.title for window in pyautogui.getAllWindows()}
    current_all_windows =[window for window in pyautogui.getAllWindows()]
    # get current all windows ded title
    current_all_windowsTitle= [window.title for window in current_all_windows]

    for pattern in window_title_maybe_pattern:
        windowTitle_is_qualified_list   = find_matches(current_all_windowsTitle, pattern)

        try:
            win = gw.getWindowsWithTitle(windowTitle_is_qualified_list[0])[0]  # 获取名为'everything'的窗体
            logging.info(win)
            if win.isActive == False:  # 如果该窗体不是当前窗体
                win.close()  # 关闭该窗体
        except IndexError:
            continue  # 如果没有找到名为'everything'的窗体，继续检测
