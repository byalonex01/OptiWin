import platform
import os
import datetime


def get_system_info():
    system_info = {
        'Operating System': platform.system(),
        'OS Version': platform.version(),
        'Machine': platform.machine(),
        'Processor': platform.processor(),
        'Node Name': platform.node(),
        'Architecture': platform.architecture(),
        'Current User': os.getlogin(),
        'Current Date and Time (UTC)': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    }
    return system_info


def print_system_info():
    info = get_system_info()
    for key, value in info.items():
        print(f'{key}: {value}')