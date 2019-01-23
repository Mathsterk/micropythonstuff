
#Hardware Platform: FireBeetle-ESP32
#Result: input MQTTlibrary and remote controls LED by mqtt communication.

from simple import MQTTClient
from machine import Pin
import network
import time
import onewire
import ds18x20

SSID="IOT"
PASSWORD="12344444"

led=Pin(2, Pin.OUT, value=0)

SERVER = "192.168.1.249"
CLIENT_ID = "esp32_temp"
TOPIC = b"home/outside/temperature"
username='esp32_temp'
password='esp32<3'
state = 0
c=None


temp = 0
prevTemp = 0


ow = onewire.OneWire(Pin(25))   #Init wire
ow.scan()
ds=ds18x20.DS18X20(ow)          #create ds18x20 object

def sub_cb(topic, msg):
  global state
  print((topic, msg))
  if msg == b"on":
    led.value(1)
    state = 0
    print("1")
  elif msg == b"off":
    led.value(0)
    state = 1
    print("0")
  elif msg == b"toggle":
    # LED is inversed, so setting it to current state
    # value will make it toggle
    led.value(state)
    state = 1 - state
def connectWifi(ssid,passwd):
  global wlan
  wlan=network.WLAN(network.STA_IF)         #create a wlan object
  wlan.active(True)                         #Activate the network interface
  wlan.disconnect()                         #Disconnect the last connected WiFi
  wlan.connect(ssid,passwd)                 #connect wifi
  while(wlan.ifconfig()[0]=='0.0.0.0'):
    time.sleep(1)

    
#Catch exceptions,stop program if interrupted accidentally in the 'try'
while True:
  try:
    connectWifi(SSID,PASSWORD)
    server=SERVER
    c = MQTTClient(CLIENT_ID, server,0,username,password)     #create a mqtt client
    #c.set_callback(sub_cb)                    #set callback
    c.connect()                               #connect mqtt
    #c.subscribe(TOPIC)                        #client subscribes to a topic
    print("Connected to %s, publishing to %s topic" % (server, TOPIC))

    while True:
      #c.wait_msg()                            #wait message 
      
      
      roms=ds.scan()                #scan ds18x20
      ds.convert_temp()             #convert temperature
      for rom in roms:
        temp = round(ds.read_temp(rom), 1)
        if(temp != prevTemp and temp != 85.0):
          prevTemp = temp

          print(temp)    #display 
          led.value(state)
          status = not status
          #c.publish(TOPIC, "{\n  \"temperature\": \"" + temp + "\"\n}")
          c.publish(TOPIC, "{\n  \"temperature\": \"" + str(temp) + "\"\n}")
          led.value(1)
          time.sleep(0.05)
          led.value(0)
        else {
          time.sleep(1)
        }
        
      time.sleep(0.5)
    

    
  except:
    pass
  finally:
    if(c is not None):
      c.disconnect()
    wlan.disconnect()
    wlan.active(False)


