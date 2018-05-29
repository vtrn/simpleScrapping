#!/usr/bin/env python3

import sys
from urllib.parse import urlparse

if __name__ == '__main__':
    from parser import *
    from publisher import *
    from config import *
else:
    from app.parser import *
    from app.publisher import *
    from app.config import *


class Dispatcher:
    def get_argv(self):
        """Обрабатывает аргументы командной строки

        """
        argv = sys.argv
        if len(argv) < 2:
            print('Утилита принимает url статьи и сохраняет текст статьи в отдельный файл.')
            print('Образец: \n[python app.py [https://имя_сайта/путь_к_статье]]')
            print('Доступные команды: \n[python app.py [-config]].')
            raise SystemExit
        if sys.argv[1] == '-config':
            Config().create_size()
            print('Настройки изменены')
            raise SystemExit
        else:
            check = self.check_url(sys.argv[1])
            if check:
                return sys.argv[1]
            else:
                print('URL невалидный, либо неверная команда.')
                raise SystemExit

    def check_url(self, url):
        """Проверяет аргумент на соотвествие формату URL

        """
        try:
            check = urlparse(url)
            if all([check.scheme, check.netloc, check.path]):
                return True
            else:
                return False
        except:
            return False

    def handle(self):
        """ Создает необходимые объекты и запускает процессы:
            проверка аргумента,
            парсинг данных,
            обработка полученных данных,
            запись данных в файл.

        """
        url = self.get_argv()
        post = Parser(url)
        corrector = Corrector(post.post, Config().size)
        corrector.processesCorrector()
        writer = Writer(url, corrector.post)
        writer.write()


if __name__ == '__main__':
    publisher = Dispatcher()
    publisher.handle()

