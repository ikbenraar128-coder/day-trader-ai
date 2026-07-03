#!/usr/bin/env python3
print("Python werkt!")

try:
    import pytz
    print("✅ pytz geïnstalleerd")
except:
    print("❌ pytz NIET geïnstalleerd - installing...")
    import os
    os.system("pip install pytz")
    import pytz
    print("✅ pytz nu geïnstalleerd")

from datetime import datetime

print("\nWORLD CLOCK - SIMPEL TEST\n")

zones = ['UTC', 'US/Eastern', 'Europe/Paris', 'Asia/Tokyo']

while True:
    print("\n" + "="*60)
    for tz_name in zones:
        tz = pytz.timezone(tz_name)
        now = datetime.now(tz)
        print(f"{tz_name:20} | {now.strftime('%H:%M:%S')} | {now.strftime('%a %m/%d')}")
    print("="*60)
    print("(Druk Ctrl+C om af te sluiten)\n")
    
    import time
    time.sleep(1)