import json

class Config:
    def __init__(self):
        self.size = self.get_size()

    def create_size(self):
        size = int(input())
        w = open('config', 'w+')
        config = {'size': size}
        config = json.dumps(config)
        w.write(config)

    def get_size(self):
        w = open('config', 'r')
        config = w.readline()
        config = json.loads(config)
        size = config['size']
        return size


