import subprocess
import logging

class Optimizer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def clean_temp_files(self):
        '''Clean temporary files from system'''
        try:
            subprocess.run(['cmd', '/c', 'del /q %temp%'], shell=True)
            self.logger.info('Temp files cleaned successfully')
            return True
        except Exception as e:
            self.logger.error(f'Error cleaning temp files: {e}')
            return False
    
    def disable_startup_services(self):
        '''Disable unnecessary startup services'''
        services_to_disable = [
            'DiagTrack',
            'dmwappushservice',
            'OneSyncSvc'
        ]
        try:
            for service in services_to_disable:
                subprocess.run(['cmd', '/c', f'sc config {service} start=disabled'], shell=True)
            self.logger.info('Startup services disabled')
            return True
        except Exception as e:
            self.logger.error(f'Error disabling services: {e}')
            return False
    
    def clear_cache(self):
        '''Clear application cache'''
        try:
            subprocess.run(['cmd', '/c', 'ipconfig /flushdns'], shell=True)
            self.logger.info('DNS cache cleared')
            return True
        except Exception as e:
            self.logger.error(f'Error clearing cache: {e}')
            return False
