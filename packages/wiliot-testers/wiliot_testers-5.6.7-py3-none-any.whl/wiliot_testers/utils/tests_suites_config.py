import sys
import json
import os.path
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from wiliot_core.local_gateway.local_gateway_core import valid_output_power_vals
from enum import Enum


class GwPatterns(Enum):
    ENERGY_18 = 'Beacon 37, 38, 39 Energy at 2480'
    ENERGY_51 = 'Beacon 37, 38, 39 Energy at 915'


BLE_ENERGY = ['neg20dBm', 'neg16dBm', 'neg12dBm', 'neg4dBm', 'neg8dBm', 'neg12dBm', 'pos8dBm', 'pos7dBm', 'pos6dBm',
              'pos7dBm', 'pos6dBm', 'pos5dBm', 'pos4dBm', 'neg16dBm', 'neg20dBm', 'pos4dBm', 'neg16dBm', 'neg20dBm']

LORA_POWER = ['0dBm', '9dBm', '14dBm', '17dBm', '20dBm', '23dBm', '26dBm', '29dBm', '32dBm']

CRITERIA_KEYS = ['external_sensor', 'num_packets', 'num_cycles', 'per_mean', 'per_std',
                 'rssi_mean', 'rssi_std', 'rssi_min', 'rssi_max', 'sprinkler_counter_mean',
                 'sprinkler_counter_std', 'sprinkler_counter_min', 'sprinkler_counter_max',
                 'tbp_mean', 'tbp_std', 'tbp_min', 'tbp_max', 'tbp_num_vals', 'ttfp',
                 'rx_rate', 'rx_rate_normalized']

FIELD_NAMES = {"plDelay": "Production Line Delay",
               "rssiThresholdHW": "RSSI Threshold HW",
               "rssiThresholdSW": "RSSI Threshold SW",
               "maxTtfp": "Max TTFP",
               "ignore_test_mode": "Ignore Test Mode Packets",
               "devMode": "Decryption",
               "run_all": "Run all stages even if fail",
               "name": "Name",
               "rxChannel": "RX Channel",
               "energizingPattern": "Energizing Pattern",
               "timeProfile": "Time Profile (msec)",
               "absGwTxPowerIndex": "Power Index/Name",
               "sub1gGwTxPower": "LoRa Power",
               "maxTime": "Test Time (sec)",
               "delayBeforeNextTest": "Stage Delay (sec)"}

DEFAULT_VALUES = {
                "plDelay": 100,
                "rssiThresholdHW": 85,
                "rssiThresholdSW": 70,
                "maxTtfp": 5,
                "ignore_test_mode": True,
                "devMode": False,
                "run_all": False,
                "tests": [{
                    "name": "",
                    "rxChannel": 37,
                    "energizingPattern": 18,
                    "timeProfile": [5, 10],
                    "absGwTxPowerIndex": len(valid_output_power_vals) - 1,
                    "sub1gGwTxPower": LORA_POWER[0],
                    "maxTime": 5,
                    "delayBeforeNextTest": 0,
                    "stop_criteria": {},
                    "quality_param": {}
                }]
            }


