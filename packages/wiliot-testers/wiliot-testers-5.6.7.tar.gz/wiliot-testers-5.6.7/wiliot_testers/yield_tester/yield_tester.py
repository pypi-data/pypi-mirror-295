#  """
#    Copyright (c) 2016- 2024, Wiliot Ltd. All rights reserved.
#
#    Redistribution and use of the Software in source and binary forms, with or without modification,
#     are permitted provided that the following conditions are met:
#
#       1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#       2. Redistributions in binary form, except as used in conjunction with
#       Wiliot's Pixel in a product or a Software update for such product, must reproduce
#       the above copyright notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the distribution.
#
#       3. Neither the name nor logo of Wiliot, nor the names of the Software's contributors,
#       may be used to endorse or promote products or services derived from this Software,
#       without specific prior written permission.
#
#       4. This Software, with or without modification, must only be used in conjunction
#       with Wiliot's Pixel or with Wiliot's cloud service.
#
#       5. If any Software is provided in binary form under this license, you must not
#       do any of the following:
#       (a) modify, adapt, translate, or create a derivative work of the Software; or
#       (b) reverse engineer, decompile, disassemble, decrypt, or otherwise attempt to
#       discover the source code or non-literal aspects (such as the underlying structure,
#       sequence, organization, ideas, or algorithms) of the Software.
#
#       6. If you create a derivative work and/or improvement of any Software, you hereby
#       irrevocably grant each of Wiliot and its corporate affiliates a worldwide, non-exclusive,
#       royalty-free, fully paid-up, perpetual, irrevocable, assignable, sublicensable
#       right and license to reproduce, use, make, have made, import, distribute, sell,
#       offer for sale, create derivative works of, modify, translate, publicly perform
#       and display, and otherwise commercially exploit such derivative works and improvements
#       (as applicable) in conjunction with Wiliot's products and services.
#
#       7. You represent and warrant that you are not a resident of (and will not use the
#       Software in) a country that the U.S. government has embargoed for use of the Software,
#       nor are you named on the U.S. Treasury Department’s list of Specially Designated
#       Nationals or any other applicable trade sanctioning regulations of any jurisdiction.
#       You must not transfer, export, re-export, import, re-import or divert the Software
#       in violation of any export or re-export control laws and regulations (such as the
#       United States' ITAR, EAR, and OFAC regulations), as well as any applicable import
#       and use restrictions, all as then in effect
#
#     THIS SOFTWARE IS PROVIDED BY WILIOT "AS IS" AND "AS AVAILABLE", AND ANY EXPRESS
#     OR IMPLIED WARRANTIES OR CONDITIONS, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED
#     WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, NONINFRINGEMENT,
#     QUIET POSSESSION, FITNESS FOR A PARTICULAR PURPOSE, AND TITLE, ARE DISCLAIMED.
#     IN NO EVENT SHALL WILIOT, ANY OF ITS CORPORATE AFFILIATES OR LICENSORS, AND/OR
#     ANY CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
#     OR CONSEQUENTIAL DAMAGES, FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES,
#     FOR ANY LOSS OF USE OR DATA OR BUSINESS INTERRUPTION, AND/OR FOR ANY ECONOMIC LOSS
#     (SUCH AS LOST PROFITS, REVENUE, ANTICIPATED SAVINGS). THE FOREGOING SHALL APPLY:
#     (A) HOWEVER CAUSED AND REGARDLESS OF THE THEORY OR BASIS LIABILITY, WHETHER IN
#     CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE);
#     (B) EVEN IF ANYONE IS ADVISED OF THE POSSIBILITY OF ANY DAMAGES, LOSSES, OR COSTS; AND
#     (C) EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.
#  """

import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from wiliot_core import *
from wiliot_tools.utils.wiliot_gui.wiliot_gui import WiliotGui, popup_message

from wiliot_testers.test_equipment import YoctoSensor
from configs.inlay_data import all_inlays
import os
import serial
from wiliot_testers.tester_utils import dict_to_csv
import logging
import threading
import time
import datetime
import matplotlib
import json
import matplotlib.pyplot as plt
from functools import partial
from wiliot_testers.utils.get_version import get_version
from wiliot_testers.utils.upload_to_cloud_api import upload_to_cloud_api
from wiliot_testers.yield_tester.simulation.yield_simulation_utils import get_simulated_gw_port, \
    AUTO_TRIGGERS, AUTO_PACKET, TIME_BETWEEN_AUTO_TRIGGERS
from wiliot_testers.yield_tester.utils.get_arduino_ports import get_arduino_ports

MAX_SUB1G_POWER = 29
MAX_BLE_POWER = 22
SECONDS_WITHOUT_PACKETS = 60
SECONDS_FOR_GW_ERROR_AFTER_NO_PACKETS = 120
TIME_BETWEEN_MATRICES = 3
RED_COLOR = 'red'
BLACK_COLOR = 'black'
SET_VALUE_MORE_THAN_100 = 110
VALUE_WHEN_NO_SENSOR = -10000
MIN_Y_FOR_PLOTS = 0
MAX_Y_FOR_PLOTS = 112
FIRST_STEP_SIZE = 10
BAUD_ARDUINO = 1000000
MAND_FIELDS = ['wafer_lot', 'wafer_num', 'matrix_num', 'thermodes_col']  # mandatory fields in GUI before the run
PACKET_DATA_FEATURES_TITLE = [
    'raw_packet', 'adv_address', 'decrypted_packet_type', 'group_id',
    'flow_ver', 'test_mode', 'en', 'type', 'data_uid', 'nonce', 'enc_uid',
    'mic', 'enc_payload', 'gw_packet', 'rssi', 'stat_param', 'time_from_start',
    'counter_tag', 'is_valid_tag_packet', 'gw_process', 'is_valid_packet', 'inlay_type'
]

script_dir = os.path.dirname(__file__)
json_file_path = os.path.join(script_dir, 'configs', 'user_inputs.json')
default_user_inputs = {
    "min_cumulative": "60",
    "min_cumulative_line": "yes",
    "min_current": "20",
    "min_current_line": "yes",
    "max_temperature": "40",
    "min_temperature": "10",
    "temperature_type": "C",
    "min_humidity": "20",
    "max_humidity": "90",
    "min_light_intensity": "0",
    "max_light_intensity": "1500",
    "red_line_cumulative": "85",
    "red_line_current": "50",
    "pin_number": "004",
    "Arduino": "Yes"
}
try:
    with open(json_file_path) as f:
        user_inputs = json.load(f)
    for key, value in default_user_inputs.items():
        if key not in user_inputs:
            user_inputs[key] = value
    with open(json_file_path, 'w') as f:
        json.dump(user_inputs, f, indent=4)
except Exception as e:
    user_inputs = default_user_inputs
    os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
    with open(json_file_path, 'w') as f:
        json.dump(user_inputs, f, indent=4)

ARDUINO_EXISTS = (user_inputs.get('Arduino') == 'Yes')
matplotlib.use('TkAgg')
lst_inlay_options = list(all_inlays.keys())
today = datetime.date.today()
formatted_today = today.strftime("%Y%m%d")  # without -
formatted_date = today.strftime("%Y-%m-%d")
current_time = datetime.datetime.now()
cur_time_formatted = current_time.strftime("%H%M%S")  # without :
time_formatted = current_time.strftime("%H:%M:%S")
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S %p')
root_logger = logging.getLogger()

for handler in root_logger.handlers:
    if isinstance(handler, logging.StreamHandler):
        handler.setLevel(logging.INFO)


