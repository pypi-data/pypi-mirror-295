class InputManager:
    def __init__(self):
        self.keys = set()

    def update(self):
        pass

    def is_key_pressed(self, key):
        return key in self.keys
