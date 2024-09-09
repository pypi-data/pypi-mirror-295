import time

class Game:
    def __init__(self):
        self.running = True
        self.clock = time.perf_counter()
        self.renderer = None
        self.input_manager = None
        self.audio_manager = None
        self.event_manager = None

    def start(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            time.sleep(1/60)  # Target 60 FPS

    def handle_events(self):
        if self.event_manager:
            self.event_manager.process_events()

    def update(self):
        pass

    def render(self):
        if self.renderer:
            self.renderer.render()

    def stop(self):
        self.running = False
