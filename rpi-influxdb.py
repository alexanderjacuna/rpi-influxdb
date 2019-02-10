import subprocess
from influxdb import InfluxDBClient

temperature = float(subprocess.check_output("cat /sys/class/thermal/thermal_zone0/temp", shell=True))
temperature = temperature / 1000
temperature = round(float(temperature * 9/5.0 + 32),1)

frequency = subprocess.check_output("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq", shell=True)
frequency = int(frequency) * 1000

memoryTotal = float(subprocess.check_output("cat /proc/meminfo | grep MemTotal | sed 's/[^0-9]*//g'", shell=True))
memoryTotal = round(float(memoryTotal / 1024),1)

memoryFree = float(subprocess.check_output("cat /proc/meminfo | grep MemFree | sed 's/[^0-9]*//g'", shell=True))
memoryFree = round(float(memoryFree / 1024),1)

memoryUsed = round(float(memoryTotal - memoryFree),1)

# SET VARUABLES
host = "192.168.1.67"
port = 8086
user = "writer"
password = "password" 
dbname = "readings"
measurement = subprocess.check_output("hostname", shell=True)
measurement = measurement.strip() + "-" + dbname

# CREATE CLIENT OBJECT
client = InfluxDBClient(host, port, user, password, dbname)

# CREATE JSON
data = [
{
  "measurement": measurement,
	  "fields": {
		  "temperature" : temperature,
		  "frequency" : frequency,
		  "memoryTotal" : memoryTotal,
		  "memoryFree" : memoryFree,
		  "memoryUsed" : memoryUsed
	  }
  } 
]

# WRITE DATA
client.write_points(data)
