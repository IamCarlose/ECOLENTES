import time
import threading

class IndustrialTimer:
    def __init__(self, callback):
        self.callback = callback
        self.start_time = 0
        self.elapsed = 0
        self.running = False
        self._thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.start_time = time.time() - self.elapsed
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()

    def stop(self):
        self.running = False

    def reset(self):
        self.stop()
        self.elapsed = 0
        self.callback(0)

    def _run(self):
        while self.running:
            self.elapsed = time.time() - self.start_time
            self.callback(self.elapsed)
            time.sleep(0.05)
