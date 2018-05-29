#!/usr/bin/env python3

import json


class Config:
    def __init__(self):
        self.size = self.get_size()

    def create_size(self):
        """Создает настройки

        """
        size = int(input('размер строки> '))
        w = open('config', 'w+')
        config = {'size': size}
        config = json.dumps(config)
        w.write(config)

    def get_size(self):
        """Читает настройки из файла, возращает
        полученные значения

        """
        w = open('config', 'r')
        config = w.readline()
        config = json.loads(config)
        size = config['size']
        return size
