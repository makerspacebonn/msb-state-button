import time


class StateLed:
    """LED status indicator with support for solid color, blinking, and state-following modes."""

    STATE_IGNORE = 0
    STATE_ERROR = 1
    STATE_BLINKING = 2

    def __init__(self, np, led_index, error_color=(100, 100, 0), blink_cycle_ms=1000):
        self.np = np
        self.led_index = led_index
        self.error_color = error_color
        self.blink_cycle_ms = blink_cycle_ms
        self.blink_state = False
        self.last_toggle_time = time.ticks_ms()
        self.state = self.STATE_IGNORE

    def ignore(self):
        """LED follows the app state color."""
        self.state = self.STATE_IGNORE

    def error(self):
        """LED shows solid error color."""
        self.state = self.STATE_ERROR

    def blinking(self):
        """LED blinks error color."""
        self.state = self.STATE_BLINKING

    def update(self):
        """Update LED based on current status. Call this in main loop.

        Does nothing if in ignore state (LED keeps whatever color was set by main loop).
        """
        if self.state == self.STATE_IGNORE:
            return
        elif self.state == self.STATE_BLINKING:
            now = time.ticks_ms()
            if time.ticks_diff(now, self.last_toggle_time) >= self.blink_cycle_ms // 2:
                self.blink_state = not self.blink_state
                self.last_toggle_time = now
            self.np[self.led_index] = self.error_color if self.blink_state else (0, 0, 0)
        else:
            self.np[self.led_index] = self.error_color
