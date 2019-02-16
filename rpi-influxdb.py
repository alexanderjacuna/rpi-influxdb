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

# SET VARIABLES
host = "192.168.1.67"
port = 8086
user = "writer"
password = "password" 
dbname = "readings"
measurement = subprocess.check_output("hostname", shell=True)
measurement1 = measurement.strip() + "-" + "temperature"
measurement2 = measurement.strip() + "-" + "frequency"
measurement3 = measurement.strip() + "-" + "memoryTotal"
measurement4 = measurement.strip() + "-" + "memoryFree"
measurement5 = measurement.strip() + "-" + "memoryUsed"

# CREATE CLIENT OBJECT
client = InfluxDBClient(host, port, user, password, dbname)

data1 = [
{
  "measurement": measurement1,
	  "fields": {
		  "temperature" : temperature
	  }
  } 
]

data2 = [
{
  "measurement": measurement2,
	  "fields": {
		  "frequency" : frequency
	  }
  } 
]

data3 = [
{
  "measurement": measurement3,
	  "fields": {
		  "memoryTotal" : memoryTotal
	  }
  } 
]

data4 = [
{
  "measurement": measurement4,
	  "fields": {
		  "memoryFree" : memoryFree
	  }
  } 
]

data5 = [
{
  "measurement": measurement5,
	  "fields": {
		  "memoryUsed" : memoryUsed
	  }
  } 
]

# WRITE DATA
client.write_points(data1)
client.write_points(data2)
client.write_points(data3)
client.write_points(data4)
client.write_points(data5)
