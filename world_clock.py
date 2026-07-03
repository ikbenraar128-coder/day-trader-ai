import sys
from datetime import datetime
import pytz
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QColor

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
        self.init_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        
    def init_ui(self):
        self.setWindowTitle('🌍 World Digital Clock')
        self.setGeometry(100, 100, 900, 500)
        self.setStyleSheet("background-color: #0a0a0a; color: #00ff00;")
        
        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel('🌍 World Clock - Multiple Time Zones')
        title.setFont(QFont('Arial', 20, QFont.Bold))
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
        self.tz_combo.setFont(QFont('Arial', 12))
        self.tz_combo.setStyleSheet("background-color: #1a1a1a; color: #00ff00;")
        tz_layout.addWidget(self.tz_combo)
        
        from PyQt5.QtWidgets import QPushButton
        add_btn = QPushButton('Add')
        add_btn.setFont(QFont('Arial', 12))
        add_btn.setStyleSheet("background-color: #00ff00; color: #000; padding: 5px;")
        add_btn.clicked.connect(self.add_timezone)
        tz_layout.addWidget(add_btn)
        
        remove_btn = QPushButton('Remove Last')
        remove_btn.setFont(QFont('Arial', 12))
        remove_btn.setStyleSheet("background-color: #ff4444; color: #fff; padding: 5px;")
        remove_btn.clicked.connect(self.remove_timezone)
        tz_layout.addWidget(remove_btn)
        
        main_layout.addLayout(tz_layout)
        
        # Clock display area
        self.clock_layout = QVBoxLayout()
        self.clock_layout.setSpacing(15)
        self.clock_labels = {}
        
        # Add default timezones
        for tz_name in ['UTC', 'EST (New York)', 'CET (Paris)', 'JST (Tokyo)']:
            self.add_clock_label(tz_name)
        
        self.clock_layout.addStretch()
        main_layout.addLayout(self.clock_layout)
        
        self.setLayout(main_layout)
        self.update_time()
        
    def add_clock_label(self, tz_name):
        if tz_name not in self.clock_labels:
            label = QLabel()
            label.setFont(QFont('Courier New', 24, QFont.Bold))
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: #00ff00; padding: 10px;")
            self.clock_layout.addWidget(label)
            self.clock_labels[tz_name] = label
    
    def add_timezone(self):
        tz_name = self.tz_combo.currentText()
        self.add_clock_label(tz_name)
    
    def remove_timezone(self):
        if self.clock_labels:
            tz_name, label = self.clock_labels.popitem()
            label.deleteLater()
    
    def update_time(self):
        for tz_name, label in self.clock_labels.items():
            tz = pytz.timezone(self.timezones[tz_name])
            current_time = datetime.now(tz)
            time_str = current_time.strftime('%H:%M:%S')
            date_str = current_time.strftime('%Y-%m-%d %A')
            label.setText(f'{tz_name}\n{time_str}\n{date_str}')

def main():
    app = QApplication(sys.argv)
    clock = WorldClock()
    clock.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()