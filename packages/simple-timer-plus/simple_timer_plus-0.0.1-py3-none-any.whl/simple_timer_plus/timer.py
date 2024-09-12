import time

class SimpleTimer:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.running = False

    def start(self):
        if not self.running:
            self.start_time = time.time()
            self.running = True
        else:
            print("Timer is already running.")

    def pause(self):
        if self.running:
            self.elapsed_time += time.time() - self.start_time
            self.running = False
        else:
            print("Timer is already paused.")
    
    def resume(self):
        if not self.running:
            self.start_time = time.time()
            self.running = True
        else:
            print("Timer is already running.")

    def reset(self):
        self.start_time = None
        self.elapsed_time = 0
        self.running = False
        print("Timer has been reset.")

    def get_elapsed_time(self):
        if self.running:
            return self.elapsed_time + (time.time() - self.start_time)
        return self.elapsed_time

    def show_elapsed_time(self):
        total_time = self.get_elapsed_time()
        hours, rem = divmod(total_time, 3600)
        minutes, seconds = divmod(rem, 60)
        print(f"Elapsed time: {int(hours):02}:{int(minutes):02}:{int(seconds):02}")
