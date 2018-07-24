import threading

COUNTDOWN_COUNT = 1


class EventTimer(object):
    def __init__(self, interval, function):
        self.is_enabled = False
        self.function = function
        self.timer = None
        self.interval = interval

    def start(self):
        self.is_enabled = True
        self.run()

    def run(self):
        if self.is_enabled:
            self.function()
            self.timer = threading.Timer(self.interval, self.run)
            self.timer.start()

    def stop(self):
        self.is_enabled = False
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None


class CountDownTimer(EventTimer):
    def __init__(self, start_from,  stop_at, interval, function):
        super(CountDownTimer, self).__init__(interval, function)

        self.counter = start_from
        self.stop_at = stop_at

    def run(self):
        if self.counter <= self.stop_at:
            self.stop()
            return
        super(CountDownTimer, self).run()


def format_decimal(value):
    return "{0:.2f}".format(value)