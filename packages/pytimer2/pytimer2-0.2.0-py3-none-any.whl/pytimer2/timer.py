import threading
import time


class Timer:
    def __init__(self):
        self.__countdown = 0

    def __start(self, duration):
        self.__countdown = duration
        for _ in range(duration):
            time.sleep(1)
            self.__countdown = self.__countdown - 1

    def get_countdown(self):
        return self.__countdown

    def start_countdown(self, duration=500):
        threading.Thread(target=self.__start, args=(duration,)).start()
