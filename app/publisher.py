import re


class Corrector:
    def __init__(self, body, size):
        self.body = body
        self.size = size
        self.new_body = []
        self.links = []
        self.post = None

    def processesCorrector(self):
        start = 0
        pattern = lambda x: 'LINK' in x

        for line in self.body:
            self.search_links(line)
            new_line = self.replace_links(line)
            new_line = self.search_head(new_line)
            new_line = self.search_indent(new_line)
            new_line = self.clear_line(new_line)
            if pattern(new_line):
                new_line = self.create_new_links(new_line, start=start)
                start += 1
            self.new_body.append(new_line)
        self.post = self.new_body
        self.get_size()

    def search_links(self, line):
        new_links = re.findall(r'<a\s.*?href="(.+?)".*?>(.+?)</a>', line)
        if new_links:
            self.links.append(new_links)

    def search_head(self, line):
        new_line = re.sub(r'<strong>' or r'</strong>', '999', line)
        return new_line

    def replace_links(self, line):
        new_line = ''
        new_line += re.sub(r'<a\s.*?href="(.+?)".*?>(.+?)</a>', 'LINK', line)
        return new_line

    def clear_line(self, line):
        new_line = re.sub(r'(?:<).*?(?:>)', '', line)
        for x in ['\n', '\t', '\r']:
            new_line = new_line.replace(x, '')
        return new_line

    def create_new_links(self, line, start=0, step=0, end=0):
        new_line = ''
        new_line += re.sub('LINK', '[' + self.links[start][step][end] + ']' + ' ' + self.links[start][step][end + 1],
                           line)
        return new_line

    def search_indent(self, line):
        new_line = line.replace('<p>', '000')
        return new_line

    def get_size(self):
        self.post = []
        for param in self.new_body:
            gen = self.split_by_spaces(param, self.size)
            while True:
                try:
                    string = gen.__next__()
                    self.post.append(string)
                except:
                    break

    def split_by_spaces(self, string, length):
        lower_bound = 0
        upper_bound = 0
        last_space_position = string.rindex(' ')
        try:
            while upper_bound < len(string):
                upper_bound = string.rindex(' ', lower_bound, lower_bound + length)
                if upper_bound == last_space_position:
                    upper_bound = len(string)
                if upper_bound - lower_bound > length:
                    string.zfill(length)
                yield string[lower_bound:upper_bound].strip()
                lower_bound = upper_bound
        except ValueError:
            raise ValueError('Невозможно получить подстроку в заданных границах')


class Writer:
    def __init__(self, file_name, obj):
        self.file_name = file_name[8:] + r'.txt'
        self.obj = obj

    def write(self):
        name = re.sub(r'/', '_', self.file_name)
        w = open(name, 'w')
        for st in self.obj:
            if '000' in st:
                st = st.replace('000', '\n ')
            if '999' in st:
                st = st.replace('999', '\n ')
            w.write(st + '\n')
        w.close()
