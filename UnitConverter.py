import PySimpleGUI as sg


# converter class containing all unit conversions supported
class Converter:
    def kg_to_lbs(self, kg):
        lbs = kg * 2.20462
        return lbs

    def lbs_to_kg(self, lbs):
        kg = lbs / 2.20462
        return kg

    def kg_to_tonne(self, kg):
        tonne = kg / 1000
        return tonne

    def tonne_to_kg(self, tonne):
        kg = tonne * 1000
        return kg


def main():
    # create layout with amount of rows corresponding to number of lists
    # each row contains some elements
    # we can give each a key which is a unique string identifier
    # we can also edit size of each element at will
    layout = [[sg.Input(key='-INPUT-'), sg.Spin(['lbs to kg', 'kg to lbs', 'kg to tonne', 'tonne to kg'], key='-SPIN_UNITS-'), sg.Button('Convert', key='-BUTTON_CONVERT-', size=(5, 2))],
              [sg.Text('OUTPUT', key='-TEXT_OUTPUT-')]]

    window = sg.Window('Converter', layout)  # create window with a title and a layout

    converter = Converter()
    while True:
        event, values = window.read()  # returns all events of that frame, along with a dict of all values

        # quit logic
        if event == sg.WIN_CLOSED:
            break

        # button pressed
        if event == '-BUTTON_CONVERT-':
            try:
                input_value = float(values['-INPUT-'])  # must pass in float as values returns a string

                # identify correct conversion
                if values['-SPIN_UNITS-'] == 'lbs to kg':
                    value = converter.lbs_to_kg(input_value)
                elif values['-SPIN_UNITS-'] == 'kg to lbs':
                    value = converter.kg_to_lbs(input_value)
                elif values['-SPIN_UNITS-'] == 'kg to tonne':
                    value = converter.kg_to_tonne(input_value)
                elif values['-SPIN_UNITS-'] == 'tonne to kg':
                    value = converter.tonne_to_kg(input_value)
            except ValueError:  # if input value is not float-like
                print("ValueError: the value inputted is not of correct form type float.")
                value = "Please enter a float number."
            except:
                print("Unknown Error.")
                value = "ERROR"

            window['-TEXT_OUTPUT-'].update(value)  # we can update the specified window element with new value

    window.close()

if __name__ == '__main__':
    main()
