import sys
from urllib.parse import urlparse



if __name__ == '__main__':
    from parser import *
    from publisher import *
else:
    from app.parser import *
    from app.publisher import *

class Dispatcher:
    def get_argv(self):
        argv = sys.argv
        if len(argv) < 2:
            print('Утилита принимает url статьи и сохраняет текст статьи в отдельный файл.')
            print('Образец: \n[test.py [https://имя_сайта_/путь_к_статье]]')
            raise SystemExit
        check = self.check_url(sys.argv[1])
        if check:
            return sys.argv[1]
        else:
            print('url невалидный')
            raise SystemExit

    def check_url(self, url):
        #order = ('sheme', 'netloc', 'path')
        try:
            check = urlparse(url)
            if all([check.scheme, check.netloc, check.path]):
                return True
            else:
                return False
        except:
            return False

    def handle(self):
        url = self.get_argv()
        post = Post(url)
        corrector = Corrector(post.post)
        corrector.handle()
        writer = Writer(url, corrector.post)
        writer.hadle()



if __name__ == '__main__':
    publisher = Dispatcher()
    publisher.handle()