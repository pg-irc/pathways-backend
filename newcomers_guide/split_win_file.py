import re


def is_chapter(line):
    regex = r'[\d ]*CHAPTER.*'
    if re.fullmatch(regex, line):
        return True
    return False


def get_chapter(line):
    regex = r'[\d ]*(CHAPTER.*)'
    result = re.match(regex, line)[1].strip()
    if len(result) < len('CHAPTER 8 - '):
        raise RuntimeError(line)
    return result


def is_title(line):
    regex = r'[\d\. ]*Topic:.*'
    if re.fullmatch(regex, line):
        return True
    return False


def get_title(line):
    regex = r'[\d\. ]*Topic:(.*)'
    result = re.match(regex, line)[1].strip()
    if result == '':
        raise RuntimeError(line)
    return result


def is_tag(line):
    regex = r'Tags:.*'
    if re.fullmatch(regex, line):
        return True
    return False


def get_tags(line):
    regex = r'Tags:(.*)'
    result = re.match(regex, line)[1].strip().split()
    return result


class Topic:
    def __init__(self, chapter, name, tags, text):
        self.chapter = chapter
        self.name = name
        self.tags = tags
        self.text = text

    def file_path(self):
        return f'{self.chapter}/topics/{self.name}/en.{self.name}.md'


class TopicWriter:
    def __init__(self):
        self.topics = []
        self.chapter = ''
        self.clear()

    def clear(self):
        self.name = ''
        self.tags = []
        self.text = ''

    def parse(self, line):
        if is_chapter(line):
            self.chapter = get_chapter(line)
        elif is_title(line):
            self.save_current_topic()
            self.name = get_title(line)
        elif is_tag(line):
            self.tags = get_tags(line)
        else:
            self.text += line + '\n'

    def save_current_topic(self):
        if self.name:
            self.topics.append(Topic(self.chapter, self.name, self.tags, self.text))
            self.clear()

    def done(self):
        self.save_current_topic()
        return self


def parse_string(text):
    writer = TopicWriter()
    for line in text.split('\n'):
        writer.parse(line)
    return writer.done()
