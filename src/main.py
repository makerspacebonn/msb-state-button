import gc
import random
import sys

import secrets
import machine
import time
import ntptime

from neopixel import NeoPixel


mqtt_server = secrets.mqtt_server
mqtt_user = secrets.mqtt_user
mqtt_pass = secrets.mqtt_pass
api_key = secrets.API_key
wifi_ssid = secrets.wifi_SSID
wifi_password = secrets.wifi_passwd
hostname_str = "spachtelknopf"

from mqtt_service import MQTTService
from button_handler import ButtonHandler
from state_manager import StateManager
from wifi_manager import WifiManager

wifi_access = secrets.wifi_access

NUM_LEDS = 16
pin = machine.Pin(5, machine.Pin.OUT)   # set GPIO0 to output to drive NeoPixels
np = NeoPixel(pin, NUM_LEDS)   # create NeoPixel driver on GPIO0 for 8 pixels
print(np[1])
np[0] = (200, 0, 0)
np.write()


# Define the GPIO pins.
led_biglight = machine.Pin(6, machine.Pin.OUT) # 21
led_buttonlight = machine.Pin(3, machine.Pin.OUT) # 16
led_wifi = machine.Pin(2, machine.Pin.OUT) # 4
led_intern = machine.Pin(4, machine.Pin.OUT) # 2

button_handler = ButtonHandler(9, cooldown_period=5000, debounce_delay=25)  # GPIO14, 5 Sekunden Cooldown
wifi_manager = WifiManager(wifi_access)

mqtt_service = MQTTService(mqtt_server, mqtt_user, mqtt_pass, "msb-state-button-" + machine.unique_id().hex())
state_manager = StateManager(secrets.API_key, mqtt_client=mqtt_service)


print("\n|-----------------------------------------------------------------------|")

time.sleep(0.3)



def neo_wlan_disconnected():
    for led in range(NUM_LEDS):
        np[led] = (0, 0, 0)
    np[0] = (100,0,0)# set the first pixel to white
    np.write()

def neo_wlan_connected():
    for led in range(NUM_LEDS):
        np[led] = (0, 0, 0)
    np[0] = (0,100,0)# set the first pixel to white
    np.write()

def neo_wlan_connecting():
    for led in range(NUM_LEDS):
        np[led] = (0, 0, 0)
    np[0] = (100,100,0)# set the first pixel to white
    np.write()



def wifi_listener(message):
    print("wifi_listener: "+message)
    if (message.startswith("connected to")):
        led_wifi.on()
        neo_wlan_connected()
    elif message.startswith("connecting to") or message.startswith("Scanning"):
        neo_wlan_connecting()
    else:
        led_wifi.off()
        neo_wlan_disconnected()

def mqtt_connection_listener(connected):
    if connected:
        print("MQTT connection established")
    else:
        print("MQTT connection lost")
        np[1] = (100, 100, 0)  # Yellow for MQTT disconnected
        np.write()

wifi_manager.addListener(wifi_listener)
mqtt_service.add_connection_listener(mqtt_connection_listener)
wifi_manager.connect_wifi()


time.sleep(0.3)
ntptime.settime()
# Activate the watchdog
wdt = machine.WDT(timeout=42000)
wdt.feed()

mqtt_service.connect_and_subscribe()
mqtt_service.check_msg()
state_manager.retrieve_state()
print("Current state from init: " + state_manager.current_state)

print(time.time())

def should_execute():
    return random.randint(1, 100) == 1


while True:
    try:
        wdt.feed()
        time.sleep(0.300)
        wifi_manager.check_and_reconnect()
        mqtt_service.check_msg()
        state_manager.retrieve_state()
        wdt.feed()

        if button_handler.button_pressed:
            gc.collect()
            print("Aktion in der Hauptschleife ausgelöst!")
            state_manager.switch_remote_state()
            button_handler.button_pressed = False  # Setze das Flag zurück

        if state_manager.current_state == "open":
            led_intern.value(1)
            led_biglight.value(1)
            led_buttonlight.value(1)
            for ledid in range(NUM_LEDS):
                np[ledid] = (0, 100, 0)
        else:
            led_intern.value(0)
            led_biglight.value(0)
            led_buttonlight.value(0)
            for ledid in range(NUM_LEDS):
                np[ledid] = (10, 0, 0)

        # np[1] shows MQTT status: yellow if disconnected, otherwise follows state
        if not mqtt_service.is_connected():
            np[1] = (100, 100, 0)
        np.write()
    except Exception as e:
        print("Error: ", e)
        sys.print_exception(e)
        time.sleep(1)

