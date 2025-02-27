import secrets
import machine
import time
import ntptime

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

# Define the GPIO pins.
led_biglight = machine.Pin(18, machine.Pin.OUT) # 21
led_buttonlight = machine.Pin(19, machine.Pin.OUT) # 16
led_wifi = machine.Pin(5, machine.Pin.OUT) # 4
led_intern = machine.Pin(2, machine.Pin.OUT) # 2

button_handler = ButtonHandler(22, cooldown_period=5000)  # GPIO14, 5 Sekunden Cooldown
wifi_manager = WifiManager(wifi_ssid, wifi_password)
mqtt_service = MQTTService(mqtt_server, mqtt_user, mqtt_pass, "msb-state-button-" + machine.unique_id().hex())
state_manager = StateManager(secrets.API_key, mqtt_client=mqtt_service)

print("\n|-----------------------------------------------------------------------|")

time.sleep(0.3)

led_wifi.off()
wifi_manager.connect_wifi()
led_wifi.on()

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
while True:
    try:
        wdt.feed()
        time.sleep(0.300)
        mqtt_service.check_msg()
        state_manager.retrieve_state()
        wdt.feed()

        if button_handler.button_pressed:
            print("Aktion in der Hauptschleife ausgelöst!")
            state_manager.switch_remote_state()
            button_handler.button_pressed = False  # Setze das Flag zurück

        if state_manager.current_state == "open":
            led_intern.value(1)
            led_biglight.value(1)
            led_buttonlight.value(1)
        else:
            led_intern.value(0)
            led_biglight.value(0)
            led_buttonlight.value(0)
    except OSError as e:
        print("Error: ", e)
        mqtt_service.connect_and_subscribe()
        print("MQTT Reconnected")
    except Exception as e:
        print("Unexpected error: ", e)
        time.sleep(5)