class AdvaProcess(object):
    """
    Counting the number of unique advas
    """

    def __init__(self, stop_event, inlay_type, logging_file, listener_path):
        self.stopped_by_user = False
        self.take_care_of_pausing = False
        self.gw_error_connection = False
        self.second_without_packets = False
        self.gw_instance = None
        self.logger_file = logging_file
        self.listener_path = listener_path
        self.all_tags = Queue()
        self.stop = stop_event
        self.gw_start_time = datetime.datetime.now()
        self.init_gw(listener_path)
        self.last_change_time = datetime.datetime.now()
        self.number_of_sensor_triggers = 0
        self.needed_time_between_matrices = TIME_BETWEEN_AUTO_TRIGGERS if AUTO_TRIGGERS else TIME_BETWEEN_MATRICES
        self.inlay_type = inlay_type
        self.gw_reset_config()
        time.sleep(1)
        self.last_change_time = datetime.datetime.now()

    def init_gw(self, listener_path=None):

        try:
            if self.gw_instance is None:
                gw_port = get_simulated_gw_port() if AUTO_PACKET else None
                self.gw_instance = WiliotGateway(auto_connect=True,
                                                 logger_name='yield',
                                                 is_multi_processes=sys.platform != "darwin",
                                                 log_dir_for_multi_processes=listener_path,
                                                 port=gw_port,
                                                 np_max_packet_in_buffer_before_error=10)

            else:
                # reconnect
                is_connected = self.gw_instance.is_connected()
                if is_connected:
                    self.gw_instance.close_port()
                self.gw_instance.open_port(self.gw_instance.port, self.gw_instance.baud)

            is_connected = self.gw_instance.is_connected()
            if is_connected:
                self.gw_instance.start_continuous_listener()
            else:
                self.logger_file.warning("Couldn't connect to GW in main thread")
                raise Exception(f"Couldn't connect to GW in main thread")

        except Exception as ee:
            raise Exception(f"Couldn't connect to GW in main thread, error: {ee}")

    def set_stopped_by_user(self, stopped):
        self.stopped_by_user = stopped
        self.take_care_of_pausing = True

    def get_gw_start_time(self):
        return self.gw_start_time

    def get_last_change_time(self):
        return self.last_change_time

    def get_gw_error_connection(self):
        return self.gw_error_connection

    def get_sensors_triggers(self):
        return self.number_of_sensor_triggers

    def gw_reset_config(self, start_gw_app=False):
        """
        Configs the gateway
        """
        if self.gw_instance.connected:
            self.gw_instance.reset_gw()
            self.gw_instance.reset_listener()
            time.sleep(2)
            if not self.gw_instance.is_gw_alive():
                self.logger_file.warning('gw_reset_and_config: gw did not respond')
                raise Exception('gw_reset_and_config: gw did not respond after rest')

            gw_config = all_inlays.get(self.inlay_type)

            cmds = {CommandDetails.scan_ch: gw_config['received_channel'],
                    CommandDetails.time_profile: gw_config['time_profile_val'],
                    CommandDetails.set_energizing_pattern: gw_config['energy_pattern_val'],
                    CommandDetails.set_sub_1_ghz_power: [MAX_SUB1G_POWER],
                    CommandDetails.set_scan_radio: self.gw_instance.get_cmd_symbol_params(
                        freq_str=gw_config['symbol_val'])
                    }
            output_power_cmds = self.gw_instance.get_cmds_for_abs_output_power(abs_output_power=MAX_BLE_POWER)
            cmds = {**cmds, **output_power_cmds}
            self.gw_instance.set_configuration(cmds=cmds, start_gw_app=start_gw_app)
            if not ARDUINO_EXISTS and not AUTO_TRIGGERS:
                pin_num = user_inputs.get('pin_number')
                cmd = '!cmd_gpio CONTROL_IN P%s 0' % pin_num.zfill(3)
                self.gw_instance.write(cmd, must_get_ack=True)
        else:
            raise Exception('Could NOT connect to GW')

    def raising_trigger_number(self):
        self.number_of_sensor_triggers += 1
        self.last_change_time = datetime.datetime.now()
        self.logger_file.info(f'Got a Trigger.  Number of Triggers {self.number_of_sensor_triggers}')

    def run(self):
        """
        Receives available data then counts and returns the number of unique advas.
        """
        self.gw_instance.set_configuration(start_gw_app=True)
        self.gw_instance.reset_start_time()
        self.gw_start_time = datetime.datetime.now()
        got_new_adva = False
        no_data_start_time = None  # Time when we first detect no data available

        while not self.stop.is_set():
            time.sleep(0)
            current_time_of_data = datetime.datetime.now()
            time_condition_met = \
                (current_time_of_data - self.last_change_time).total_seconds() >= self.needed_time_between_matrices

            gw_rsp = self.gw_instance.get_gw_rsp()

            if not self.stopped_by_user and self.take_care_of_pausing:
                self.gw_reset_config(start_gw_app=True)
                self.take_care_of_pausing = False
            elif self.stopped_by_user and self.take_care_of_pausing:
                self.gw_instance.reset_gw()
                self.take_care_of_pausing = False

            if AUTO_TRIGGERS and time_condition_met:

                self.raising_trigger_number()

            elif time_condition_met:
                # Check if GW response is a new matrix
                if gw_rsp is not None and ('Detected High-to-Low peak' in gw_rsp['raw'] or
                                           'Detected Low-to-High peak' in gw_rsp['raw']) and not self.stopped_by_user:
                    self.raising_trigger_number()

            if self.gw_instance.is_data_available() and not self.stopped_by_user:
                raw_packets_in = self.gw_instance.get_packets(action_type=ActionType.ALL_SAMPLE,
                                                              data_type=DataType.RAW, tag_inlay=self.inlay_type)
                if not self.all_tags.full():
                    self.all_tags.put(raw_packets_in)
                else:
                    self.logger_file.warning(f"Queue is full.. Packet: {raw_packets_in}")
                got_new_adva = True
                no_data_start_time = None
            else:
                if not self.stopped_by_user:
                    if no_data_start_time is None:
                        no_data_start_time = time.time()
                    if time.time() - no_data_start_time >= SECONDS_WITHOUT_PACKETS:
                        got_new_adva = False
                        if not self.second_without_packets:
                            self.logger_file.warning("One minute without packets..")
                            self.second_without_packets = True
                        time.sleep(5)
                        if not self.gw_instance.is_connected():
                            self.reconnect()
                    if time.time() - no_data_start_time >= SECONDS_FOR_GW_ERROR_AFTER_NO_PACKETS:
                        self.gw_error_connection = True
                        break
                    if self.gw_instance.get_read_error_status():
                        self.logger_file.warning("Reading error.. Listener did recovery flow.")
                    time.sleep(0.050 if not got_new_adva else 0)
                else:
                    no_data_start_time = None
        self.gw_instance.reset_gw()
        self.gw_instance.exit_gw_api()

    def reconnect(self):
        self.logger_file.info('Trying to reconnect to GW')
        try:
            self.init_gw()
            self.gw_reset_config(start_gw_app=True)
        except Exception as e:
            self.logger_file.warning(f"Couldn't reconnect GW, due to: {e}")

    def get_raw_packets_queue(self):
        """
        Returns the packet queue that is created above
        """
        return self.all_tags


