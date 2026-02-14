import psutil
import subprocess

def get_cpu_temp():
    result = subprocess.check_output(['vcgencmd', 'measure_temp'], text=True)
    return result.strip().split("=")[1].split("'")[0]

def get_cpu_clock():
    result = subprocess.check_output(['vcgencmd','measure_clock','arm'],text = True)
    return int(result.strip().split('=')[1])

def get_gpu_temp():
    result = subprocess.check_output(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
    return result.strip().replace('temp=', '').replace('\'C', '')

def get_gpu_clock():
    result = subprocess.check_output(['vcgencmd', 'measure_clock', 'core'], capture_output=True, text=True)
    return result.strip().split('=')[1]


cpu_usage = psutil.cpu_percent(interval=1)
cpu_temp = get_cpu_temp()
cpu_clock = get_cpu_clock()
gpu_temp = get_gpu_temp()
gpu_clock = get_gpu_clock()