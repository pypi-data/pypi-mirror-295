import threading
import time


class Timer:
    def __init__(self):
        self.__countdown = 0
        self.__task = None
        self.__stop_event = threading.Event()
        self.__pause_event = threading.Event()

    def __start(self, duration):
        self.__countdown = duration
        self.__pause_event.set()
        while self.__countdown > 0:
            self.__pause_event.wait()

            if self.__stop_event.is_set():
                self.__countdown = 0
                break

            time.sleep(1)
            if self.__pause_event.is_set():
                self.__countdown -= 1

    def get_countdown(self):
        return self.__countdown

    def start_countdown(self, duration=500):
        self.__stop_event.clear()
        self.__pause_event.set()
        self.__task = threading.Thread(target=self.__start, args=(duration,))
        self.__task.start()
        time.sleep(0.05)

    def stop_countdown(self):
        if self.__task and self.__task.is_alive():
            self.__stop_event.set()
            self.__pause_event.set()
            self.__task.join()

    def pause_countdown(self):
        if self.__task and self.__task.is_alive():
            self.__pause_event.clear()

    def resume_countdown(self):
        if self.__task and self.__task.is_alive():
            self.__pause_event.set()
            time.sleep(0.05)


