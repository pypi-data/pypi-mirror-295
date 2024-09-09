import PySimpleGUI as sg
from wiliot_testers.test_equipment import YoctoSensor


class YoctoSensorGUI:
    def __init__(self):
        self.main_sensor = self.initialize_sensor()
        self.real_values_array = []
        self.measured_values_array = []

    def initialize_sensor(self):
        try:
            sensor = YoctoSensor(logger='Light')
            return sensor
        except Exception as ee:
            sg.popup_error('No sensor is connected')
            raise SystemExit('No sensor is connected')

    def single_calibration(self):
        read_layout = [[sg.Text('Current Light Value:'), sg.Text('', key='-LIGHT-')],
                       [sg.Text('Enter real LUX value:'), sg.Input(key='real_value', size=(4, 1)), sg.Button('Add')],
                       [sg.Button('Close')]]
        read_window = sg.Window('Single Calibration', read_layout, keep_on_top=True)

        while True:
            event, values = read_window.read(timeout=1000)  # Update every second
            if event in (sg.WINDOW_CLOSED, 'Close'):
                break
            elif event == 'Add':
                try:
                    real_value = int(values['real_value'])
                    self.main_sensor.calibration_light_point(real_value)
                except Exception as e:
                    sg.popup_error('Invalid real LUX value')
            try:
                light_value = self.main_sensor.get_light()
                read_window['-LIGHT-'].update(light_value)
            except Exception as e:
                read_window['-LIGHT-'].update(f'Error: {e}')

        read_window.close()

    def collect_calibration_points(self):
        calibration_layout = [
            [sg.Text('Enter real LUX value:'), sg.Input(key='real_value')],
            [sg.Button('Add'), sg.Button('Submit', visible=False), sg.Button('Cancel')]
        ]
        calibration_window = sg.Window('Calibration', calibration_layout)

        while True:
            event, values = calibration_window.read()
            if event == sg.WINDOW_CLOSED or event == 'Cancel':
                break
            elif event == 'Add':
                real_value = values['real_value']
                if real_value:
                    try:
                        real_value = float(real_value)
                        measured_value = self.main_sensor.get_light()
                        self.real_values_array.append(real_value)
                        self.measured_values_array.append(measured_value)
                        sg.popup(f'Added: Real LUX: {real_value}, Measured LUX: {measured_value}')
                        if len(self.real_values_array) >= 2:
                            calibration_window['Submit'].update(visible=True)
                    except ValueError:
                        sg.popup_error('Invalid real LUX value')
            elif event == 'Submit' and len(self.real_values_array) >= 2:
                self.main_sensor.calibration_points(self.real_values_array, self.measured_values_array)
                sg.popup('Calibration submitted')
                break

        calibration_window.close()

    def read_sensor_data(self):
        read_layout = [[sg.Text('Current Light Value:'), sg.Text('', key='-LIGHT-')],
                       [sg.Button('Close')]]
        read_window = sg.Window('Read Sensor Data', read_layout, keep_on_top=True)

        while True:
            event, values = read_window.read(timeout=1000)  # Update every second
            if event in (sg.WINDOW_CLOSED, 'Close'):
                break
            try:
                light_value = self.main_sensor.get_light()
                read_window['-LIGHT-'].update(light_value)
            except Exception as e:
                read_window['-LIGHT-'].update(f'Error: {e}')

        read_window.close()

    def run(self):
        layout = [
            [  # [sg.Button('Calibrate Points')],
                [sg.Button('Calibration', size=(35, 6), button_color='Orange')],
                [sg.Button('Read Data', size=(35, 6), button_color='Green')],
                [sg.Button('Quit', size=(35, 4), button_color='Red')]]
        ]

        window = sg.Window('Lightmeter Tool', layout, size=(300, 300))

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Quit':
                break
            elif event == 'Calibrate Points':
                self.collect_calibration_points()
            elif event == 'Calibration':
                self.single_calibration()
            elif event == 'Read Data':
                self.read_sensor_data()

        window.close()
        sys.exit()


# Run the GUI
if __name__ == '__main__':
    gui = YoctoSensorGUI()
    gui.run()
