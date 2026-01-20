# State Button for the Makerspace Bonn

A physical button for our makerspace that changes the publicly available opening information. LED indicators show the current space state and connection status.

## Features

- **Physical Button**: Press to toggle space open/closed state
- **LED Strip Status**: 16 NeoPixel LEDs showing space state (green = open, red = closed)
- **Status LEDs**:
  - LED 0 (first): WiFi status - blinks yellow when connecting, solid yellow on error, follows state when connected
  - LED 1 (second): MQTT status - blinks yellow when disconnected, follows state when connected
- **Robust Connectivity**:
  - WiFi reconnection with timeout (30s) and retries (3 attempts)
  - MQTT reconnection with exponential backoff (5s to 60s)
- **Watchdog**: 42s timeout to recover from hangs

## Hardware

- ESP32 (WROOM)
- WS2812B NeoPixel LED strip (16 LEDs)
- Physical button
- Status LEDs (optional GPIO LEDs)

### Pin Configuration

| Component | GPIO Pin |
|-----------|----------|
| NeoPixel Strip | 5 |
| Button | 9 |
| Big Light LED | 6 |
| Button Light LED | 3 |
| Internal LED | 4 |

## Software Setup

### ESP32

1. Install MicroPython: https://micropython.org/download/ESP32_GENERIC/
2. Flash the firmware to your ESP32

### IDE (PyCharm recommended)

1. Install MicroPython Tools plugin: https://plugins.jetbrains.com/plugin/26227-micropython-tools
2. Create run configuration for your ESP32

### Stubs for IDE Support

https://micropython-stubs.readthedocs.io/en/main/24_pycharm.html

## Configuration

Create a `secrets.py` file in `src/` (see `secrets_example.py`):

```python
mqtt_server = 'mqtt.example.com'
mqtt_user = 'username'
mqtt_pass = 'password'

API_key = 'your-api-key'

# Dictionary of known WiFi networks to connect to
wifi_access = {
    'MyWiFi': 'wifi-password',
    'BackupWiFi': 'backup-password',
}
```

## Architecture

```
src/
├── main.py           # Main loop and initialization
├── mqtt_service.py   # MQTT client with reconnection logic
├── wifi_manager.py   # WiFi management with reconnection
├── state_led.py      # Status LED control (ignore/error/blinking)
├── state_manager.py  # Space state management
├── button_handler.py # Button debouncing and cooldown
└── secrets.py        # Configuration (not in repo)
```

## References

- Makerspace Bonn Infocenter

## Mentions

Inspired by the project from https://gitlab.com/jhaand/hacker-hotel-space-state/
