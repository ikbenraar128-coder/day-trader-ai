import sys
import json
from modules.screen_capture import ScreenCapture
from modules.chart_analyzer import ChartAnalyzer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit
from PyQt5.QtCore import QTimer
from datetime import datetime

class DayTraderAI(QWidget):
    def __init__(self):
        super().__init__()
        self.active = False
        self.screen_capture = ScreenCapture()
        self.analyzer = ChartAnalyzer()
        self.trades_log = []
        self.init_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.analyze_tradingview)
        
    def init_ui(self):
        self.setWindowTitle('🤖 TradingView Day Trader AI')
        self.setGeometry(100, 100, 600, 500)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")
        
        layout = QVBoxLayout()
        self.status_label = QLabel('Status: OFFLINE ⚪')
        self.status_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #888;")
        layout.addWidget(self.status_label)
        
        self.toggle_btn = QPushButton('🚀 START AI')
        self.toggle_btn.setStyleSheet("background-color: #00c851; color: white; font-size: 14px; padding: 15px;")
        self.toggle_btn.clicked.connect(self.toggle_ai)
        layout.addWidget(self.toggle_btn)
        
        self.info_label = QLabel('⏳ Bereid om TradingView charts te analyseren...')
        layout.addWidget(self.info_label)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("background-color: #2d2d2d; color: #00ff00; font-family: Courier;")
        layout.addWidget(self.log_text)
        
        self.setLayout(layout)
        self.show_log("🚀 TradingView Day Trader AI geladen")
        
    def toggle_ai(self):
        self.active = not self.active
        if self.active:
            self.timer.start(2000)
            self.toggle_btn.setText('⏹️ STOP AI')
            self.status_label.setText('Status: ONLINE 🟢')
            self.show_log("[START] AI geactiveerd")
        else:
            self.timer.stop()
            self.toggle_btn.setText('🚀 START AI')
            self.status_label.setText('Status: OFFLINE ⚪')
            self.show_log("[STOP] AI uitgeschakeld")
    
    def analyze_tradingview(self):
        try:
            screenshot = self.screen_capture.capture()
            signals = self.analyzer.analyze_screenshot(screenshot)
            if signals and signals['action'] != 'HOLD':
                self.trades_log.append(signals)
                self.update_ui(signals)
        except Exception as e:
            self.show_log(f"⚠️ Fout: {str(e)}")
    
    def update_ui(self, signals):
        timestamp = datetime.now().strftime("%H:%M:%S")
        action = signals.get('action', 'HOLD')
        self.show_log(f"[{timestamp}] {action} | RSI: {signals.get('RSI')}")
    
    def show_log(self, message):
        self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

def main():
    app = QApplication(sys.argv)
    trader = DayTraderAI()
    trader.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()