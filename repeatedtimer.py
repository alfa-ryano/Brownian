from threading import Timer

class RepeatedTimer(object):
    def __init__(self, interval, function, count_limit, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.counter = 0
        self.count_limit = count_limit
        self.args = args
        self.kwargs = kwargs
        self.is_running = False

    def _run(self):
        if self.is_running:
            self.function(*self.args, **self.kwargs)
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            if self.count_limit > 0:
                self.counter += 1
                if self.counter >= self.count_limit:
                    self.stop()

    def start(self):
        if not self.is_running:
            self.is_running = True
            self._timer = Timer(self.interval, self._run)
            self._timer.start()

    def stop(self):
        self._timer.cancel()
        self.is_running = False
        self.counter = 0