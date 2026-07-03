import sys
from datetime import datetime
import pytz
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

class WorldClock(QWidget):
    def __init__(self):
        super().__init__()
        self.timezones = {
            'UTC': 'UTC',
            'EST (New York)': 'US/Eastern',
            'CST (Chicago)': 'US/Central',
            'CET (Paris)': 'Europe/Paris',
            'IST (India)': 'Asia/Kolkata',
            'JST (Tokyo)': 'Asia/Tokyo',
            'AEST (Sydney)': 'Australia/Sydney',
            'NZST (Auckland)': 'Pacific/Auckland'
        }
        self.clock_labels = {}
        self.setup_ui()
        self.setup_timer()
        
    def setup_ui(self):
        self.setWindowTitle('World Clock')
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: #111; color: #0f0;")
        
        main = QVBoxLayout()
        
        title = QLabel('WORLD CLOCK')
        title.setFont(QFont('Courier', 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #0ff;")
        main.addWidget(title)
        
        controls = QHBoxLayout()
        lbl = QLabel('Add:')
        lbl.setFont(QFont('Courier', 12))
        controls.addWidget(lbl)
        
        self.combo = QComboBox()
        self.combo.addItems(self.timezones.keys())
        self.combo.setFont(QFont('Courier', 11))
        self.combo.setStyleSheet("background-color: #222; color: #0f0;")
        controls.addWidget(self.combo)
        
        btn_add = QPushButton('ADD')
        btn_add.setFont(QFont('Courier', 10, QFont.Bold))
        btn_add.setStyleSheet("background-color: #0f0; color: #000;")
        btn_add.clicked.connect(self.add_clock)
        controls.addWidget(btn_add)
        
        btn_del = QPushButton('DEL')
        btn_del.setFont(QFont('Courier', 10, QFont.Bold))
        btn_del.setStyleSheet("background-color: #f00; color: #fff;")
        btn_del.clicked.connect(self.del_clock)
        controls.addWidget(btn_del)
        
        controls.addStretch()
        main.addLayout(controls)
        
        self.clocks = QVBoxLayout()
        self.clocks.setSpacing(10)
        
        for tz in ['UTC', 'EST (New York)', 'CET (Paris)', 'JST (Tokyo)']:
            self.create_clock(tz)
        
        main.addLayout(self.clocks)
        main.addStretch()
        self.setLayout(main)
        
    def create_clock(self, tz_name):
        if tz_name in self.clock_labels:
            return
        label = QLabel()
        label.setFont(QFont('Courier', 18, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("background-color: #1a1a1a; color: #0f0; padding: 10px; border: 1px solid #0f0;")
        label.setMinimumHeight(60)
        self.clocks.insertWidget(len(self.clock_labels), label)
        self.clock_labels[tz_name] = label
        
    def add_clock(self):
        tz = self.combo.currentText()
        self.create_clock(tz)
        
    def del_clock(self):
        if self.clock_labels:
            tz = list(self.clock_labels.keys())[-1]
            label = self.clock_labels.pop(tz)
            label.deleteLater()
    
    def setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clocks)
        self.timer.start(1000)
        self.update_clocks()
        
    def update_clocks(self):
        for tz_name, label in self.clock_labels.items():
            tz = pytz.timezone(self.timezones[tz_name])
            now = datetime.now(tz)
            time_text = now.strftime('%H:%M:%S')
            date_text = now.strftime('%A %Y-%m-%d')
            label.setText(f'{tz_name}\n{time_text}\n{date_text}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = WorldClock()
    clock.show()
    sys.exit(app.exec_())