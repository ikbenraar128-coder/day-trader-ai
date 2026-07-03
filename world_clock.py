#!/usr/bin/env python3
import time
from datetime import datetime
import pytz

class WorldClock:
    def __init__(self):
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
        self.active_zones = ['UTC', 'New York', 'Paris', 'Tokyo']
    
    def clear_screen(self):
        import os
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def display(self):
        self.clear_screen()
        print("\n" + "="*80)
        print(" "*25 + "🌍 WORLD CLOCK 🌍")
        print("="*80 + "\n")
        
        for tz_name in self.active_zones:
            tz = pytz.timezone(self.timezones[tz_name])
            now = datetime.now(tz)
            time_str = now.strftime('%H:%M:%S')
            date_str = now.strftime('%A, %Y-%m-%d')
            print(f"  {tz_name:15} | {time_str} | {date_str}")
        
        print("\n" + "-"*80)
        print("  Commands: ADD <city> | DEL | LIST | QUIT")
        print("-"*80 + "\n")
    
    def list_zones(self):
        print("\nAvailable timezones:")
        for i, city in enumerate(self.timezones.keys(), 1):
            print(f"  {i}. {city}")
    
    def add_zone(self, city):
        if city in self.timezones:
            if city not in self.active_zones:
                self.active_zones.append(city)
                print(f"✅ Added {city}")
            else:
                print(f"⚠️  {city} already active")
        else:
            print(f"❌ {city} not found. Use LIST to see available zones.")
    
    def remove_zone(self):
        if len(self.active_zones) > 1:
            removed = self.active_zones.pop()
            print(f"❌ Removed {removed}")
        else:
            print("⚠️  Need at least 1 zone")
    
    def run(self):
        print("World Clock starting...\n")
        time.sleep(2)
        
        while True:
            self.display()
            
            try:
                cmd = input("Enter command: ").strip().upper()
                
                if cmd == 'QUIT' or cmd == 'Q':
                    print("Goodbye! 👋")
                    break
                elif cmd == 'LIST':
                    self.list_zones()
                elif cmd.startswith('ADD '):
                    city = cmd[4:].strip()
                    self.add_zone(city)
                elif cmd == 'DEL':
                    self.remove_zone()
                elif cmd == '':
                    continue
                else:
                    print("Unknown command")
                
                time.sleep(1)
            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == '__main__':
    clock = WorldClock()
    clock.run()