import socket
import network
import time
import binascii
from struct import *
import uctypes


host='192.168.1.185'
port = 10000
SSID="IOT"
PASSWORD="12344444"
wlan=None
s=None
{
  "i": 0 | uctypes.UINT32
}


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
      command = pack('!9b8sQ', 86, 66, 65, 78, 0x52, 0x00, 0x00, 0x00, 0x10, 'Command1', i,)
      
      command += pack("32s", 'testing')
      s.sendto(command,(host,port))    #send data
      print(len(command))
      i += 1
      time.sleep(1)
except:
  if (s):
    s.close()
  wlan.disconnect()
  wlan.active(False)


