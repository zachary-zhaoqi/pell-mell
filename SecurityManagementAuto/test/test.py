import sys
import os

import win32api,win32con

current_file_path=os.path.dirname(os.path.abspath(__file__))
print(current_file_path)

# ##提醒OK消息框
# print('提醒OK消息框'+str(win32api.MessageBox(0, "这是一个测试提醒OK消息框", "提醒",win32con.MB_OK)))

# ##是否信息框
# print('是否信息框'+str(win32api.MessageBox(0, "这是一个测试是否信息框", "提醒",win32con.MB_YESNO)))
  
# ##说明信息框
# print('说明信息框'+str(win32api.MessageBox(0, "这是一个测试说明信息框", "提醒",win32con.MB_HELP)))
  
# ##警告信息框
# print('警告信息框'+str(win32api.MessageBox(0, "这是一个测试警告信息框", "提醒",win32con.MB_ICONWARNING)))
  
# ##疑问信息框
# print('疑问信息框'+str(win32api.MessageBox(0, "这是一个测试疑问信息框", "提醒",win32con.MB_ICONQUESTION)))
  
# ##提示信息框
# print('提示信息框'+str(win32api.MessageBox(0, "这是一个测试提示信息框", "提醒",win32con.MB_ICONASTERISK)))
  
# ##确认信息框
# print('确认信息框'+str(win32api.MessageBox(0, "这是一个测试确认信息框", "提醒",win32con.MB_OKCANCEL)))
  
# ##重试信息框
# print('重试信息框'+str(win32api.MessageBox(0, "这是一个测试重试信息框", "提醒",win32con.MB_RETRYCANCEL)))
  
# ##是否取消信息框
# print('是否取消信息框'+str(win32api.MessageBox(0, "这是一个测试是否取消信息框", "提醒",win32con.MB_YESNOCANCEL)))