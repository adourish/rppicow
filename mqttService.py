import settingsService 
from umqttsimple  import MQTTClient
import time
import machine

broker = settingsService.get('broker')
sub_topic = settingsService.get('subtopic')
pub_topic = settingsService.get('pubtopic')
#client_id = ubinascii.hexlify(machine.unique_id())
#client_id = mac
client_id = settingsService.get('client_id')


def init():
    connect_and_subscribe()

def sub_cb():
    print("sub_cb")

def settimeout(duration): 
     pass


def sub_cb(topic, msg):
  print((topic, msg))
  if msg == b'LEDon':
    print('Device received LEDon message on subscribed topic')
    led.value(1)
  if msg == b'LEDoff':
    print('Device received LEDoff message on subscribed topic')
    led.value(0)


def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, broker)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(sub_topic)
  print('Connected to %s MQTT broker as client ID: %s, subscribed to %s topic' % (broker, client_id, sub_topic))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
    client.check_msg()
    if (time.time() - last_message) > message_interval:
      pub_msg = b'Hello #%d' % counter
      client.publish(pub_topic, pub_msg)
      last_message = time.time()
      counter += 1
  except OSError as e:
    restart_and_reconnect()