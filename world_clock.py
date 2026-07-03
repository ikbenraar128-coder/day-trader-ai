import sys
from datetime import datetime
import pytz
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QScrollArea
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

class WorldClock(QWidget):
    def __init__(self):
        super().__init__()
        self.timezones = {
            'UTC': 'UTC',
            'GMT': 'GMT',
            'EST (New York)': 'US/Eastern',
            'CST (Chicago)': 'US/Central',
            'MST (Denver)': 'US/Mountain',
            'PST (Los Angeles)': 'US/Pacific',
            'CET (Paris)': 'Europe/Paris',
            'GMT+1 (London)': 'Europe/London',
            'IST (India)': 'Asia/Kolkata',
            'JST (Tokyo)': 'Asia/Tokyo',
            'AEST (Sydney)': 'Australia/Sydney',
            'NZST (Auckland)': 'Pacific/Auckland'
        }
        self.clock_labels = {}
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('🌍 World Digital Clock')
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: #0a0a0a; color: #00ff00;")
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title
        title = QLabel('🌍 World Clock - Multiple Time Zones')
        title.setFont(QFont('Arial', 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #00ffff;")
        main_layout.addWidget(title)
        
        # Timezone selection
        tz_layout = QHBoxLayout()
        tz_label = QLabel('Add Timezone:')
        tz_label.setFont(QFont('Arial', 12))
        tz_layout.addWidget(tz_label)
        
        self.tz_combo = QComboBox()
        self.tz_combo.addItems(self.timezones.keys())
        self.tz_combo.setFont(QFont('Arial', 11))
        self.tz_combo.setStyleSheet("background-color: #1a1a1a; color: #00ff00; padding: 5px;")
        self.tz_combo.setMinimumWidth(200)
        tz_layout.addWidget(self.tz_combo)
        
        add_btn = QPushButton('➕ Add')
        add_btn.setFont(QFont('Arial', 11, QFont.Bold))
        add_btn.setStyleSheet("background-color: #00ff00; color: #000; padding: 8px 15px; border-radius: 5px;")
        add_btn.clicked.connect(self.add_timezone)
        add_btn.setMaximumWidth(120)
        tz_layout.addWidget(add_btn)
        
        remove_btn = QPushButton('🗑️ Remove')
        remove_btn.setFont(QFont('Arial', 11, QFont.Bold))
        remove_btn.setStyleSheet("background-color: #ff4444; color: #fff; padding: 8px 15px; border-radius: 5px;")
        remove_btn.clicked.connect(self.remove_timezone)
        remove_btn.setMaximumWidth(120)
        tz_layout.addWidget(remove_btn)
        
        tz_layout.addStretch()
        main_layout.addLayout(tz_layout)
        
        # Separator
        sep = QLabel("─" * 100)
        sep.setStyleSheet("color: #00ff00;")
        main_layout.addWidget(sep)
        
        # Scroll area for clocks
        scroll = QScrollArea()
        scroll.setStyleSheet("background-color: #0a0a0a; border: none;")
        scroll.setWidgetResizable(True)
        
        scroll_widget = QWidget()
        self.clock_layout = QVBoxLayout(scroll_widget)
        self.clock_layout.setSpacing(20)
        self.clock_layout.setContentsMargins(10, 10, 10, 10)
        
        # Add default timezones
        default_zones = ['UTC', 'EST (New York)', 'CET (Paris)', 'JST (Tokyo)']
        for tz_name in default_zones:
            self.add_clock_label(tz_name)
        
        self.clock_layout.addStretch()
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
        
        self.setLayout(main_layout)
        
        # Start timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        
        self.update_time()
        
    def add_clock_label(self, tz_name):
        if tz_name not in self.clock_labels:
            label = QLabel()
            label.setFont(QFont('Courier New', 20, QFont.Bold))
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("""
                background-color: #1a1a1a;
                color: #00ff00;
                padding: 15px;
                border: 2px solid #00ff00;
                border-radius: 10px;
            """)
            self.clock_layout.insertWidget(len(self.clock_labels), label)
            self.clock_labels[tz_name] = label
    
    def add_timezone(self):
        tz_name = self.tz_combo.currentText()
        self.add_clock_label(tz_name)
    
    def remove_timezone(self):
        if self.clock_labels:
            tz_name = list(self.clock_labels.keys())[-1]
            label = self.clock_labels.pop(tz_name)
            label.deleteLater()
    
    def update_time(self):
        try:
            for tz_name, label in self.clock_labels.items():
                tz = pytz.timezone(self.timezones[tz_name])
                current_time = datetime.now(tz)
                time_str = current_time.strftime('%H:%M:%S')
                date_str = current_time.strftime('%A, %Y-%m-%d')
                label.setText(f'{tz_name}\n{time_str}\n{date_str}')
        except Exception as e:
            print(f"Error updating time: {e}")

def main():
    try:
        app = QApplication(sys.argv)
        clock = WorldClock()
        clock.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
