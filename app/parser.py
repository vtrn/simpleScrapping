import urllib.request
import bs4 as bs


class Post:
    def __init__(self, url):
        self.url = url
        self.post = self.handle()

    def get_html(self):
        html = urllib.request.urlopen(self.url)
        html = html.read()
        return html

    def get_post_and_title(self, html):
        post = bs.BeautifulSoup(html, 'html.parser')
        title = post.find_all('title')
        post = post.find_all('p')
        post.insert(0, str(title))
        return post

    def get_transform(self, post):
        post = [str(x) for x in post]
        return post

    def handle(self):
        html = self.get_html()
        post = self.get_post_and_title(html)
        post = self.get_transform(post)
        return post