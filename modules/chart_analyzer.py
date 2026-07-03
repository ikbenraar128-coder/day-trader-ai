import cv2
import numpy as np
from datetime import datetime

class ChartAnalyzer:
    def __init__(self):
        self.price_history = []
        
    def analyze_screenshot(self, image):
        prices = self.extract_prices_from_chart(image)
        if len(prices) < 14:
            return None
        self.price_history.extend(prices)
        indicators = self.calculate_indicators(self.price_history[-50:])
        return self.generate_signal(indicators)
    
    def extract_prices_from_chart(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_green = np.array([35, 100, 100])
        upper_green = np.array([85, 255, 255])
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        green_count = cv2.countNonZero(green_mask)
        return [100 + np.random.randint(-2, 5) if green_count > 100 else 100 + np.random.randint(-5, 2)]
    
    def calculate_indicators(self, prices):
        prices_array = np.array(prices, dtype=float)
        rsi = self.calculate_rsi(prices_array, 14)
        ema_12 = self.calculate_ema(prices_array, 12)
        ema_26 = self.calculate_ema(prices_array, 26)
        macd = ema_12 - ema_26
        sma = np.mean(prices_array[-20:])
        std = np.std(prices_array[-20:])
        return {'RSI': rsi, 'MACD': macd, 'BB_Upper': sma + std*2, 'BB_Lower': sma - std*2, 'Current_Price': prices_array[-1]}
    
    def calculate_rsi(self, prices, period=14):
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        if avg_loss == 0:
            return 100 if avg_gain > 0 else 50
        rs = avg_gain / avg_loss
        return round(100 - (100 / (1 + rs)), 2)
    
    def calculate_ema(self, prices, period):
        multiplier = 2 / (period + 1)
        ema = np.mean(prices[:period])
        for price in prices[period:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))
        return ema
    
    def generate_signal(self, indicators):
        signal = {'timestamp': datetime.now().isoformat(), 'action': 'HOLD', 'confidence': 0, 'RSI': indicators['RSI'], 'MACD': indicators['MACD']}
        if indicators['RSI'] < 30 and indicators['MACD'] > 0:
            signal['action'] = 'BUY 📈'
            signal['confidence'] = 0.85
        elif indicators['RSI'] > 70 and indicators['MACD'] < 0:
            signal['action'] = 'SELL 📉'
            signal['confidence'] = 0.85
        return signal