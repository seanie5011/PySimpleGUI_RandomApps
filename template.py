import PySimpleGUI as sg


def main():
    layout = [[]]

    window = sg.Window('Title', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

    window.close()

if __name__ == '__main__':
    main()
