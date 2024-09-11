# PyTimer2

`PyTimer2` is a simple Python countdown timer package that offers start, pause, resume, and stop functionalities. This tool is perfect for managing timed tasks, creating simple scheduling systems, or integrating into larger applications where precise countdown control is required.

[![Downloads](https://static.pepy.tech/badge/pytimer2)](https://pepy.tech/project/pytimer2)  
## Features

- **Start Countdown:** Initiate a countdown for a specified duration.
- **Pause Countdown:** Pause the countdown at any moment without losing the current time.
- **Resume Countdown:** Resume the countdown from where it was paused.
- **Stop Countdown:** Completely stop the countdown and reset the timer.
- **Non-Blocking Execution:** Runs in a separate thread, allowing your main application to continue running without interruption.

## Installation

You can install PyTimer directly from GitHub or from PyPI:

```bash
# Install pytimer2
pip install pytimer2

# Usage
from pytimer2 import Timer
import time

# Create a Timer instance
timer = Timer()

# Start the countdown with a duration of 500 seconds
timer.start_countdown(duration=500)

# Access the current countdown value
print(f"Current countdown: {timer.get_countdown()} seconds")

# Let it run for a few seconds and then pause
time.sleep(3)
timer.pause_countdown()
print(f"Countdown paused: {timer.get_countdown()} seconds")

# Wait and then resume the countdown
time.sleep(5)
print(f"Countdown still paused: {timer.get_countdown()} seconds")
timer.resume_countdown()
print("Timer resumed...")

# Run for a few more seconds
time.sleep(2)
print(f"Countdown resumed and current time: {timer.get_countdown()} seconds")

# Stop the countdown
timer.stop_countdown()
print(f"Countdown stopped at: {timer.get_countdown()} seconds")



