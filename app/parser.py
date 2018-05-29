#!/usr/bin/env python3

import urllib.request
import bs4 as bs


class Parser:
    def __init__(self, url):
        self.url = url
        self.post = self.parse()

    def get_html(self):
        """Получает данные

        """
        try:
            html = urllib.request.urlopen(self.url)
            html = html.read()
            return html
        except:
            print('Невозможно получить данные.')

    def get_post_and_title(self, html):
        """Собирает данные из необходимых тегов

        """
        garbage = bs.BeautifulSoup(html, 'html.parser')
        title = garbage.find_all('title')
        post = garbage.find_all('p')

        # ниже другой алгоритм получения,
        # необходимых данных,
        #count = {}
        #for d in post:
        #    for p in d:
        #        if '<script>' not in str(p):
        #            for l in p:
        #                count[len(l)] = post.index(d)
        #pos = max(count.keys())
        #index = count[pos]

        post.insert(0, str(title[0]))
        return post

    def get_transform(self, post):
        """Преобразовывает сырые данные в строки

        """
        post = [str(x) for x in post]
        return post

    def parse(self):
        """Запускает процессы

        """
        html = self.get_html()
        post = self.get_post_and_title(html)
        post = self.get_transform(post)
        return post