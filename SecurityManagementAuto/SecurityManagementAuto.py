import logging
import time

import win32event
import win32service
import win32serviceutil


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
        while self.run:
            self.logger.info("service is run....")
            
            time.sleep(10)

    def SvcStop(self):
        self.logger.info("service is stop....")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.run = False
       
    def _getLogger(self):
        logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)
        handler = logging.FileHandler("c:\\Users\\zachary\\Desktop\\WorkSpace\\pell-mell\\SecurityManagementAuto\\log.txt")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)

        return logger

if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(SecurityManagementAuto)
