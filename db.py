import configs

class InMemoryDb:
    counter = 0
    notes = {}

    def add_note(self, title, content):
        self.counter += 1
        note = Note(self.counter, title, content)
        self.notes[self.counter] = note
        return note.get()

    def get_note(self, id_):
        return self.notes.get(id_)

    def get_notes(self, query=None):
        return list(map(lambda x: x.get(), filter(lambda x: x.contains(query), self.notes.values())))

    def modify_note(self, id_, title, content):
        if not self.notes.get(id_):
            return None
        note = Note(id_, title, content)
        self.notes[id_] = note

        return note

    def delete(self, id_):
        if not self.notes.get(id_):
            return False

        self.notes.pop(id_, None)
        return True

class Note:
    def __init__(self, id_, title, content):
        self.id = id_
        self.title = title
        self.content = content

    def contains(self, query=None):
        if not query:
            return True
        return query in self.title or query in self.content

    def get(self):
        title = self.title
        if not title:
            title = self.content[:configs.amount_of_content_symbols_if_title_missed]

        return {
            'id': self.id,
            'title': title,
            'content': self.content
        }