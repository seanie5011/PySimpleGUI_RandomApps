import PySimpleGUI as sg


# global
theme_menu = ['menu', ['LightGrey1', 'dark', 'DarkGray8', 'Reddit']]


def create_window(theme):
    ''' creates the window and elements used in this project, with ability to change theme'''
    # window options and settings
    sg.theme(theme)
    button_size = (6, 3)
    sg.set_options(font='Franklin 14', button_element_size=button_size)  # for some reason x-axis size does not work unless we specify for every button

    layout = [
        [sg.Text('output',
                 font='Franklin 26',
                 justification='right',
                 expand_x=True,
                 pad=(10, 20),
                 right_click_menu=theme_menu,
                 key='-TEXT_OUTPUT-'
                 )
         ],
        [sg.Button('Clear', expand_x=True), sg.Button('Enter', expand_x=True)],
        [sg.Button(7, size=button_size), sg.Button(8, size=button_size), sg.Button(9, size=button_size), sg.Button('*', size=button_size)],
        [sg.Button(4, size=button_size), sg.Button(5, size=button_size), sg.Button(6, size=button_size), sg.Button('/', size=button_size)],
        [sg.Button(1, size=button_size), sg.Button(2, size=button_size), sg.Button(3, size=button_size), sg.Button('-', size=button_size)],
        [sg.Button(0, expand_x=True), sg.Button('.', size=button_size), sg.Button('+', size=button_size)]
        ]

    return sg.Window('Calculator', layout)


def main():
    # call function to create window with desired theme, can select by right-clicking text
    window = create_window('LightGrey1')

    current_num = []  # contain current numbers inputted in a list
    full_operation = []  # contain all numbers and operations inputted in a list

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        # if user selects new theme, close this window and recreate with new theme
        if event in theme_menu[1]:
            window.close()
            window = create_window(event)

        # all input checks
        if event in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            current_num.append(event)
            num_string = ''.join(current_num)  # creates a string of all inputted numbers
            window['-TEXT_OUTPUT-'].update(num_string)

        if event in ['*', '/', '-', '.', '+']:
            full_operation.append(''.join(current_num))
            full_operation.append(event)
            window['-TEXT_OUTPUT-'].update('')  # update with empty slot upon operation
            current_num = []  # reset current number

        if event in 'Enter':
            full_operation.append(''.join(current_num))  # add number currently inputted
            result = eval(''.join(full_operation))  # eval evaluates the expression written in the string
            window['-TEXT_OUTPUT-'].update(result)
            current_num = [str(result)]  # set current number to new output
            full_operation = []

        if event in 'Clear':  # reset all
            window['-TEXT_OUTPUT-'].update('')
            current_num = []
            full_operation = []

    window.close()

if __name__ == '__main__':
    main()
