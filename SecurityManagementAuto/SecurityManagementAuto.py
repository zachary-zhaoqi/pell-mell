import logging
import os
import time
import json

import win32api
import win32con
import win32event
import win32service
import win32serviceutil

import checksecurityitem

class SecurityManagementAuto(win32serviceutil.ServiceFramework):
    _svc_name_ = "SecurityManagementAuto"
    _svc_display_name_ = "Security Management Auto"
    _svc_description_ = "对“电脑安全项目”自动设置并长期监控"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.logger = self._getLogger()
        self.run = True

    def SvcDoRun(self):
        self.logger.info("service is run....")
        while self.run:
            # 根据待检项目读取当前设置并保持在日志
            current_REG_settings_list=checksecurityitem.read_REG_current_settings()
            self.logger.info("==========================本次检查结果==========================")
            self.logger.info(json.dumps(current_REG_settings_list,ensure_ascii=False))
            self.logger.info("==========================结果输出完毕==========================")
            
            #对照当前设置与期望是否相同 并保存差异在日志中
            contrast_result=checksecurityitem.contrast(current_REG_settings_list)
            self.logger.info("==========================本次修改项目==========================")
            self.logger.info(json.dumps(contrast_result,ensure_ascii=False))
            self.logger.info("==========================结果输出完毕==========================")
            
            self.logger.info("==========================开始进行设置修改=======================")
            set_REG_results=checksecurityitem.set_all_REG()
            set_REG_fail_results=checksecurityitem.get_set_REG_fail_results(set_REG_results)
            self.logger.info("==========================修改失败项目如下=======================")
            self.logger.info(json.dumps(set_REG_fail_results,ensure_ascii=False))
            self.logger.info("==========================修改完毕==============================")

            time.sleep(30)

    def SvcStop(self):
        self.logger.info("service is stop....")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.run = False
       
    def _getLogger(self):
        current_file_path=os.path.dirname(os.path.abspath(__file__))
        logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)
        handler = logging.FileHandler(current_file_path+'\\log\\checkResult.log',encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)

        return logger

if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(SecurityManagementAuto)