class CountThread(object):
    """
    Counting the number of tags
    """

    def __init__(self, stop_event, logger_file, matrix_size=1, ther_cols=1):
        self.arduino_connection_error = False
        self.pause_triggers = False
        self.logger_file = logger_file
        self.last_arduino_trigger_time = datetime.datetime.now()
        self.comPortObj = None
        self.trigger_port = None
        if not AUTO_TRIGGERS:
            self.connect()
        self.matrix_size = matrix_size
        self.ther_cols = ther_cols
        self.stop = stop_event
        self.tested = 0

    def connect(self):
        optional_ports = get_arduino_ports()
        if len(optional_ports) == 0:
            raise Exception("NO ARDUINO")
        for port in optional_ports:
            try:
                self.comPortObj = serial.Serial(port, BAUD_ARDUINO, timeout=0.1)
                time.sleep(2)
                initial_message = self.comPortObj.readline().decode().strip()
                if "Wiliot Yield Counter" in initial_message:
                    self.trigger_port = port
            except Exception as e:
                raise Exception(f'could not connect to port {port} due to {e}')

    def raising_trigger(self):
        self.last_arduino_trigger_time = datetime.datetime.now()
        self.tested += self.matrix_size
        self.logger_file.info(f'Got a Trigger.  Number of Triggers {int(self.tested / self.matrix_size)}')

    def reconnect(self):
        """
        Attempts to reconnect to the Arduino.
        """
        connected = False
        start_time = time.time()
        while not connected and not self.stop.is_set() and time.time() - start_time < 60:
            try:
                self.comPortObj = serial.Serial(self.trigger_port, BAUD_ARDUINO, timeout=0.1)
                connected = True
                self.logger_file.info("Reconnected to Arduino")
            except serial.SerialException:
                self.logger_file.error("Reconnection failed. Trying again...")
                time.sleep(5)
        if not connected:
            self.arduino_connection_error = True

    def run(self):
        """
        Tries to read data and then counts the number of tags
        """
        while not self.stop.is_set():
            time.sleep(0.100)
            if not AUTO_TRIGGERS:
                try:
                    data = self.comPortObj.readline()
                    if data.__len__() > 0:
                        try:
                            tmp = data.decode().strip(' \t\n\r')
                            if "pulses detected" in tmp and not self.pause_triggers:
                                self.raising_trigger()
                        except Exception as ee:
                            self.logger_file.error(f'Warning: Could not decode counter data or Warning: {ee}')
                except serial.SerialException as e:
                    self.logger_file.error("Arduino is disconnected   ", e)
                    self.reconnect()
                except Exception as ee:
                    self.logger_file.error(f"NO READLINE: {ee}")
            else:
                self.raising_trigger()
                time.sleep(TIME_BETWEEN_AUTO_TRIGGERS)
        if not AUTO_TRIGGERS:
            self.comPortObj.close()

    def set_pause_triggers(self, paused):
        self.pause_triggers = paused

    def get_tested(self):
        """
        returns the number of tags
        """
        return self.tested

    def get_last_arduino_trigger_time(self):
        return self.last_arduino_trigger_time

    def get_arduino_connection_error(self):
        return self.arduino_connection_error


