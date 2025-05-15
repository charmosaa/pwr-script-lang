import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import datetime
from tkcalendar import DateEntry

import backend as bk

class LogEntry:
    def __init__(self, http_request):
        self.timestamp = http_request.timestamp
        self.uid = http_request.uid
        self.orig_host = http_request.orig_host
        self.orig_port = http_request.orig_port
        self.resp_host = http_request.resp_host
        self.resp_port = http_request.resp_port
        self.method = http_request.method
        self.host = http_request.host
        self.uri = http_request.uri
        self.status_code = http_request.status_code

    def __str__ (self):
        timestamp_str = self.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') if self.timestamp else "N/A"
        raw_string = f"{timestamp_str} {self.uid} {self.orig_host} {self.orig_port} {self.resp_host} {self.resp_port} {self.method} {self.host} {self.uri} {self.status_code}"
        return raw_string[:40] + "..."

class LogViewerApp:
    def __init__(self, master):
        self.master = master
        master.title("HTTP Logs Viewer")

        self.style = ttk.Style()
        self.configure_styles()

        self.log_entries = []
        self.filtered_log_entries = []
        self.current_index = -1

        # UI elements - Use ttk.Button instead of tk.Button
        self.load_button = ttk.Button(master, text="Load Logs", command=self.load_logs, style="Load.TButton")
        self.load_button.pack(pady=5)

        self.filter_frame = tk.Frame(master)
        self.filter_frame.pack(pady=5)

        tk.Label(self.filter_frame, text="From date:").pack(side=tk.LEFT)
        self.from_date_calendar = DateEntry(self.filter_frame, width=12, background='darkgreen',
                                             foreground='white', borderwidth=2,
                                             date_pattern='yyyy-mm-dd')
        self.from_date_calendar.pack(side=tk.LEFT)
        self.from_time_hour = ttk.Spinbox(self.filter_frame, from_=0, to=23, width=3, format="%02.0f")
        self.from_time_hour.pack(side=tk.LEFT)
        tk.Label(self.filter_frame, text=":").pack(side=tk.LEFT)
        self.from_time_minute = ttk.Spinbox(self.filter_frame, from_=0, to=59, width=3, format="%02.0f")
        self.from_time_minute.pack(side=tk.LEFT)
        tk.Label(self.filter_frame, text=":").pack(side=tk.LEFT)
        self.from_time_second = ttk.Spinbox(self.filter_frame, from_=0, to=59, width=3, format="%02.0f")
        self.from_time_second.pack(side=tk.LEFT)

        tk.Label(self.filter_frame, text="To date:").pack(side=tk.LEFT)
        self.to_date_calendar = DateEntry(self.filter_frame, width=12, background='darkgreen',
                                           foreground='white', borderwidth=2,
                                           date_pattern='yyyy-mm-dd')
        self.to_date_calendar.pack(side=tk.LEFT)
        self.to_time_hour = ttk.Spinbox(self.filter_frame, from_=0, to=23, width=3, format="%02.0f")
        self.to_time_hour.pack(side=tk.LEFT)
        tk.Label(self.filter_frame, text=":").pack(side=tk.LEFT)
        self.to_time_minute = ttk.Spinbox(self.filter_frame, from_=0, to=59, width=3, format="%02.0f")
        self.to_time_minute.pack(side=tk.LEFT)
        tk.Label(self.filter_frame, text=":").pack(side=tk.LEFT)
        self.to_time_second = ttk.Spinbox(self.filter_frame, from_=0, to=59, width=3, format="%02.0f")
        self.to_time_second.pack(side=tk.LEFT)

        self.filter_button = ttk.Button(self.filter_frame, text="Filter Time", command=self.filter_by_time, style="Filter.TButton")
        self.filter_button.pack(side=tk.LEFT, padx=5)

        self.master_frame = tk.Frame(master)
        self.master_frame.pack(pady=5)
        self.log_list_label = tk.Label(self.master_frame, text="Logs List:")
        self.log_list_label.pack(side=tk.LEFT)
        self.log_list = tk.Listbox(self.master_frame, width=80, height=15)
        self.log_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.log_list.bind('<<ListboxSelect>>', self.show_details)

        self.detail_frame = tk.LabelFrame(master, text="Log Details")
        self.detail_frame.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

        self.details_labels = {}
        self._create_detail_widgets()

        self.navigation_frame = tk.Frame(master)
        self.navigation_frame.pack(pady=5)
        self.prev_button = ttk.Button(self.navigation_frame, text="Previous", command=self.prev_log, state=tk.DISABLED, style="Navigation.TButton")
        self.prev_button.pack(side=tk.LEFT)
        self.next_button = ttk.Button(self.navigation_frame, text="Next", command=self.next_log, state=tk.DISABLED, style="Navigation.TButton")
        self.next_button.pack(side=tk.LEFT)

    def configure_styles(self):
        self.style.theme_use('clam') # Choose a theme

        self.style.configure("TButton", 
                             padding=5)

        self.style.configure("Load.TButton",
                             foreground="white",
                             background="darkgreen",
                             font=("Arial", 10, "bold"),
                             padding=8)
        self.style.map("Load.TButton",
                       background=[('pressed', 'green'),
                                   ('active', 'forestgreen')])

        self.style.configure("Filter.TButton",
                             foreground="black",
                             background="lightyellow",
                             padding=8)
        self.style.map("Filter.TButton",
                       background=[('pressed', 'yellow'),
                                   ('active', 'khaki')])

        self.style.configure("Navigation.TButton",
                             foreground="black",
                             background="lightblue",
                             padding=(8, 3))
        self.style.map("Navigation.TButton",
                       background=[('disabled', 'lightgray'),
                                   ('pressed', 'darkblue'),
                                   ('active', 'blue')])

    def _create_detail_widgets(self):
        labels = {
            "Timestamp:": (0, 0),
            "UID:": (1, 0),
            "Original Host Address:": (2, 0),
            "Original Port:": (3, 0),
            "Response Host Address:": (4, 0),
            "Response Port:": (5, 0),
            "Method:": (6, 0),
            "Host:": (7, 0),
            "URI:": (8, 0),
            "Status Code:": (9, 0),
        }

        for label_text, (row, col) in labels.items():
            tk.Label(self.detail_frame, text=label_text, anchor='w').grid(row=row, column=col, sticky='ew', padx=5, pady=2)
            detail_label = tk.Label(self.detail_frame, text="", anchor='w', font=('TkFixedFont', 10))
            detail_label.grid(row=row, column=col+1, sticky='ew', padx=5, pady=2)
            self.details_labels[label_text[:-1].lower().replace(' ', '_')] = detail_label
        self.detail_frame.columnconfigure(1, weight=1)

    def load_logs(self):
        file_path = filedialog.askopenfilename(title="Select log file")
        if file_path:
            try:
                http_requests = bk.read_log(file_path)
                self.log_entries = [LogEntry(req) for req in http_requests if req]
                self.filtered_log_entries = self.log_entries
                self._update_log_list()
                self.current_index = -1
                self._update_navigation_buttons()
            except FileNotFoundError:
                messagebox.showerror("Error", "Cannot open the file.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while loading the file: {e}")

    def _update_log_list(self):
        self.log_list.delete(0, tk.END)
        for entry in self.filtered_log_entries:
            self.log_list.insert(tk.END, str(entry))

    def show_details(self, event):
        selected_index = self.log_list.curselection()
        if selected_index:
            self.current_index = self.filtered_log_entries[selected_index[0]]  
            self._update_details_view(self.current_index)
            self._update_navigation_buttons()

    def _update_details_view(self, log_entry):
        timestamp_str = log_entry.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') if log_entry.timestamp else "N/A"
        self.details_labels['timestamp']['text'] = timestamp_str
        self.details_labels['uid']['text'] = log_entry.uid if log_entry.uid is not None else "-"
        self.details_labels['original_host_address']['text'] = log_entry.orig_host if log_entry.orig_host is not None else "-"
        self.details_labels['original_port']['text'] = log_entry.orig_port if log_entry.orig_port is not None else "-"
        self.details_labels['response_host_address']['text'] = log_entry.resp_host if log_entry.resp_host is not None else "-"
        self.details_labels['response_port']['text'] = log_entry.resp_port if log_entry.resp_port is not None else "-"
        self.details_labels['method']['text'] = log_entry.method if log_entry.method is not None else "-"
        self.details_labels['host']['text'] = log_entry.host if log_entry.host is not None else "-"
        self.details_labels['uri']['text'] = log_entry.uri if log_entry.uri is not None else "-"
        self.details_labels['status_code']['text'] = str(log_entry.status_code) if log_entry.status_code is not None else "-"

    def filter_by_time(self):
        from_date = self.from_date_calendar.get_date()
        to_date = self.to_date_calendar.get_date()

        from_hour = self.from_time_hour.get()
        from_minute = self.from_time_minute.get()
        from_second = self.from_time_second.get()

        to_hour = self.to_time_hour.get()
        to_minute = self.to_time_minute.get()
        to_second = self.to_time_second.get()

        try:
            from_datetime_str = f"{from_date.year}-{from_date.month:02d}-{from_date.day:02d} {from_hour}:{from_minute}:{from_second}"
            to_datetime_str = f"{to_date.year}-{to_date.month:02d}-{to_date.day:02d} {to_hour}:{to_minute}:{to_second}"

            from_datetime = datetime.datetime.strptime(from_datetime_str, '%Y-%m-%d %H:%M:%S')
            to_datetime = datetime.datetime.strptime(to_datetime_str, '%Y-%m-%d %H:%M:%S')

            self.filtered_log_entries = bk.get_entries_by_date(self.log_entries, from_datetime, to_datetime)
            self._update_log_list()
            self.current_index = -1 # unselect item
            self._update_details_view(LogEntry(bk.HttpRequest(None, '', '', None, '', None, '', '', '', None))) # clear details with an empty request
            self._update_navigation_buttons()
        except ValueError:
            messagebox.showerror("Error", "Invalid date and time format.")

    def prev_log(self):
        if not self.filtered_log_entries:
            return
        current_selected = self.log_list.curselection()
        if current_selected:
            prev_index = current_selected[0] - 1
            if prev_index >= 0:
                self.log_list.selection_clear(0, tk.END)
                self.log_list.selection_set(prev_index)
                self.log_list.activate(prev_index)
                self.log_list.see(prev_index)
                self.show_details(None)

    def next_log(self):
        if not self.filtered_log_entries:
            return
        current_selected = self.log_list.curselection()
        if current_selected:
            next_index = current_selected[0] + 1
            if next_index < len(self.filtered_log_entries):
                self.log_list.selection_clear(0, tk.END)
                self.log_list.selection_set(next_index)
                self.log_list.activate(next_index)
                self.log_list.see(next_index)
        else: 
            self.log_list.selection_set(0)
            self.log_list.activate(0)
        self.show_details(None)

    def _update_navigation_buttons(self):
        if not self.filtered_log_entries:
            self.prev_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)
            return

        selected_index = self.log_list.curselection()
        if not selected_index:
            self.prev_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.NORMAL if self.filtered_log_entries else tk.DISABLED)
        else:
            if selected_index[0] == 0:
                self.prev_button.config(state=tk.DISABLED)
            else:
                self.prev_button.config(state=tk.NORMAL)

            if selected_index[0] == len(self.filtered_log_entries) - 1:
                self.next_button.config(state=tk.DISABLED)
            else:
                self.next_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = LogViewerApp(root)
    root.mainloop()