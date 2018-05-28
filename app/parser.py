import urllib.request
import bs4 as bs


class Parser:
    def __init__(self, url):
        self.url = url
        self.post = self.parse()

    def get_html(self):
        html = urllib.request.urlopen(self.url)
        html = html.read()
        return html

    def get_post_and_title(self, html):
        garbage = bs.BeautifulSoup(html, 'html.parser')
        title = garbage.find_all('title')
        div = garbage.find_all('p')
        #count = {}
        #for d in div:
        #    for p in d:
        #        if '<script>' not in str(p):
        #            for l in p:
        #                count[len(l)] = div.index(d)
        #pos = max(count.keys())
        #index = count[pos]
        post = div
        post.insert(0, str(title))
        return post

    def get_transform(self, post):
        post = [str(x) for x in post]
        return post

    def parse(self):
        html = self.get_html()
        post = self.get_post_and_title(html)
        post = self.get_transform(post)
        return post