import sys
from urllib.parse import urlparse
import bs4 as bs
import urllib.request
import re


class Corrector:
    def __init__(self, body):
        self.body = body
        self.new_body = []
        self.links = []
        self.post = None

    def handler(self):
        start = 0
        pattern = lambda x: 'LINK' in x

        for line in self.body:
            self.search_links(line)
            new_line = self.replace_links(line)
            new_line = self.search_indent(new_line)
            new_line = self.clear_line(new_line)
            if pattern(new_line):
                new_line = self.create_new_links(new_line, start=start)
                start += 1
            self.new_body.append(new_line)
        self.post = self.format_size()

    def search_links(self, line):
        new_links = re.findall(r'<a\s.*?href="(.+?)".*?>(.+?)</a>', line)
        if new_links:
            self.links.append(new_links)

    def replace_links(self, line):
        new_line = ''
        new_line += re.sub(r'<a\s.*?href="(.+?)".*?>(.+?)</a>', 'LINK', line)
        return new_line

    def clear_line(self, line):
        new_line = re.sub(r'(?:<).*?(?:>)', '', line)
        return new_line

    def create_new_links(self, line, start=0, step=0, end=0):
        new_line = ''
        new_line += re.sub('LINK', '[' + self.links[start][step][end] + ']' + ' ' + self.links[start][step][end + 1],
                           line)
        return new_line

    def search_indent(self, line):
        new_line = re.sub(r'<p>', "000 "
                                  "", line)
        return new_line

    def format_size(self):
        post = []
        for par in self.new_body:
            list_par = par.split()
            new_par = []
            string = []
            for s in list_par:
                if s == '000':
                    s = '  '
                string.append(s)
                if len(' '.join(string)) > 70:
                    new_par.append(' '.join(string))
                    string = []
            post.append(new_par)
        return post


class Writter:
    def __init__(self, file_name, obj):
        self.file_name = file_name + r'.txt'
        self.obj = obj

    def hadler(self):
        name = re.sub(r'/', '_', self.file_name)
        w = open(name, 'w')
        for par in self.obj:
            for string in par:
                w.write('\n' + string)
        w.close()


class Post:
    def __init__(self, url):
        self.url = url
        self.title, self.post = self.handler()

    def get_html(self):
        html = urllib.request.urlopen(self.url)
        html = html.read()
        return html

    def get_post_and_title(self, html):
        post = bs.BeautifulSoup(html, 'html.parser')
        title = post.find_all('title')
        post = post.find_all('p')
        return title, post

    def get_transform(self, post):
        post = [str(x) for x in post]
        return post

    def handler(self):
        html = self.get_html()
        title, post = self.get_post_and_title(html)
        post = self.get_transform(post)
        return title, post


class Dispatcher:
    def get_argv(self):
        argv = sys.argv
        if len(argv) < 2:
            print('Утилита принимает url статьи и сохраняет текст статьи в отдельный файл.')
            print('Образец: \n[test.py [https://имя_сайта_/путь_к_статье]]')
            raise SystemExit
        check = self.check_url(sys.argv[1])
        print(check)
        if check:
            return sys.argv[1]
        else:
            print('url невалидный')
            raise SystemExit

    def check_url(self, url):
        order = ('sheme', 'netloc', 'path')
        try:
            check = urlparse(url)
            if all([check.scheme, check.netloc, check.path]):
                return True
            else:
                return False
        except:
            return False

    def handler(self):
        url = self.get_argv()
        post = Post(url)
        corrector = Corrector(post.post)
        corrector.handler()
        writter = Writter(url, corrector.post)
        writter.hadler()



if __name__ == '__main__':
    publisher = Dispatcher()
    publisher.handler()
