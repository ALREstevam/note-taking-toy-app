class Note:
    def __init__(self, show=None):
        self.title = None
        self.content = None
        self.show = show

    def print(self):
        self.show(self)

    def config(self, show=None):
        if show: self.show = show

    def write(self, title=None, content=None):
        if title:
            self.title = title
        if content:
            self.content = content
        return self

    def search_points(self, query):
        return 0.7 * self.title.lower().count(query.lower()) +\
               0.3 * self.content.lower().count(query.lower())


