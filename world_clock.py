#!/usr/bin/env python3
import time

print("\n" + "="*60)
print("WORLD CLOCK - STARTING")
print("="*60 + "\n")

time.sleep(2)

print("Checking Python version...")
import sys
print(f"✅ Python {sys.version}")
time.sleep(1)

print("\nChecking pytz...")
try:
    import pytz
    print("✅ pytz is installed")
except ImportError as e:
    print(f"❌ ERROR: pytz not found: {e}")
    print("\nInstalling pytz...")
    import os
    os.system("pip install pytz")
    import pytz
    print("✅ pytz installed successfully")

time.sleep(1)

print("\nChecking datetime...")
from datetime import datetime
print("✅ datetime works")

time.sleep(1)

print("\n" + "="*60)
print("LOADING WORLD CLOCK")
print("="*60 + "\n")

time.sleep(2)

zones = ['UTC', 'US/Eastern', 'Europe/Paris', 'Asia/Tokyo']

counter = 0
try:
    while True:
        counter += 1
        print(f"\n--- UPDATE #{counter} ---")
        for tz_name in zones:
            try:
                tz = pytz.timezone(tz_name)
                now = datetime.now(tz)
                time_str = now.strftime('%H:%M:%S')
                date_str = now.strftime('%a %m/%d')
                print(f"{tz_name:20} | {time_str} | {date_str}")
            except Exception as e:
                print(f"❌ Error with {tz_name}: {e}")
        
        print("\n(Press Ctrl+C to stop)\n")
        time.sleep(2)
        
except KeyboardInterrupt:
    print("\n\n" + "="*60)
    print("CLOCK STOPPED - Goodbye!")
    print("="*60 + "\n")
    time.sleep(2)
except Exception as e:
    print(f"\n❌ FATAL ERROR: {e}")
    import traceback
    traceback.print_exc()
    time.sleep(5)