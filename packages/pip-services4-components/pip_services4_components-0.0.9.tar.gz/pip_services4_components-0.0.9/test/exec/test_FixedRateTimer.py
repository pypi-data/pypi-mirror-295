# -*- coding: utf-8 -*-
import time

from pip_services4_components.exec.FixedRateTimer import FixedRateTimer

class TestFixedRateTimer:
    counter = 0

    def setup_method(self):
        self.counter = 0

    def test_run_with_task(self):

        def callback():
            self.counter += 1

        timer = FixedRateTimer(callback, 100, 0)

        timer.start()
        time.sleep(0.5)
        timer.stop()

        assert self.counter > 3

    def test_run_with_callback(self):
        def callback():
            self.counter += 1

        timer = FixedRateTimer(callback, 100, 0)

        timer.start()
        time.sleep(0.5)
        timer.stop()

        assert self.counter > 3
