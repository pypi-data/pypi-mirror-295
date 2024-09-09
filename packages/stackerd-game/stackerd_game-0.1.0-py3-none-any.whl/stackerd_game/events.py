class EventManager:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def process_events(self):
        for event in self.events:
            print(f"Processing event: {event}")
        self.events.clear()
