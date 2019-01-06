import socket
import network
import time
import binascii
from struct import *
import uctypes
from machine import ADC,Pin
import machine



host='192.168.1.185'
port = 6980
SSID="IOT"
PASSWORD="12344444"

adc0=ADC(Pin(36))
adc0.atten(machine.ADC.ATTN_11DB)

adc1=ADC(Pin(39))
adc1.atten(machine.ADC.ATTN_11DB)

adc2=ADC(Pin(34))
adc2.atten(machine.ADC.ATTN_11DB)

adc3=ADC(Pin(35))
adc3.atten(machine.ADC.ATTN_11DB)

adc4=ADC(Pin(32))
adc4.atten(machine.ADC.ATTN_11DB)

adc5=ADC(Pin(33))
adc5.atten(machine.ADC.ATTN_11DB)



wlan=None
s=None
{
  "i": 0 | uctypes.UINT32
}
i=0
averages = 20

gain = [-60.0]*6
prevGain = [gain]*6
avg = [[0]*averages]*6
avgCount = 0
avgSum = [0]*6


def connectWifi(ssid,passwd):
  global wlan
  wlan=network.WLAN(network.STA_IF)                 #create a wlan object
  wlan.active(True)                                 #Activate the network interface
  wlan.disconnect()                                 #Disconnect the last connected WiFi
  wlan.connect(ssid,passwd)                         #connect wifi
  while(wlan.ifconfig()[0]=='0.0.0.0'):
    time.sleep(1)
  return True
  
#Catch exceptions,stop program if interrupted accidentally in the 'try'
try:
  if(connectWifi(SSID,PASSWORD) == True):           #judge whether to connect WiFi
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #create socket
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  #Set the value of the given socket option
    ip=wlan.ifconfig()[0]                           #get ip addr
    while True:
      print("1")
      avg[avgCount][0] = adc0.read()
      avg[avgCount][1] = adc1.read()
      avg[avgCount][2] = adc2.read()
      avg[avgCount][3] = adc3.read()
      avg[avgCount][4] = adc4.read()
      avg[avgCount][5] = adc5.read()
      print("2")
      avgCount += 1
      if avgCount >= averages:
        avgCount = 0
      for b in range(6):
        for a in range(averages):
          avgSum[b] += avg[a]
        avgSum[b] = avgSum[b] / averages
        print("3")
        if(avgSum[b] >= 1):
          gain[b] = avgSum[b] / 56 - 60.00
        else:
          gain[b] = -60.0

        if(gain[b] >=12.0):
          gain[b] = 12.0
        elif(gain[b] <=-60.0):
          gain[b] = -60.0

  #    if(abs(prevGain[] - gain[]) > 0.1):
  #      prevGain[] = gain[]
        #command = pack('!8b8sbQ2bb', 86, 66, 65, 78, 0x52, 0x00, 0x00, 0x10, 'Command1', 0x00, i)
        command = None
        if(abs(prevGain[0] - gain[0]) > 0.1):
          command += pack("12s", 'Bus(0).gain=')
          command += pack("5s", str(gain[0]))
          command += pack("s", ';')
        if(abs(prevGain[1] - gain[1]) > 0.1):
          command += pack("12s", 'Bus(1).gain=')
          command += pack("5s", str(gain[1]))
          command += pack("s", ';')

        if(abs(prevGain[2] - gain[2]) > 0.1):
          command += pack("14s", 'Strip(0).gain=')
          command += pack("5s", str(gain[2]))
          command += pack("s", ';')
        if(abs(prevGain[3] - gain[3]) > 0.1):
          command += pack("14s", 'Strip(1).gain=')
          command += pack("5s", str(gain[3]))
          command += pack("s", ';')
        if(abs(prevGain[4] - gain[4]) > 0.1):
          command += pack("14s", 'Strip(3).gain=')
          command += pack("5s", str(gain[4]))
          command += pack("s", ';')
        if(abs(prevGain[5] - gain[5]) > 0.1):
          command += pack("14s", 'Strip(4).gain=')
          command += pack("5s", str(gain[5]))
          command += pack("s", ';')


        
        if(command != 0):
          command = pack('!8b8sbQ2bb', 86, 66, 65, 78, 0x52, 0x00, 0x00, 0x10, 'Command1', 0x00, i) + command
          s.sendto(command,(host,port))    #send data
          i += 1
          print(i, "\t", gain)
          
      time.sleep(0.01)
except:
  if (s):
    s.close()
  wlan.disconnect()
  wlan.active(False)


