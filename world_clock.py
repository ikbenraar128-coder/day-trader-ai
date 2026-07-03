#!/usr/bin/env python3
import sys
import os
from datetime import datetime
import pytz

# Check if PyQt5 is installed
try:
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QHBoxLayout
    from PyQt5.QtCore import QTimer, Qt
    from PyQt5.QtGui import QFont
except ImportError:
    print("PyQt5 not installed. Installing...")
    os.system("pip install PyQt5 pytz")
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QHBoxLayout
    from PyQt5.QtCore import QTimer, Qt
    from PyQt5.QtGui import QFont

class Clock(QWidget):
    def __init__(self):
        super().__init__()
        self.zones = ['UTC', 'US/Eastern', 'Europe/Paris', 'Asia/Tokyo', 'Australia/Sydney']
        self.labels = []
        self.init()
        
    def init(self):
        self.setWindowTitle('Clock')
        self.setGeometry(50, 50, 600, 400)
        self.setStyleSheet("background: black; color: lime;")
        
        layout = QVBoxLayout()
        layout.setSpacing(5)
        
        title = QLabel('TIME ZONES')
        title.setFont(QFont('Monospace', 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Controls
        ctrl = QHBoxLayout()
        self.tz_select = QComboBox()
        self.tz_select.addItems(['UTC', 'US/Eastern', 'US/Central', 'Europe/Paris', 'Asia/Tokyo', 'Australia/Sydney', 'Asia/Kolkata', 'Europe/London'])
        self.tz_select.setStyleSheet("background: #333; color: lime;")
        ctrl.addWidget(self.tz_select)
        
        add_btn = QPushButton('ADD')
        add_btn.setStyleSheet("background: lime; color: black;")
        add_btn.clicked.connect(self.add)
        ctrl.addWidget(add_btn)
        
        rm_btn = QPushButton('RM')
        rm_btn.setStyleSheet("background: red; color: white;")
        rm_btn.clicked.connect(self.remove)
        ctrl.addWidget(rm_btn)
        
        layout.addLayout(ctrl)
        
        # Clock area
        self.clock_layout = QVBoxLayout()
        self.clock_layout.setSpacing(3)
        
        # Add default
        for tz in ['UTC', 'US/Eastern', 'Europe/Paris', 'Asia/Tokyo']:
            self.add_label(tz)
        
        layout.addLayout(self.clock_layout)
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(1000)
        self.tick()
    
    def add_label(self, tz):
        if any(l[0] == tz for l in self.labels):
            return
        lbl = QLabel()
        lbl.setFont(QFont('Monospace', 14, QFont.Bold))
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("background: #222; color: lime; padding: 5px;")
        self.clock_layout.insertWidget(len(self.labels), lbl)
        self.labels.append([tz, lbl])
    
    def add(self):
        self.add_label(self.tz_select.currentText())
    
    def remove(self):
        if self.labels:
            tz, lbl = self.labels.pop()
            lbl.deleteLater()
    
    def tick(self):
        for tz, lbl in self.labels:
            now = datetime.now(pytz.timezone(tz))
            txt = now.strftime('%H:%M:%S') + '\n' + tz + '\n' + now.strftime('%a %m/%d')
            lbl.setText(txt)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Clock()
    w.show()
    sys.exit(app.exec_())