class TestConfigEditorApp(tk.Tk):
    def __init__(self, json_file):
        super().__init__()
        self.json_file = json_file
        self.data = self.load_data()
        self.current_config = None
        self.dynamic_widgets = {}
        self.test_name_label, self.selected_config = None, None
        self.config_dropdown, self.canvas, self.scrollable_frame, self.vsb = None, None, None, None
        self.create_widgets()
        self.style = None
        self.configure_styles()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_data(self):
        try:
            with open(self.json_file, 'r') as file:
                return json.load(file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON data: {e}")
            self.quit()

    def configure_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # General Styles
        self.style.configure('TFrame', background='#f7f7f7')
        self.style.configure('TLabel', background='#f7f7f7', foreground='#333333', font=('Helvetica', 9))
        self.style.configure('TButton', background='#e0e0e0', foreground='#333333', font=('Helvetica', 9, 'bold'))
        self.style.configure('TEntry', background='#ffffff', foreground='#333333', font=('Helvetica', 9), padding=5)
        self.style.configure('TCombobox', background='#ffffff', foreground='#333333', font=('Helvetica', 9))

        # LabelFrame Styles
        self.style.configure('TLabelframe', background='#f7f7f7', foreground='#333333', padding=10)
        self.style.configure('TLabelframe.Label', background='#f7f7f7', foreground='#333333',
                             font=('Helvetica', 10, 'bold'))

        # Scrollable Frame Styles
        self.style.configure('Canvas.TFrame', background='#f7f7f7')

    def create_widgets(self):
        self.geometry("600x800")
        self.title("Test Suite Editor")
        self.configure(background='#f7f7f7')

        selection_frame = ttk.Frame(self, padding=5)
        selection_frame.pack(side=tk.TOP, fill=tk.X)

        self.test_name_label = ttk.Label(selection_frame, text="", font=('Helvetica', 11, 'bold'), background='#d0d0d0')
        self.test_name_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.selected_config = tk.StringVar()
        self.config_dropdown = ttk.Combobox(selection_frame, textvariable=self.selected_config, state="readonly",
                                            width=30)
        self.config_dropdown['values'] = list(self.data.keys())
        self.config_dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=10)
        self.config_dropdown.bind("<<ComboboxSelected>>", self.on_config_selected)

        control_frame = ttk.Frame(self, padding=5)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Button(control_frame, text="Save", command=self.on_save).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Clear", command=self.load_initial_values).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="New", command=self.create_new_test).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Delete", command=self.delete_current_test).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Duplicate", command=self.duplicate_current_test).pack(side=tk.LEFT, padx=5)

        self.canvas = tk.Canvas(self, borderwidth=0, background='#f7f7f7')
        self.scrollable_frame = ttk.Frame(self.canvas, style='Canvas.TFrame')
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.limit_scroll_region()

    def _on_mousewheel(self, event):
        if 'combobox' in str(event.widget):
            return
        if event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        elif event.delta > 0 and self.canvas.canvasy(0) > 0:
            self.canvas.yview_scroll(-1, "units")

    def on_frame_configure(self, event=None):
        self.limit_scroll_region()

    def limit_scroll_region(self):
        self.update_idletasks()
        bbox = self.canvas.bbox("all")
        if bbox:
            x1, y1, x2, y2 = bbox
            self.canvas.configure(scrollregion=(x1, 0, x2, y2))

    def on_config_selected(self, event=None):
        config_name = self.selected_config.get()
        if config_name and config_name in self.data:
            self.current_config = config_name
            config_values = self.data[config_name]
            self.clear_display()
            self.generate_fields(config_values)
            self.test_name_label.config(text=f"Current Configuration: {config_name}")
        else:
            self.clear_display()
            self.test_name_label.config(text="No configuration selected.")
        self.limit_scroll_region()

    def generate_fields(self, config_values):
        ttk.Label(self.scrollable_frame, text="General Configuration:", style='TLabelframe').pack(
            fill=tk.X, padx=5, pady=5)
        for key in ['plDelay', 'rssiThresholdHW', 'rssiThresholdSW', 'maxTtfp']:
            if key in config_values:
                self.generate_field(key, config_values[key], FIELD_NAMES.get(key, key), int, 0, 1000)
        for key in ['ignore_test_mode', 'devMode', 'run_all']:
            if key in config_values:
                if key == 'ignore_test_mode':
                    self.generate_boolean_field(key, True, FIELD_NAMES.get(key, key))
                else:
                    self.generate_boolean_field(key, config_values[key], FIELD_NAMES.get(key, key))
            else:
                self.generate_boolean_field(key, False, FIELD_NAMES.get(key, key))
        self.generate_test_fields(config_values.get("tests", []))

    def generate_field(self, key, value, display_name, field_type, min_val, max_val):
        frame = ttk.Frame(self.scrollable_frame, style='Canvas.TFrame')
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text=f"{display_name}: ", width=25).pack(side=tk.LEFT)
        var = tk.StringVar(value=str(value))
        entry = ttk.Entry(frame, textvariable=var, width=10)
        entry.pack(side=tk.LEFT, padx=5)
        self.dynamic_widgets[key] = (var, field_type)

    def generate_boolean_field(self, key, value, display_name):
        frame = ttk.Frame(self.scrollable_frame, style='Canvas.TFrame')
        frame.pack(fill=tk.X, padx=10, pady=5)
        var = tk.BooleanVar(value=str(value).lower() == 'true')
        check = ttk.Checkbutton(frame, text=display_name, variable=var)
        check.pack(side=tk.LEFT)
        self.dynamic_widgets[key] = var

    def generate_test_fields(self, tests):
        for index, test in enumerate(tests):
            frame = ttk.LabelFrame(self.scrollable_frame, text=f"Stage {index + 1}", style='TLabelframe', padding=10)
            frame.pack(fill=tk.X, expand=True, padx=10, pady=20)
            self.create_test_inputs(frame, test, index)
            ttk.Button(frame, text="Delete Stage", command=lambda idx=index: self.delete_test(idx)).pack(
                side=tk.LEFT, padx=5, pady=5)
        ttk.Button(self.scrollable_frame, text="Add New Stage", command=self.add_new_test).pack(pady=10)

    def create_test_inputs(self, frame, test, index):
        for key in DEFAULT_VALUES["tests"][0].keys():
            if key not in test:
                test[key] = DEFAULT_VALUES["tests"][0][key]

        ordered_keys = ['name', 'rxChannel', 'energizingPattern', 'timeProfile', 'absGwTxPowerIndex', 'sub1gGwTxPower',
                        'maxTime', 'delayBeforeNextTest']

        for key in ordered_keys:
            value = test[key]
            friendly_name = FIELD_NAMES.get(key, key)
            sub_frame = ttk.Frame(frame, style='Canvas.TFrame')
            sub_frame.pack(fill=tk.X, expand=True, padx=5, pady=5)
            if isinstance(value, list) and key == "timeProfile":
                self.create_time_profile_input(sub_frame, value, index, friendly_name)
            elif key == "name":
                self.create_standard_input(sub_frame, key, value, friendly_name, index, l_expand=True)
            elif key == "absGwTxPowerIndex":
                current_index = value if isinstance(value, int) else None
                self.create_power_dropdown(sub_frame, index, current_index, friendly_name)
            elif key == "sub1gGwTxPower":
                current_value = value if isinstance(value, int) else 0
                self.create_lora_power_dropdown(sub_frame, index, current_value, friendly_name)
            elif key not in ["stop_criteria", "quality_param"]:
                self.create_standard_input(sub_frame, key, value, friendly_name, index)

        self.create_criteria_fields(test.get('stop_criteria', {}), frame, f"{index}_stop_criteria", 'Stop Criteria')
        self.create_criteria_fields(test.get('quality_param', {}), frame, f"{index}_quality_param", 'Quality Param')

    def create_lora_power_dropdown(self, frame, index, current_value, friendly_name):
        ttk.Label(frame, text=f"{friendly_name}: ", width=25).pack(side=tk.LEFT)
        options = LORA_POWER
        var = tk.StringVar(frame)
        dropdown = ttk.Combobox(frame, textvariable=var, values=options, state="readonly", width=15)
        dropdown.pack(side=tk.LEFT, padx=5, pady=5)

        if f"{current_value}dBm" in options:
            var.set(f"{current_value}dBm")
        else:
            var.set('0dBm')
        self.dynamic_widgets[f"{index}_sub1gGwTxPower"] = var

        return var

    def create_new_test(self):
        new_name = simpledialog.askstring("New Test", "Enter the name for the new test configuration:")
        if new_name:
            if new_name in self.data:
                messagebox.showerror("Error", "A test with this name already exists.")
                return

            self.data[new_name] = DEFAULT_VALUES.copy()
            self.selected_config.set(new_name)
            self.update_dropdown()

            self.on_config_selected()

    def create_standard_input(self, frame, key, value, friendly_name, index, l_expand=False):
        var = tk.StringVar(value=str(value))
        ttk.Label(frame, text=f"{friendly_name}: ", width=25).pack(side=tk.LEFT)
        entry = ttk.Entry(frame, textvariable=var, width=10)
        if l_expand:
            entry.pack(side=tk.LEFT, expand=l_expand, fill=tk.X)
        else:
            entry.pack(side=tk.LEFT, padx=5)
        self.dynamic_widgets[f"{index}_{key}"] = var

    def create_time_profile_input(self, frame, values, index, friendly_name):
        ttk.Label(frame, text=f"{friendly_name}: ", width=25).pack(side=tk.LEFT)
        profile_vars = []
        for i, val in enumerate(values):
            var = tk.IntVar(value=val)
            entry = ttk.Entry(frame, textvariable=var, width=5)
            entry.pack(side=tk.LEFT, padx=5)
            profile_vars.append(var)
        self.dynamic_widgets[f"{index}_timeProfile"] = profile_vars

    def create_power_dropdown(self, frame, index, current_index, friendly_name):
        ttk.Label(frame, text=f"{friendly_name}: ", width=25).pack(side=tk.LEFT)
        options = [f"{item['abs_power']} dBm ({item['gw_output_power']}, "
                   f"PA Bypass: {item['bypass_pa']})" for item in valid_output_power_vals]
        var = tk.StringVar(frame)
        dropdown = ttk.Combobox(frame, textvariable=var, values=options, state="readonly", width=30)
        dropdown.pack(side=tk.LEFT, padx=5, pady=5)

        if current_index is not None and isinstance(current_index, int) and \
                current_index < len(valid_output_power_vals):
            var.set(options[current_index])
        else:
            var.set(options[-1])
        self.dynamic_widgets[f"{index}_absGwTxPowerIndex"] = var

    def create_criteria_fields(self, criteria_dict, frame, identifier, name):
        criteria_frame = ttk.LabelFrame(frame, text=name, style='TLabelframe', padding=10)
        criteria_frame.pack(fill=tk.X, expand=True, padx=5, pady=10)

        test_index = int(identifier.split('_')[0])
        category = "_".join(identifier.split('_')[1:3])

        for criterion, values in criteria_dict.items():
            if values:
                self.create_single_criterion_input(criteria_frame, criterion, values, int(test_index), category)

        add_button = ttk.Button(criteria_frame, text="Add Criterion",
                                command=lambda: self.add_criterion(criteria_frame, identifier))
        add_button.pack(side=tk.TOP, pady=5)

    def add_criterion_button(self, criteria_frame, identifier):
        ttk.Button(criteria_frame, text="Add Criterion",
                   command=lambda: self.add_criterion(criteria_frame, identifier)).pack(side=tk.BOTTOM, pady=5)

    def add_criterion(self, criteria_frame, identifier):
        add_frame = ttk.Frame(criteria_frame, style='Canvas.TFrame')
        add_frame.pack(fill=tk.X, expand=True, padx=5, pady=5, side=tk.TOP)

        criterion_var = tk.StringVar()
        criterion_dropdown = ttk.Combobox(add_frame, textvariable=criterion_var, values=CRITERIA_KEYS, state="readonly")
        criterion_dropdown.pack(side=tk.LEFT, padx=5)

        ttk.Button(add_frame, text="Add", command=lambda: self.confirm_add_criterion(
            criterion_var.get(), criteria_frame, identifier, add_frame)).pack(side=tk.LEFT, padx=10)
        ttk.Button(add_frame, text="Cancel", command=add_frame.destroy).pack(side=tk.LEFT, padx=5)

        for widget in criteria_frame.winfo_children():
            if isinstance(widget, ttk.Button) and 'Add Criterion' in widget.cget('text'):
                widget.pack_forget()
                widget.pack(side=tk.BOTTOM, pady=5)

    def duplicate_current_test(self):
        if not self.current_config:
            messagebox.showwarning("Warning", "No configuration selected to duplicate.")
            return

        new_name = simpledialog.askstring("Duplicate Test", "Enter the name for the duplicated test configuration:")
        old_name = self.current_config
        if not new_name:
            return

        if new_name in self.data:
            messagebox.showerror("Error", "A test with this name already exists.")
            return

        self.data[new_name] = json.loads(json.dumps(self.data[self.current_config]))
        self.update_dropdown()
        self.selected_config.set(new_name)
        self.on_config_selected()

        messagebox.showinfo("Duplicate Successful", f"Configuration '{old_name}' duplicated as '{new_name}'.")

    @staticmethod
    def extract_numeric_index(identifier):
        parts = identifier.split('_')
        if parts and parts[0].isdigit():
            return int(parts[0])
        raise ValueError(f"Invalid identifier {identifier}")

    def confirm_add_criterion(self, criterion_key, criteria_frame, identifier, add_frame):
        test_index, category = identifier.split('_')[:2]
        full_category = "_".join(identifier.split('_')[1:])

        existing_keys = self.data[self.current_config]['tests'][int(test_index)].get(full_category, {})
        if criterion_key in existing_keys:
            messagebox.showerror("Error", f"The criterion '{criterion_key}' already exists in {full_category}.")
            return

        self.data[self.current_config]['tests'][int(test_index)].setdefault(full_category, {})[criterion_key] = [0, 999]
        self.create_single_criterion_input(criteria_frame, criterion_key, [0, 999], int(test_index), full_category)
        add_frame.destroy()

    def create_single_criterion_input(self, frame, criterion, values, test_index, category):
        crit_frame = ttk.Frame(frame, name=criterion, style='Canvas.TFrame')
        crit_frame.pack(fill=tk.X, expand=True, padx=5, pady=5)

        min_val, max_val = values
        ttk.Label(crit_frame, text=f"{criterion}: ", style='TLabel').pack(side=tk.LEFT, padx=5)

        min_var = tk.IntVar(value=min_val)
        max_var = tk.IntVar(value=max_val)

        min_key = f"{test_index}_{category}_{criterion}_min"
        max_key = f"{test_index}_{category}_{criterion}_max"

        self.dynamic_widgets[min_key] = min_var
        self.dynamic_widgets[max_key] = max_var

        min_entry = ttk.Entry(crit_frame, textvariable=min_var, style='TEntry', width=10)
        min_entry.pack(side=tk.LEFT, padx=5)
        max_entry = ttk.Entry(crit_frame, textvariable=max_var, style='TEntry', width=10)
        max_entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(crit_frame, text="Delete", command=lambda: self.delete_criterion(
            crit_frame, criterion, f"{test_index}_{category}")).pack(side=tk.RIGHT, padx=5)

    def delete_current_test(self):
        if self.current_config and messagebox.askyesno("Delete Test",
                                                       f"Are you sure you want to delete '{self.current_config}'?"):
            del self.data[self.current_config]
            self.update_dropdown()

    def delete_criterion(self, frame, criterion, identifier):
        criterion_name = criterion
        try:
            parts = identifier.split('_')
            if len(parts) < 3:
                messagebox.showerror("Error", "Invalid criterion identifier.")
                return

            test_index = int(parts[0])
            category = "_".join(parts[1:3])

            if category in self.data[self.current_config]['tests'][test_index]:
                if criterion_name in self.data[self.current_config]['tests'][test_index][category]:
                    del self.data[self.current_config]['tests'][test_index][category][criterion_name]
                    frame.destroy()

                    if not self.data[self.current_config]['tests'][test_index][category]:
                        self.data[self.current_config]['tests'][test_index][category] = {}

                    self.refresh_criteria_display(test_index, category)
                else:
                    messagebox.showerror("Error", f"Criterion '{criterion_name}' not found in '{category}'.")
            else:
                messagebox.showerror("Error", f"Category '{category}' not found in test index {test_index}.")

        except KeyError as e:
            messagebox.showerror("Error", f"Failed to delete criterion: '{criterion_name}'")
        except ValueError:
            messagebox.showerror("Error", "Invalid operation or data structure issues.")

    @staticmethod
    def output_power_string_to_index(selected_string):
        try:
            abs_power = int(selected_string.split(' ')[0])
        except Exception as e:
            raise Exception(f'could not parse the absolute power from the selected string: '
                            f'{selected_string} due to: {e}')
        for i, item in enumerate(valid_output_power_vals):
            if item['abs_power'] == abs_power:
                return i
        raise Exception(f'could not find the relevant output power index for the specified string: {selected_string}')

    def clear_criteria_section(self, test_index, category):
        try:
            test_frame = next((child for child in self.scrollable_frame.winfo_children()
                               if isinstance(child, ttk.LabelFrame) and
                               f"Stage {test_index + 1}" in child.cget('text')), None)
            if test_frame:
                criteria_frame = next((child for child in test_frame.winfo_children()
                                       if isinstance(child, ttk.LabelFrame) and
                                       category.lower() in child.cget('text').lower()), None)
                if criteria_frame:
                    criteria_frame.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def check_stage_exists(self, test_index):
        return any(isinstance(child, ttk.LabelFrame) and f"Stage {test_index + 1}" in child.cget('text')
                   for child in self.scrollable_frame.winfo_children())

    def update_dropdown(self):
        self.config_dropdown['values'] = list(self.data.keys())
        if self.data:
            if self.selected_config.get() not in self.data:
                self.selected_config.set(next(iter(self.data.keys())))
            self.on_config_selected()
        else:
            self.selected_config.set('')
            self.clear_display()

    def clear_display(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        ttk.Label(self.scrollable_frame, text="No configuration selected or available.", style='TLabelframe').pack()

    def refresh_criteria_display(self, test_index, category):
        try:
            test_frame = next((child for child in self.scrollable_frame.winfo_children()
                               if isinstance(child, ttk.LabelFrame) and
                               f"Stage {test_index + 1}" in child.cget('text')), None)
            if not test_frame:
                raise Exception("Test frame not found.")

            criteria_frame = next((child for child in test_frame.winfo_children()
                                   if isinstance(child, ttk.LabelFrame) and
                                   category.lower() in child.cget('text').lower()), None)
            if not criteria_frame:
                return

            for widget in criteria_frame.winfo_children():
                widget.destroy()

            new_criteria_dict = self.data[self.current_config]['tests'][test_index][category]
            identifier = f"{test_index}_{category}"
            self.create_criteria_fields(new_criteria_dict, criteria_frame, identifier, category.capitalize())
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_new_test(self):
        self.update_current_state()
        new_test = {
            "name": "",
            "rxChannel": 37,
            "energizingPattern": 18,
            "timeProfile": [5, 10],
            "absGwTxPowerIndex": len(valid_output_power_vals) - 1,
            "sub1gGwTxPower": LORA_POWER[0],
            "maxTime": 5,
            "delayBeforeNextTest": 0,
            "stop_criteria": {},
            "quality_param": {}
        }
        self.data[self.current_config]["tests"].append(new_test)
        self.on_config_selected()
        self.limit_scroll_region()

    def delete_test(self, index):
        self.update_current_state()
        del self.data[self.current_config]['tests'][index]
        self.on_config_selected()
        self.limit_scroll_region()

    def update_current_state(self):
        if self.current_config is None:
            return

        config_values = self.data[self.current_config]
        for key in ['plDelay', 'rssiThresholdHW', 'rssiThresholdSW', 'maxTtfp']:
            if key in self.dynamic_widgets:
                var, field_type = self.dynamic_widgets[key]
                config_values[key] = field_type(var.get())

        for key in ['devMode', 'run_all']:
            if key in self.dynamic_widgets:
                config_values[key] = "true" if self.dynamic_widgets[key].get() else "false"

        if self.dynamic_widgets['ignore_test_mode'].get():
            config_values['ignore_test_mode'] = ""
        else:
            if 'ignore_test_mode' in config_values:
                del config_values['ignore_test_mode']

        updated_tests = []
        for index in range(len(config_values['tests'])):
            test = {}
            test_prefix = f"{index}_"
            for key in FIELD_NAMES.keys():
                widget_key = f"{test_prefix}{key}"
                if widget_key in self.dynamic_widgets:
                    widget = self.dynamic_widgets[widget_key]
                    if key == 'absGwTxPowerIndex':
                        selected_text = widget.get()
                        selected_index = self.output_power_string_to_index(selected_text)
                        test[key] = selected_index - len(valid_output_power_vals)
                    elif key == 'sub1gGwTxPower':
                        selected_text = widget.get()
                        if selected_text != '0dBm':
                            selected_value = int(selected_text[:-3])
                            test[key] = selected_value
                        else:
                            if 'sub1gGwTxPower' in test:
                                del test['sub1gGwTxPower']
                    elif key in ['rxChannel', 'energizingPattern']:
                        test[key] = int(widget.get())
                    elif key == 'timeProfile':
                        test[key] = [var.get() for var in widget]
                    elif key in ['maxTime', 'delayBeforeNextTest']:
                        test[key] = int(widget.get())
                    else:
                        test[key] = widget.get()

            stop_criteria = {}
            quality_param = {}
            for criterion in CRITERIA_KEYS:
                if criterion in config_values['tests'][index].get('stop_criteria', {}).keys():
                    min_key = f"{test_prefix}stop_criteria_{criterion}_min"
                    max_key = f"{test_prefix}stop_criteria_{criterion}_max"
                    if min_key in self.dynamic_widgets and max_key in self.dynamic_widgets:
                        min_var = self.dynamic_widgets[min_key]
                        max_var = self.dynamic_widgets[max_key]
                        stop_criteria[criterion] = [min_var.get(), max_var.get()]
                if criterion in config_values['tests'][index].get('quality_param', {}).keys():
                    min_key = f"{test_prefix}quality_param_{criterion}_min"
                    max_key = f"{test_prefix}quality_param_{criterion}_max"
                    if min_key in self.dynamic_widgets and max_key in self.dynamic_widgets:
                        min_var = self.dynamic_widgets[min_key]
                        max_var = self.dynamic_widgets[max_key]
                        quality_param[criterion] = [min_var.get(), max_var.get()]

            for criterion in list(config_values['tests'][index].get('stop_criteria', {}).keys()):
                if f"{test_prefix}stop_criteria_{criterion}_min" not in self.dynamic_widgets:
                    del stop_criteria[criterion]
            for criterion in list(config_values['tests'][index].get('quality_param', {}).keys()):
                if f"{test_prefix}quality_param_{criterion}_min" not in self.dynamic_widgets:
                    del quality_param[criterion]

            test['stop_criteria'] = stop_criteria
            test['quality_param'] = quality_param

            updated_tests.append(test)

        config_values['tests'] = updated_tests

    def store_current_state(self):
        if self.current_config is None:
            return

        config_values = self.data[self.current_config]
        for key in ['plDelay', 'rssiThresholdHW', 'rssiThresholdSW', 'maxTtfp']:
            if key in self.dynamic_widgets:
                var, field_type = self.dynamic_widgets[key]
                config_values[key] = field_type(var.get())

        for key in ['devMode', 'run_all']:
            if key in self.dynamic_widgets:
                config_values[key] = "true" if self.dynamic_widgets[key].get() else "false"

        if self.dynamic_widgets['ignore_test_mode'].get():
            config_values['ignore_test_mode'] = ""
        else:
            if 'ignore_test_mode' in config_values:
                del config_values['ignore_test_mode']

        updated_tests = []
        for index in range(len(config_values['tests'])):
            test = {}
            test_prefix = f"{index}_"
            for key in FIELD_NAMES.keys():
                widget_key = f"{test_prefix}{key}"
                if widget_key in self.dynamic_widgets:
                    widget = self.dynamic_widgets[widget_key]
                    if key == 'absGwTxPowerIndex':
                        selected_text = widget.get()
                        selected_index = self.output_power_string_to_index(selected_text)
                        test[key] = selected_index - len(valid_output_power_vals)
                    elif key == 'sub1gGwTxPower':
                        selected_text = widget.get()
                        if selected_text != '0dBm':
                            selected_value = int(selected_text[:-3])
                            test[key] = selected_value
                        else:
                            if 'sub1gGwTxPower' in test:
                                del test['sub1gGwTxPower']
                    elif key in ['rxChannel', 'energizingPattern']:
                        test[key] = int(widget.get())
                    elif key == 'timeProfile':
                        test[key] = [var.get() for var in widget]
                    elif key in ['maxTime', 'delayBeforeNextTest']:
                        test[key] = int(widget.get())
                    else:
                        test[key] = widget.get()

            stop_criteria = {}
            quality_param = {}
            for criterion in CRITERIA_KEYS:
                if criterion in config_values['tests'][index].get('stop_criteria', {}).keys():
                    min_key = f"{test_prefix}stop_criteria_{criterion}_min"
                    max_key = f"{test_prefix}stop_criteria_{criterion}_max"
                    if min_key in self.dynamic_widgets and max_key in self.dynamic_widgets:
                        min_var = self.dynamic_widgets[min_key]
                        max_var = self.dynamic_widgets[max_key]
                        stop_criteria[criterion] = [min_var.get(), max_var.get()]
                if criterion in config_values['tests'][index].get('quality_param', {}).keys():
                    min_key = f"{test_prefix}quality_param_{criterion}_min"
                    max_key = f"{test_prefix}quality_param_{criterion}_max"
                    if min_key in self.dynamic_widgets and max_key in self.dynamic_widgets:
                        min_var = self.dynamic_widgets[min_key]
                        max_var = self.dynamic_widgets[max_key]
                        quality_param[criterion] = [min_var.get(), max_var.get()]

            for criterion in list(config_values['tests'][index].get('stop_criteria', {}).keys()):
                if f"{test_prefix}stop_criteria_{criterion}_min" not in self.dynamic_widgets:
                    del stop_criteria[criterion]
            for criterion in list(config_values['tests'][index].get('quality_param', {}).keys()):
                if f"{test_prefix}quality_param_{criterion}_min" not in self.dynamic_widgets:
                    del quality_param[criterion]

            test['stop_criteria'] = stop_criteria
            test['quality_param'] = quality_param

            updated_tests.append(test)

        config_values['tests'] = updated_tests
        self.save_to_json()

    def save_to_json(self):
        try:
            formatted_data = self.format_data(self.data)
            with open(self.json_file, 'w') as file:
                json.dump(formatted_data, file, indent=4, separators=(',', ': '), ensure_ascii=False)
            messagebox.showinfo("Success", "Configuration saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save JSON data: {e}")

    def format_data(self, data):
        formatted_data = {}
        for key, value in data.items():
            if isinstance(value, dict) and 'tests' in value:
                formatted_tests = [self.format_test(test) for test in value['tests']]
                value['tests'] = formatted_tests
            formatted_data[key] = value
        return formatted_data

    def format_test(self, test):
        formatted_test = {}
        ordered_keys = ['name', 'rxChannel', 'energizingPattern', 'timeProfile', 'absGwTxPowerIndex', 'sub1gGwTxPower',
                        'maxTime', 'delayBeforeNextTest']
        for key in ordered_keys:
            if key in test:
                formatted_test[key] = test[key]
        if 'timeProfile' in test:
            formatted_test['timeProfile'] = test['timeProfile']
        if 'stop_criteria' in test:
            formatted_test['stop_criteria'] = {k: v for k, v in test['stop_criteria'].items()}
        if 'quality_param' in test:
            formatted_test['quality_param'] = {k: v for k, v in test['quality_param'].items()}
        return formatted_test

    def on_save(self):
        if not self.current_config:
            messagebox.showwarning("Warning", "Please select a configuration.")
            return

        self.store_current_state()

    def on_close(self):
        self.destroy()
        sys.exit()

    def load_initial_values(self):
        self.data = self.load_data()
        if self.current_config:
            self.on_config_selected()


if __name__ == "__main__":
    if os.path.isfile("../offline/configs/tests_suites_eng.json"):
        app = TestConfigEditorApp("../offline/configs/tests_suites_eng.json")
    else:
        app = TestConfigEditorApp("../offline/configs/tests_suites.json")
    app.mainloop()
