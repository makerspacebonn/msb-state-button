import machine
import time

class ButtonHandler:
    def __init__(self, pin_number, debounce_delay=50, cooldown_period=5000):
        self.button_pin = machine.Pin(pin_number, machine.Pin.IN, machine.Pin.PULL_UP)
        self.last_button_state = self.button_pin.value()
        self.last_debounce_time = 0
        self.debounce_delay = debounce_delay
        self.button_press_count = 0
        self.button_pressed = False
        self.cooldown_period = cooldown_period
        self.last_press_time = 0
        self.button_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.button_interrupt_handler)
        self.click_callback = None
    def set_click_callback(self, click_callback):
        self.click_callback = click_callback

    def button_interrupt_handler(self, pin):
        current_time = time.ticks_ms()

        if time.ticks_diff(current_time, self.last_debounce_time) > self.debounce_delay:
            current_button_state = pin.value()

            if current_button_state != self.last_button_state:
                self.last_debounce_time = current_time
                self.last_button_state = current_button_state

                if current_button_state == 0:  # Button pressed
                    if time.ticks_diff(current_time, self.last_press_time) > self.cooldown_period:
                        self.button_press_count += 1
                        print("Button pressed! Count:", self.button_press_count)
                        self.button_pressed = True
                        self.last_press_time = current_time
                        if (self.click_callback is not None):
                            self.click_callback(pin)
                    else:
                        print("Button pressed, but on cooldown")