import Battery
import Utilization


volt = Battery.bus_voltage
current = Battery.current
charge = Battery.charge

cpu_use = Utilization.cpu_usage
cpu_temp = Utilization.cpu_temp
cpu_clock = Utilization.cpu_clock
gpu_temp = Utilization.gpu_temp
gpu_clock = Utilization.gpu_clock



data ={volt,current,charge,cpu_use,cpu_temp,cpu_clock,gpu_temp,gpu_clock}
with open('System_Metrics.csv','a') as csvfile:
    csvfile.write(f"{data}\n")