# Simple Timer Plus

Simple Timer Plus is a Python package for measuring the time spent on tasks or code execution.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Simple Timer:

```bash
pip install simple-timer
```

## Usage
Here's how to use the Simple Timer:

```
from simple_timer import SimpleTimer
import time

timer = SimpleTimer()

timer.start()
# Perform some tasks
time.sleep(3)
timer.pause()
timer.show_elapsed_time()  # Output: Elapsed time: 00:00:03
```
## Features
* Start, pause, resume, and reset the timer.
* Get the elapsed time in hours, minutes, and seconds.

## Author
Orlando Gomes

## License
This project is licensed under the [MIT License.](https://choosealicense.com/licenses/mit/)

