import threading
import time


class Timer:
    def __init__(self):
        self.countdown = 0

    def start(self, duration):
        self.countdown = duration
        for _ in range(duration):
            time.sleep(1)
            self.countdown = self.countdown - 1

    def get_countdown(self):
        return self.countdown

    def start_countdown(self, duration=500):
        threading.Thread(target=self.start, args=(duration,)).start()
