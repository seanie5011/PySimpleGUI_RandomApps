import PySimpleGUI as sg
from pathlib import Path

# global
smileys = [
    'happy', [':)', 'xD', ':D', '<3'],
    'sad', [':(', 'T_T'],
    'other', [':3']
    ]  # these are ordered in "name", [events] -> "name", [events] -> etc

menu_layout = [
    ['File', ['Open', 'Save as', '---', 'Exit']],
    ['Tools', ['Word Count']],
    ['Add', smileys]
    ]


def main():
    sg.theme('GrayGrayGray')
    layout = [
        [sg.Menu(menu_layout)],
        [sg.Text('Untitled', key='-DOCNAME-')],
        [sg.Multiline(no_scrollbar=True, size=(40, 30), key='-TEXTBOX-')]
        ]

    window = sg.Window('Text Editor', layout)

    smiley_events = smileys[1] + smileys[3] + smileys[5]  # get all the event lists and add from smileys

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        # open file text from browse
        if event == 'Open':
            file_path = sg.popup_get_file('open', no_window=True)  # opens up the file browser without the extra observing window

            if file_path:
                file = Path(file_path)  # uses pathlib module to import this file
                window['-TEXTBOX-'].update(file.read_text())  # reads the text from this file and puts it into our text editor
                window['-DOCNAME-'].update(file_path.split('/')[-1])  # find last element in list of file path (is file name)

        # save this file on computer
        if event == 'Save as':
            file_path = sg.popup_get_file('Save as', no_window=True, save_as=True) + '.txt'
            file = Path(file_path)
            file.write_text(values['-TEXTBOX-'])
            window['-DOCNAME-'].update(file_path.split('/')[-1])

        # create a popup of the word count
        if event == 'Word Count':
            full_text = values['-TEXTBOX-']

            clean_text = full_text.replace('\n', ' ')  # replace all new lines with spaces
            clean_text = clean_text.split(' ')  # split into a list containing all words delimited by a space
            clean_text = list(filter(None, clean_text))  # remove all empty strings

            word_count = len(clean_text)
            char_count = len(''.join(clean_text))  # combine all words together in string

            sg.popup(f'word count: {word_count}\ncharacters: {char_count}')

        # add a smiley to the text
        if event in smiley_events:
            full_text = values['-TEXTBOX-']

            new_text = full_text + event

            window['-TEXTBOX-'].update(new_text)

    window.close()

if __name__ == '__main__':
    main()
