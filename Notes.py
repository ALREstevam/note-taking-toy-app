from Note import Note
import json
import zlib
from pathlib import Path

class Archive:

    @staticmethod
    def compress(decompressed):
        return zlib.compress(decompressed.encode('utf-8'))

    @staticmethod
    def decompress(compressed):
        return zlib.decompress(compressed).decode('utf-8')

    @staticmethod
    def obj_to_json(notes):
        return json.dumps(
            list(
                map(lambda note: {'title': note.title, 'content': note.content}, notes)
            )
        )

    @staticmethod
    def dict_to_json(notes):
        return json.dumps(
            list(
                map(lambda note: { 'title': note['title'], 'content': note['content']}, notes)
            )
        )

    @staticmethod
    def json_to_obj(data):
        return list(
            map( lambda el: Note().write(el['title'], el['content']), json.loads(data))
        )

    @staticmethod
    def json_to_dict(data):
        return json.loads(data)

    @staticmethod
    def archive(notes, mode='obj', path='./.notes'):
        with open(Path(path), 'wb') as file:
            if mode == 'obj':
                file.write(
                        Archive.compress(Archive.obj_to_json(notes))
                )
            else:
                file.write(
                        Archive.compress(Archive.dict_to_json(notes))
                )

    @staticmethod
    def unarchive(mode='obj', path='./.notes'):
        try:
            with open(Path(path), 'rb') as file:
                if mode == 'obj':
                    return Archive.json_to_obj(Archive.decompress(file.read()))
                else:
                    return Archive.json_to_dict(Archive.decompress(file.read()))
        except FileNotFoundError:
            return []


class Notes:
    def __init__(self, note_display):
        self.note_display = note_display
        self.notes = {}
        self.load_notes()

    def load_notes(self):
        for item in Archive.unarchive(mode='dict'):
            self.add_edit(item['title'], item['content'], archive=False)

    def display_all(self):
        for key in self.notes.keys():
            self.notes[key].print()

    def note(self, title):
        return self.notes[title]

    def display(self, title):
        if title in self.notes:
            self.notes[title].print()

    def titles(self):
        return self.notes.keys()

    def add_edit(self, title, content, archive=True):
        self.notes[title] = Note(self.note_display).write(title, content)
        if archive:
            Archive.archive(self.notes.values(), mode='obj')

    def search(self, query):

        filtered = list(filter(lambda el: el.search_points(query) > 0, list(self.notes.values())))

        return reversed(
                (
                    sorted(filtered, key=lambda el: el.search_points(query))
                )
            )

    def delete(self, title, archive=True):
        if title in self.notes:
            del self.notes[title]
            if archive:
                Archive.archive(self.notes.values(), mode='obj')