class MainWindow:
    """
    The main class the runs the GUI and supervise the multi-threading process of fraction's calculation and GUI viewing
    """

    def __init__(self):
        self.current_values = None
        self.current_status_text = None
        self.cumulative_status_text = None
        self.neg_advas = None
        self.main_gui = None
        self.test_started = True
        self.user_response_after_arduino_connection_error = False
        self.advanced_window = None
        self.user_response_after_gw_connection_error = False
        self.env_choice = 'prod'
        self.matrix_size = None
        self.latest_yield_value = None
        self.filling_missed_field = None
        self.latest_yield_formatted = 0
        self.number_of_unique_advas = None
        self.start_run = None
        self.inlay_select = None
        self.logger = None
        self.ttfp = None
        self.cnt = None
        self.curr_adva_for_log = None
        self.matrix_tags = None
        self.conversion_type = None
        self.surface = None
        self.adva_process = None
        self.adva_process_thread = None
        self.count_process = None
        self.count_process_thread = None
        self.folder_path = None
        self.py_wiliot_version = None
        self.final_path_run_data = None
        self.run_data_dict = None
        self.tags_num = 0
        self.last_printed = 0
        self.stop = threading.Event()
        self.thermodes_col = None
        self.print_neg_advas = True
        self.selected = ''
        self.wafer_lot = ''
        self.wafer_number = ''
        self.matrix_num = ''
        self.operator = ''
        self.tester_type = 'yield'
        self.tester_station_name = ''
        self.comments = ''
        self.gw_energy_pattern = None
        self.gw_time_profile = None
        self.rows_number = 1
        self.upload_flag = True
        self.cmn = ''
        self.final_path_packets_data = None
        self.seen_advas = set()
        self.not_neg_advas = 0  # used only to be shown in the small window
        self.update_packet_data_flag = False
        self.tags_counter_time_log = 0
        self.advas_before_tags = set()
        self.stop_run = False
        self.fig_canvas_agg1 = None

    def setup_logger(self):
        # Logger setup
        self.init_file_path()
        self.logger = logging.getLogger('yield')
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        self.logger.setLevel(logging.INFO)
        final_path_log_file = os.path.join(self.folder_path, self.cmn + '@yield_log.log')
        file_handler = logging.FileHandler(final_path_log_file)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'))
        file_handler.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)

    def get_result(self):
        """
        Calculates the yield fraction
        """
        result = 0
        tags_num = self.get_number_of_tested()
        if tags_num > 0:
            result = (self.not_neg_advas / tags_num) * 100
        return result

    def run(self):
        """
        Viewing the window and checking if the process stops
        """
        self.open_session()
        if self.start_run:
            self.init_processes(self.selected)
            time.sleep(0.5)
            self.init_run_data()
            self.start_processes()
            self.overlay_window()
        else:
            self.logger.warning('Error Loading Program')

    def init_file_path(self):
        self.py_wiliot_version = get_version()
        d = WiliotDir()
        d.create_tester_dir(tester_name='yield_tester')
        yield_test_app_data = d.get_tester_dir('yield_tester')
        self.cmn = self.wafer_lot + '.' + self.wafer_number
        run_path = os.path.join(yield_test_app_data, self.cmn)
        if not os.path.exists(run_path):
            os.makedirs(run_path)
        self.cmn = self.wafer_lot + '.' + self.wafer_number + '_' + formatted_today + '_' + cur_time_formatted
        self.folder_path = os.path.join(run_path, self.cmn)
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

    def init_run_data(self):
        self.final_path_run_data = os.path.join(self.folder_path, self.cmn + '@run_data.csv')
        gw_version = self.adva_process.gw_instance.get_gw_version()[0]
        start_time = datetime.datetime.now()
        run_start_time = start_time.strftime("%H:%M:%S")
        value = all_inlays[self.selected]
        self.run_data_dict = {'common_run_name': self.cmn, 'tester_station_name': self.tester_station_name,
                              'operator': self.operator, 'received_channel': value['received_channel'],
                              'run_start_time': formatted_date + ' ' + run_start_time, 'run_end_time': '',
                              'wafer_lot': self.wafer_lot, 'wafer_number': self.wafer_number,
                              'matrix_num': self.matrix_num, 'upload_date': '',
                              'tester_type': self.tester_type, 'gw_energy_pattern': self.gw_energy_pattern,
                              'comments': self.comments, 'inlay': self.selected, 'total_run_tested': 0,
                              'total_run_responding_tags': 0, 'conversion_type': self.conversion_type,
                              'gw_version': gw_version, 'surface': self.surface, 'matrix_tags': self.matrix_tags,
                              'py_wiliot_version': self.py_wiliot_version, 'thermodes_col': self.thermodes_col,
                              'gw_time_profile': self.gw_time_profile}

    @staticmethod
    def update_run_data_file(run_data_path, run_data_dict, run_end_time, tags_num, advas, result, conversion, surface,
                             upload_date=''):
        """
        Updates the run_data CSV file while running the program
        """
        run_data_dict['run_end_time'] = run_end_time
        run_data_dict['upload_date'] = upload_date
        run_data_dict['total_run_tested'] = tags_num
        run_data_dict['total_run_responding_tags'] = advas
        run_data_dict['yield'] = result
        run_data_dict['conversion_type'] = conversion
        run_data_dict['surface'] = surface
        dict_to_csv(dict_in=run_data_dict, path=run_data_path)

    def calc_tag_matrix_ttfp(self, packet_time, trigger_time):
        try:
            tag_matrix_ttfp = (self.adva_process.get_gw_start_time() - trigger_time).total_seconds() + packet_time
        except Exception as e:
            self.logger.warning(f'could not calculate tag matrix ttfp due to {e}')
            tag_matrix_ttfp = -1.0
        return tag_matrix_ttfp

    def update_packet_data(self):
        """
        Updates the run_data CSV file while running the program
        """
        raw_packet_queue = self.adva_process.get_raw_packets_queue()

        self.number_of_unique_advas = len(self.seen_advas)
        if ARDUINO_EXISTS:
            trigger_time = self.count_process.get_last_arduino_trigger_time()
        else:
            trigger_time = self.adva_process.get_last_change_time()
        if not raw_packet_queue.empty():
            cur_df = pd.DataFrame()
            n_elements = raw_packet_queue.qsize()
            # Collecting Packets from the queue and putting them into a TagCollection
            for _ in range(n_elements):
                for p in raw_packet_queue.get():
                    tag_matrix_ttfp = self.calc_tag_matrix_ttfp(p['time'], trigger_time)
                    cur_p = Packet(p['raw'], time_from_start=p['time'], inlay_type=self.inlay_select,
                                   custom_data={
                                       'common_run_name': self.cmn,
                                       'matrix_tags_location': self.cnt,
                                       'matrix_timestamp': trigger_time,
                                       'tag_matrix_ttfp': tag_matrix_ttfp,
                                       'environment_light_intensity': self.light_intensity,
                                       'environment_humidity': self.humidity,
                                       'environment_temperature': self.temperature})
                    if not cur_p.is_valid_packet:
                        continue
                    tag_id = cur_p.get_adva()

                    if self.get_number_of_tested() == 0:
                        self.advas_before_tags.add(tag_id)
                    else:
                        if self.print_neg_advas:
                            self.logger.info('neglected advas:  %05d', len(self.advas_before_tags))
                            self.print_neg_advas = False

                    if tag_id not in self.seen_advas and tag_id not in self.advas_before_tags:
                        cur_p_df = cur_p.as_dataframe(sprinkler_index=0)
                        cur_df = pd.concat([cur_df, cur_p_df], ignore_index=True)
                        self.seen_advas.add(tag_id)
                        self.logger.info(f"New adva {tag_id}")

            # writing to DataFrame and then to CSV
            if not cur_df.empty:
                self.final_path_packets_data = os.path.join(self.folder_path, f"{self.cmn}@packets_data.csv")
                try:
                    if not self.update_packet_data_flag:
                        cur_df.to_csv(self.final_path_packets_data, mode='w', header=True, index=False)
                        self.update_packet_data_flag = True
                    else:
                        cur_df.to_csv(self.final_path_packets_data, mode='a', header=False, index=False)
                except Exception as ee:
                    self.logger.error(f"Exception occurred: {ee}")

    def stop_button(self, run_end_time, tags_num, advas, result, upload_date):
        """
        Finishing the program and saves the last changes after pressing Stop in the second window
        """
        self.logger.info(f"User quit from application")
        self.adva_process_thread.join()
        if ARDUINO_EXISTS:
            self.count_process_thread.join()
        self.update_run_data_file(self.final_path_run_data, self.run_data_dict, formatted_date + ' ' + run_end_time,
                                  tags_num, advas, result, self.conversion_type, self.surface, upload_date)
        self.update_packet_data()

    def init_processes(self, inlay_select):
        """
        Initializing the two main instances and threads in order to start working
        """
        try:
            self.adva_process = AdvaProcess(stop_event=self.stop,
                                            inlay_type=inlay_select,
                                            logging_file=self.logger,
                                            listener_path=self.folder_path)
            self.adva_process_thread = threading.Thread(target=self.adva_process.run, args=())
        except Exception as e:
            self.logger.warning(f"{e}")
            popup_message(msg='GW is not connected. Please connect it.', logger=self.logger)
            raise Exception('GW is not connected')

        if ARDUINO_EXISTS:
            try:
                self.count_process = CountThread(self.stop, self.logger, self.matrix_size, self.thermodes_col)
                self.count_process_thread = threading.Thread(target=self.count_process.run, args=())
            except Exception as e:
                self.logger.warning(f"{e}")
                popup_message(msg='Arduino is not connected. Please connect it.', logger=self.logger)
                raise Exception('Arduino is not connected')

    def start_processes(self):
        """
        Starting the work of the both threads
        """
        self.adva_process_thread.start()
        if ARDUINO_EXISTS:
            self.count_process_thread.start()

    def draw_figure(self, canvas, figure):
        """
        Embeds a Matplotlib figure in a PySimpleGUI Canvas Element
        """
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().grid(row=3, column=0, sticky="nsew", columnspan=120)
        figure_canvas_agg.get_tk_widget().configure(width=520, height=500)
        return figure_canvas_agg

    def upload_to_cloud(self):
        yes_or_no = ['Yes', 'No']
        upload_layout_dic = {'ask_to_upload': {'widget_type': 'label', 'value': 'Do you want to stop or upload?'},
                             'upload': {'text': 'Upload:', 'value': yes_or_no[0], 'widget_type': 'combobox',
                                        'options': yes_or_no},
                             'env_choice': {'text': 'Select Environment:', 'value': 'prod', 'widget_type': 'combobox',
                                            'options': ['prod', 'test']}}
        upload_layout_dic_gui = WiliotGui(params_dict=upload_layout_dic, parent=self.main_gui.layout)
        upload_layout_dic_values_out = upload_layout_dic_gui.run()

        if upload_layout_dic_values_out:
            self.upload_flag = upload_layout_dic_values_out['upload'] == 'Yes'
            self.env_choice = upload_layout_dic_values_out['env_choice']

        if self.upload_flag:
            try:
                is_uploaded = upload_to_cloud_api(self.cmn, self.tester_type + '-test',
                                                  run_data_csv_name=self.final_path_run_data,
                                                  packets_data_csv_name=self.final_path_packets_data,
                                                  env=self.env_choice, is_path=True)

            except Exception as ee:
                is_uploaded = False
                self.upload_flag = is_uploaded
                self.logger.error(f"Exception occurred: {ee}")
                exit()

            if is_uploaded:
                self.logger.info("Successful upload")
            else:
                self.logger.info('Failed to upload the file')
                popup_message(msg="Run upload failed. Check exception error at the console"
                                  " and check Internet connection is available"
                                  " and upload logs manually", tk_frame=self.main_gui.layout, logger=self.logger)
            self.main_gui.on_close()
            self.upload_flag = is_uploaded
        else:
            self.logger.info('File was not uploaded')

    def error_popup(self, error_type):
        self.logger.warning(f'{error_type} connection error occurred')
        popup_message(msg=f'{error_type} Connection error occurred.\n' f'Yield test was stopped',
                      tk_frame=self.main_gui, logger=self.logger)
        self.logger.info(f'User reacted to {error_type} connection error')

    def init_graphs(self, gui, min_current, min_cumulative):
        # create the main figure and two subplots
        fig, (ax, axy) = plt.subplots(1, 2, figsize=(12, 7))
        fig.subplots_adjust(left=0.05, right=0.95, top=0.85, bottom=0.15, wspace=0.2)
        # initialize the first graph
        prev_tests = None
        prev_val = None
        text_box1 = axy.text(0.18, 1.05, f"Cumulative Yield: 0.0 %", transform=axy.transAxes,
                             fontweight='bold')
        ax.set_xlabel('Number of tags')
        ax.set_ylabel('Yield %')
        ax.set_ylim([-MIN_Y_FOR_PLOTS, MAX_Y_FOR_PLOTS])
        ax_y_ticks = np.arange(MIN_Y_FOR_PLOTS, MAX_Y_FOR_PLOTS + 10, FIRST_STEP_SIZE)
        ax.set_yticks(ax_y_ticks)
        plt.ion()
        ax.yaxis.grid(True)
        text_box = ax.text(0.18, 1.05, f"Current Matrix Yield: {self.latest_yield_formatted:.2f} %",
                           transform=ax.transAxes, fontweight='bold')
        if user_inputs.get('min_current_line') == 'yes':
            ax.axhline(y=min_current, color='black', linestyle='--')
        # initialize the second graph
        prev_tests1 = None
        prev_val1 = None
        axy.set_xlabel('Number of tags')
        axy.set_ylabel('Yield %')
        axy.set_ylim([MIN_Y_FOR_PLOTS, MAX_Y_FOR_PLOTS])
        axy_y_ticks = np.arange(MIN_Y_FOR_PLOTS, MAX_Y_FOR_PLOTS + 10, FIRST_STEP_SIZE)
        axy.set_yticks(axy_y_ticks)
        plt.ion()
        axy.yaxis.grid(True)
        if prev_val:
            text_box1 = axy.text(0.18, 1.05, f"Cumulative Yield: {prev_val:.2f} %", transform=axy.transAxes,
                                 fontweight='bold')
        if user_inputs.get('min_cumulative_line') == 'yes':
            axy.axhline(y=min_cumulative, color='black', linestyle='--')

        canvas_elem1 = gui.layout
        self.fig_canvas_agg1 = self.draw_figure(canvas_elem1, fig)
        return ax, axy, prev_tests, prev_val, prev_tests1, prev_val1, text_box, text_box1

    def update_current_graph(self, ax, new_num_rows, min_current, red_line_current, prev_tests,
                             prev_val, current_tested):
        curr_tests = new_num_rows
        curr_val = 100 * ((len(self.seen_advas) - self.curr_adva_for_log) / self.matrix_size)
        if curr_val > 100:
            curr_val = SET_VALUE_MORE_THAN_100
        self.curr_adva_for_log = len(self.seen_advas)

        if not hasattr(self, 'current_status_text') or self.current_status_text is None:
            self.current_status_text = None
        if curr_val < min_current:
            status_message_current = f'Current yield is lower than {min_current}%'
            if self.current_status_text is None:
                self.current_status_text = ax.text(0.5, -0.16, status_message_current,
                                                   transform=ax.transAxes,
                                                   fontsize=12, color='red',
                                                   fontweight='bold',
                                                   ha='center')
            else:
                self.current_status_text.set_text(status_message_current)
        else:
            if self.current_status_text is not None:
                self.current_status_text.remove()
                self.current_status_text = None
        figure_color_current = 'red' if curr_val < red_line_current else 'blue'
        # Plot the first point only if it's the first update
        ax.plot([prev_tests, curr_tests], [prev_val, curr_val], color=figure_color_current)
        prev_tests = curr_tests
        prev_val = curr_val
        prev_tested = current_tested
        self.last_printed = current_tested
        self.cnt += 1

        return prev_tests, prev_val, prev_tested

    def update_cumulative_graph(self, axy, new_num_rows, min_cumulative, red_line_cumulative, prev_tests1,
                                prev_val1, text_box1):
        curr_tests1 = new_num_rows
        curr_val1 = self.get_result()

        if curr_val1 > 100:
            curr_val1 = SET_VALUE_MORE_THAN_100

        if not hasattr(self, 'cumulative_status_text') or self.cumulative_status_text is None:
            self.cumulative_status_text = None
        if curr_val1 < min_cumulative and self.get_number_of_tested() != 0:
            status_message_cumulative = f'Cumulative yield is lower than {min_cumulative}%'
            if self.cumulative_status_text is None:
                self.cumulative_status_text = axy.text(0.5, -0.16,
                                                       status_message_cumulative,
                                                       transform=axy.transAxes,
                                                       fontsize=12, color='red',
                                                       fontweight='bold',
                                                       ha='center')
            else:
                self.cumulative_status_text.set_text(status_message_cumulative)
        else:
            if self.cumulative_status_text is not None:
                self.cumulative_status_text.remove()
                self.cumulative_status_text = None
        figure_color_cumulative = 'red' if curr_val1 < red_line_cumulative else 'blue'
        axy.plot([prev_tests1, curr_tests1], [prev_val1, curr_val1], color=figure_color_cumulative)
        prev_tests1 = curr_tests1
        prev_val1 = curr_val1
        text_box1.set_text(f"Cumulative Yield : {curr_val1:.2f} %")
        self.fig_canvas_agg1.draw()

        return prev_tests1, prev_val1

    def handling_advanced_settings_window(self, window, ax, current_min_y_value, current_max_y_value,
                                          current_size_value, axy, cumulative_min_y_value, cumulative_max_y_value,
                                          cumulative_size_value, matrix_num):
        self.logger.info('Advanced settings was pressed')
        advanced_layout_dict = {
            'current_min_y_value': {'text': 'Current" min y:', 'value': '', 'widget_type': 'entry'},
            'current_max_y_value': {'text': '"Current" max y:', 'value': '', 'widget_type': 'entry'},
            'current_size_value': {'text': '"Current" step:', 'value': '', 'widget_type': 'entry'},
            'cumulative_min_y_value': {'text': '"Cumulative" min y:', 'value': '', 'widget_type': 'entry'},
            'cumulative_max_y_value': {'text': '"Cumulative" max y', 'value': '', 'widget_type': 'entry'},
            'cumulative_size_value': {'text': '"Cumulative" step:', 'value': '', 'widget_type': 'entry'},
            'matrix_num': {'text': 'Matrix num:', 'value': '', 'widget_type': 'entry'},
            'reset_button': {'text': 'Reset', 'value': '', 'widget_type': 'button'},
        }

        default_values = {
            'current_min_y_value': 0,
            'current_max_y_value': 120,
            'current_size_value': 10,
            'cumulative_min_y_value': 0,
            'cumulative_max_y_value': 120,
            'cumulative_size_value': 10,
            'matrix_num': 1
        }

        def reset_button():
            self.logger.info("Reset values from advanced settings")

            for key in default_values:
                advanced_gui.update_widget(key, default_values[key])
                globals()[key] = default_values[key]

            ax.set_ylim([current_min_y_value, current_max_y_value])
            ax.set_yticks(np.arange(current_min_y_value, current_max_y_value + current_size_value, current_size_value))

            axy.set_ylim([cumulative_min_y_value, cumulative_max_y_value])
            axy.set_yticks(np.arange(cumulative_min_y_value, cumulative_max_y_value + cumulative_size_value,
                                     cumulative_size_value))
            self.main_gui.matrix_num = 1
            self.main_gui.update_widget('counting_row_matrix_num_value', f'Matrix num: 1')

            self.fig_canvas_agg1.draw()

        advanced_gui = WiliotGui(params_dict=advanced_layout_dict, exit_sys_upon_cancel=False, parent=window.layout)
        advanced_gui.set_button_command('reset_button', reset_button)
        user_out = advanced_gui.run()

        if not self.current_values:
            self.current_values = {
                'current_min_y_value': current_min_y_value,
                'current_max_y_value': current_max_y_value,
                'current_size_value': current_size_value,
                'cumulative_min_y_value': cumulative_min_y_value,
                'cumulative_max_y_value': cumulative_max_y_value,
                'cumulative_size_value': cumulative_size_value,
                'matrix_num': matrix_num
            }

        def get_adv_value():
            if not adv_value.isdigit() and adv_value != '':
                popup_message(msg=f"A not-number character in {adv_key}", tk_frame=advanced_gui.layout,
                              logger=self.logger)
                return
            if adv_value != '':
                new_value = int(adv_value)  # if user wrote a value
            elif self.current_values[adv_key]:
                new_value = self.current_values[
                    adv_key]  # if the user did not write a value and not the first submit
            else:
                new_value = int(default_values[adv_key])
            self.current_values[adv_key] = new_value
            self.logger.info(
                f"{adv_key} changed to {new_value}")  # if the user did not write a value and first submit
            return new_value

        if user_out:
            for adv_key, adv_value in user_out.items():
                if adv_value and adv_key != 'matrix_num':
                    get_adv_value()
                else:
                    new_value = get_adv_value()
                    self.matrix_num = new_value
                    window.matrix_num = new_value
                    window.update_widget('counting_row_matrix_num_value', f'Matrix num: {window.matrix_num}')

            ax.set_ylim([self.current_values['current_min_y_value'], self.current_values['current_max_y_value']])
            ax.set_yticks(np.arange(self.current_values['current_min_y_value'],
                                    self.current_values['current_max_y_value'] + self.current_values[
                                        'current_size_value'],
                                    self.current_values['current_size_value']))

            axy.set_ylim([self.current_values['cumulative_min_y_value'], self.current_values['cumulative_max_y_value']])
            axy.set_yticks(np.arange(self.current_values['cumulative_min_y_value'],
                                     self.current_values['cumulative_max_y_value'] + self.current_values[
                                         'cumulative_size_value'],
                                     self.current_values['cumulative_size_value']))

            self.fig_canvas_agg1.draw()

    def get_number_of_tested(self):
        if ARDUINO_EXISTS:
            tags_num = self.count_process.get_tested()
        else:
            tags_num = self.adva_process.get_sensors_triggers() * self.matrix_size
        return tags_num

    def stop_or_error_process(self):
        end_time = datetime.datetime.now()
        run_end_time = end_time.strftime("%H:%M:%S")
        if self.upload_flag:
            upload_date = run_end_time
        else:
            upload_date = ''
        advas = len(self.seen_advas)
        tags_num = self.get_number_of_tested()
        result = float(100 * (advas / tags_num)) if tags_num != 0 else float('inf')
        self.stop_button(run_end_time, tags_num, advas, result, upload_date)
        return True

    def overlay_window(self):
        """
        The small window open session
        """
        # taking values from user_input json file
        temperature_type = user_inputs.get('temperature_type', default_user_inputs['temperature_type'])
        min_current = float(user_inputs.get('min_current', default_user_inputs['min_current']))
        min_cumulative = float(user_inputs.get('min_cumulative', default_user_inputs['min_cumulative']))
        min_humidity = float(user_inputs.get('min_humidity', default_user_inputs['min_humidity']))
        max_humidity = float(user_inputs.get('max_humidity', default_user_inputs['max_humidity']))
        max_light_intensity = float(user_inputs.get('max_light_intensity', default_user_inputs['max_light_intensity']))
        min_light_intensity = float(user_inputs.get('min_light_intensity', default_user_inputs['min_light_intensity']))
        min_temperature = float(user_inputs.get('min_temperature', default_user_inputs['min_temperature']))
        max_temperature = float(user_inputs.get('max_temperature', default_user_inputs['max_temperature']))
        red_line_current = float(user_inputs.get('red_line_current', default_user_inputs['red_line_current']))
        red_line_cumulative = float(user_inputs.get('red_line_cumulative', default_user_inputs['red_line_cumulative']))

        # creating the main window
        temp_val = self.temperature if temperature_type == "C" else self.temperature * 9 / 5 + 32
        overlay_layout_dict = {
            'counting_row': [{'num_rows': {'text': '', 'widget_type': 'label', 'value': 'Number of tags:',
                                           'options': {'font': ('Arial', 14, 'bold')}}},
                             {'num_advas': {'text': '', 'widget_type': 'label', 'value': 'Number of advas:',
                                            'options': {'font': ('Arial', 14, 'bold')}}},

                             {'matrix_num_value': {'widget_type': 'label',
                                                   'value': f'Matrix num: {self.matrix_num}',
                                                   'options': {'font': ('Arial', 14, 'bold')}}}],

            'sensor_row': [{'light_intensity_value': {'text': '', 'widget_type': 'label',
                                                      'options': {'font': ('Arial', 14, 'bold')},
                                                      'value': f'Light Intensity: {self.light_intensity}'}},
                           {'temperature_value': {'widget_type': 'label', 'options': {'font': ('Arial', 14, 'bold')},
                                                  'value': f'Temperature: {temp_val} {temperature_type}'}},
                           {'humidity_value': {'widget_type': 'label', 'value': f'Humidity: {self.humidity}',
                                               'options': {'font': ('Arial', 14, 'bold')}, }
                            }, ],

            'space': {'value': '', 'widget_type': 'label'},
            'buttons_row': [
                {'advanced_settings_button': {'text': 'Advanced Settings', 'value': '', 'widget_type': 'button'}},
                {'stop_button': {'text': 'Stop', 'value': '', 'widget_type': 'button'}},
                {'pause_button': {'text': 'Pause Test', 'value': '', 'widget_type': 'button'}}]

        }

        def stop_button_callback():
            self.stop.set()
            final_tags = self.get_number_of_tested()
            self.logger.info('Final Yield: %s, Final Tags: %05d, Final Advas: %05d,',
                             self.get_result(), final_tags, len(self.seen_advas), )
            self.upload_to_cloud()
            self.stop_run = self.stop_or_error_process()

        def toggle_test_callback():
            self.test_started = not self.test_started
            if ARDUINO_EXISTS:
                self.count_process.set_pause_triggers(not self.test_started)
            self.adva_process.set_stopped_by_user(not self.test_started)
            if self.test_started:
                self.logger.info('Test was started by user')
                self.main_gui.update_widget('buttons_row_pause_button', 'Pause Test')

            else:
                self.logger.info('Test was paused by user')
                self.main_gui.update_widget('buttons_row_pause_button', 'Start Test')

        # values before running
        self.neg_advas = len(self.seen_advas)
        self.curr_adva_for_log = len(self.seen_advas)
        self.cnt = 1
        sub = False
        current_min_y_value = MIN_Y_FOR_PLOTS
        current_max_y_value = MAX_Y_FOR_PLOTS
        current_size_value = FIRST_STEP_SIZE
        cumulative_min_y_value = MIN_Y_FOR_PLOTS
        cumulative_max_y_value = MAX_Y_FOR_PLOTS
        cumulative_size_value = FIRST_STEP_SIZE
        prev_tested = 0
        result = float('inf')

        self.main_gui = WiliotGui(params_dict=overlay_layout_dict, full_screen=True, do_button_config=False)
        # initializing graphs
        ax, axy, prev_tests, prev_val, prev_tests1, prev_val1, text_box, text_box1 = \
            self.init_graphs(self.main_gui, min_current, min_cumulative)
        advanced_settings_callback = partial(
            self.handling_advanced_settings_window, self.main_gui, ax, current_min_y_value,
            current_max_y_value, current_size_value, axy, cumulative_min_y_value,
            cumulative_max_y_value, cumulative_size_value, self.matrix_num
        )
        self.main_gui.set_button_command('buttons_row_advanced_settings_button', advanced_settings_callback)
        self.main_gui.set_button_command('buttons_row_stop_button', stop_button_callback)
        self.main_gui.set_button_command('buttons_row_pause_button', toggle_test_callback)
        # initialize num_advas and num_rows
        num_rows = 0
        num_advas = 0
        self.main_gui.update_widget('counting_row_num_rows', f"Number of tags: {num_rows}")
        self.main_gui.update_widget('counting_row_num_advas', f"Number of advas: {num_advas}")

        def update_gui():
            nonlocal num_rows, num_advas, prev_tests, prev_val, prev_tests1, prev_val1, prev_tested, result, sub

            new_num_rows = self.get_number_of_tested()
            new_num_advas = len(self.seen_advas) - self.neg_advas
            self.not_neg_advas = new_num_advas

            # update packet data
            self.update_packet_data()

            # updating number of rows in GUI
            if new_num_rows != num_rows:
                num_rows = new_num_rows
                self.main_gui.update_widget('counting_row_num_rows', f"Number of tags: {num_rows}")

            # updating number of advas in GUI
            if new_num_advas != num_advas and new_num_advas > 0:
                num_advas = new_num_advas
                self.main_gui.update_widget('counting_row_num_advas', f"Number of advas: {num_advas - self.neg_advas}")

            # all processes when getting a new matrix
            current_tested = self.get_number_of_tested()
            if (current_tested - prev_tested) % (
                    self.matrix_size * int(self.matrix_num)) == 0 and current_tested != self.last_printed:
                temperature_display = f"{self.temperature:.2f} °C"
                if self.main_sensor:
                    self.light_intensity = self.main_sensor.get_light()
                    self.humidity = self.main_sensor.get_humidity()
                    self.temperature = self.main_sensor.get_temperature()
                if temperature_type == "F":
                    temperature_display = f"{self.temperature * 9 / 5 + 32:.2f} °F"

                temperature_color = BLACK_COLOR if (
                        min_temperature <= self.temperature <= max_temperature) else RED_COLOR
                light_intensity_color = BLACK_COLOR if (
                        min_light_intensity <= self.light_intensity <= max_light_intensity) else RED_COLOR
                humidity_color = BLACK_COLOR if (min_humidity <= self.humidity <= max_humidity) else RED_COLOR
                self.main_gui.update_widget('sensor_row_temperature_value', f'Temperature: {temperature_display}',
                                            color=temperature_color)
                self.main_gui.update_widget('sensor_row_light_intensity_value',
                                            f'Light Intensity: {self.light_intensity} lux',
                                            color=light_intensity_color)
                self.main_gui.update_widget('sensor_row_humidity_value', f'Humidity: {self.humidity} %',
                                            color=humidity_color)

                yield_result = "%.5f" % self.get_result()
                latest_adva = len(self.seen_advas) - self.curr_adva_for_log
                self.latest_yield_value = float(latest_adva / self.matrix_size) * 100
                self.latest_yield_formatted = "{:.5f}".format(self.latest_yield_value).zfill(9)
                text_box.set_text(f"Current Matrix Yield : {self.latest_yield_value:.2f} %")
                if '.' in yield_result and len(yield_result.split('.')[0]) < 2:
                    yield_result = "0" + yield_result
                latest_adva = len(self.seen_advas) - self.curr_adva_for_log
                self.latest_yield_formatted = "{:.5f}".format(float(latest_adva / self.matrix_size) * 100).zfill(9)
                if ARDUINO_EXISTS:
                    matrix_num = self.count_process.get_tested() / self.matrix_size
                    all_tested = self.count_process.get_tested()
                else:
                    matrix_num = self.adva_process.get_sensors_triggers()
                    all_tested = self.adva_process.get_sensors_triggers() * self.matrix_size
                self.logger.info(
                    'Matrix Number: %05d, Cumulative Yield: %s, Cumulative Tags: %05d, Cumulative Advas: %05d,'
                    'Latest Yield: %s, Latest Tags: %05d, Latest Advas: %05d, Light Intensity: '
                    '%05.1f, Humidity: %05.1f, Temperature: %05.1f',
                    matrix_num, yield_result, all_tested, len(self.seen_advas), self.latest_yield_formatted,
                    self.matrix_size, latest_adva, self.light_intensity, self.humidity, self.temperature)

                # updating the first graph
                prev_tests, prev_val, prev_tested = self.update_current_graph(ax, new_num_rows, min_current,
                                                                              red_line_current, prev_tests, prev_val,
                                                                              current_tested)

            # updating the second graph
            prev_tests1, prev_val1 = self.update_cumulative_graph(axy, new_num_rows, min_cumulative,
                                                                  red_line_cumulative, prev_tests1, prev_val1,
                                                                  text_box1)

            end_time = datetime.datetime.now()
            run_end_time = end_time.strftime("%H:%M:%S")
            advas = len(self.seen_advas)
            tags_num = self.get_number_of_tested()
            result = float(100 * (advas / tags_num)) if tags_num != 0 else float('inf')
            self.update_run_data_file(
                self.final_path_run_data, self.run_data_dict, formatted_date + ' ' + run_end_time,
                tags_num, advas, result, self.conversion_type, self.surface)
            if self.adva_process.get_gw_error_connection() or \
                    (ARDUINO_EXISTS and self.count_process.get_arduino_connection_error()):
                if ARDUINO_EXISTS:
                    if self.count_process.get_arduino_connection_error():
                        self.user_response_after_arduino_connection_error = True
                        self.logger.warning('User responded to Arduino error')
                self.user_response_after_gw_connection_error = True
                self.logger.warning('User responded to GW error')
                self.stop_or_error_process()
            if self.user_response_after_gw_connection_error:
                connection_error = 'GW'
                self.error_popup(connection_error)
                self.upload_to_cloud()
                end_time = datetime.datetime.now()
                run_end_time = end_time.strftime("%H:%M:%S")
                if self.upload_flag:
                    upload_date = run_end_time
                else:
                    upload_date = ''
                self.update_run_data_file(
                    self.final_path_run_data, self.run_data_dict, formatted_date + ' ' + run_end_time,
                    self.get_number_of_tested(), len(self.seen_advas), result, self.conversion_type, self.surface,
                    upload_date)

            if sub or self.stop_run:
                self.stop_or_error_process()
                time.sleep(1)
                self.adva_process_thread.join()
                sys.exit()

            # self.main_gui.layout.after(100, update_gui)

        # update_gui()
        self.main_gui.add_recurrent_function(500, update_gui)
        self.main_gui.run()

    def open_session(self):
        """
        Opening a session for the process
        """
        # Load previous input from the config file
        if os.path.exists("configs/gui_input_do_not_delete.json"):
            with open("configs/gui_input_do_not_delete.json", "r") as f:
                previous_input = json.load(f)
        else:
            previous_input = {
                'inlay': '', 'number': '', 'received_channel': '',
                'energy_pattern_val': '', 'tester_station_name': '',
                'comments': '', 'operator': '', 'wafer_lot': '', 'wafer_num': '',
                'conversion_type': '', 'surface': '', 'matrix_tags': '',
                'thermodes_col': '0', 'gw_energy_pattern': '', 'gw_time_profile': '',
                'matrix_num': ''
            }

        self.start_run = False
        conv_opts = ['Not converted', 'Standard', 'Durable']
        surfaces = ['Air', 'Cardboard', 'RPC', 'General Er3', 'General Er3.5']
        selected_inlay = all_inlays.get(previous_input['inlay'], {})
        self.selected = selected_inlay.get('inlay', {})
        self.rows_number = selected_inlay.get('number_of_rows', 1)
        energy_pat = selected_inlay.get('energy_pattern_val', 'Invalid Selection')
        time_pro = selected_inlay.get('time_profile_val', 'Invalid Selection')
        rec_channel = selected_inlay.get('received_channel', 'Invalid Selection')
        default_matrix_tags = int(previous_input.get('thermodes_col', 0)) * self.rows_number

        open_session_layout = {
            'wafer_lot': {'text': 'Wafer Lot:', 'value': previous_input['wafer_lot'], 'widget_type': 'entry'},
            'wafer_num': {'text': 'Wafer Number:', 'value': previous_input['wafer_num'], 'widget_type': 'entry'},
            'matrix_num': {'text': 'Num of matrices:', 'value': previous_input['matrix_num'], 'widget_type': 'entry'},
            'thermodes_col': {'text': 'Thermode Col:', 'value': previous_input['thermodes_col'],
                              'widget_type': 'entry'},
            'matrix_tags': {'text': '', 'widget_type': 'label', 'value': f'Matrix tags: {str(default_matrix_tags)}'},
            'inlay_dict': [
                {'inlay': {'text': 'Inlay:', 'value': previous_input['inlay'], 'widget_type': 'combobox',
                           'options': lst_inlay_options}},
                {'energy_pattern_val': {'widget_type': 'label', 'value': f'Energy Pattern: {energy_pat}'}},
                {'time_profile_val': {'widget_type': 'label', 'value': f'Time Profile: {time_pro}'}},
                {'received_channel': {'widget_type': 'label', 'value': f'Received Channel: {rec_channel}'}}
            ],
            'tester_station_name': {'text': 'Tester Station:', 'value': previous_input['tester_station_name'],
                                    'widget_type': 'entry'},
            'comments': {'text': 'Comments:', 'value': previous_input['comments'], 'widget_type': 'entry'},
            'operator': {'text': 'Operator:', 'value': previous_input['operator'], 'widget_type': 'entry'},
            'conversion_type': {'text': 'Conversion:', 'value': previous_input['conversion_type'],
                                'widget_type': 'combobox', 'options': conv_opts},
            'surface': {'text': 'Surface:', 'value': previous_input['surface'], 'widget_type': 'combobox',
                        'options': surfaces},
            'buttons_row': [{'submit_button': {'text': 'Submit', 'value': '', 'widget_type': 'button', }},
                            {'space': {'text': '', 'value': '', 'widget_type': 'label', }},
                            {'space': {'text': '', 'value': '', 'widget_type': 'label', }},
                            {'space': {'text': '', 'value': '', 'widget_type': 'label', }},
                            {'space': {'text': '', 'value': '', 'widget_type': 'label', }},
                            {'cancel_button': {'text': 'Cancel', 'value': '', 'widget_type': 'button', }}, ]
        }

        open_session_gui = WiliotGui(params_dict=open_session_layout, do_button_config=False)

        def on_inlay_change(*args):
            inlay_select = inlay_var.get()
            self.selected = inlay_select
            if inlay_select in all_inlays:
                selected_inlay = all_inlays[inlay_select]
                energy_pat = selected_inlay['energy_pattern_val']
                time_pro = selected_inlay['time_profile_val']
                rec_channel = selected_inlay['received_channel']
                default_matrix_tags = int(open_session_gui.widgets_vals['thermodes_col'].get()) * selected_inlay.get(
                    'number_of_rows', 1)
            else:
                energy_pat = 'Invalid Selection'
                time_pro = 'Invalid Selection'
                rec_channel = 'Invalid Selection'
                default_matrix_tags = 0

            open_session_gui.update_widget('inlay_dict_energy_pattern_val', f'Energy Pattern: {energy_pat}')
            open_session_gui.update_widget('inlay_dict_time_profile_val', f'Time Profile: {time_pro}')
            open_session_gui.update_widget('inlay_dict_received_channel', f'Received Channel: {rec_channel}')
            open_session_gui.update_widget('matrix_tags', f'Matrix tags: {str(default_matrix_tags)}')

        def on_submit_button(*args):
            wafer_number = open_session_gui.widgets.get('wafer_num').get()
            wafer_lot = open_session_gui.widgets.get('wafer_lot').get()
            missing_fields = []
            self.filling_missed_field = []
            self.setup_logger()
            for field in MAND_FIELDS:
                session_value = open_session_gui.widgets.get(field).get().strip()
                if not session_value:
                    missing_fields.append(field)
                    self.filling_missed_field.append(field)

            if missing_fields:
                error_msg = f"Please fill all the " \
                            f"mandatory fields {', '.join([f'[{field}]' for field in missing_fields])}"
                self.logger.warning(error_msg)
                popup_message(msg=error_msg, tk_frame=open_session_gui.layout, logger=self.logger)
                return  # Skip the rest and prompt for missing fields again
            for missed_field in self.filling_missed_field:
                setattr(self, missed_field, open_session_gui.widgets.get(missed_field).get().strip())

            for value, value_name in [(wafer_lot, "Wafer lot"), (wafer_number, "Wafer number")]:
                for character in value:
                    if not character.isalpha() and not character.isdigit():
                        popup_message(msg=f"{value_name} can't include '{character}' not letter/digit",
                                      tk_frame=open_session_gui.layout, logger=self.logger)
                        return
            open_session_gui.on_submit()

        open_session_gui.add_event(widget_key='buttons_row_cancel_button', command=open_session_gui.on_cancel, event_type='button')
        open_session_gui.add_event(widget_key='buttons_row_submit_button', command=on_submit_button, event_type='button')
        # Bind the change event to the combobox
        inlay_var = open_session_gui.widgets_vals['inlay_dict_inlay']
        inlay_var.trace('w', on_inlay_change)

        values_out = open_session_gui.run()
        if values_out:
            selected_inlay = all_inlays.get(self.selected)
            self.wafer_lot = values_out['wafer_lot']
            self.wafer_number = values_out['wafer_num']
            self.matrix_num = values_out['matrix_num']
            self.comments = values_out['comments']
            self.rows_number = int(selected_inlay['number_of_rows'])
            self.gw_energy_pattern = energy_pat
            self.gw_time_profile = time_pro
            self.thermodes_col = values_out['thermodes_col']
            self.matrix_tags = str(int(values_out['thermodes_col']) * self.rows_number)
            self.conversion = values_out['conversion_type']
            self.surface = values_out['surface']
            self.tester_station_name = values_out['tester_station_name']
            self.operator = values_out['operator']
            self.matrix_size = int(self.thermodes_col) * int(self.rows_number)

            try:
                self.main_sensor = YoctoSensor(self.logger)
            except Exception as ee:
                self.main_sensor = None
                print(f'No sensor is connected ({ee})')
            if self.main_sensor:
                self.light_intensity = self.main_sensor.get_light()
                self.humidity = self.main_sensor.get_humidity()
                self.temperature = self.main_sensor.get_temperature()
            else:
                self.temperature = VALUE_WHEN_NO_SENSOR
                self.humidity = VALUE_WHEN_NO_SENSOR
                self.light_intensity = VALUE_WHEN_NO_SENSOR

            self.start_run = True

            # Save the correct values to previous_input
            previous_input = {
                'inlay': values_out['inlay_dict_inlay'],
                'received_channel': values_out.get('received_channel', ''),
                'energy_pattern_val': values_out.get('energy_pattern_val', ''),
                'time_profile_val': values_out.get('time_profile_val', ''),
                'tester_station_name': values_out.get('tester_station_name', ''),
                'comments': values_out.get('comments', ''),
                'operator': values_out.get('operator', ''),
                'wafer_lot': values_out.get('wafer_lot', ''),
                'wafer_num': values_out.get('wafer_num', ''),
                'conversion_type': values_out.get('conversion_type', ''),
                'surface': values_out.get('surface', ''),
                'matrix_tags': values_out.get('matrix_tags', ''),
                'thermodes_col': values_out.get('thermodes_col', '0'),
                'gw_energy_pattern': values_out.get('gw_energy_pattern', ''),
                'gw_time_profile': values_out.get('gw_time_profile', ''),
                'matrix_num': values_out.get('matrix_num', '')
            }

            with open("configs/gui_input_do_not_delete.json", "w") as f:
                json.dump(previous_input, f)


if __name__ == '__main__':
    m = MainWindow()
    m.run()
