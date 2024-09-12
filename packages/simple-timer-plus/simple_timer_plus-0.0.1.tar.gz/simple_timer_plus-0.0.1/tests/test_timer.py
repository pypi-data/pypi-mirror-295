import time
from simple_timer.timer import SimpleTimer

def test_timer():
    timer = SimpleTimer()
    timer.start()
    time.sleep(1)
    timer.pause()
    assert round(timer.get_elapsed_time(), 0) == 1, "Timer should be paused at ~1 second"
