import time

class Clock:
    def __init__(self, target_fps):
        self.target_fps = target_fps
        self.target_frame_time = 1.0 / target_fps
        self.last_tick_time = time.time()
        self.delta_time = 0.0
        self.frame_count = 0
        self.fps = 0.0
        self.start_time = self.last_tick_time

    def tick(self) -> None:
        current_time = time.time()
        elapsed_time = current_time - self.last_tick_time

        # Calculate sleep time to achieve the target FPS
        sleep_time = max(0, self.target_frame_time - elapsed_time)

        if sleep_time > 0:
            time.sleep(sleep_time)

        current_time = time.time()
        self.delta_time = current_time - self.last_tick_time
        self.last_tick_time = current_time

        self.frame_count += 1
        if self.frame_count % self.target_fps == 0:
            self.fps = self.frame_count / (current_time - self.start_time)
            self.frame_count = 0
            self.start_time = current_time

    def get_delta_time(self) -> float:
        return self.delta_time

    def get_fps(self) -> float:
        return round(self.fps, 2)