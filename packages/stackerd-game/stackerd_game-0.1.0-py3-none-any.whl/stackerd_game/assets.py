class AssetManager:
    def __init__(self):
        self.assets = {}

    def load(self, name, path):
        self.assets[name] = path
        print(f"Loaded asset: {name} from {path}")

    def get(self, name):
        return self.assets.get(name)
