import json
import time

import gc
import urequests as requests

class StateManager:
    base_url = "https://status.makerspacebonn.de/api"
    open_url = base_url + "/msb/state/open"
    close_url = base_url + "/msb/state/close"
    state_url = base_url + "/msb/state"

    def __init__(self, api_key = None, mqtt_client = None):
        self.current_state = "unknown"
        self.last_time_read = 0
        self.poll_time_in_secs = 10
        self.api_key = api_key
        self.state_provider = mqtt_client

    def retrieve_state(self):
        self.state = self.state_provider.get_state()
        if self.state != None:
            self.current_state = "open" if self.state["open"] else "closed"

    def switch_remote_state(self):
        if self.current_state == "open":
            url = self.close_url
        else:
            url = self.open_url
        headers = {
            "msb-key": self.api_key,
        }
        print("mem free: ", gc.mem_free())
        r = requests.get(url, headers=headers)
        data = json.loads(r.text)
        self.current_state = "open" if data["state"]["open"] else "closed"
        r.close()
        return self.current_state