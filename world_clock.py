#!/usr/bin/env python3
import tkinter as tk
from datetime import datetime
import pytz
import threading

class WorldClock:
    def __init__(self, root):
        self.root = root
        self.root.title("World Clock")
        self.root.geometry("800x500")
        self.root.configure(bg='black')
        
        self.timezones = {
            'UTC': 'UTC',
            'New York': 'US/Eastern',
            'Chicago': 'US/Central',
            'Denver': 'US/Mountain',
            'Los Angeles': 'US/Pacific',
            'Paris': 'Europe/Paris',
            'London': 'Europe/London',
            'India': 'Asia/Kolkata',
            'Tokyo': 'Asia/Tokyo',
            'Sydney': 'Australia/Sydney',
            'Auckland': 'Pacific/Auckland'
        }
        
        self.clock_labels = {}
        self.setup_ui()
        self.update_time()
        
    def setup_ui(self):
        # Title
        title = tk.Label(self.root, text="WORLD CLOCK", font=("Courier", 24, "bold"), 
                        bg='black', fg='cyan')
        title.pack(pady=10)
        
        # Control Frame
        control_frame = tk.Frame(self.root, bg='black')
        control_frame.pack(pady=5)
        
        tk.Label(control_frame, text="Add:", font=("Courier", 10), 
                bg='black', fg='lime').pack(side=tk.LEFT, padx=5)
        
        self.tz_var = tk.StringVar(value='UTC')
        tz_menu = tk.OptionMenu(control_frame, self.tz_var, *self.timezones.keys())
        tz_menu.configure(bg='#333', fg='lime', font=("Courier", 10))
        tz_menu.pack(side=tk.LEFT, padx=5)
        
        add_btn = tk.Button(control_frame, text="ADD", command=self.add_clock,
                           bg='lime', fg='black', font=("Courier", 10, "bold"),
                           padx=10)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        del_btn = tk.Button(control_frame, text="DEL", command=self.del_clock,
                           bg='red', fg='white', font=("Courier", 10, "bold"),
                           padx=10)
        del_btn.pack(side=tk.LEFT, padx=5)
        
        # Clocks Frame
        self.clocks_frame = tk.Frame(self.root, bg='black')
        self.clocks_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add default clocks
        for tz in ['UTC', 'New York', 'Paris', 'Tokyo']:
            self.add_clock(tz)
        
        # Update every second
        self.update_clock()
    
    def add_clock(self, tz_name=None):
        if tz_name is None:
            tz_name = self.tz_var.get()
        
        if tz_name in self.clock_labels:
            return
        
        label = tk.Label(self.clocks_frame, text="", font=("Courier", 12, "bold"),
                        bg='#1a1a1a', fg='lime', pady=10)
        label.pack(fill=tk.X, pady=5)
        self.clock_labels[tz_name] = label
    
    def del_clock(self):
        if self.clock_labels:
            tz_name = list(self.clock_labels.keys())[-1]
            label = self.clock_labels.pop(tz_name)
            label.destroy()
    
    def update_time(self):
        for tz_name, label in self.clock_labels.items():
            tz = pytz.timezone(self.timezones[tz_name])
            now = datetime.now(tz)
            time_str = now.strftime('%H:%M:%S')
            date_str = now.strftime('%A, %Y-%m-%d')
            text = f"{tz_name}  |  {time_str}  |  {date_str}"
            label.config(text=text)
    
    def update_clock(self):
        self.update_time()
        self.root.after(1000, self.update_clock)

if __name__ == '__main__':
    root = tk.Tk()
    app = WorldClock(root)
    root.mainloop()