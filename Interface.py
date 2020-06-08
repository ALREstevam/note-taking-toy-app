import inquirer
from Notes import Notes
from Colorful import B, F, S, BOLD, linecolorprint, colorprint
from Note import Note

class Display:

    @staticmethod
    def display_note(note):
        linecolorprint(3 *' ' + note.title, pos='left', fore=F.GREEN, back=B.GREEN, style=S.BRIGHT)
        for line in ['', *note.content.split('\n'), '']:
            linecolorprint(line, pos='left', back=B.BLUE)
        print('\n\n')

    @staticmethod
    def header(name, page=None):
        linecolorprint(name, ' : ' if page is not None else '', page , pos='center', fore=F.BLUE, back=B.BLUE, style=S.BRIGHT)

    @staticmethod
    def clear():
        import subprocess, platform
        if platform.system()=="Windows":
            subprocess.Popen("cls", shell=True).communicate() #I like to use this instead of subprocess.call since for multi-word commands you can just type it out, granted this is just cls and subprocess.call should work fine
        else: #Linux and Mac
            print("\033c", end="")

class Interface:

    def __init__(self):
        self.notes = Notes(Display.display_note)
        self.app_name = 'Notes'

    def exit(self, *args):
        Display.clear()
        exit()


    def main_menu(self):
        Display.clear()

        self.picker({
            '[ See notes ]': self.see_notes,
            '[ Add note ]': self.add_note,
            '[ Edit notes ]': self.edit_note,
            '[ Search notes ]': self.search_note,
            '[ Delete notes ]': self.delete_note,
            '[ Exit ]': self.exit
        }, 'main menu', back_action=self.exit)



    def picker(self, options : dict, header, back_action=None):
        default = None
        back = False

        while not back:
            try:
                Display.clear()
                Display.header(self.app_name, header)

                questions = [
                  inquirer.List('task',
                                choices=list(options.keys()),
                                default=default
                            ),
                ]
                answer = inquirer.prompt(questions)

                if answer and answer['task']:
                    default = answer['task']
                    done = options[answer['task']](answer['task'])

                    if type(done) == dict:
                        if 'back' in done:
                            back = done['back']
                        else:
                            back = False

                        if 'header' in done: header = done['header']
                        if 'options' in done: options = done['options']
                        if 'default' in done: default = done['default']
                        if 'back_action' in done: back_action = done['back_action']

                    else:
                        back = done

                else:
                    back = True
            except KeyboardInterrupt:
                if back_action:
                    return back_action()


    def filled_input(self, query):
        text = ''

        while not text or text == '':
            text = str(input(query))

        return text

    def yesno(self, query):
        try:
            questions = [
              inquirer.List('yesno',
                            message=query,
                            choices=['Yes', 'No'],
                        ),
            ]
            answer = inquirer.prompt(questions)
            return answer and answer['yesno'] == 'Yes'

        except KeyboardInterrupt:
            return False

    def see_notes(self, *args):

        def display_all(*args):
            Display.clear()
            self.notes.display_all()
            input('[ Press enter to go back]')

        def back(*args):
            Display.clear()
            self.main_menu()
            return True


        def display_specific(answer):
            Display.clear()
            self.notes.display(answer)
            input('[ Press enter to go back]')


        options = {
            '[ Display all ]': display_all,
            '[ Back ]': back,
        }

        for title in self.notes.titles():
            options[title] = display_specific

        self.picker(options, 'see notes', back_action=self.main_menu)


    def note_editor(self, title, default=None):
        questions = [
          inquirer.Editor('content', message=f'{title} content' if title else 'content', default=default)
        ]
        answers = inquirer.prompt(questions)

        if answers and 'content' in answers:
            return answers['content']
        else:
            return None

    def add_note(self, *args):
        try:
            Display.clear()
            Display.header(self.app_name, 'add note')

            title = self.filled_input('Note\'s title (leave empty to fill later): ')
            print()

            content = self.note_editor(title)

            print()
            print(content)
            print()

            if not title:
                title = self.filled_input('Note\'s title: ')

            Display.clear()
            Display.header(self.app_name, 'review note')

            Note(Display.display_note).write(title, content).print()

            if self.yesno('Save'):
                self.notes.add_edit(title, content)
            self.main_menu()
        except KeyboardInterrupt:
            self.main_menu()


    def edit_note(self, *args):

        def back(answer):
            Display.clear()
            self.main_menu()
            return True


        def edit(title):
            note = self.notes.note(title)

            Display.clear()
            Display.header(self.app_name, 'edit note')

            print(f'The note\'s title is "{title}"')
            new_title = str(input('New title (leave empty to keep / fill later): '))

            content = self.note_editor(new_title if new_title else title, note.content)

            if not new_title:
                new_title = str(input(f'New title (leave empty to keep "{title}"): '))

            if new_title and title is not new_title:
                self.notes.delete(title)

            self.notes.add_edit(
                new_title if new_title else title,
                content if content else note.content
            )

            options = {
                '[ Back ]': back,
            }

            for title in self.notes.titles():
                options[title] = edit

            return {
                'options': options,
                'default': new_title if new_title else title
            }


        options = {
            '[ Back ]': back,
        }

        for title in self.notes.titles():
            options[title] = edit

        self.picker(options, 'edit notes', back_action=self.edit_note)

    def search_note(self, *args):
        try:
            Display.clear()
            query = self.filled_input('Search: ')

            for note in self.notes.search(query):
                note.print()

            input('[ Press enter to go back]')


        except KeyboardInterrupt:
            return self.main_menu()


    def delete_note(self, *args):
        Display.clear()

        def back(answer):
            Display.clear()
            self.main_menu()
            return True


        def delete(title):
            note = self.notes.note(title)

            Display.clear()
            Display.header(self.app_name, 'edit note')

            if self.yesno(f'Delete "{title}"'):
                self.notes.delete(title)

            options = {
                '[ Back ]': back,
            }

            for title in self.notes.titles():
                options[title] = delete

            return {
                'options': options,
            }


        options = {
            '[ Back ]': back,
        }

        for title in self.notes.titles():
            options[title] = delete

        self.picker(options, 'delete notes', back_action=self.delete_note)




