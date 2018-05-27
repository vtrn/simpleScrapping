import re


class Corrector:
    def __init__(self, body):
        self.body = body
        self.new_body = []
        self.links = []
        self.post = None

    def handle(self):
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
            print(post)
        return post

class Writer:
    def __init__(self, file_name, obj):
        self.file_name = file_name[8:] + r'.txt'
        self.obj = obj
    def hadle(self):
        name = re.sub(r'/', '_', self.file_name)
        w = open(name, 'w')
        for par in self.obj:
            if par:
                w.write('\n')
                for string in par:
                    w.write('\n' + string)
        w.close()
